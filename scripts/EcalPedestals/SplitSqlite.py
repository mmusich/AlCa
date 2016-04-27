#!/usr/bin/env python
# Oringally from G.Benelli and Arun Mittal  
# modified by M. Musich                                                                                                                                                                                
#Oct 3 2015                                                                                                                                                                                                 

import subprocess
#Input IOVs:                                                                                                                                                                                                
#Reference for the use of subprocess Popen to execute a command:                                                                                                                                            
#subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()                                                                                                         
#Let's prepare a container for the list of IOVs:                                                                                                                                                            
IOVs=[]
for line in subprocess.Popen("conddb --noLimit --db EcalPedestals_express.db list EcalPedestals_express",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.readlines():
    if "<EcalPedestal>" in line:
        #IOVs.append((line.split()[2].strip(')')).strip('('))
        IOVs.append(line.split()[0])
print IOVs
print "There are %s IOVs!"%len(IOVs)

#Prepare the conddb_import commands template:                                                                                                                                     
#Let's assemble the commands now!                                                                                                                                                                           
#Let's pick IOVs every 80:                                                                                                                                                                                   
RelevantIOVs=[(IOV,IOVs[IOVs.index(IOV)+79],IOVs[IOVs.index(IOV)+80]) for IOV in IOVs if IOVs.index(IOV)==0 or ((IOVs.index(IOV))%80==0 and (IOVs.index(IOV)+80)<len(IOVs))]

RelevantIOVs.append((RelevantIOVs[-1][2],IOVs[-1],IOVs[-1]))

print RelevantIOVs
for i,splitIOVs in enumerate(RelevantIOVs):
    begin=splitIOVs[0]
    end=splitIOVs[1]
    upperLimit=splitIOVs[1]
    print i,begin,end,upperLimit
    command="conddb_import -f sqlite_file:EcalPedestals_express.db -c sqlite:EcalPedestals_"+begin+"_"+end+".db -i EcalPedestals_express -t EcalPedestals_express -b "+begin +" -e "+end
#+" -e "+upperLimit
    print command
    
    #Now if we want to execute it inside Python uncomment the following two lines:                                                                                      
    STDOUT=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()                                                             
    print STDOUT                                                                                                                                                           

#for counter in range(0,len(IOVs),5):                                                                                                                                  
#    if counter+1<len(IOVs):                                                                                                                                               
#        print counter, IOVs[counter], IOVs[counter+1]                                                                                                                     
#    else:                                                                                                                                                                  
#        print counter, IOVs[counter]
