import os
import sys
import numpy as np
import pandas as pd
import astropy.units as u
import astropy.constants as const

import matplotlib
import matplotlib.pyplot as plt

try:
    from cube.visualization import standard, brie
    plt.style.use(brie)
except:
    pass

def pol_percentage_err(I, Q, U, eI, eQ, eU):
    
    term_1 = (1 / (Q**2 + U**2)) * ((Q * eQ)**2 + (U * eU)**2) 
    term_2 = (((Q / I)**2 + (U / I)**2) * (eI**2)) 
    
    return (100 / I) * np.sqrt(term_1 + term_2)


if __name__ == "__main__":
    amapola_data_file = './data/amapola.txt'
    amapola_data = pd.read_csv(amapola_data_file, delimiter='\t')
    amapola_data['Date'] = pd.to_datetime(amapola_data['Date'])

    # polpercentage
    amapola_data['polpercentage'] = 100 * np.sqrt(amapola_data['Q']**2 + amapola_data['U']**2) / amapola_data['I']
    amapola_data['epolpercentage'] = pol_percentage_err(amapola_data['I'], amapola_data['Q'], amapola_data['U'], amapola_data['eI'], amapola_data['eQ'], amapola_data['eU'])

    amapola_data['p'] =  amapola_data['P'] / amapola_data['I']
    amapola_data['polangle'] = np.arctan2(amapola_data['U'], amapola_data['Q'])
    amapola_data['rotatedpolangle'] = np.arctan2(amapola_data['U'], amapola_data['Q']) + (np.pi / 2)

    freq = 233
    band_7 = amapola_data.loc[amapola_data['Freq'] == freq].copy()

    targets =  ['J1331+3030', 'J1229+0203', 'J1256-0547']
    names_3c = ['3C286', '3C273', '3C279']
    for source, name_3c in zip(targets, names_3c):
        this_source_only = band_7.loc[band_7['Src'] == source + ' '].copy()

        plot_obj, sp_obj = plt.subplots(5, 1, figsize=(8, 10), sharex=True, dpi=200) # gridspec_kw={'hspace': 0, 'wspace': 0}
        sp_obj = sp_obj.ravel()

        sp_obj[0].set_title(f"{source} ({name_3c}) @ {freq} GHz")

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
        #sp_obj[1].legend(fancybox=False, loc='lower left', handletextpad=0.7, frameon=False)

        # Stokes U
        sp_obj[2].plot(this_source_only['Date'], this_source_only['U'], '.', color='firebrick')
        sp_obj[2].errorbar(this_source_only['Date'], this_source_only['U'], this_source_only['eU'], ls='none', color='firebrick')
        sp_obj[2].set_ylabel("Stokes U [Jy]")
        #sp_obj[2].legend(fancybox=False, loc='lower left', handletextpad=0.7, frameon=False)

        # Polarization Percentage
        sp_obj[3].plot(this_source_only['Date'], this_source_only['polpercentage'], '.', color='firebrick')
        sp_obj[3].errorbar(this_source_only['Date'], this_source_only['polpercentage'], this_source_only['epolpercentage'], ls='none', color='firebrick')
        sp_obj[3].axhline(np.mean(this_source_only['polpercentage']),  ls='--', label=f"mean = {np.mean(this_source_only['polpercentage']):0.3f}, std={np.std(this_source_only['polpercentage']):0.3f}", color='darkorchid')
        sp_obj[3].axhspan(np.mean(this_source_only['polpercentage']) - np.std(this_source_only['polpercentage']), np.mean(this_source_only['polpercentage']) + np.std(this_source_only['polpercentage']), alpha=0.12, color='red', edgecolor=None)
        sp_obj[3].set_ylabel("Pol. Percentage [%]")
        sp_obj[3].legend(fancybox=False, loc='lower left', handletextpad=0.7, frameon=False)
        #sp_obj[1].set_ylim((0.0, 10))

        # Polarization Angle.
        evpa_arr = (np.array(this_source_only['EVPA']) * u.radian).to_value(u.degree)
        eevpa_arr = (np.array(this_source_only['eEVPA']) * u.radian).to_value(u.degree)
        sp_obj[4].plot(this_source_only['Date'], evpa_arr, '.', color='firebrick')
        sp_obj[4].errorbar(this_source_only['Date'], evpa_arr, eevpa_arr, ls='none', color='firebrick')
        #sp_obj[4].plot(this_source_only['Date'], np.arctan(np.tan(this_source_only['polangle'])) *  (360 /  (2 * np.pi)), '.')
        sp_obj[4].set_ylabel("EVPA [Degree]")
        sp_obj[4].set_ylim((-90, 90))
        #sp_obj[4].legend(fancybox=False, loc='lower left', handletextpad=0.7, frameon=False)

        plot_obj.tight_layout()
        plot_obj.savefig(f'./plots/amapola/{name_3c}.png', dpi=250)
        plt.close('all')