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
    # tree_topology = "((((aaaaaaaaai:1,aaaaaaaaaj:1)1:1,((aaaaaaaaak:1,(aaaaaaaaal:1,aaaaaaaaam:1)1:1)1:1,((aaaaaaaaan:1,aaaaaaaaao:1)1:1,(aaaaaaaaap:1,aaaaaaaaaq:1)1:1)1:1)1:1)1:1,(((aaaaaaaaar:1,(aaaaaaaaas:1,aaaaaaaaat:1)1:1)1:1,((aaaaaaaaau:1,(aaaaaaaaav:1,(aaaaaaaaaw:1,aaaaaaaaax:1)1:1)1:1)1:1,((aaaaaaaaay:1,(aaaaaaaaaz:1,aaaaaaaabb:1)1:1)1:1,((aaaaaaaabc:1,aaaaaaaabd:1)1:1,(aaaaaaaabe:1,(aaaaaaaabf:1,aaaaaaaabg:1)1:1)1:1)1:1)1:1)1:1)1:1,((aaaaaaaaaa:1,aaaaaaaaab:1)1:1,(aaaaaaaaac:1,aaaaaaaaad:1)1:1)1:1)1:1)1:1,((aaaaaaaaae:1,aaaaaaaaaf:1)1:1,(aaaaaaaaag:1,aaaaaaaaah:1)1:1)1:1);"

n_positive = float(argv[9])


basedir = "/hps/nobackup/goldman/charwest/omega_ai/data/simulations/test_datasets/"

if aligner != "clustal":
    outdir = basedir + dataset_id + "_" + aligner
else:
    outdir = basedir + dataset_id
os.system("mkdir -p " + outdir)

folder = outdir + "/" + "group_" + start
os.system("mkdir " + folder)
os.chdir(folder)

os.system("mkdir prankaa_test_x prankc_test_x mafft_test_x clustal_test_x test_y reference length")
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


# indelible & clustalo executable, pal2nal perl script should be in the directory
def simulate_align(ID, shuffle=False):
    tool_dir = "/hps/nobackup/goldman/charwest/omega_ai/tools/"
    indelible = tool_dir + "indelible"
    clustal = tool_dir + "clustalo"
    pal2nal = tool_dir + "pal2nal.pl"
    prank = tool_dir + "prank/bin/prank"
    mafft = tool_dir + "mafft/bin/mafft"

    os.system(indelible)

    if shuffle:
        # Specify the input FASTA file
        sequences = list(SeqIO.parse("dna.fas", "fasta"))
        os.system("rm dna.fas")
        # print("sequences:")
        # print(sequences)

        random.shuffle(sequences)

        # Write the shuffled sequences to the input file
        SeqIO.write(sequences, "dna.fas", "fasta")

    translated = list()  # translate DNA to aa squence, write to aa.fas
    for record in SeqIO.parse("dna.fas","fasta"):
        record.seq = record.seq.translate()
        translated.append(record)
    with open("aa.fas","w") as file:
        SeqIO.write(translated,file,"fasta")
   
    # CLUSTAL #
    os.system("{} --threads 2 -i aa.fas -o aa_aligned.fas".format(clustal))
    os.system("perl {} -output fasta aa_aligned.fas dna.fas >> codon_aligned.fas".format(pal2nal))
    os.system("mv codon_aligned.fas clustal_test_x/"+ID+".fas")
    os.system("rm aa_aligned.fas")
    
    # MAFFT #
    os.system("{} --thread 2 --quiet aa.fas > aa_aligned.fas".format(mafft))
    os.system("perl {} -output fasta aa_aligned.fas dna.fas >> codon_aligned.fas".format(pal2nal))
    os.system("mv codon_aligned.fas mafft_test_x/"+ID+".fas")
    os.system("rm aa_aligned.fas")
    
    # PRANK_AA #
    os.system("{} -protein -d=aa.fas -o=tmp_aa".format(prank))
    prank_align_dic = {}
    for record in AlignIO.read("tmp_aa.best.fas", "fasta"):
        prank_align_dic[str(record.id)] = str(record.seq)
    with open("aa_aligned.fas", "w") as out_fi:
        if shuffle:
            for header in list(prank_align_dic.keys()):
                out_fi.write(">{}\n{}\n".format(header, prank_align_dic[header]))
        else:
            for header in sorted(list(prank_align_dic.keys())):
                out_fi.write(">{}\n{}\n".format(header, prank_align_dic[header]))
    # Change to correct order 
    seq_order = read_sequence_order("dna.fas")
    reorder_seqs("aa_aligned.fas", seq_order, "corrected_aa_aligned.fas")

    os.system("perl {} -output fasta corrected_aa_aligned.fas dna.fas >> codon_aligned.fas".format(pal2nal))
    os.system("mv codon_aligned.fas prankaa_test_x/"+ID+".fas")
    os.system("rm tmp_aa.best.fas aa_aligned.fas corrected_aa_aligned.fas")

    # PRANK_CODON #
    os.system("{} -codon -d=dna.fas -o=tmp_dna".format(prank))
    for record in AlignIO.read("tmp_dna.best.fas", "fasta"):
       prank_align_dic[str(record.id)] = str(record.seq)
    with open("codon_aligned.fas", "w") as out_fi:
        if shuffle:
            for header in list(prank_align_dic.keys()):
                out_fi.write(">{}\n{}\n".format(header, prank_align_dic[header]))
        else:
            for header in sorted(list(prank_align_dic.keys())):
                out_fi.write(">{}\n{}\n".format(header, prank_align_dic[header]))
    # Change to correct order
    reorder_seqs("codon_aligned.fas", seq_order, "corrected_codon_aligned.fas")
    os.system("mv corrected_codon_aligned.fas prankc_test_x/"+ID+".fas")
    os.system("rm tmp_dna.best.fas")

    # clean
    os.system("rm aa.fas trees.txt")
    os.system("mv LOG.txt reference/LOG/LOG_"+ID+".txt")
    os.system("mv dna.fas reference/output/dna_"+ID+".fas")
    os.system("mv dna_TRUE.fas reference/output_TRUE/dna_TRUE_"+ID+".fas")
    os.system("mv dna_RATES.txt reference/site_classes/dna_RATES_"+ID+".txt")
    os.system("mv control.txt reference/controlFiles/control_"+ID+".txt")
    os.system("rm codon_aligned.fas")


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
    # length = 200

    while length < 100 or length > 600:  # restriction on root length: 100-600 suggested in the group chat
        length = np.random.gamma(4.2,scale=85)
        # length = 200
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
    elif indel_distribution == "POW":
        create_zeta_control(p0,p1,w0,w1,w2,tree_topology,length,k,indel_rate,randomseed=indelible_seed)

    if len(argv) > 10:
        simulate_align(str(x), True)
    else:
        simulate_align(str(x))


os.chdir("../")
os.system("chmod -R 777 "+folder)
