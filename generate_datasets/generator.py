import numpy as np
import time
import os
from sys import argv
from Bio import SeqIO
from Bio import AlignIO
import random


def create_NB_control(p0,p1,w0,w1,w2,tree,length,kappa,indel_rate,randomseed,indel_q=0.35):
    start_cntrl = time.time()
    """
    Write an INDELible control file using geometrically distributed indel lengths.
    """
    file = open("control.txt","w")
    file.write("[TYPE] CODON 1\n[SETTINGS]\n[printrates] TRUE\n[randomseed] "+str(randomseed)+"\n[output]  FASTA\n")
    file.write("[MODEL]  modelname\n[submodel]\n"+str(kappa)+"\n"+str(p0)+" "+str(p1)+"\n"+str(w0)+" "+str(w1)+" "+str(w2))
    file.write("\n[indelrate] "+str(indel_rate)+"\n[indelmodel] NB "+str(indel_q)+" 1")  # r=1, makes distribution geometric
    file.write("\n[TREE] treename  \n"+tree)
    file.write("\n[PARTITIONS] partitionname [treename modelname "+str(length)+"]")
    file.write("\n[EVOLVE] partitionname 1 dna\n")
    file.close()
    end_cntrl = time.time() - start_cntrl
    print("Control file write runtime: " + str(end_cntrl), flush=True)


def create_zeta_control(p0,p1,w0,w1,w2,tree,length,kappa,indel_rate,randomseed,indel_zeta=1.8,max_indel=40):
    start_cntrl = time.time()
    """
    Write an INDELible control file using power law distributed indel lengths.
    """
    file = open("control.txt","w")
    file.write("[TYPE] CODON 1\n[SETTINGS]\n[printrates] TRUE\n[randomseed] "+str(randomseed)+"\n[output]  FASTA\n")
    file.write("[MODEL]  modelname\n[submodel]\n"+str(kappa)+"\n"+str(p0)+" "+str(p1)+"\n"+str(w0)+" "+str(w1)+" "+str(w2))
    file.write("\n[indelrate] "+str(indel_rate)+"\n[indelmodel] POW "+str(indel_zeta)+" "+str(max_indel))
    file.write("\n[TREE] treename  "+tree)
    file.write("\n[PARTITIONS] partitionname [treename modelname "+str(length)+"]")
    file.write("\n[EVOLVE] partitionname 1 dna\n")
    file.close()
    end_cntrl = time.time() - start_cntrl
    print("Control file write runtime: " + str(end_cntrl))

def create_branch_site_control(p0, p1, w0_fg, w1_fg, w2_fg, w0_bg, w1_bg, w2_bg, t, kappa, random_seed, length):
    file = open("control.txt","w")
    file.write("[TYPE] CODON 1\n[SETTINGS]\n[randomseed] " + str(random_seed) + "\n[output]  FASTA\n")
    file.write("[MODEL] x1 [submodel] " + str(kappa) + " " + str(p0) + " " + str(p1) + " " + str(w0_bg) + " " + str(w1_bg) + " " + str(w2_bg) + " ")
    file.write("[MODEL] x2 [submodel] " + str(kappa) + " " + str(p0) + " " + str(p1) + " " + str(w0_fg) + " " + str(w1_fg) + " " + str(w2_fg) + " ")
    file.write("[indelmodel] NB 0.35 1 [indelrate] 0.1\n")
    file.write("[TREE] t1 (((((((((A:" + t + ", B:" + t + "):" + t + ", C:" + t + "):" + t + ", D:" + t + "):" + t + ", E:" + t + "):" + t + ", F:" + t + "):" + t + ", G:" + t + "):" + t + ", H:" + t + "):" + t + ", I:" + t + "):" + t + ", J:" + t + ");\n")
    file.write("[BRANCHES] b1 (((((((((A #x2, B #x1) #x1, C #x1) #x1, D #x2) #x1, E #x1) #x1, F #x1) #x1, G #x1) #x1, H #x1) #x1, I #x1) #x1, J #x1) #x1;\n")
    file.write("[PARTITIONS] Pname [t1 b1 " + str(length) + "]\n")
    file.write("[EVOLVE] Pname 1 dna\n")
    file.close()

