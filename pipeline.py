import argparse
from glob import glob
from datetime import datetime

import tensorflow as tf
from tensorflow import keras, io
from tensorflow.keras import layers
from tensorflow.keras.models import load_model

from tensorflow.python.client import device_lib

from numpy.random import seed


# ===================================== CLI arguments
parser = argparse.ArgumentParser(description="CNN hyperparameters")

parser.add_argument("-bs", help="Batch size (train, test, and validation)",
                    default=512, type=int, dest="batch_size")

parser.add_argument("-p", help="Dropout probability",
                    default=0.5, type=float, dest="dropout_p")

parser.add_argument("-lr", help="Learning rate for Adam optimizer",
                    default=1e-3, type=float, dest="learning_rate")

parser.add_argument("-l", help="L2 penalty (weight decay)",
                    default=0, type=float, dest="weight_decay")

parser.add_argument("-n", help="Number of epochs for training",
                    default=50, type=int, dest="n_epochs")

parser.add_argument("--fchannels", help="Output channels from first filter",
                    default=1024, type=int, dest="first_out_channels")

parser.add_argument("--fstride", help="Stride of first filter",
                    default=3, type=int, dest="first_stride")

parser.add_argument("--first_height", help="Height of initial filter",
                    default=8, type=int, dest="first_height")

parser.add_argument("--dataset", help="ID of the dataset to train with",
                    default="baseline", type=str, dest="dataset_id")

parser.add_argument("--mixed_trees", help="Specify to use mixed trees",
                    default="", type=str, dest="mixed_trees")

parser.add_argument("--pool", help="Max or average conv pooling",
                    default="average", type=str, dest="pool")

parser.add_argument("--global_pool", help="Max or average global pooling",
                    default="average", type=str, dest="global_pool")

parser.add_argument("--init", help="Glorot weight initializer",
                    default="uniform", type=str, dest="initializer")

parser.add_argument("--opt", help="Optimizer flag",
                    default="adam", type=str, dest="optimizer")

parser.add_argument("-w", help="""Maximum number of processes to spin up
                                  when using process-based threading""",
                    default=1, type=int, dest="n_workers")

parser.add_argument("-q", help="Maximum size for the generator queue",
                    default=1, type=int, dest="queue_size")

# tfrecord files contain 10k alignments per file
parser.add_argument("--restrict", help="Restrict number of training files to use",
                    default=0, type=int, dest="restrict_files")

parser.add_argument("--continue", help="Continue training model",
                    default="", type=str, dest="continue_model")

parser.add_argument("--run_id", help="Output name for this training run",
                    default="", type=str, dest="run_id")

parser.add_argument("--num_128_layers", help="Number of conv layers with filter size=128",
                    default=4, type=int, dest="num_128_layers")

parser.add_argument("--seed", help="Random seed value",
                    default=42, type=int, dest="seed")


# parse CLI arguments
args = parser.parse_args()


def add_conv_block(model, out_channels, kernel_size, pool_size,
                   stride=1, dropout_p=args.dropout_p,
                   padding="valid", channel_dim="channels_last"):
    """
    Add a convolutional layer with batch normalisation, dropout, and average
    pooling.
    """
    # define weight initialiser, Glorot Uniform used as standard
    if args.initializer == "normal":
        from tensorflow.keras.initializers import GlorotNormal
        conv_init = GlorotNormal()
    else:
        from tensorflow.keras.initializers import GlorotUniform
        conv_init = GlorotUniform()
    
    # add block to network
    model.add(layers.Conv2D(out_channels,
                            kernel_size,
                            stride,
                            padding,
                            kernel_initializer=conv_init,
                            data_format=channel_dim,
                            activation="relu"))
    model.add(layers.BatchNormalization(axis=-1))
    model.add(layers.Dropout(rate=dropout_p))

    # determine if average of max pooling is used
    if args.pool == "average":
        model.add(layers.AveragePooling2D(pool_size=pool_size))
    elif args.pool == "max":
        model.add(layers.AveragePooling2D(pool_size=pool_size))
    else:
        raise argparse.ArgumentTypeError("Pooling must be either \"max\" or \"average\"")
    return model


def add_fc_layer(model, dropout_p=args.dropout_p):
    """
    Add a fully-connected layer with batch normalisation and dropout.
    """
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.BatchNormalization(axis=-1))
    model.add(layers.Dropout(rate=dropout_p))
    return model


def generate_model():
    """
    Define the fully convolutional neural network.
    """
    model = keras.Sequential()
    model = add_conv_block(model,
                           out_channels=1024,
                           kernel_size=(args.first_height,3),
                           stride=args.first_stride,
                           pool_size=1)
    model = add_conv_block(model,
                           out_channels=1024,
                           kernel_size=(1,2),
                           pool_size=(1,4))
    model = add_conv_block(model,
                           out_channels=128,
                           kernel_size=(1,2),
                           pool_size=(1,4))
    # the rest of the blocks are identical, loop through number of desired
    # layers to add
    for _ in range(args.num_128_layers):
        model = add_conv_block(model,
                               out_channels=128,
                               kernel_size=(1,2),
                               pool_size=(1,2))
    if args.global_pool == "average":
        model.add(layers.GlobalAveragePooling2D())
    elif args.global_pool == "max":
        model.add(layers.GlobalMaxPooling2D())
    else:
        raise argparse.ArgumentTypeError("Pooling must be either \"max\" or \"average\"")
    model = add_fc_layer(model)
    model.add(layers.Dense(1, activation="sigmoid", name="final_layer"))
    return model


