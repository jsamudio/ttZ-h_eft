import uproot
import sys
import numpy as np
import awkward
import concurrent.futures
from collections import defaultdict
#import functools
from modules.AnaDict import AnaDict
from modules.getdata import getData
from lib.fun_library import clop_pear_ci

year = sys.argv[1]

def pickle_mcdata():

    roodir  = '/cms/data/store/user/ttxeft/Skim_nanoAOD/' 
    
    n_events = AnaDict()

    mu_id_map = {0:'loose',1:'med',2:'tight'}
    el_id_map = {0:'fail', 1:'veto',2:'loose',3:'med',4:'tight'}

    
    def mc_ana():
        roofile = f'{roodir}MC_{year}_lep.root'
        with uproot.open(roofile) as f:
            t = {'ttzh':f.get('Training_bb/TTZH'),
                 'tt'  :f.get('Training_bb/TTBarLep')}
            for key in t.keys():
                mu_data, el_data, weight = get_tree_data(t[key])
                if key == 'tt' : calc_lepSel_eff(mu_data,el_data)
                n_events[key] = calc_n_wLepSel(mu_data, el_data, weight)
                del mu_data, el_data, weight
            ##
            s_over_sqrt_b = {k : n_events['ttzh'][k]['sum_w']/np.sqrt(n_events['tt'][k]['sum_w']) for k in n_events['tt']}
            print(f'\n\nTTZH over sqrt TTBarLep, {year} MC\n')
            [print(f'{k:100}\t s/sqrt(b): {v}') for k,v in sorted(s_over_sqrt_b.items(), key=lambda item: item[1], reverse=True)]         
    #
    def data_ana():
        roofile = f'{roodir}Data_{year}_lep.root'
        with uproot.open(roofile) as f:
            t = {'el' : f.get('Training_bb/EleData'),
                 'mu' : f.get('Training_bb/MuData')}
            for key in t.keys():
                mu_data, el_data, weight = get_tree_data(t[key])
                n_events[key] = calc_n_wLepSel(mu_data, el_data, weight, opt=key)
                del mu_data, el_data, weight
            n_data = {k : n_events['el'][k]['sum_w']+n_events['mu'][k]['sum_w'] for k in n_events['el']}
            print(f'\n\n{year} Data Yield\n')
            [print(f"{k:100}\t Yield: {v:10}\t Ele Yield: {n_events['el'][k]['sum_w']}\t Mu Yield: {n_events['mu'][k]['sum_w']}") for k,v in sorted(n_data.items(), key=lambda item: item[1], reverse=True)]

    mc_ana()
    data_ana()
    n_events.to_pickle(f'mcdata_lepsel_{year}.pkl')

def calc_lepSel_eff(mu, el):
    event_mask = getData.DF_Container.event_mask
    mu_num = mu['Muon_pt'][(mu["Muon_miniPFRelIso_all"] < 0.2) & (mu['Muon_FlagId'] >= 1 )][event_mask].flatten() # med id, .2 miniIso
    mu_den = mu['Muon_pt'][event_mask].flatten()
    #
    el_num = el['Electron_pt'][(el['Electron_miniPFRelIso_all'] < 99) & (el['Electron_cutBasedNoIso'] >= 4)][event_mask].flatten() # tight id, .1 miniIso
    el_den = el['Electron_pt'][(el['Electron_cutBasedNoIso'] >= 2)][event_mask].flatten()
    #
    import matplotlib.pyplot as plt
    def plot_eff(num, den, lep):
        bins = np.append(np.linspace(0,100,8+1),[125,150,175,200,250,300,400,500])
        print(bins)
        n_num, _     = np.histogram(num, bins=bins, range=(0,500))
        n_den, edges = np.histogram(den, bins=bins, range=(0,500))
        bin_c = (edges[1:]+edges[:-1])/2
        bin_w = (edges[1:]-edges[:-1])
        lo, hi = clop_pear_ci(n_num,n_den,return_error=True)
        y = n_num/n_den
        yerr = [lo,hi]
        plt.errorbar(x=bin_c, xerr=bin_w/2,
                     y=y, yerr=yerr, fmt='.')
        plt.grid(True)
        plt.xlabel(f'{lep} pT (GeV)')
        plt.title(f'{lep} Selectrion Efficiency, {year}')
        plt.show()
        plt.clf()
        
    plot_eff(el_num,el_den,'Electron')
    plot_eff(mu_num,mu_den,'Muon')
    exit()