def read_sequence_order(dna_fasta_file):
    """
    Reads the DNA FASTA file and returns the order of headers as a list.
    """
    order = []
    with open(dna_fasta_file, "r") as dna_file:
        for record in SeqIO.parse(dna_file, "fasta"):
            order.append(record.id)
    return order

def reorder_seqs(seq_file, dna_order, output_file):
    """
    Reorders the amino acid sequences based on the order from the DNA FASTA file
    and creates a new amino acid FASTA file with the desired order.
    """
    records = []
    with open(seq_file, "r") as aa_file:
        for record in SeqIO.parse(aa_file, "fasta"):
            index = dna_order.index(record.id)
            records.append((index, record))

    sorted_records = [record for _, record in sorted(records)]
    with open(output_file, "w") as output_aa_file:
        SeqIO.write(sorted_records, output_aa_file, "fasta")

def simulate_align(ID, aligner, shuffle=False):
    """
    Simulate an alignment using parameters defined in main.
    """
    tool_dir = "/hps/nobackup/goldman/charwest/omega_ai/tools/"
    indelible = tool_dir + "indelible"
    clustal = tool_dir + "clustalo"
    pal2nal = tool_dir + "pal2nal.pl"
    mafft = tool_dir + "mafft/bin/mafft"
    prank = tool_dir + "prank/bin/prank"

    # tool_dir = "/hps/nobackup/goldman/charwest/omega_ai/tools/"
    # indelible = tool_dir + "INDELibleV1.03/src/indelible"
    # clustal = tool_dir + "clustalo"
    # pal2nal = tool_dir + "pal2nal.pl"
    # mafft = tool_dir + "bin/mafft"

    # call INDELible
    indelible_start = time.time()
    os.system(indelible)
    indelible_end = time.time() - indelible_start
    print("indelible runtime: " + str(indelible_end), flush=True)

    # print("can currently see:")
    # file_list = []
    # for root, directories, files in os.walk(os.getcwd()):
    #     for file_name in files:
    #         file_list.append(file_name)
    
    # print(file_list)
    
    # # print(os.listdir(os.getcwd()))
    if shuffle:
        # Specify the input FASTA file
        sequences = list(SeqIO.parse("dna.fas", "fasta"))
        os.system("rm dna.fas")
        # print("sequences:")
        # print(sequences)

        random.shuffle(sequences)

        # Write the shuffled sequences to the input file
        SeqIO.write(sequences, "dna.fas", "fasta")


    # translate DNA to AA squence, write to aa.fas
    aa_start = time.time()
    translated = list()  
    for record in SeqIO.parse("dna.fas","fasta"):
        record.seq = record.seq.translate()
        translated.append(record)
    with open("aa.fas","w") as file:
        SeqIO.write(translated,file,"fasta")
    aa_end = time.time() - aa_start
    print("convert to AA seq runtime: " + str(aa_end), flush=True )

    # align using clustal
    if aligner == "clustal":
        clustal_start = time.time()
        os.system("{} --threads 2 -i aa.fas -o aa_aligned.fas".format(clustal))
        clustal_end = time.time() - clustal_start
        print("Clustal runtime: " + str(clustal_end), flush=True)
        # pal2nal convertion of AA alignment to codon alignment
        pal_start = time.time()
        os.system("perl {} -output fasta aa_aligned.fas dna.fas >> codon_aligned.fas".format(pal2nal))
        pal_end = time.time() - pal_start
        print("pal2nal runtime: " + str(pal_end), flush=True)

    # align using mafft
    elif aligner == "mafft":
        mafft_start = time.time()
        os.system("{} --quiet aa.fas > aa_aligned.fas".format(mafft))
        mafft_end = time.time() - mafft_start
        print("Mafft runtime: " + str(mafft_end))
        # pal2nal convertion of AA alignment to codon alignment
        pal_start = time.time()
        os.system("perl {} -output fasta aa_aligned.fas dna.fas >> codon_aligned.fas".format(pal2nal))
        pal_end = time.time() - pal_start
        print("pal2nal runtime: " + str(pal_end))
        # os.system("mv codon_aligned.fas mafft_test_x/"+ID+".fas")
        os.system("rm aa_aligned.fas")

    elif aligner == "prankc":
        prankc_start = time.time()
            # PRANK_CODON #
        seq_order = read_sequence_order("dna.fas")
        os.system("{} -codon -d=dna.fas -o=tmp_dna".format(prank))
        prank_align_dic = {}
        for record in AlignIO.read("tmp_dna.best.fas", "fasta"):
            prank_align_dic[str(record.id)] = str(record.seq)
        with open("codon_aligned_unordered.fas", "w") as out_fi:
            if shuffle:
                for header in list(prank_align_dic.keys()):
                    out_fi.write(">{}\n{}\n".format(header, prank_align_dic[header]))
            else:
                for header in sorted(list(prank_align_dic.keys())):
                    out_fi.write(">{}\n{}\n".format(header, prank_align_dic[header]))
        # Change to correct order
        reorder_seqs("codon_aligned_unordered.fas", seq_order, "codon_aligned.fas")
        # os.system("mv corrected_codon_aligned.fas prankc_test_x/"+ID+".fas")
        os.system("rm tmp_dna.best.fas codon_aligned_unordered.fas")
        prankc_end = time.time() - prankc_start
        print("PRANK codon runtime: " + str(prankc_end))    

    else:
        raise ValueError

    mv_files_start = time.time()
    # remove intermediate files
    os.system("rm aa.fas aa_aligned.fas trees.txt")  
     # collect the output and control files in folders
    os.system("mv codon_aligned.fas train_x/"+ID+".fas") 
    os.system("mv LOG.txt reference/LOG/LOG_"+ID+".txt")
    os.system("mv dna.fas reference/output/dna_"+ID+".fas")
    os.system("mv dna_TRUE.fas reference/output_TRUE/dna_TRUE_"+ID+".fas")
    os.system("mv dna_RATES.txt reference/site_classes/dna_RATES_"+ID+".txt")
    os.system("mv control.txt reference/controlFiles/control_"+ID+".txt")
    mv_files_end = time.time() - mv_files_start
    print("Move files runtime: " + str(mv_files_end), flush=True)

