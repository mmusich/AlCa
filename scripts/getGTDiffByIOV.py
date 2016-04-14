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
    parser.add_option('-L','--last',help='compares the very last IOV' , dest='lastIOV',action='store_true', default=False)
    parser.add_option('-T','--TargetGT'   ,help='Target Global Tag'   , dest='tarGT', action='store', default='74X_dataRun2_HLTValidation_Queue')
    (opts, args) = parser.parse_args()

    import CondCore.Utilities.CondDBFW.shell as shell
    con = shell.connect()

    myGTref = con.global_tag(name=opts.refGT).tags(amount=1000).as_dicts()
    myGTtar = con.global_tag(name=opts.tarGT).tags(amount=1000).as_dicts()

    differentTags = {}

    for element in myGTref:
        RefRecord = element["record"]
        RefLabel  = element["label"]
        RefTag    = element["tag_name"]

        for element2 in myGTtar:
            if (RefRecord == element2["record"] and RefLabel==element2["label"]): 
                if RefTag != element2["tag_name"]:
                    differentTags[RefRecord]=(RefTag,element2["tag_name"],RefLabel)

    print "| *Record* | *"+opts.refGT+"* | *"+opts.tarGT+"* |"
       
    

    for Rcd in sorted(differentTags):

        #print Rcd,differentTags[Rcd][2]," 1:",differentTags[Rcd][0]," 2:",differentTags[Rcd][1]

        refTagIOVs = con.tag(name=differentTags[Rcd][0]).iovs().as_dicts()
        tarTagIOVs = con.tag(name=differentTags[Rcd][1]).iovs().as_dicts()

        if(opts.lastIOV):

            #print "COMPARING the LAST IOV"

            hash_lastRefTagIOV = refTagIOVs[-1]["payload_hash"]
            hash_lastTagTagIOV = tarTagIOVs[-1]["payload_hash"]

            time_lastRefTagIOV = str(refTagIOVs[-1]["insertion_time"])
            time_lastTagTagIOV = str(tarTagIOVs[-1]["insertion_time"])

            if(hash_lastRefTagIOV!=hash_lastTagTagIOV):
                print "| ="+Rcd+"= ("+differentTags[Rcd][2]+") | =="+differentTags[Rcd][0]+"==  | =="+differentTags[Rcd][1]+"== |"
                print "|^|"+hash_lastRefTagIOV+" ("+time_lastRefTagIOV+") | "+hash_lastTagTagIOV+" ("+time_lastTagTagIOV+") |"

        else:    

            theGoodRefIOV=-1
            theGoodTarIOV=-1
            theRefPayload=""
            theTarPayload=""
            theRefTime=""
            theTarTime=""

            for IOV in refTagIOVs:
                sinceRefTagIOV = IOV["since"]
                if (sinceRefTagIOV < int(opts.testRunNumber)):
                    theGoodRefIOV=sinceRefTagIOV
                    theRefPayload=IOV["payload_hash"]
                    theRefTime=str(IOV["insertion_time"])
          
            for IOV in tarTagIOVs:
                sinceTarTagIOV = IOV["since"]
                if (sinceTarTagIOV < int(opts.testRunNumber)):
                    theGoodTarIOV=sinceTarTagIOV
                    theTarPayload=IOV["payload_hash"]
                    theTarTime=str(IOV["insertion_time"])
        
                    if(theRefPayload!=theTarPayload):
                        print "| ="+Rcd+"= ("+differentTags[Rcd][2]+") | =="+differentTags[Rcd][0]+"==  | =="+differentTags[Rcd][1]+"== |"
                        print "|^|"+theRefPayload+" ("+theRefTime+") | "+theTarPayload+" ("+theTarTime+") |"
                       

if __name__ == "__main__":        
    main()


