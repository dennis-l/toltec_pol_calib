import astroplan.plots
from astroplan import Observer, FixedTarget
import numpy as np
from astropy.time import Time
import astropy.units as u
import astropy.constants as const
from astropy.coordinates import EarthLocation
import matplotlib
import matplotlib.pyplot as plt
try:
    from cube.visualization import standard, brie
    plt.style.use(brie)
except:
    pass

lmt_location = EarthLocation.from_geodetic(
    '-97d18m52.6s',
    '+18d59m10s',
    (4640 << u.m)
)

lmt_observer = Observer(location=lmt_location, 
    name="Large Millimeter Telescope", 
    timezone='America/Mexico_City'
)

start_datetime = '2022-11-15 00:00:00'
observe_time =  Time(start_datetime) + np.linspace(0, 24, 100)*u.hour

names_3c = ['3C286', '3C273', '3C279']
for source in names_3c:
    target = FixedTarget.from_name(source)

    plt.figure()
    astroplan.plots.plot_altitude(
        target, 
        observer=lmt_observer, 
        time=observe_time,
        brightness_shading=True,
    )
    plt.title(source)
    plt.axhline(y=20, linestyle='--', color='black')
    plt.tight_layout()
    plt.savefig(f'./plots/obsplanner/{source}.png', dpi=250)
    plt.close('all')
    
    #sun_rise = lmt_observer.sun_rise_time(observe_time[0], which='next')
    #sun_set = lmt_observer.sun_set_time(observe_time[0], which='next')