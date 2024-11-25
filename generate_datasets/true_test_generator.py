"""new features after Aug 17th meeting:
1. takes ID argument (start and end, should be numbers),branch length, random seed from commond line
2. python script should be run from parallel.sh for parallelising the task
3. modified choice of parameters by Viacheslav"s simulation scripts:  kappa distribution, in/del rate disribution, in/del Zipfian alpha distribution
4. alignment is done differently: first translate DNA seq to AA seq, align AA seq using Clustal O, then recover condon alignment by pal2nal
5. minor changes to adjust to parallel computing
"""
import numpy as np
import os
from sys import argv
from Bio import SeqIO
from Bio import AlignIO
import random

# get arugments form command line
start = argv[1]
end = argv[2]  # start and end ID, should be numbers

if argv[3] == "baseline":
    branch = str(0.2)
elif argv[3] == "high":
    branch = str(0.6)
elif argv[3] == "low":
    branch = str(0.05)
else:
    branch = str(argv[3])  # branch length specified directly

# seed = str((int(start) + 1) * 3)  # random seed
indel_distribution = argv[4]  # NB or POW
indel_rate = str(argv[5])
dataset_id = argv[6]
aligner = argv[7]

if argv[8] in ["32", "64", "128"]:
    with open("/hps/nobackup/goldman/charwest/omega_ai/data/gene_trees/artificial/{}_tips.tree".format(argv[8]), "r") as tree_f:
        tree_topology = tree_f.read().strip()
else:
    tree_topology = "(((A:"+branch+",B:"+branch+"):"+branch+",(C:"+branch+",D:"+branch+"):"+branch+"):"+branch+",((E:"+branch+",F:"+branch+"):"+branch+",(G:"+branch+",H:"+branch+"):"+branch+"):"+branch+");"

n_positive = float(argv[9])


basedir = "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/"

outdir = basedir + dataset_id
os.system("mkdir -p " + outdir)

folder = outdir + "/" + "group_" + start
os.system("mkdir " + folder)
os.chdir(folder)

os.system("mkdir true_test_x test_y reference length")
os.system("mkdir reference/{LOG,output,output_TRUE,site_classes,controlFiles,parameters}")


#indel rate and max indel length suggested by Viacheslav
#two functions, to generate control files, to run the simulation and alignment
def create_NB_control(p0,p1,w0,w1,w2,tree,length,kappa,indel_rate,randomseed,indel_q=0.35):
    file = open("control.txt","w")
    file.write("[TYPE] CODON 1\n[SETTINGS]\n[printrates] TRUE\n[randomseed] "+str(randomseed)+"\n[output]  FASTA\n")
    file.write("[MODEL]  modelname\n[submodel]\n"+str(kappa)+"\n"+str(p0)+" "+str(p1)+"\n"+str(w0)+" "+str(w1)+" "+str(w2))
    file.write("\n[indelrate] "+str(indel_rate)+"\n[indelmodel] NB "+str(indel_q)+" 1")  # r=1, makes distribution geometric
    file.write("\n[TREE] treename  "+tree)
    file.write("\n[PARTITIONS] partitionname [treename modelname "+str(length)+"]")
    file.write("\n[EVOLVE] partitionname 1 dna\n")
    file.close()
    # file.write("\n[insertrate] "+str(insert)+"\n[insertmodel] POW "+str(a_in)+" "+str(maxInsert))
    # file.write("\n[deleterate] "+str(delete)+"\n[deletemodel] POW "+str(a_del)+" "+str(maxDelete))


def create_zeta_control(p0,p1,w0,w1,w2,tree,length,kappa,indel_rate,randomseed,indel_zeta=1.8,max_indel=40):
    file = open("control.txt","w")
    file.write("[TYPE] CODON 1\n[SETTINGS]\n[printrates] TRUE\n[randomseed] "+str(randomseed)+"\n[output]  FASTA\n")
    file.write("[MODEL]  modelname\n[submodel]\n"+str(kappa)+"\n"+str(p0)+" "+str(p1)+"\n"+str(w0)+" "+str(w1)+" "+str(w2))
    file.write("\n[indelrate] "+str(indel_rate)+"\n[indelmodel] POW "+str(indel_zeta)+" "+str(max_indel))
    file.write("\n[TREE] treename  "+tree)
    file.write("\n[PARTITIONS] partitionname [treename modelname "+str(length)+"]")
    file.write("\n[EVOLVE] partitionname 1 dna\n")
    file.close()

def create_no_indel_control(p0,p1,w0,w1,w2,tree,length,kappa,indel_rate,randomseed,indel_q=0.35):
    file = open("control.txt","w")
    file.write("[TYPE] CODON 1\n[SETTINGS]\n[printrates] TRUE\n[randomseed] "+str(randomseed)+"\n[output]  FASTA\n")
    file.write("[MODEL]  modelname\n[submodel]\n"+str(kappa)+"\n"+str(p0)+" "+str(p1)+"\n"+str(w0)+" "+str(w1)+" "+str(w2))
    file.write("\n[TREE] treename  "+tree)
    file.write("\n[PARTITIONS] partitionname [treename modelname "+str(length)+"]")
    file.write("\n[EVOLVE] partitionname 1 dna\n")
    file.close()

