import os
import time
from sys import argv
from datetime import datetime

# argv[1], argv[2] = start, end
# argv[3] = divergence flag (baseline/low/high)
# argv[4] = indel distribution (NB=negative binomial, POW=power law)
# argv[5] = indel rate
# argv[6] = dataset ID
# argv[7] = test flag
# argv[8] = aligner
# argv[9] = tree, 8 for 8-tip baseline; 32/64 for alternate topologies
# argv[10] = proportion of alignments to be simulated with high values of omega

max_size = 2000

start = int(argv[1])
end = int(argv[2])

diff = end - start
e = start
for x in range(diff//max_size):
    s = start + x * max_size
    e = s + max_size

    start_i = time.time()
    print("this is length of argv: {}".format(len(argv)))

    if len(argv) == 12:
        os.system("python simple_generator.py "+str(s)+" "+str(e)+" "+argv[3]+" "+argv[4]+" "+argv[5]+" "+argv[6]+" "+argv[7]+" "+argv[8]+" "+argv[9]+" "+argv[10]+" "+argv[11])   
    elif (len(argv)==13):
        os.system("python simple_generator.py "+str(s)+" "+str(e)+" "+argv[3]+" "+argv[4]+" "+argv[5]+" "+argv[6]+" "+argv[7]+" "+argv[8]+" "+argv[9]+" "+argv[10]+" "+argv[11]+" "+argv[12])
    else:
        os.system("python simple_generator.py "+str(s)+" "+str(e)+" "+argv[3]+" "+argv[4]+" "+argv[5]+" "+argv[6]+" "+argv[7]+" "+argv[8]+" "+argv[9]+" "+argv[10])
    end_i = time.time() - start_i
    print("Per run time: " + str(end_i))

start = time.time()
if len(argv) == 12:
    os.system("python simple_generator.py "+str(e)+" "+str(end)+" "+argv[3]+" "+argv[4]+" "+argv[5]+" "+argv[6]+" "+argv[7]+" "+argv[8]+" "+argv[9]+" "+argv[10]+" "+argv[11])
elif (len(argv)==13):
    os.system("python simple_generator.py "+str(e)+" "+str(end)+" "+argv[3]+" "+argv[4]+" "+argv[5]+" "+argv[6]+" "+argv[7]+" "+argv[8]+" "+argv[9]+" "+argv[10]+" "+argv[11]+" "+argv[12])
else:
    os.system("python simple_generator.py "+str(e)+" "+str(end)+" "+argv[3]+" "+argv[4]+" "+argv[5]+" "+argv[6]+" "+argv[7]+" "+argv[8]+" "+argv[9]+" "+argv[10])
end = time.time() - start
print("Final run time: " + str(end))
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("Final datetime is: " + current_datetime)