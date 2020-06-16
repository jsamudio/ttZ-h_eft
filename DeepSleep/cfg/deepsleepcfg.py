###############
## Config for ##
## Deep Sleep ##
################
#
master_file_path  = './files/'
# Overhead #
file_path         = '/cms/data/store/user/ttxeft/Skim_nanoAOD/'
tree_dir          = 'Training'
##
ZHptcut           = 200
##
##############
##### TTZ, Z to bb CONFIG #####
ZHbbFitCfg    = (['result_2017'],#
                 #['WJets','ZJets','DY','DiBoson','TriBoson','TTX','QCD','TTBarHad','TTBarLep','TTZ/H'],
                 [ 'TTZH', 'QCD',  'TTX',  'DY', 'WJets', 'TTBarHad',  'DiBoson',  'TriBoson', 'TTBarLep','ZJets'],
                 #[ 'TTZH', 'QCD',  'TTX',  'DY', 'WJets', 'DiBoson',  'TriBoson', 'TTBarLep'],#'ZJets'],
                 
#                 ['TTBarLep'],
)
ZHbbFitMinJets = 4
ZHbbFitMaxJets = 100
ZHbb_btagWP    = .4941 # Med for 2017
# ttZ/H->bb SM x-section
ZHbbXsec = {'ttZbb': .1157,
            'ttHbb': .2934 }
ZHbbtotXsec = ZHbbXsec['ttZbb'] + ZHbbXsec['ttHbb']
# ttZ/H->bb MC count 2017
n_ZHbbMC_dict      = {'ttZbb': 163876,
                      'ttHbb': 5698653 }
n_ZHbbMC           = n_ZHbbMC_dict['ttZbb'] + n_ZHbbMC_dict['ttHbb']

###################
# Input Variables #
LC = '_drLeptonCleaned'
#
ana_vars = {
    'ak4vars'    : ['Jet_btagDeepB'+LC, 'Jet_deepFlavourlepb'+LC, 'Jet_deepFlavouruds'+LC, 'Jet_deepFlavourb'+LC, 'Jet_deepFlavourbb'+LC],
    'ak4lvec'    : {'TLV'         :['JetTLV'+LC],
                    'TLVarsLC'    :['Jet_pt'+LC, 'Jet_eta'+LC, 'Jet_phi'+LC, 'Jet_mass'+LC],
                    'TLVars'      :['Jet_pt', 'Jet_eta', 'Jet_phi', 'Jet_mass'],
                    'jesTotUp'    :['Jet_pt_jesTotalUp', 'Jet_eta' 'Jet_phi', 'Jet_mass_jesTotalUp'],
                    'jesTotDown'  :['Jet_pt_jesTotalDown', 'Jet_eta' 'Jet_phi', 'Jet_mass_jesTotalDown'],
                    'jerUp'       :['Jet_pt_jerUp', 'Jet_eta' 'Jet_phi', 'Jet_mass_jerUp'],
                    'jerDown'     :['Jet_pt_jerDown', 'Jet_eta' 'Jet_phi', 'Jet_mass_jerDown'],
                },
#
    'ak8vars'    : ['FatJet_tau1'+LC,'FatJet_tau2'+LC,'FatJet_tau3'+LC,'FatJet_tau4'+LC,
                    'FatJet_deepTag_WvsQCD'+LC,'FatJet_deepTag_TvsQCD'+LC,'FatJet_deepTag_ZvsQCD'+LC,
                    'FatJet_deepTagMD_H4qvsQCD'+LC, 'FatJet_deepTagMD_HbbvsQCD'+LC, 'FatJet_deepTagMD_TvsQCD'+LC, 
                    'FatJet_deepTagMD_WvsQCD'+LC, 'FatJet_deepTagMD_ZHbbvsQCD'+LC, 'FatJet_deepTagMD_ZHccvsQCD'+LC, 
                    'FatJet_deepTagMD_ZbbvsQCD'+LC, 'FatJet_deepTagMD_ZvsQCD'+LC, 'FatJet_deepTagMD_bbvsLight'+LC, 'FatJet_deepTagMD_ccvsLight'+LC, 
                    'FatJet_msoftdrop'+LC,'FatJet_btagDeepB'+LC,'FatJet_btagHbb'+LC,
                    'FatJet_subJetIdx1'+LC,'FatJet_subJetIdx2'+LC],
    'ak8lvec'    : {'TLV'      :['FatJetTLV'+LC],
                    'TLVarsLC' :['FatJet_pt'+LC, 'FatJet_eta'+LC, 'FatJet_phi'+LC, 'FatJet_mass'+LC],
                    'TLVars'   :['FatJet_pt', 'FatJet_eta', 'FatJet_phi', 'FatJet_mass']},
    'ak8sj'      : ['SubJet_pt', 'SubJet_btagDeepB'],
#
    'genpvars'   : ['GenPart_pt', 'GenPart_eta', 'GenPart_phi', 'GenPart_mass', 'GenPart_status', 'GenPart_pdgId', 'GenPart_genPartIdxMother'], # these are MC only
    'genLevCuts' : ['passGenCuts','isZToLL'], # these are MC only
    'valvars'    : ['nResolvedTops'+LC,'nMergedTops'+LC,'nBottoms'+LC,'nSoftBottoms'+LC,'nJets30'+LC,
                    'MET_phi', 'MET_pt', 'Lep_pt', 'Lep_eta', 'Lep_phi', 'Lep_E',
                    'Pass_IsoTrkVeto', 'Pass_TauVeto', 'Pass_ElecVeto', 'Pass_MuonVeto',
                    'Stop0l_trigger_eff_Electron_pt', 'Stop0l_trigger_eff_Muon_pt', 
                    'Pass_trigger_muon', 'Pass_trigger_electron'],
    'sysvars'    : ['genWeight','weight','BTagWeight','puWeight','ISRWeight','PrefireWeight', # these are MC only
                    'BTagWeight_Up', 'BTagWeight_Down', 'puWeight_Up','puWeight_Down', 'pdfWeight_Up','pdfWeight_Down',
                   'ISRWeight_Up','ISRWeight_Down','PrefireWeight_Up','PrefireWeight_Down'],
    'valRCvars'  : ['ResolvedTopCandidate_discriminator', 'ResolvedTopCandidate_j1Idx', 'ResolvedTopCandidate_j2Idx', 'ResolvedTopCandidate_j3Idx'],
    'label'      : ['isTAllHad']
}