def get_tree_data(tree):
    executor = concurrent.futures.ThreadPoolExecutor()
    getData.DF_Container.set_attr(True, year, 4, 99, None,None)
    getData.DF_Container.set_current_tree_mask(tree)
    #
    mu_keys   = ["Muon_pt","Muon_eta","Muon_phi","Muon_mass",
                 "Muon_miniPFRelIso_all","Muon_pfRelIso04_all",
                 "Muon_FlagId"]  # 0,1,2 = loose, med, tight
    el_keys = ["Electron_pt","Electron_eta","Electron_phi","Electron_mass",
               "Electron_miniPFRelIso_all", 
               "Electron_cutBasedNoIso", "Electron_cutBased"] # 0,1,2,3,4 = fail, veto, loose, med, tight
    #
    mu_data = AnaDict({k:tree.array(k, executor=executor) for k in mu_keys})
    el_data = AnaDict({k:tree.array(k, executor=executor) for k in el_keys})
    mc_weight = tree.array('weight',   executor=executor)
    g_weight  = tree.array('genWeight',executor=executor) if b'genWeight' in tree.keys() else 1
    weight = mc_weight*np.sign(g_weight)
    #
    mu_data = mu_data[(mu_data['Muon_pt']     >= 30) & (abs(mu_data['Muon_eta'])     <= 2.4)]
    el_data = el_data[(el_data['Electron_pt'] >= 30) & (abs(el_data['Electron_eta']) <= 2.4)]
    #
    return mu_data, el_data, weight

def calc_n_wLepSel(mu, el, w, opt=None):
    #
    event_mask = getData.DF_Container.event_mask 
    mu_id_map = {0:'loose',1:'med',2:'tight'}
    el_id_map = {0:'fail', 1:'veto',2:'loose',3:'med',4:'tight'}
    lep_sel_yield = AnaDict()
    for i in [0.2,0.4]:
        for j in [0.1,0.15]:
            for k in [1,2]:
                for l in [3,4]:
                    lep_config = f'Muon miniIso: {i}, Muon Id: {mu_id_map[k]:5}, Ele miniIso: {j:5}, Ele Id(noIso): {el_id_map[l]:5}'
                    mask, lep_pt, lep_eta = test_lep_sel((mu["Muon_miniPFRelIso_all"] < i),
                                                         (mu['Muon_FlagId'] >= k ),
                                                         (el['Electron_miniPFRelIso_all'] < j), 
                                                         (el['Electron_cutBasedNoIso'] >= l),
                                                         mu,el,opt=opt)
                    lep_sel_yield[lep_config] = {'sum_w'  : w[mask & event_mask].sum(),
                                                 'weight' : w[mask & event_mask],
                                                 'Lep_pt' : lep_pt[mask & event_mask].flatten(),
                                                 'Lep_eta': lep_eta[mask & event_mask].flatten()}
                            
    for i in [0.15, 0.25]:
        for k in [1,2]:
            for l in [3,4]:
                lep_config = f'Muon Iso: {i}, Muon Id: {mu_id_map[k]:5}, Ele Id(Iso): {el_id_map[l]:5}'
                mask, lep_pt, lep_eta  = test_lep_sel((mu["Muon_pfRelIso04_all"] < i),
                                                      (mu['Muon_FlagId'] >= k ),
                                                      (el['Electron_miniPFRelIso_all'] < 99999), 
                                                      (el['Electron_cutBased'] >= l),
                                                      mu,el,opt=opt)
                lep_sel_yield[lep_config] = {'sum_w'  : w[mask & event_mask].sum(),
                                             'weight' : w[mask & event_mask],
                                             'Lep_pt' : lep_pt[mask & event_mask].flatten(),
                                             'Lep_eta': lep_eta[mask & event_mask].flatten()}

    return lep_sel_yield