def _parse_alignment(example):
    """
    Parse the input TFRecord alignment file. The TFRecords contain
    pairs of alignments and labels in{0, 1}.
    """
    alignment_feature_description = {
        "alignment": io.FixedLenFeature([], tf.string),
        "y_label": io.FixedLenFeature([], tf.int64)
    }
    example = io.parse_single_example(example, alignment_feature_description)
    alignment = io.parse_tensor(example["alignment"], out_type=tf.float32)
    y_label = tf.cast(example["y_label"], tf.int32)
    return alignment, y_label


def main():
    # Check if Tensor is able to utilise CPU and GPU
    print(device_lib.list_local_devices())

    # set random seeds
    seed(args.seed)
    tf.random.set_seed(args.seed)
    print("here1")

    # determine if a previously incomplete network training run should be
    # continued, or if a new training run is started
    if args.continue_model:
        model = load_model("/omega_ai/data/saved_models/" + args.continue_model)
        already_trained = int(args.continue_model.split("/")[-1])
        n_epochs = args.n_epochs - already_trained
    else:
        n_epochs = args.n_epochs
        model = generate_model()
        x = tf.ones((512, args.first_height, 2340, 5))
        model.predict(x)
        model.summary()
  
    print("here2")

    # specify the optimiser. Adam used as standard, tested out AdamW for one run
    if args.optimizer == "adam":
        opt = keras.optimizers.Adam(learning_rate=args.learning_rate)
    elif args.optimizer == "adamw":
        import tensorflow_addons as tfa
        opt = tfa.optimizers.AdamW(learning_rate=args.learning_rate,
                                   weight_decay=1e-2)
    
    print("here3")

    # compile the CNN
    model.compile(optimizer=opt,
                  loss="binary_crossentropy",
                  metrics=["binary_accuracy", tf.keras.metrics.AUC(name="auc")])

    # print the ID of the dataset
    print("DATASET ID:", args.dataset_id)
    
    print("here4")

    # determine if more than one set of tree topologies should be used for training
    # not standard, just trying it out
    if args.mixed_trees:
        train_files, val_files = [], []
        for tree in ["baseline", "tips_32", "tips_64"]:
            train_files.extend(glob("/omega_ai/data/tf_records/{}/training/*tfrecord".format(tree)))
            val_files.extend(glob("/omega_ai/data/tf_records/{}/validation/*tfrecord".format(tree)))
    else:
        train_files = glob("/omega_ai/data/tf_records/{}/training/*tfrecord".format(args.dataset_id))
        val_files = glob("/omega_ai/data/tf_records/{}/validation/*tfrecord".format(args.dataset_id))
 
    print("here5")

    # if specified, restrict the number of files used for training
    if args.restrict_files != 0:
        import random
        n_files = args.restrict_files // 10000
        random.seed(n_files)
        random.shuffle(train_files)
        train_files = train_files[:n_files]
    
    print("here6")

    # define training and validation TFRecord datasets
    training_dataset = tf.data.TFRecordDataset(train_files).map(_parse_alignment).padded_batch(
        args.batch_size,
        padded_shapes=([None,None,None],[]))
    validation_dataset = tf.data.TFRecordDataset(val_files).map(_parse_alignment).padded_batch(
        args.batch_size,
        padded_shapes=([None,None,None],[]))
    
    print("here7")

    # show shape of input data
    print(training_dataset)
    print(next(iter(training_dataset))[0].shape)

    print("here8")

    # generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # network parameters
    pool_operation = str(args.pool)
    dropout_p = str(args.dropout_p)
    bs = str(args.batch_size)
    lr = str(args.learning_rate)
    ds = str(args.dataset_id)
    
    # generate an ID for this run if nothing specified
    run_id = "_".join([timestamp, ds, pool_operation, dropout_p, bs, lr])

    # determine if the full training dataset should be used or not, if not,
    # change the run ID to indicate the no. of samples used for training
    if args.restrict_files != 0:
        run_id = "_".join([timestamp, ds, pool_operation, dropout_p, bs, lr, str(args.restrict_files)])

    # continue training until 50 epochs if 50 epochs not completed in
    # first run
    if args.continue_model:
        run_id = args.continue_model
        # run_id = args.continue_model.split("/")[0]
    #     epoch = args.continue_model.split("/")[-1]
    #     print(f"Continuing from epoch {epoch}")
    # else:
    #     epoch =''

    # tweak run ID if multiple trees are used
    if args.mixed_trees:
        run_id = "_".join([timestamp, "mixed_trees", pool_operation, dropout_p, bs, lr])

    # manually specify unique ID for this run
    if args.run_id:
        run_id = str(args.run_id)

    # define logs for TensorBoard

    log_dir = "/omega_ai/data/saved_models/" + run_id + "/logs/scalars/"
    # checkpoint_dir = "/omega_ai/data/saved_models/" + run_id + "/{}".format(epoch)
    # print("this is log_dir: {}".format(log_dir))
    # print("this is checkpoint_dir: {}".format(checkpoint_dir))
    callbacks = [
        keras.callbacks.TensorBoard(log_dir=log_dir,
                                    update_freq=200),
        keras.callbacks.ModelCheckpoint(filepath="/omega_ai/data/saved_models/" + run_id + "/{epoch}",
                                        save_freq="epoch")
    ]  # tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5
        # keras.callbacks.ModelCheckpoint(filepath="/omega_ai/data/saved_models/" + run_id + "/{}".format(epoch),

    # train network
    model.fit(training_dataset,
              validation_data=validation_dataset,
              epochs=n_epochs,
              batch_size=args.batch_size,
              use_multiprocessing=True,
              workers=args.n_workers,
              max_queue_size=args.queue_size,
              callbacks=callbacks,
              shuffle=True)

    print("here_end")

if __name__ == "__main__":
    main()
