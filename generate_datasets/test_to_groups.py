import os
from sys import argv

# argv[1], argv[2] = start, end
# argv[3] = divergence flag (baseline/low/high)
# argv[4] = indel distribution (NB=negative binomial, POW=power law)
# argv[5] = indel rate
# argv[6] = dataset ID
# argv[7] = test flag

max_size = 2000

start = int(argv[1])
end = int(argv[2])

diff = end - start
e = start
for x in range(diff//max_size):
    s = start + x * max_size
    e = s + max_size

    if len(argv) == 11:
        os.system("python test_generator.py "+str(s)+" "+str(e)+" "+argv[3]+" "+argv[4]+" "+argv[5]+" "+argv[6]+" "+argv[7]+" "+argv[8]+" "+argv[9]+" "+argv[10])
    else:
        os.system("python test_generator.py "+str(s)+" "+str(e)+" "+argv[3]+" "+argv[4]+" "+argv[5]+" "+argv[6]+" "+argv[7]+" "+argv[8]+" "+argv[9])

if len(argv) == 11:
    os.system("python test_generator.py "+str(e)+" "+str(end)+" "+argv[3]+" "+argv[4]+" "+argv[5]+" "+argv[6]+" "+argv[7]+" "+argv[8]+" "+argv[9]+" "+argv[10])
else:
    os.system("python test_generator.py "+str(e)+" "+str(end)+" "+argv[3]+" "+argv[4]+" "+argv[5]+" "+argv[6]+" "+argv[7]+" "+argv[8]+" "+argv[9])
