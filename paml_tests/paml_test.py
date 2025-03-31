#!/usr/bin/env python3

# Code Authorship:
#   Original implementation: Xingze Xu
#   Contributors:
#       - Conor R. Walker
#       - Charlotte West

from Bio.Phylo.PAML import codeml
import os
from scipy.stats import chi2
import time
from sys import argv


def paml_selection(alignment_file, tree_file, work_dir):
    """Test for selection using codeml.
    
    Args:
        alignment_file:
            The path to a nucleotide alignment in fasta format.
        tree_file:
            The path to a tree in newick format. Assumes branch lengths are
            specified.
    Returns:
        1 if the alignment is inferred to have evolved under positive selection,
        0 otherwise.
    """
    # initialize codeml
    cml = codeml.Codeml(

        alignment=alignment_file,
        tree=tree_file,
        working_dir=work_dir,
        out_file=work_dir + alignment_file.split('/')[-1] + ".out"
    )
    
    # provide verbose output
    cml.set_options(verbose=1)
    # 0: indicates a user-specified tree is provided
    cml.set_options(runmode=0)
    # 1: indicates codon sequences are provided
    cml.set_options(seqtype=1)
    # 2: estimates codon frequencies using F3x4 (assume individual nucleotide
    # frequencies at each codon position)
    cml.set_options(CodonFreq=2)
    # 0: do not assume a molecular clock
    cml.set_options(clock=0)
    # 0: JC69
    cml.set_options(model=0)
    # model comparisons
    # 1: M1a (neutral), 2: M2a (selection), 7: M7 (beta), and 8: M8 (beta&w)
    cml.set_options(NSsites=[1, 2, 7, 8])
    # 1: universal code
    cml.set_options(icode=0)
    # 0: kappa is estimated
    cml.set_options(fix_kappa=0)
    # 2: initial kappa
    cml.set_options(kappa=2)
    # 0: omega is estimated
    cml.set_options(fix_omega=0)
    # 1: initial omega
    cml.set_options(omega=1)
    # 1: fix gamma share parameter
    cml.set_options(fix_alpha=1)
    # 0: infinity (constant rate)
    cml.set_options(alpha=0)
    # 0: different alphas for genes
    cml.set_options(Malpha=0)
    # 0: don't get standard errors of estimates
    cml.set_options(getSE=0)
    # 0: do not reconstruct ancestral states
    cml.set_options(RateAncestor=0)
    # 2: fix branch lengths # 1: let paml estimate branch lengths
    cml.set_options(fix_blength=1)
    # 0: update all parmaeters including branch lengths simultaneously
    cml.set_options(method=0)

    res = cml.run(command=os.path.join(os.getcwd(), "codeml"))

    # calculate likelihood ratios
    lmd1 = 2 * (res["NSsites"][2]["lnL"] - res["NSsites"][1]["lnL"])
    lmd2 = 2 * (res["NSsites"][8]["lnL"] - res["NSsites"][7]["lnL"])

    # return 1 (positive selection if both chi2 model comparisons pass 5% alpha)
    lmd1_res = chi2.cdf(lmd1, 2)
    lmd2_res = chi2.cdf(lmd2, 2)

    if (lmd1_res > 0.95) and (lmd2_res > 0.95):
        result = 1
    else:
        result = 0

    return result, lmd1_res, lmd2_res


def main():
    paml_result, lmd1_res, lmd2_res = paml_selection(argv[1], argv[2], argv[3])

    file_base = argv[4]

    with open(file_base + "_res.txt", 'w') as file:
        file.write(str(paml_result))
    
    with open(file_base + "_probs.txt", 'w') as file:
        file.write("{0},{1}".format(lmd1_res, lmd2_res))

if __name__ == "__main__":
    main()