##### DNN backend for Z/H -> bb #####
dnn_ZH_dir  = 'NN_files/'
# only event level variables
dnn_ZH_vars = [
    'max_lb_dr','max_lb_invM', 'n_Zh_btag_sj', 'n_ak4jets', 'Zh_score', 'best_rt_score',
    'n_q_outZh', 'n_b_outZh', 'Zh_l_dr', 'n_Zh_sj', 'n_b_inZh', 'Zh_bestb_sj', 'Zh_worstb_sj',
    'Zh_eta','Zh_deepB','b1_outZh_score', 'best_Zh_b_invM_sd', 'Zh_b1_invM_sd', 'Zh_b2_invM_sd','Zh_l_invM_sd',
    'Zh_Wscore', 'Zh_Tscore', 'n_ak8_Zhbb', 'n_ak8jets', 'n_ak4jets', 'nonZhbb_b1_dr', 'nonZhbb_b2_dr', 
    'Zh_bbscore_sj', 
    'b1_over_Zhpt', 'bb_over_Zhpt',
    'spher','aplan','n_q_inZh']
    #'H_M',
    #'H_pt',
    #'min_lb_invm', 'MET_pt', 'b2oHZpt' 
    #'lb_mtb1', 'lb_invm1', 'lb_dr1',
    ##'weight', 'genWeight'] ####### dont do this...
old_dnn_ZH_vars = [
    'max_lb_dr','max_lb_invm', 'n_H_sj_btag', 'nJets30', 'H_score', 'best_rt_score',
    'n_qnonHbb', 'n_nonHbb', 'Hl_dr', 'n_H_sj', 'n_b_Hbb', 'H_sj_bestb', 'H_sj_worstb',
    'H_eta','H_bbscore','b1_outH_score', 'best_Wb_invM_sd', 'Hb_invM1_sd', 'Hb_invM2_sd','Hl_invm_sd',
    'H_Wscore', 'H_Tscore', 'nhbbFatJets', 'nFatJets', 'nJets', 'nonHbb_b1_dr', 'nonHbb_b2_dr', 
    'H_sj_bbscore', 
    'b1oHZpt', 'bboHZpt',
    'spher','aplan',
    #'H_M',
    #'H_pt',
    #'min_lb_invm', 'MET_pt', 'b2oHZpt' 
    #'lb_mtb1', 'lb_invm1', 'lb_dr1',
    'n_q_Hbb', 'weight', 'genWeight']
uncor_dnn_ZH_vars = [ # tests_failed >= 4 
    'min_lb_dr', 'b2_outH_score'
]
#
dnn_ZH_alpha      = 0.00003 # 200: 0.0003 # 300 : 0.00003
dnn_ZH_batch_size = 512
fl_gamma          = .2 # 200: .1    , 300: 1.5 / .4
fl_alpha          = .85 # 200: .85 , 300: .80 /.85
dnn_ZH_epochs     = 0 #210 ### 200: 120, 300: 100
DNNoutputDir      = 'NN_files/'
DNNoutputName     = 'corr_noweight_noM.h5'
DNNmodelName      = 'corr_noweight_model_noM.h5' 
DNNuseWeights     = True
