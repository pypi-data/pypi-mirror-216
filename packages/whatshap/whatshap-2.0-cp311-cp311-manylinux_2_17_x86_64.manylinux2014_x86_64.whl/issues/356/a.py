import sys
from whatshap.vcf import VcfReader

vcf = VcfReader(sys.argv[1], phases=True)
for record in vcf:
  print(record)
