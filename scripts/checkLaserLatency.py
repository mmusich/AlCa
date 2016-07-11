#!/usr/bin/env python

"""
Example script to extract tags given an hash
"""

import os
import sys
import optparse
import hashlib
import tarfile
import netrc
import getpass
import errno
import sqlite3
import json
import tempfile
from prettytable import PrettyTable
from datetime import datetime,timedelta

def unpack(i):
    """unpack 64bit unsigned long long into 2 32bit unsigned int, return tuple (high,low)
    """
    high=i>>32
    low=i&0xFFFFFFFF
    return(high,low)


#### Needs cmsrel inside a CMSSW > 80X
countWrongIOVs=0
from CondCore.Utilities.CondDBFW import querying
connection = querying.connect("frontier://pro/CMS_CONDITIONS")
TagIOVs = connection.tag(name="EcalLaserAPDPNRatios_prompt_v2").iovs().as_dicts()
for iIOV in TagIOVs:
    since = datetime.fromtimestamp(unpack(int(iIOV["since"]))[0])
    #print iIOV["insertion_time"],iIOV["since"],since
    if( ((iIOV["insertion_time"]-since) > timedelta(days=2) ) and iIOV["insertion_time"] > datetime(2016, 1, 1, 0, 0, 0) ):
        print "For Since=", since," the delay is > 2 days, i.e.: ====> ",(iIOV["insertion_time"]-since)
        countWrongIOVs=countWrongIOVs+1

print countWrongIOVs
        