def test_lep_sel(mu_iso_cut, mu_id_cut, el_iso_cut, el_id_cut, mu_data, el_data, opt=None):
    mu_mask = ((mu_iso_cut)  & (mu_id_cut))
    mu_data = mu_data[mu_mask]
    el_mask = ((el_iso_cut)  & (el_id_cut))
    el_data = el_data[el_mask]
    #
    base_mask = (mu_mask[mu_mask].counts + el_mask[el_mask].counts == 1)
    #lep_pt = mu_data['Muon_pt'][base_mask] 
    lep_pt   = awkward.JaggedArray.concatenate([mu_data['Muon_pt'], el_data['Electron_pt']],axis=1)
    lep_eta  = awkward.JaggedArray.concatenate([mu_data['Muon_eta'], el_data['Electron_eta']],axis=1)

    #
    opt = '' if opt is None else opt
    mask_dict = {''  : base_mask,
                 'el': (base_mask  & (el_mask[el_mask].counts == 1)),
                 'mu': (base_mask & (mu_mask[mu_mask].counts == 1))
    }
    oneLep_mask = mask_dict[opt]
    return oneLep_mask, lep_pt, lep_eta

#
def plot_pickle():
    
    f_name = f'mcdata_lepsel_{year}.pkl'
    a_dict = AnaDict.read_pickle(f_name)
    #print(a_dict)
    miniIso_keys = [k for k in a_dict['el'] if 'mini'  in k]
    iso_keys     = [k for k in a_dict['el'] if '(Iso)' in k]
    #
    iso_dict  = processKeys(iso_keys)
    miso_dict = processKeys(miniIso_keys)
    # make plots for miniIso
    import matplotlib.pyplot as plt

    def plot_from_dict_miso(dict_, title):
        fig, ax = plt.subplots(2,2, figsize=(8,6))
        fig.subplots_adjust(
            top=0.88,
            bottom=0.11,
            left=0.11,
            right=0.88,
            hspace=0.4,
            wspace=0.2
        )
        for i,m_id in enumerate(miso_dict['Muon Id']):
            for j,el_id in enumerate(miso_dict['Ele Id(noIso)']):
                val = []
                for m_iso in miso_dict['Muon miniIso']:
                    val.append([dict_[f'Muon miniIso: {float(m_iso)}, Muon Id: {m_id:5}, Ele miniIso: {float(el_iso):5}, Ele Id(noIso): {el_id:5}'] for el_iso  in miso_dict['Ele miniIso']])
                #
                ax[i,j].imshow(val, cmap="YlGn")
                #ax[i,j].table(val)
                ax[i,j].set_yticks(np.arange(len(miso_dict['Muon miniIso'])))
                ax[i,j].set_yticklabels(miso_dict['Muon miniIso'])
                ax[i,j].set_ylabel('Muon miniIso')
                #
                ax[i,j].set_xticks(np.arange(len(miso_dict['Ele miniIso'])))
                ax[i,j].set_xticklabels(miso_dict['Ele miniIso'])
                ax[i,j].set_xlabel('Ele miniIso')
                ax[i,j].set_title(f'Muon Id: {m_id}, Ele Id(noIso): {el_id}')
                #
                for l in range(len(miso_dict['Muon miniIso'])):
                    for m in range(len(miso_dict['Ele miniIso'])):
                        ax[i,j].text(m,l, f'{np.array(val)[l,m]:6.2f}', ha="center", va="center", color="k")
                
        fig.suptitle(title)
        #plt.show()
    #
    def plot_from_dict_iso(dict_, title):
        fig, ax = plt.subplots(1,2)
        fig.subplots_adjust(
            top=0.88,
            bottom=0.11,
            left=0.11,
            right=0.88,
            hspace=0.2,
            wspace=0.4
        )
        for i,el_id in enumerate(iso_dict['Ele Id(Iso)']):
            val = []
            for m_id in iso_dict['Muon Id']:
                val.append([dict_[f'Muon Iso: {float(m_iso)}, Muon Id: {m_id:5}, Ele Id(Iso): {el_id:5}'] for m_iso  in iso_dict['Muon Iso']])
            #
            ax[i].imshow(val, cmap="YlGn")
            ax[i].set_yticks(np.arange(len(iso_dict['Muon Id'])))
            ax[i].set_yticklabels(iso_dict['Muon Id'])
            ax[i].set_ylabel('Muon Id')
            #
            ax[i].set_xticks(np.arange(len(iso_dict['Muon Iso'])))
            ax[i].set_xticklabels(iso_dict['Muon Iso'])
            ax[i].set_xlabel('Muon Iso')
            ax[i].set_title(f'Ele Id(Iso): {el_id}')
            #
            for l in range(len(iso_dict['Muon Id'])):
                for m in range(len(iso_dict['Muon Iso'])):
                    ax[i].text(m,l, f'{np.array(val)[l,m]:6.2f}', ha="center", va="center", color="k")
                
        fig.suptitle(title)
        #plt.show()
                
    #
    mifunc = plot_from_dict_miso
    ifunc  = plot_from_dict_iso

    s_over_sqrt_b = {k : a_dict['ttzh'][k]/np.sqrt(a_dict['tt'][k]) for k in a_dict['tt']}
    n_data = {k : a_dict['el'][k]+a_dict['mu'][k] for k in a_dict['el']}

    to_do = [[a_dict['tt'], 'ttbar Yield'],
             [a_dict['ttzh'], 'ttZ/h Yield'], 
             [s_over_sqrt_b, 'Sig/sqrt(BkG)'],
             [a_dict['el'], 'Ele Data Yield'],
             [a_dict['mu'], 'Muon Data Yield'],
             [n_data, 'Total Data Yield']]
    for a,b in to_do:
        mifunc(a,b)
        ifunc(a,b)
    #
    import matplotlib.backends.backend_pdf as matpdf
    pdf = matpdf.PdfPages(f'pdf/lep_sel_criteria.pdf')
    for fig_ in range(1, plt.gcf().number+1):
        pdf.savefig( fig_ )
    pdf.close()
    plt.close('all')
    
    
