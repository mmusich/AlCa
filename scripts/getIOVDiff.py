#!/usr/bin/env python

import datetime,time
import os,sys
import string, re
import subprocess
import ConfigParser
from optparse import OptionParser,OptionGroup

#####################################################################
def getCommandOutput(command):
#####################################################################
    """This function executes `command` and returns it output.
    Arguments:
    - `command`: Shell command to be invoked by this function.
    """
    child = os.popen(command)
    data = child.read()
    err = child.close()
    if err:
        print '%s failed w/ exit code %d' % (command, err)
    return data

#################
def main():            
### MAIN LOOP ###

    desc="""This is a description of %prog."""
    parser = OptionParser(description=desc,version='%prog version 0.1')
    parser.add_option('-r','--run', help='test run number', dest='testRunNumber', action='store', default='251883')
    parser.add_option('-R','--ReferenceGT',help='Reference Global Tag', dest='refGT', action='store', default='GR_H_V58C')
    parser.add_option('-T','--TargetGT'   ,help='Target Global Tag'   , dest='tarGT', action='store', default='74X_dataRun2_HLTValidation_Queue')
    (opts, args) = parser.parse_args()

    out = getCommandOutput("conddb diff "+opts.refGT+" "+opts.tarGT) 
    lines = out.split('\n')
    listOfRefTags = []
    listOfTarTags = []

    for line in lines[2:]:
        tags = line.split(" ")
        tag_list = filter(None, tags) # fastest
        #print tag_list
        if(len(tag_list)>0):
            listOfRefTags.append(tag_list[2])
            listOfTarTags.append(tag_list[3])
      
    #print listOfRefTags
    #print listOfTarTags

    for i in range(len(listOfRefTags)):
         out2 = getCommandOutput("conddb diff "+listOfRefTags[i]+" "+listOfTarTags[i]+" -s")
         rawIOVs = out2.split('\n')
         for rawIOV in rawIOVs[2:]:
             IOV = rawIOV.split(" ")
             filteredIOVs = filter(None,IOV) # fastest
             if(len(filteredIOVs) > 0):
                b_run = int((filteredIOVs[0].replace('[','')).replace(',',''))
                e_run = -999999
                if ('Infinity' in filteredIOVs[1]):
                    e_run = 9999999
                else:
                    e_run = int(filteredIOVs[1].replace(')',''))
                if (b_run < int(opts.testRunNumber) and e_run > int(opts.testRunNumber)):
                    print rawIOVs[0]
                    print rawIOVs[1]
                    print b_run,"-",e_run,filteredIOVs[2],filteredIOVs[3]

if __name__ == "__main__":        
    main()


