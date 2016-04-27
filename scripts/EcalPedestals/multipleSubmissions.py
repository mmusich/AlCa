#!/usr/bin/env python
from subprocess import Popen

runRanges = ['124333_133621','133622_142340','142345_147521','147523_160666','160669_169977','170098_176558','176559_187329','187330_198739','198740_208953','209216_262439','264480_271569']

runRanges.sort()

for iIOV in range(len(runRanges)):
    print iIOV, runRanges[iIOV]
    Popen('cp EcalPedestals_1_124332.txt EcalPedestals_'+str(runRanges[iIOV])+'.txt',shell=True).wait()
    Popen('uploadConditions.py EcalPedestals_'+str(runRanges[iIOV])+'.db',shell=True).wait()
              
              

