import sys
if __name__ == '__main__':
    import subprocess as sb
    sys.path.insert(1, sb.check_output('echo $(git rev-parse --show-cdup)', shell=True).decode().strip('\n')+'DeepSleep/')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FixedLocator, FormatStrFormatter
from matplotlib.patches import Patch, Rectangle
from matplotlib import rc, lines
rc("figure", max_open_warning=600)
rc("figure", figsize=(8, 6*(6./8.)), dpi=200)

import numpy as np
import re

import config.ana_cff as cfg
from lib.fun_library import save_pdf, import_mpl_settings, upperlefttext, CMSlabel


wc_latex = {
    #'cbW'  : r'$\frac{{c}_{\mathrm{bW}}}{{\Lambda}^{2}}$',
    #'cptb' : r'$\frac{{c}_{\varphi \mathrm{tb}}}{{\Lambda}^{2}}$',
    #'cpt'  : r'$\frac{{c}_{\varphi \mathrm{t}}}{{\Lambda}^{2}}$',
    #'ctp'  : r'$\frac{{c}_{\mathrm{t} \varphi}}{{\Lambda}^{2}}$',
    #'ctZ'  : r'$\frac{{c}_{\mathrm{tZ}}}{{\Lambda}^{2}}$',
    #'ctW'  : r'$\frac{{c}_{\mathrm{tW}}}{{\Lambda}^{2}}$',
    #'cpQ3' : r'$\frac{{c}_{\varphi \mathrm{Q}}^{3}}{{\Lambda}^{2}}$',
    #'cpQM' : r'$\frac{{c}_{\varphi \mathrm{Q}}^{-}}{{\Lambda}^{2}}$',
    'ctZ'  : r'$ \frac{\mathsf{c_{tZ}}}{\Lambda^\mathsf{2}}$',
    'cbW'  : r'$\frac{\mathsf{c_{bW}}}{\Lambda^\mathsf{2}}$',
    'ctW'  : r'$ \frac{\mathsf{c_{tW}}}{\Lambda^\mathsf{2}}$',
    'cptb' : r'$ \frac{\mathsf{c_{\varphi t b}}}{\Lambda^\mathsf{2}}$',
    'cpt'  : r'$\frac{\mathsf{c_{\varphi t}}}{\Lambda^\mathsf{2}}$',
    'cpQ3' : r'$ \frac{\mathsf{c^3_{\varphi Q}}}{\Lambda^\mathsf{2}}$',
    'cpQM' : r'$\frac{\mathsf{c^{-}_{\varphi Q}}}{\Lambda^\mathsf{2}}$',
    'ctp'  : r'$\frac{\mathsf{c_{t \varphi}}}{\Lambda^\mathsf{2}}$',
}
wc_bf_ffl = { # best-fit value, but values are obselete now and not used in this script!!!
    'fixed':{'cbW' : -2.34,'cptb': 0.56,'cpt' : -0.26,'ctp' : 15.30,'ctZ' : 0.01,'ctW' : -0.05,'cpQ3': -0.54,'cpQM': -0.04,},
    'float':{'cbW' : 2.46,'cptb': 1.08,'cpt' : -0.34,'ctp' : 15.13,'ctZ' : -0.06,'ctW' : -0.07,'cpQ3': -0.27,'cpQM': 0.02,},
}
wc_top22_006_ffl = { # 68% CL lower, upper with respect to best-fit
    #'fixed':{'cbW' : [-3.41,3.33],'cptb': [-4.97,6.02],'cpt' : [-7.11,2.43],  'ctp' : [6.74,23.62],'ctZ' : [-0.57,0.63],'ctW' : [-0.59,0.50],'cpQ3': [-2.40,1.37],'cpQM': [-3.06,4.93],}, # old toppt
    'fixed':{'cbW' : [-1.30,1.30],'cptb': [-5.16,5.16],'cpt' : [-3.41,3.41],  'ctp' : [-4.45,5.39],'ctZ' : [-1.14,1.09],'ctW' : [-0.68,0.62],'cpQ3': [-2.05,2.01],'cpQM': [-2.63,2.22],}, #
    #'float':{'cbW' : [-3.49,3.54],'cptb': [-4.86,6.94],'cpt' : [-7.54,3.50],  'ctp' : [6.95,23.13],'ctZ' : [-1.02,1.01],'ctW' : [-0.96,0.90],'cpQ3': [-2.43,2.02],'cpQM': [-4.17,5.55],}, # old toppt
    'float':{'cbW' : [-1.43,1.43],'cptb': [-5.50,5.50],'cpt' : [-10.19,10.5],  'ctp' : [-6.41,8.83],'ctZ' : [-1.14,1.09],'ctW' : [-0.90,0.84],'cpQ3': [-2.20,2.19],'cpQM': [-5.95,11.69],}, #
}
wc_nfive_ffl = { # 95% CL lower, upper with respect to best-fit
    'fixed':{'cbW' : [-4.53,4.49],'cptb': [-14.65,14.66],'cpt' : [-16.20,9.67], 'ctp' : [-9.28,39.17],'ctZ' : [-1.40,1.45],'ctW' : [-1.40,1.33],'cpQ3': [-5.72,4.92],'cpQM': [-9.32,12.20],},# old toppt
    #'fixed':{'cbW' : [-4.22,4.18],'cptb': [-9.89,10.75],'cpt' : [-12.03,6.33], 'ctp' : [0.20,30.10],'ctZ' : [-1.05,1.11],'ctW' : [-1.05,0.96],'cpQ3': [-4.13,3.04],'cpQM': [-6.56,8.73],},
    'float':{'cbW' : [-4.61,4.60],'cptb': [-16.40,16.35],'cpt' : [-18.58,13.21],'ctp' : [-9.46,39.53],'ctZ' : [-2.08,2.06],'ctW' : [-2.14,2.09],'cpQ3': [-6.69,6.23],'cpQM': [-12.49,15.07],},
    #'float':{'cbW' : [-4.31,4.32],'cptb': [-10.21,11.66],'cpt' : [-12.71,7.92],'ctp' : [0.56,29.50],'ctZ' : [-1.68,1.67],'ctW' : [-1.63,1.57],'cpQ3': [-4.43,3.92],'cpQM': [-8.28,9.92],},# old toppt
}
## old
#wc_bf_ffl = { # best-fit value
#    'fixed':{'cbW' : -2.34,'cptb': 0.56,'cpt' : -0.26,'ctp' : 15.30,'ctZ' : 0.01,'ctW' : -0.05,'cpQ3': -0.54,'cpQM': -0.04,},
#    'float':{'cbW' : 2.46,'cptb': 1.08,'cpt' : -0.34,'ctp' : 15.13,'ctZ' : -0.06,'ctW' : -0.07,'cpQ3': -0.27,'cpQM': 0.02,},
#}
#wc_nfive_ffl = { # 95% CL lower, upper with respect to best-fit
#    'fixed':{'cbW' : [-2.21,6.86],'cptb': [-10.00,9.59],'cpt' : [-8.24,5.65], 'ctp' : [-15.17,14.88],'ctZ' : [-1.00,1.01],'ctW' : [-0.98,0.99],'cpQ3': [-3.32,3.42],'cpQM': [-4.73,5.67],},
#    'float':{'cbW' : [-7.06,2.16],'cptb': [-10.53,9.58],'cpt' : [-10.73,7.91],'ctp' : [-14.63,14.50],'ctZ' : [-1.47,1.54],'ctW' : [-1.49,1.53],'cpQ3': [-3.77,3.83],'cpQM': [-6.71,7.95],},
#}
#wc_top22_006_ffl = { # 68% CL lower, upper with respect to best-fit
#    'fixed':{'cbW' : [-1.21,5.86],'cptb': [-5.46,5.28],'cpt' : [-3.54,2.99],'ctp' : [-8.65,8.50],'ctZ' : [-0.58,0.58],'ctW' : [-0.53,0.54],'cpQ3': [-1.77,1.80],'cpQM': [-2.47,2.70],},
#    'float':{'cbW' : [-6.05,1.19],'cptb': [-5.63,5.25],'cpt' : [-5.22,4.39],'ctp' : [-8.15,8.08],'ctZ' : [-0.88,0.92],'ctW' : [-0.85,0.87],'cpQ3': [-2.00,2.03],'cpQM': [-3.66,4.02],},
#}

