import glob
import matplotlib.pyplot as plt
import numpy as np
import uproot3 as uproot
from matplotlib import gridspec
from gammapy.stats import CashCountsStatistic


plt.rcParams.update({'font.size': 20})

def plot(path1, path2, source_name):
    f=uproot.open(path1)
    f1=uproot.open(path2)
    e_0 = f['sedULs'].xvalues
    s_0 = f['sedULs'].yvalues
    e_1 = f1['sedULs'].xvalues
    s_1 = f1['sedULs'].yvalues
    print(e_0, s_0)
    print(e_1, s_1)
    plt.figure(figsize=(12,7))
    plt.loglog(e_1, s_1, 'rv', markersize=10, label="Analysis.")
    plt.loglog(e_0, s_0, 'bv', markersize=10, label="X-check.")
    plt.xlim([45, 800])
    plt.xlabel("Energy [GeV]")
    plt.ylabel("E$^2$ d$\Theta$/dE [TeV cm$^{-2}$ s$^{-1}$]")
    plt.legend()
    plt.grid(True, which='both')
    plt.title(source_name)
    #plt.show()
    
def plot_ratio(path1, path2, source_name):
    f=uproot.open(path1)
    f1=uproot.open(path2)
    e_0 = f['sedULs'].xvalues
    s_0 = f['sedULs'].yvalues
    e_1 = f1['sedULs'].xvalues
    s_1 = f1['sedULs'].yvalues
    fig, ax = plt.subplots(figsize=(8,7))
    ratio = s_1[:10]/s_0[:10]
    ax.plot(e_0[:10], ratio, 'bv', markersize=10, label="ratio = Analys 2 / Analys 1")
    ax.set_xlim([45, 800])
    ax.set_xlabel("Energy [GeV]")
    ax.set_ylabel("ratio")
    plt.legend(fontsize=12)
    #plt.grid(True, which='both')
    plt.title(source_name)
    #plt.show()
    
def read_foam_log_output(foam_log_file):
    with open(foam_log_file) as f:
        lines = f.readlines()
        for l in lines:
            if 'Eest range' in l:
                s=l.split(',')
                E_0 = float(l.split(" ")[3])
                if E_0 > 50 and E_0 < 600:
                    print(s[0], s[1], end=" ")
                    n_on = int(l.split(',')[0].split(" ")[-1])
                    n_off = float(l.split(',')[1].split(" ")[4])
                    s=CashCountsStatistic(n_on=n_on, mu_bkg=n_off)
                    print(", TS = {:.2f}".format(s.ts))
            if 'dF/dE(' in l and E_0 > 50 and E_0 < 600:
                print(l.split(" ")[11], l.split(" ")[12])
                print()
                
def get_teff(output_flute_file_list):
    sum_teff = 0
    i = 0
    #fig, ax = plt.subplots(figsize=(14, 4))
    x = []
    y = []
    for path in output_flute_file_list:
        with uproot.open(path) as f:
            date = f['teffLC'].xvalues
            teff_array = f['teffLC'].yvalues
            sum_teff_i = sum(teff_array)
            sum_teff += sum_teff_i
            print(path.split("/")[-1])
            print(sum_teff_i)
            x.extend(np.int64(date))
            y.extend(teff_array)

    #ax.plot(np.arange(len(x)), y, 'bo-')
    #ax.set_xticks(np.arange(len(x)))
    #ax.set_xticklabels(x, rotation=60)
    #plt.show()
    print("Sum teff = {}".format(sum_teff))
    print("Sum teff = {} h".format(sum_teff/3600))
    
def get_sum_teff(output_flute_file_list):
    sum_teff = 0
    for path in output_flute_file_list:
        with uproot.open(path) as f:
            date = f['teffLC'].xvalues
            teff_array = f['teffLC'].yvalues
            sum_teff_i = sum(teff_array)
            sum_teff += sum_teff_i
        
    print("Sum teff = {} h".format(sum_teff/3600))
    return sum_teff

def get_time_flux_LC(output_file):
    x = []
    y = []
    with uproot.open(output_file) as f:
        x.extend(list(f['UpperLimLC'].xvalues))
        y.extend(list(f['UpperLimLC'].yvalues))
    return x, y

def plot_ligh_curve(list_output_flute_files_1, list_output_flute_files_2):
    x1 = []
    y1 = []
    for path in list_output_flute_files_1:
        with uproot.open(path) as f:
            x1.extend(list(f['UpperLimLC'].xvalues))
            y1.extend(list(f['UpperLimLC'].yvalues))
    
    x2 = []
    y2 = []
    for path in list_output_flute_files_2:
        with uproot.open(path) as f:
            x2.extend(list(f['UpperLimLC'].xvalues))
            y2.extend(list(f['UpperLimLC'].yvalues))
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.plot(x1, y1, 'bv', markersize=10, label="Analysis")
    plt.plot(x2, y2, 'gv', markersize=10, label="X-check")
    ax.set_xlabel("Time [MJD]")
    ax.set_ylabel("Flux U.L. [cm$^{-2}$ s$^{-1}$] \n for $E > 100 GeV$")
    ax.set_yscale('log')
    plt.legend(fontsize=15)

def plot_sed_ratio(path1, path2):
    
    with uproot.open(path1) as f_1:
        e_1 = f_1['sedULs'].xvalues
        s_1 = f_1['sedULs'].yvalues
        h_1 = f_1['TotalEffTimevsAzZd'].numpy()
    sum_teff_1 = np.sum(h_1[0][:])/3600
    print(path1, end="\t")
    print("Time = {}".format(sum_teff_1))
    
    with uproot.open(path2) as f_2:
        e_2 = f_2['sedULs'].xvalues
        s_2 = f_2['sedULs'].yvalues
        h_2 = f_2['TotalEffTimevsAzZd'].numpy()
    sum_teff_2 = np.sum(h_2[0][:])/3600
    print(path2, end="\t")
    print("Time = {}".format(sum_teff_2))
    
    fig = plt.figure(figsize=(12, 9)) 
    gs = gridspec.GridSpec(2, 1, height_ratios=[2.5, 1]) 
    ax0 = plt.subplot(gs[0])
    ax0.loglog(e_1, s_1, 'bv', markersize=10, label="X-check.")
    ax0.plot(e_2, s_2, 'rv', markersize=10, label="Analysis.")
    
    ax0.set_xlim([45, 800])
    ax0.set_ylim([1e-14, 1e-9])
    ax0.set_xlabel("Energy [GeV]")
    ax0.set_ylabel("E$^2$ d$\Theta$/dE [TeV cm$^{-2}$ s$^{-1}$]")
    plt.legend()
    
    ax1 = plt.subplot(gs[1])
    ratio = s_2[:10]/s_1[:10]
    ax1.plot(e_1[:10], ratio, 'C4o')
    ax1.set_xscale('log')
    ax1.set_xlim([45, 800])
    ax1.set_ylim([0, 5])
    ax1.plot([0, 800], [2, 2], 'g-')
    ax1.plot([0, 800], [0.5, 0.5], 'g-')
    ax1.plot([0, 800], [1, 1], 'k--')
    ax1.set_ylabel("Ratio \n Analysis/X-check")
    ax1.set_xlabel("Energy [GeV]")
    plt.legend()
    plt.tight_layout()