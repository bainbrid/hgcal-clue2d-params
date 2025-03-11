# hgcal-clue2d-params

## Build
```
# log into lxplus
cmsrel CMSSW_14_1_0_pre5
cd CMSSW_14_1_0_pre5/src
cmsenv
git cms-init
git cms-rebase-topic waredjeb:split_clue2d_parameters
git cms-checkdeps -a -A
scram b -j 8
```

## Run 
```
git clone git@github.com:bainbrid/hgcal-clue2d-params.git
cd hgcal-clue2d-params
cmsRun CE_E_Front_120um_cfi_GEN_SIM.py
cmsRun step2_DIGI_L1TrackTrigger_L1_L1P2GT_DIGI2RAW_HLT.py
# edit delta_c setting in RecoLocalCalo/HGCalRecProducers/python/hgcalLayerClusters_cff.py
cmsRun step3_RAW2DIGI_RECO_RECOSIM_PAT_VALIDATION_DQM.py
# ntuple found in "histo.root"
```