@save_pdf('eft_22_006_comparison.pdf')
#@save_pdf('eft_results_table.pdf')
def main():
    fig, ax = beginPlt()
    for i,k in enumerate(wc_bf_ffl):
        plot_eft_result(ax,k,i)
    #
    endPlt(fig,ax)
    #plt.show()


def plot_eft_result(ax, f_fl, i_off):
    #wc_top22_006 = np.array([np.array(wc_top22_006_ffl[f_fl][wc]) + wc_bf_ffl[f_fl][wc] for wc in wc_latex])
    #wc_nfive  = np.array([np.array(wc_nfive_ffl[f_fl][wc])  + wc_bf_ffl[f_fl][wc] for wc in wc_latex])
    wc_top22_006 = np.array([np.array(wc_top22_006_ffl[f_fl][wc])  for wc in wc_latex])
    wc_nfive  = np.array([np.array(wc_nfive_ffl[f_fl][wc])   for wc in wc_latex])
    y = np.arange(len(wc_latex))-(i_off*.3*np.ones(len(wc_latex)))+(.15/2)
    y2 = np.arange(len(wc_latex))-(i_off*.3*np.ones(len(wc_latex)))+.15+(.15/2)

    # plot 95% CL lines
    if f_fl == 'fixed':
        ax.hlines(
            y=y, xmin=wc_nfive[:,0], xmax=wc_nfive[:,1],
            color='k', linestyle=(0, (1, 1)), linewidth=1)
    if f_fl == 'float':
        ax.hlines(
            y=y, xmin=wc_nfive[:,0], xmax=wc_nfive[:,1],
            color='k', linestyle='-', linewidth=1)
      # plot 68% CL lines
    ax.hlines(
        y=y2, xmin=wc_top22_006[:,0], xmax=wc_top22_006[:,1],
        color='r', linestyle='-' if f_fl == 'float' else (0, (1, 1)), linewidth=1)
    ax.hlines(
        y=7.0-(.15/2), xmin=24.05, xmax =30.69,
        color = 'r', linestyle='-', linewidth = 1)