def simulate_true_align(ID, shuffle=False):
    """
    Simulate an alignment using parameters defined in main.
    """
    tool_dir = "/hps/nobackup/goldman/charwest/omega_ai/tools/"
    indelible = tool_dir + "indelible"

    # call INDELible
    indelible_start = time.time()
    os.system(indelible)
    indelible_end = time.time() - indelible_start
    print("indelible runtime: " + str(indelible_end), flush=True)

    if shuffle:
        # Specify the input FASTA file
        sequences = list(SeqIO.parse("dna_TRUE.fas", "fasta"))

        random.shuffle(sequences)

        # Write the shuffled sequences to the input file
        SeqIO.write(sequences, "dna_TRUE_shuffle.fas", "fasta")

    # remove intermediate files
    if shuffle:
        os.system("sed -i -e 's/ //g' -e '/^\s*$/d' dna_TRUE_shuffle.fas")
        os.system("mv dna_TRUE_shuffle.fas train_x/"+ID+".fas") #true alignment
    else:
        os.system("sed -i -e 's/ //g' -e '/^\s*$/d' dna_TRUE.fas")
        os.system("scp dna_TRUE.fas train_x/"+ID+".fas") #true alignment
    os.system("rm trees.txt")
    # collect the output and control files in folders
    os.system("mv LOG.txt reference/LOG/LOG_"+ID+".txt")
    os.system("mv dna.fas reference/output/dna_"+ID+".fas")
    os.system("mv dna_TRUE.fas reference/output_TRUE/dna_TRUE_"+ID+".fas")
    os.system("mv dna_RATES.txt reference/site_classes/dna_RATES_"+ID+".txt")
    os.system("mv control.txt reference/controlFiles/control_"+ID+".txt")



