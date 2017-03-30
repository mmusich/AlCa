#!/bin/tcsh

set listOfRuns=(Run290198 Run290336 Run290346 Run290348 Run290351)

foreach i (`seq $#listOfRuns`)
    echo $i
    set mydbfile=`eos ls /store/express/tier0_harvest | grep SiStripBadStrip_pcl | grep $listOfRuns[$i] | grep .db` 
    echo $mydbfile
    set mymetadata=`eos ls /store/express/tier0_harvest | grep SiStripBadStrip_pcl | grep $listOfRuns[$i] | grep .txt |grep uploaded` 
    echo $mymetadata
    cmsStage /store/express/tier0_harvest/$mydbfile .
    cmsStage /store/express/tier0_harvest/$mymetadata .
    set out=`echo $mymetadata | sed "s:.uploaded::g"`
    mv ./$mymetadata ./$out
end
