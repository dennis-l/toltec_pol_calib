import os
import sys
import numpy as np
import pandas as pd
import astropy.units as u
import astropy.constants as const


import matplotlib
import matplotlib.pyplot as plt

from cube.visualization import standard, brie
plt.style.use(brie)

amapola_data_file = 'data/amapola.txt'


amapola_data = pd.read_csv(amapola_data_file, delimiter='\t')
amapola_data['Date'] = pd.to_datetime(amapola_data['Date'])
amapola_data['polpercentage'] = 100 * np.sqrt(amapola_data['Q']**2 + amapola_data['U']**2) / amapola_data['I']
amapola_data['p'] =  amapola_data['P'] / amapola_data['I']
amapola_data['polangle'] = np.arctan2(amapola_data['U'], amapola_data['Q'])
amapola_data['rotatedpolangle'] = np.arctan2(amapola_data['U'], amapola_data['Q']) + (np.pi / 2)

band_7 = amapola_data.loc[amapola_data['Freq'] == 233].copy()
print((const.c  / (233 * u.GHz)).to(u.mm))

# search
targets = []
for src in band_7['Src']:
    if src[0:3] in ['J17', 'J18', 'J19', 'J20', 'J21']:
    #if src[0:3] in ['J18', 'J19', 'J20']:
        targets.append(src)

band_7_targets = band_7[band_7['Src'].isin(targets)].copy()

pol_5 = band_7_targets.loc[band_7_targets['polpercentage'] >= 5].copy()
obj_list = list(set(pol_5["Src"].tolist()))

print(len(obj_list))

actual_used = []
for source in obj_list:
    name_3c = source
    this_source_only = pol_5.loc[pol_5['Src'] == source].copy()
    if this_source_only.shape[0] < 10:
        continue
    else:
        actual_used.append(source)

    name_3c = source.strip()
    plot_obj, sp_obj = plt.subplots(5, 1, figsize=(8, 10), sharex=True, dpi=200) # gridspec_kw={'hspace': 0, 'wspace': 0}
    sp_obj = sp_obj.ravel()

    sp_obj[0].set_title(f"{source} ({name_3c})")

    # Total Intensity (Stokes I )
    sp_obj[0].plot(this_source_only['Date'], this_source_only['I'], '.', color='firebrick')
    sp_obj[0].errorbar(this_source_only['Date'], this_source_only['I'], this_source_only['eI'], ls='none', color='firebrick')
    sp_obj[0].axhline(np.mean(this_source_only['I']),  ls='--', label=f"mean ={np.mean(this_source_only['I']):0.3f}, std={np.std(this_source_only['I']):0.3f}", color='firebrick')
    sp_obj[0].axhspan(np.mean(this_source_only['I']) - np.std(this_source_only['I']), np.mean(this_source_only['I']) + np.std(this_source_only['I']), alpha=0.12, color='red', edgecolor=None)
    sp_obj[0].set_ylabel("Stokes I [Jy]")
    sp_obj[0].legend(fancybox=False, loc='lower left', handletextpad=0.7, frameon=False)

    # Stokes Q
    sp_obj[1].plot(this_source_only['Date'], this_source_only['Q'], '.', color='firebrick')
    sp_obj[1].errorbar(this_source_only['Date'], this_source_only['Q'], this_source_only['eQ'], ls='none', color='firebrick')
    sp_obj[1].set_ylabel("Stokes Q [Jy]")
    sp_obj[1].legend(fancybox=False, loc='lower left', handletextpad=0.7, frameon=False)

    # Stokes U
    sp_obj[2].plot(this_source_only['Date'], this_source_only['U'], '.', color='firebrick')
    sp_obj[2].errorbar(this_source_only['Date'], this_source_only['U'], this_source_only['eU'], ls='none', color='firebrick')
    sp_obj[2].set_ylabel("Stokes U [Jy]")
    sp_obj[2].legend(fancybox=False, loc='lower left', handletextpad=0.7, frameon=False)

    # Polarization Percentage
    sp_obj[3].plot(this_source_only['Date'], this_source_only['polpercentage'], '.')
    sp_obj[3].axhline(np.mean(this_source_only['polpercentage']),  ls='--', label=f"mean = {np.mean(this_source_only['polpercentage']):0.3f}, std={np.std(this_source_only['polpercentage']):0.3f}", color='darkorchid')
    sp_obj[3].axhspan(np.mean(this_source_only['polpercentage']) - np.std(this_source_only['polpercentage']), np.mean(this_source_only['polpercentage']) + np.std(this_source_only['polpercentage']), alpha=0.12, color='red', edgecolor=None)
    sp_obj[3].set_ylabel("Pol. Percentage [%]")
    sp_obj[3].legend(fancybox=False, loc='lower left', handletextpad=0.7, frameon=False)
    #sp_obj[1].set_ylim((0.0, 10))

    sp_obj[4].plot(this_source_only['Date'], np.arctan(np.tan(this_source_only['polangle'])) *  (360 /  (2 * np.pi)), '.')
    sp_obj[4].set_ylabel("Pol. Angle [Degree]")
    sp_obj[4].set_ylim((-90, 90))
    sp_obj[4].legend(fancybox=False, loc='lower left', handletextpad=0.7, frameon=False)

    plot_obj.tight_layout()
    plot_obj.savefig(f'plots/filtered_5/{name_3c}.pdf', format='pdf', dpi=690)
    plt.close('all')

for src in actual_used:
    print(f"http://www.alma.cl/~skameno/AMAPOLA/{src.strip()}.flux.html")

#QSO B2155-152 
#QSO B1730-130