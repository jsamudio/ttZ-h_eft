### ######## ###
## Config for ##
# jme handling #
## ########## ##
#import subprocess as sb
from config.ana_cff import cdir
# get current working directory according to git
#_wdir = sb.check_output('echo $(git rev-parse --show-toplevel)', shell=True).decode().strip('\n')+'/DeepSleep/'
_wdir, _cdir = cdir()
'''
For now this serves as just
a file referencing map
for ak8 jme correction module
'''

jme_dir  = _wdir+'data'

jec_vc   = {'2016':'Summer16_07Aug2017_V11_MC', # good 
            '2017':'Fall17_17Nov2017_V32_MC',   # good 
            '2018':'Autumn18_V19_MC'            # good 
        }
jer_vc   = {'2016':'Summer16_25nsV1b_MC',       # good 
            '2017':'Fall17_V3b_MC',             # V3 (not V3b...) 
            '2018':'Autumn18_V7b_MC'            # V8 (or V7, not V7b)
        }


ak8_jme_files = {'jec'  : (lambda year : 
                           [f'{jme_dir}/jec/{jec_vc[year]}/{jec_vc[year]}_L1FastJet_AK8PFPuppi.jec.txt',
                            f'{jme_dir}/jec/{jec_vc[year]}/{jec_vc[year]}_L2Relative_AK8PFPuppi.jec.txt',
                            f'{jme_dir}/jec/{jec_vc[year]}/{jec_vc[year]}_L3Absolute_AK8PFPuppi.jec.txt']),
                 'junc' : (lambda year : 
                           f'{jme_dir}/jec/{jec_vc[year]}/{jec_vc[year]}_Uncertainty_AK8PFPuppi.junc.txt'),
                 'jer'  : (lambda year : 
                           f'{jme_dir}/jer/{jer_vc[year]}/{jer_vc[year]}_PtResolution_AK8PFPuppi.jr.txt'),
                 'jersf': (lambda year : 
                           f'{jme_dir}/jer/{jer_vc[year]}/{jer_vc[year]}_SF_AK8PFPuppi.jersf.txt') 
             }