def main():
    # get arugments from command line
    start = argv[1]
    end = argv[2]  # start and end ID, should be integers

    # the "baseline" divergence is a branch length of 0.2
    # high divergence is 0.6, low is 0.05, otherwise specify directly
    if argv[3] == "baseline":
        branch = str(0.2)
    elif argv[3] == "high":
        branch = str(0.6)
    elif argv[3] == "low":
        branch = str(0.05)
    else:
        branch = str(argv[3])  # branch length specified directly

    # define indel distribution; NB = negative binomial i.e. geometric, POW = power law
    indel_distribution = argv[4]  # NB or POW
    # define the indel rate, 0.1 by default
    indel_rate = str(argv[5])
    # define a unique ID for the dataset
    dataset_id = argv[6]

    # define if test or train data is to be generated
    if argv[7] == "test":
        basedir = "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/"
    else:
        basedir = "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/datasets/"

    # add aligner to dataset ID if it isn't the default of clustal
    if argv[8] != "clustal":
        outdir = basedir + argv[8] + "_" + dataset_id
    else:
        outdir = basedir + dataset_id

    # make output directories
    mkdir_start = time.time()
    os.system("mkdir -p " + outdir)
    folder = outdir + "/" + "group_" + start
    os.system("mkdir " + folder)
    os.chdir(folder)
    os.system("mkdir train_x train_y reference length")
    # os.system("mkdir reference/{LOG,output,output_TRUE,site_classes,controlFiles,parameters}")
    os.system("mkdir reference/LOG")
    os.system("mkdir reference/output")
    os.system("mkdir reference/output_TRUE")
    os.system("mkdir reference/site_classes")
    os.system("mkdir reference/controlFiles")
    os.system("mkdir reference/parameters")
    mkdir_end = time.time() - mkdir_start
    print("Make dirs runtime: " + str(mkdir_end), flush=True)

    # either define the baseline tree topology or retrieve from file
    tree_start = time.time()
    if argv[9] in ["32", "64", "128"]:
        with open("/hps/nobackup/goldman/charwest/omega_ai/data/gene_trees/artificial/{}_tips.tree".format(argv[9]), "r") as tree_f:
            tree_topology = tree_f.read().strip()
    elif argv[9] == "mix":
        tree_topology = ""
    else:
        tree_topology = "(((A:"+branch+",B:"+branch+"):"+branch+",(C:"+branch+",D:"+branch+"):"+branch+"):"+branch+",((E:"+branch+",F:"+branch+"):"+branch+",(G:"+branch+",H:"+branch+"):"+branch+"):"+branch+");"

    tree_end = time.time() - tree_start
    print("Tree runtime: " + str(tree_end), flush=True)
    # define the number of training alignments that are to be simulated under high
    # omega values (positive selection)
    n_positive = float(argv[10])

    # loop through a set number of simulations
    # loop_start = time.time()
    for x in range(int(start),int(end)):
        if argv[7] == "test":
            # add arbitrary value to random seed for test alignments
            np.random.seed(x + 2000000)
            indelible_seed = x + 2000000
        else:
            np.random.seed(x)
            indelible_seed = x

        # e.g. clustal
        aligner = argv[8]

        # define omega values of each site class
        p0 = np.random.uniform(low=0.5,high=0.8)
        p2 = np.random.uniform(low=0.01,high=0.1)
        p1 = 1-p0-p2
        w0 = np.random.uniform(low=0.1,high=0.5)
        w1 = np.random.uniform(low=0.5,high=0.9)
        n_neutral = round((1 - n_positive) * 0.2, 3)
        n_negative = round((1 - n_positive) * 0.8, 3)

        # 3 types of w2: 50% positive selection, 10% neutral, 40% negative
        randomSiteFlag = np.random.multinomial(1,[n_positive,n_neutral,n_negative])

        if randomSiteFlag[0] == 1:  # whether there is positve selection or not
            flag = 1
            # p0 = np.random.uniform(low=0.2,high=0.4)
            # p2 = np.random.uniform(low=0.05,high=0.5)
            # p1 = 1-p0-p2
        else:
            if randomSiteFlag[1] == 1:
                flag = 0
            else:
                flag = -1

        # w2 are sampled in 3 diff ways
        w2_list = np.array([np.random.uniform(low=1.5,high=5),1,np.random.uniform(low=0.9,high=1.0)])
        w2 = np.dot(randomSiteFlag,w2_list)

        # define kappa
        k = np.random.uniform(low=2,high=3)

        # root length distribution: gamma, scale 85, shape 4.2 (suggested by Viacheslav)
        length = np.random.gamma(4.2,scale=85)
        # length = 200

        # restriction on root length: 100-600 codons
        while length < 100 or length > 600:  
            length = np.random.gamma(4.2,scale=85)
            # length = 200
        # gene length has to be integer    
        length = int(length)

        # write training y labels
        train_start = time.time()
        with open("train_y/"+str(x)+".txt","w") as file:
            file.write(str(flag))
        train_end = time.time() - train_start
        print("Writing training data runtime: " + str(train_end), flush=True)

        # write lengths
        with open("length/"+str(x)+".txt","w") as file:
            file.write(str(length))

        # write parameter values used to generate the data
        start_open = time.time()
        with open("reference/parameters/"+str(x)+".txt","w") as file:
            file.write(str(p0)+"\n")
            file.write(str(p1)+"\n")
            file.write(str(w0)+"\n")
            file.write(str(w0)+"\n")
            file.write(str(w1)+"\n")
            file.write(str(w2)+"\n")
            file.write(str(length)+"\n")
            file.write(str(k)+"\n")
        end_open = time.time() - start_open
        print("Writing params runtime: " + str(end_open), flush=True)

        if argv[9] == "mix":
            # with open("/hps/nobackup/goldman/charwest/danaides/data/trees/500k_trees/trees/{0}.nwk".format(x)) as file:
            print(f"got here {x}")
            with open("/hps/nobackup/goldman/charwest/danaides/data/trees/500k_trees/trees/{0}.nwk".format(x)) as file:
                tree_topology = file.read().strip()
                print(tree_topology)

        # write control file using either geometric or power law distributed indel lengths
        if indel_distribution == "NB":
            create_NB_control(p0,p1,w0,w1,w2,tree_topology,length,k,indel_rate,randomseed=indelible_seed)
        elif indel_distribution == "POW":
            create_zeta_control(p0,p1,w0,w1,w2,tree_topology,length,k,indel_rate,randomseed=indelible_seed)

        # perform simulation using INDELible
        if (len(argv) == 12):
            if (argv[11] == 'shuffle'):
                # print("got here 1")
                simulate_align(str(x), aligner, True)
            elif (argv[11] == 'true_align'):
                # print("got here 2")
                simulate_true_align(str(x), False)
        elif (len(argv) > 12):
            # print("got here 3")
            simulate_true_align(str(x), True)
        else:
            # print("got here 4")
            simulate_align(str(x), aligner)

    os_start = time.time()
    os.chdir("../")
    os.system("chmod -R 777 "+folder)
    os_end = time.time() - os_start
    print("Final OS operations runtime: " + str(os_end), flush=True)


if __name__ == "__main__":
    main()