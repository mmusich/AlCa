#!/bin/env python

# This script dumps the content of the AlCaRecoTriggerBits tag provided in input and checks that all the hlt selection paths are selecting some triggers
# by looking at the HLT menu also provided as input. It does the mapping between AlCaRecos and Primary Datasets with the AlCaRecoMatrix.
# The AlCaRecoMatrix is read from the wiki file /afs/cern.ch/cms/CAF/CMSALCA/ALCA_GLOBAL/GTDoc/doc/AlCaRecoMatrix.wiki.
# It produces an output file called validation.txt with the list of matched triggers including prescales.

import sys
import os

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print "Usage: ValidateHLTMenu.py HLTMenu AlCaRecoHLTpathsTag [RunNumber]"
    print "Example: ./ValidateHLTMenu.py /online/collisions/2012/7e33/v2.1/HLT AlCaRecoHLTpaths8e29_5e33_v2_prompt"
    print "If no run number is provided the number 1000000 will be used."
    sys.exit()

HLTMenuName = sys.argv[1]
AlCaRecoHLTPathsTag = sys.argv[2]
RunNumber = 1000000

if len(sys.argv) == 4:
    RunNumber = sys.argv[3]

#os.system("cmscond_2XML -c frontier://PromptProd/CMS_COND_31X_HLT -t "+AlCaRecoHLTPathsTag+" -b " + str(runNumber))
#os.system("edmConfigFromDB --configName "+HLTMenuName+" > hlt.py")
#os.system("conddb_ -c frontier://FrontierProd/CMS_CONDITIONS -c sqlite:"+AlCaRecoHLTPathsTag+".db -i "+AlCaRecoHLTPathsTag+" -t tmp1 -b " + str(runNumber))

os.system("cp AlCaRecoTriggerBitsRcdRead_FromTag_cfg.py "+AlCaRecoHLTPathsTag+"_BitsRcdRead_FromTag_cfg.py")
os.system("sed -i 's~AlCaRecoHLTPathsTag~"+AlCaRecoHLTPathsTag+"~g' "+AlCaRecoHLTPathsTag+"_BitsRcdRead_FromTag_cfg.py")
os.system("sed -i 's~RunNumber~"+str(RunNumber)+"~g' "+AlCaRecoHLTPathsTag+"_BitsRcdRead_FromTag_cfg.py")

os.system("cmsRun "+AlCaRecoHLTPathsTag+"_BitsRcdRead_FromTag_cfg.py")

os.system("hltGetConfiguration "+HLTMenuName+" --unprescale --offline > hlt.py")
os.system("hltDumpStream hlt.py > dumpStream.txt")


# print "Validating AlCaRecoTriggerBits with HLT menu"
# print "Extract the list of PDs and associated triggers from the menu"

# Need to check: trigger names matching the ones in the AlCaRecoTriggerBits, if they are prescaled, if all the PDs required in the alcareco matrix match or not.

outputFile = open("validation.txt", "w")

def findHLTPath(PrimaryDataset, HLTpath, HLTMenu):
    matchingTriggers = []
    PDmatch=''
    for AlCaRecoPD in PrimaryDataset:
      # loop over all primary dataset that an ALCARECO is in
      for PD in HLTMenu:
        #print 'PD in HLT menu ',PD[0]
        if PD[0].find("dataset "+AlCaRecoPD) != -1:
            if(PDmatch==''):
              PDmatch=AlCaRecoPD
            else : PDmatch=PDmatch+','+AlCaRecoPD
            for path in PD:
                if path.find(HLTpath.rstrip("*")) != -1:
                    matchingTriggers.append(path.rstrip("\n"))
        else : continue

    if len(matchingTriggers) == 0:
        # print "\nError: no matching triggers found for selection string " + HLTpath + "\n"
        outputFile.write("\nError: no matching triggers found for selection string " + HLTpath + "\n\n")
    else:
        outputFile.write("The following matching triggers were found in the Primary Dataset " +PDmatch+ " for trigger selection string \"" + HLTpath + "\":\n\n")
        for trigger in matchingTriggers:
            # print trigger
            outputFile.write(trigger+"\n")
        outputFile.write("\n") 