# indelible & clustalo executable, pal2nal perl script should be in the directory
def simulate_run(ID, shuffle=False):
    tool_dir = "/hps/nobackup/goldman/charwest/omega_ai/tools/"
    indelible = tool_dir + "indelible"
    # clustal = tool_dir + "clustalo"
    # pal2nal = tool_dir + "pal2nal.pl"
    # prank = tool_dir + "prank/bin/prank"
    # mafft = tool_dir + "mafft/bin/mafft"

    os.system(indelible)

    if shuffle:
        # Specify the input FASTA file
        sequences = list(SeqIO.parse("dna_TRUE.fas", "fasta"))

        random.shuffle(sequences)

        # Write the shuffled sequences to the input file
        SeqIO.write(sequences, "dna_TRUE_shuffle.fas", "fasta")        
   
    # clean
    if shuffle:
        os.system("mv dna_TRUE_shuffle.fas true_train_x/"+ID+".fas") #true alignment
    else:
        os.system("scp dna_TRUE.fas true_test_x/"+ID+".fas")
    os.system("rm trees.txt")
    os.system("mv LOG.txt reference/LOG/LOG_"+ID+".txt")
    os.system("mv dna.fas reference/output/dna_"+ID+".fas")
    os.system("mv dna_TRUE.fas reference/output_TRUE/dna_TRUE_"+ID+".fas")
    os.system("mv dna_RATES.txt reference/site_classes/dna_RATES_"+ID+".txt")
    os.system("mv control.txt reference/controlFiles/control_"+ID+".txt")


for x in range(int(start),int(end)):
    np.random.seed(x + 2000000)
    indelible_seed = x + 2000000

    p0 = np.random.uniform(low=0.5,high=0.8)
    p2 = np.random.uniform(low=0.01,high=0.1)
    p1 = 1-p0-p2

    w0 = np.random.uniform(low=0.1,high=0.5)
    w1 = np.random.uniform(low=0.5,high=0.9)

    n_neutral = round((1 - n_positive) * 0.2, 3)
    n_negative = round((1 - n_positive) * 0.8, 3)
    randomSiteFlag = np.random.multinomial(1,[n_positive,n_neutral,n_negative])  # 3 types of w2: 50% positive selection, 10% neutral, 40% negative

    # randomSiteFlag = np.random.multinomial(1,[0.5,0.1,0.4])  # 3 types of w2: 50% positive selection, 10% neutral, 40% negative

    if randomSiteFlag[0] == 1:  # whether there is positve selection or not
        flag = 1
    else:
        if randomSiteFlag[1] == 1:
            flag = 0
        else:
            flag = -1

    w2_list = np.array([np.random.uniform(low=1.5,high=5),1,np.random.uniform(low=0.9,high=1.0)])  # w2 are sampled in 3 diff ways
    w2 = np.dot(randomSiteFlag,w2_list)

    k = np.random.uniform(low=2,high=3)

    length = np.random.gamma(4.2,scale=85)  # root length distribution: gamma, scale 85, shape 4.2 (suggested by Viacheslav)
    # length = 500

    while length < 100 or length > 600:  # restriction on root length: 100-600 suggested in the group chat
        length = np.random.gamma(4.2,scale=85)
        # length = 500

    length = int(length)  # gene length has to be integer

    with open("test_y/"+str(x)+".txt","w") as file:
        file.write(str(flag))

    with open("length/"+str(x)+".txt","w") as file:
        file.write(str(length))

    with open("reference/parameters/"+str(x)+".txt","w") as file:
        file.write(str(p0)+"\n")
        file.write(str(p1)+"\n")
        file.write(str(w0)+"\n")
        file.write(str(w0)+"\n")
        file.write(str(w1)+"\n")
        file.write(str(w2)+"\n")
        file.write(str(length)+"\n")
        file.write(str(k)+"\n")

    if indel_distribution == "NB":
        create_NB_control(p0,p1,w0,w1,w2,tree_topology,length,k,indel_rate,randomseed=indelible_seed)
        # create_no_indel_control(p0,p1,w0,w1,w2,tree_topology,length,k,indel_rate,randomseed=indelible_seed)
    elif indel_distribution == "POW":
        create_zeta_control(p0,p1,w0,w1,w2,tree_topology,length,k,indel_rate,randomseed=indelible_seed)
        # create_no_indel_control(p0,p1,w0,w1,w2,tree_topology,length,k,indel_rate,randomseed=indelible_seed)
    if (len(argv)) > 10:
        simulate_run(str(x), True)
    else:
        simulate_run(str(x))


os.chdir("../")
os.system("chmod -R 777 "+folder)