def beginPlt(year=None):
    fig, ax = plt.subplots()
    fig.subplots_adjust(top=0.88,bottom=0.11,left=0.18,right=0.95,wspace=0.0)
    CMSlabel(fig,ax,lumi= round(cfg.Lumi[year],1) if year is not None else round(cfg.Lumi['Total']), opt='Simulation Preliminary', fontsize=14)
    #CMSlabel(fig,ax,lumi= round(cfg.Lumi[year],1) if year is not None else round(cfg.Lumi['Total']))
    return fig, ax

def endPlt(fig,ax):
    ax.tick_params(which='both', direction='in', top=True)
    # yaxis
    ax.set_yticks(np.arange(len(wc_latex)))
    ax.set_yticklabels([wc_latex[wc] for wc in wc_latex], fontsize=16, usetex=True)
    # xaxis
    #ax.set_xlabel(r'Wilson coefficient limit [$\text{TeV}^{-2}$]', usetex=True)
    #ax.set_xlabel(r'Wilson coefficient limit $\left[\smash{\text{TeV}}^\mathsf{-2}\right]$', usetex=True)
    ax.set_xlabel(r'95\% CL interval \raisebox{0.25ex}{[}$\text{TeV}^\mathsf{-2}$\raisebox{0.25ex}{]}', usetex=True)
    ax.set_xticks([-15,-10, -5, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
    ax.set_xticklabels(['-20','','-10', '', '0', '', '10', '', '20', '', '30','','40'])
    ax.set_xlim(-20,45)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.grid(axis='x', linestyle=':')
    # legend
    handles = [
        lines.Line2D([],[], linestyle=(0, (1, 1)), linewidth=1, color='k'),
        lines.Line2D([],[], linestyle='-', linewidth=1, color='k'),
        lines.Line2D([],[], linestyle=(0, (1, 1)), linewidth=1, color='r'),
        lines.Line2D([],[], linestyle='-', linewidth=1, color='r'),
    ]
    #labels  = [
    #    'Others profiled (95% CL)',
    #    'Others fixed to SM (95% CL)',
    #    'Others profiled (68% CL)',
    #    'Others fixed to SM (68% CL)'
    #]
    labels  = [
        'Others fixed to SM',
        'Others profiled',
    ]
    #leg_68 = ax.legend(handles[2:], labels, loc='upper right', bbox_to_anchor=(1.03, 0.89), fontsize=10, framealpha=1, title='68\% CL interval')
    #ax.legend(handles[:2], labels, loc='upper right', bbox_to_anchor=(1.03, 0.67), fontsize=10, framealpha=1, title='95\% CL interval')
    leg_68 = ax.legend(handles[2:], labels, loc='upper right', bbox_to_anchor=(1.03, 0.40), fontsize=10, framealpha=1, title='TOP-22-006 (Exp.)')
    ax.legend(handles[:2], labels, loc='upper right', bbox_to_anchor=(1.03, 0.22), fontsize=10, framealpha=1, title='TOP-21-003 (Exp.)')
    ax.add_artist(leg_68)
    #plt.show()


if __name__ == '__main__':
    import_mpl_settings(1, length=2, disable_sansmath=True)
    main()
