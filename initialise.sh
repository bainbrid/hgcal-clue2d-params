runTheMatrix.py -w upgrade -l 29696.203 -j 0 --nEvents 1000
cd 29696.203_CloseByPGun_CE_E_Front_120um+2026D110_ticl_v5
cat <<@EOF >> step3_RAW2DIGI_RECO_RECOSIM_PAT_VALIDATION_DQM.py 
from RecoHGCal.TICL.customiseTICLFromReco import customiseTICLForDumper
process = customiseTICLForDumper(process)
@EOF