# read the AlCaRecoMatrix and prepare a dictionary of AlCaReco-PD
AlCaRecoMatrix = {}
for line in open("AlCaRecoMatrix.wiki"):
    if line.find("*Primary Dataset*") != -1:
        continue
    splittedLine = line.split("|")
    if len(splittedLine) > 2:
        for AlCaReco in splittedLine[2].split(","):
            if AlCaReco.strip() not in AlCaRecoMatrix : # alca reco attached to a PD 
              AlCaRecoMatrix[AlCaReco.strip()]=[];
              AlCaRecoMatrix[AlCaReco.strip()].append(splittedLine[1].strip())
            else : # if alca reco already attached to another PD, append the new PD
              AlCaRecoMatrix[AlCaReco.strip()].append(splittedLine[1].strip()) 

# Read the trigger menu and prepare a list of triggers for each PD
HLTMenu = []
for line in open("dumpStream.txt"):
    if line.startswith("    dataset "):
        HLTMenu.append([])
        HLTMenu[len(HLTMenu)-1].append(line.strip())
    if len(HLTMenu) > 0:
        HLTMenu[len(HLTMenu)-1].append(line.strip())

# Read the AlCaRecoTriggerBits xml dump and find the triggers in the menu
isAlCaRecoName = True
for line in open("triggerBits_"+AlCaRecoHLTPathsTag+".twiki") : #"AlCaRecoHLTpaths8e29_5e33_v2_prompt.xml"):
    if line.find("|") != -1:
        #print 'AlCaReco is ',line.split('|')[1].strip().strip("\'")
        if isAlCaRecoName:
            AlCaReco = line.split('|')[1].strip().strip("\'")
            isAlCaRecoName = False
        else:
            # print "\n\n---------------------------------------------------------------------------------------------------"
            # print "Checking AlCaReco: \"" + AlCaReco + "\" with selection string: \"" + element + "\""
            # print "---------------------------------------------------------------------------------------------------\n"
            AlCaReco = line.split('|')[1].strip().strip("\'").strip()
            element = line.split('|')[2].strip().strip("\'").strip()
            #print 'HLT paths are ',element
            outputFile.write("\n\n---------------------------------------------------------------------------------------------------\n")
            outputFile.write("Checking AlCaReco: \"" + AlCaReco + "\" with selection string: \"" + element + "\"\n")
            outputFile.write("---------------------------------------------------------------------------------------------------\n\n")
            #isAlCaRecoName = True
            # Some of the AlCaRecos have no keys
            triggerSelectionStringList = element
            if triggerSelectionStringList == "":
                # print "This AlCaReco has no keys. It is either disabled or accepting everything. Listing all the triggers available in the PD"
               if AlCaReco in AlCaRecoMatrix:       
                  PDmatch=''
                  PDunmatch=''
                  for AlCaRecoPD in AlCaRecoMatrix[AlCaReco]:
                     isInHLTMenu=False 
                     for PD in HLTMenu:
                         print "PD in HLT menu ",PD[0]
                         if PD[0].find("dataset "+AlCaRecoPD) != -1:
                            if PDmatch=='' :
                               PDmatch=AlCaRecoPD
                            else :
                               PDmatch=PDmatch+','+AlCaRecoPD
                            isInHLTMenu=True
                     if isInHLTMenu==False :
                        if PDunmatch=='' :
                           PDunmatch=AlCaRecoPD
                        else :
                           PDunmatch=PDunmatch+','+AlCaRecoPD
                  if(PDmatch=='') :
                       outputFile.write("This AlCaReco has no keys. But It is either disabled or accepting everything but the PD "+PDunmatch+" not in the HLT menu"+"\n")
                  elif (PDunmatch=='') : 
                          outputFile.write("This AlCaReco has no keys. It is either disabled or accepting everything in the PD "+PDmatch+" in the menu"+"\n")
                  else : 
                       outputFile.write("This AlCaReco has no keys. It is either disabled or accepting everything in the PD "+PDmatch+" in the menu but PD "+PDunmatch+" not the menu"+"\n")
               else:
                  outputFile.write("This AlCaReco is not in the matrix\n")
            else:
                if AlCaReco in AlCaRecoMatrix:
                   for triggerSelectionString in triggerSelectionStringList.split(","):
                        triggerSelectionString=triggerSelectionString.strip().strip("\'")
                        print 'trigger ',triggerSelectionString,' for AlCaReco ',AlCaReco
                        findHLTPath(AlCaRecoMatrix[AlCaReco], triggerSelectionString, HLTMenu)
                else:
                    ## print "This AlCaReco is not in the matrix"
                   outputFile.write("This AlCaReco is not in the matrix\n")

outputFile.close()

print "Comparison done. Please, check the validation.txt file for details."

