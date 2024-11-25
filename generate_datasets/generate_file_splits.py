#!/usr/local/bin/python

from glob import glob
from pathlib import Path
from sys import argv


def main():
    basedir = "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/datasets/"
    dataset_id = argv[1]
    
    alignments = glob(basedir + dataset_id + "/group_*/train_x/*fas")
    n = 10000
    alignments = [alignments[i:i + n] for i in range(0, len(alignments), n)]
    Path("file_lists/" + dataset_id).mkdir(parents=True, exist_ok=True)
    for i, j in enumerate(alignments):
        with open("file_lists/{}/{}.txt".format(dataset_id, i+1), "w") as f:
            for al in j:
                f.write(al + "\n")


if __name__ == "__main__":
    main()