def processKeys(keys):
    dict_ = defaultdict(list)
    for key in keys:
        i_k = key.split(',')
        for i in i_k:
            k,v = i.split(':')
            dict_[k.strip()].append(v.strip())
    dict_ = {k:list(set(v)) for k,v in dict_.items()}
    return dict_
            

def plot_sig_over_bkg():
    f_name = f'mcdata_lepsel_{year}.pkl'
    a_dict = AnaDict.read_pickle(f_name)
    #print(a_dict)
    miniIso_keys = [k for k in a_dict['el'] if 'mini'  in k]
    iso_keys     = [k for k in a_dict['el'] if '(Iso)' in k]
    # tt is bkg, ttzh is sig
    import matplotlib.pyplot as plt
    pt_bins = [30,40,50,60,120,200,300,500]
    fig, ax = plt.subplots(1,2)
    fig.subplots_adjust(
        top=0.88,
        bottom=0.11,
        left=0.11,
        right=0.88,
        hspace=0.0,
        wspace=0.4
    )
    for i,k in enumerate(miniIso_keys+iso_keys):
        if (('0.1,' not in k or '0.2,' not in k) and '(noIso)' in k) or (('(Iso): tight' not in k or '0.15' not in k) and '(Iso)' in k) : continue
        n_sig, edges = np.histogram(np.clip(a_dict['ttzh'][k]['Lep_pt'],pt_bins[0], pt_bins[-1]), bins=pt_bins, range=(pt_bins[0], pt_bins[-1]), weights=a_dict['ttzh'][k]['weight'])
        n_bkg, _     = np.histogram(np.clip(a_dict['tt'][k]['Lep_pt']  ,pt_bins[0], pt_bins[-1]), bins=pt_bins,   range=(pt_bins[0], pt_bins[-1]), weights=a_dict['tt'][k]['weight'])
        bin_c = (edges[1:]+edges[:-1])/2
        bin_w = (edges[1:]-edges[:-1])
        y    = n_sig/np.sqrt(n_bkg)
        #yerr = abs(y) * np.sqrt( np.power( np.sqrt() ,2) ) 
        ax[0].errorbar(x=bin_c, xerr=bin_w/2,
                    y=y, #yerr=yerr
                    fmt='.', label=k)
    #
    ax[0].set_xlabel('Lep pt (GeV)')
    ax[0].set_xscale('log')
    ax[0].set_ylabel('Sig/sqrt(Bkg)')
    ax[0].grid(True)
    ax[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax[0].set_title(f'Lep Selection Significance, {year}')
    ax[1].axis('off')
    plt.show()
    #import matplotlib.backends.backend_pdf as matpdf
    #pdf = matpdf.PdfPages(f'pdf/lep_sel_criteria.pdf')
    #for fig_ in range(1, plt.gcf().number+1):
    #    pdf.savefig( fig_ )
    #pdf.close()
    #plt.close('all')
        

if __name__ == '__main__':
    #
    pickle_mcdata()
    #
    #plot_pickle()
    #
    plot_sig_over_bkg()
    