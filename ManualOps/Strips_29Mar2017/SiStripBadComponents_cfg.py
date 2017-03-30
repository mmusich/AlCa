import FWCore.ParameterSet.Config as cms

process = cms.Process("CALIB")
##########################################################################
# Message Logger
#########################################################################
process.MessageLogger = cms.Service("MessageLogger",
    destinations = cms.untracked.vstring('cout','cerr','BadComponents_Mar29_2017'), #Reader, cout                                                         
    categories = cms.untracked.vstring('SiStripQualityStatistics'),

    debugModules = cms.untracked.vstring('siStripDigis',
                                         'siStripClusters',
                                         'siStripZeroSuppression',
                                         'SiStripClusterizer',
                                         'siStripOfflineAnalyser'),
    cerr = cms.untracked.PSet(threshold = cms.untracked.string('ERROR')
                              ),
    cout = cms.untracked.PSet(threshold = cms.untracked.string('INFO'),
                                default = cms.untracked.PSet(limit=cms.untracked.int32(0))
                              ),
   BadComponents_Mar29_2017 = cms.untracked.PSet(threshold = cms.untracked.string('INFO'),
                                default = cms.untracked.PSet(limit=cms.untracked.int32(0)),
                                SiStripQualityStatistics = cms.untracked.PSet(limit=cms.untracked.int32(100000))
                                )

)
process.load('Configuration.Geometry.GeometryIdeal_cff')
##########################################################################
# Empty Source specifying a run number to select the IOV
#########################################################################
process.source = cms.Source("EmptyIOVSource",
    firstValue = cms.uint64(290198),
    lastValue = cms.uint64(290198),
    timetype = cms.string('runnumber'),
    interval = cms.uint64(1)
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
#######################################################
# Specifying Global Tag (suitable for the CMSSW release)
######################################################
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '90X_dataRun2_Prompt_v2', '')
process.poolDBESSource = cms.ESSource("PoolDBESSource",
                                      connect = cms.string('sqlite_file:/afs/cern.ch/work/m/musich/public/AlCAOperations/CMSSW_9_0_0/payload/Run290198@SiStripBadStrip_pcl@49ec8d04-1382-11e7-8cac-02163e01a426.db'), 
                                      toGet = cms.VPSet(cms.PSet(record = cms.string('SiStripBadFiberRcd'),
                                                                 tag = cms.string('SiStripBadStrip_pcl')
                                                                 )
                                                        )
                                      )
process.prefer_poolDBESSource = cms.ESPrefer("PoolDBESSource","poolDBESSource")


#####################################################################################################
# BadChannels using a list of modules
#####################################################################################################
#process.load("CalibTracker.SiStripESProducers.fake.SiStripBadModuleConfigurableFakeESSource_cfi")
#process.SiStripBadModuleGenerator.BadComponentList = cms.untracked.VPSet(   cms.PSet(
#    SubDet = cms.string('TEC'),
#    wheel = cms.uint32(0),             ## SELECTION: side = 1(TEC-), 2(TEC+),  0(ALL)	
#    petal = cms.uint32(0),             ## wheel = 1..9, 0(ALL)				
#    detid = cms.uint32(0),             ## petal_bkw_frw = 1(backward) 2(forward) 0(all)	
#    ster = cms.uint32(0),              ## petal = 1..8, 0(ALL)				
#    petal_bkw_frw = cms.uint32(0),     ## ring = 1..7, 0(ALL)				
#    ring = cms.uint32(0),              ## ster = 1(sterero), else(nonstereo), 0(ALL)	
#    side = cms.uint32(0),                  ## detid number = 0 (ALL),  specific number    
#    detidList = cms.untracked.vuint32(
#        470050924
#        )
#    )
#)
#process.siStripBadModuleConfigurableFakeESSource.appendToDataLabel = cms.string('BadModules_from_TECBadCL')

#####################################################################################################
# Create BadChannels from FED detected Errors 
#####################################################################################################
#process.load("CalibTracker.SiStripESProducers.SiStripBadModuleFedErrESSource_cfi")
#process.siStripBadModuleFedErrESSource.appendToDataLabel = cms.string('BadModules_from_FEDBadChannel')
#process.siStripBadModuleFedErrESSource.ReadFromFile = cms.bool(True)
#process.siStripBadModuleFedErrESSource.FileName = cms.string('/afs/cern.ch/user/d/dutta/work/public/BadChannel/MCTags/2017/MCProd/DQM_V0001_R000284035__ZeroBias__Run2016H-PromptReco-v2__DQMIO.root')

###############################################################################################################################
# Use SiStripQualityESProducer to crate Bad Component list merging information from different sources and removing duplications
###############################################################################################################################
process.siStripQualityESProducer.ListOfRecordToMerge = cms.VPSet(
        cms.PSet(record = cms.string('SiStripDetCablingRcd'), tag = cms.string('')),    # Use Detector cabling information to exclude detectors not connected
        cms.PSet(record = cms.string('SiStripBadFiberRcd'), tag = cms.string('')),     # Bad Channel list from the selected IOV
        cms.PSet(record = cms.string("RunInfoRcd"), tag = cms.string("")),            # List of FEDs exluded during data taking
        #        cms.PSet(record = cms.string('SiStripBadModuleFedErrRcd'), tag = cms.string('BadModules_from_FEDBadChannel')) # BadChannel list from FED erroes
)

#################################################################################
#Tool to print list of Bad modules and create Tracker Map indicating Bad modules
#################################################################################
process.stat = cms.EDAnalyzer("SiStripQualityStatistics",
    TkMapFileName = cms.untracked.string('TkMap_Mar29_2017.png'),
    dataLabel = cms.untracked.string('')
)
#### Add these lines to produce a tracker map
process.load("DQMServices.Core.DQMStore_cfg")
process.TkDetMap = cms.Service("TkDetMap")
process.SiStripDetInfoFileReader = cms.Service("SiStripDetInfoFileReader")
####


####################################
# Process Definition
####################################

process.out = cms.OutputModule("AsciiOutputModule")
process.p = cms.Path(process.stat)

process.ep = cms.EndPath(process.out)
