#!/users/shared/anaconda/envs/py35/bin/python3

import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd


## 
HOME = os.getenv("HOME")
birddata = pd.read_csv( os.path.join(HOME,"data","bird_tracking.csv") )
print( birddata.describe() )
bird_names = pd.unique(birddata.bird_name)


# To move forward, we need to specify a 
# specific projection that we're interested 
# in using.
proj = ccrs.Mercator() 
#proj = ccrs.PlateCarree()
#proj = ccrs.LambertCylindrical()
#proj = ccrs.Mercator()


## 
plt.figure(figsize=(6.5,6.5))
ax = plt.axes(projection=proj)

ax.stock_img()    ## no effect

#ax.set_extent((-25.0, 20.0, 52.0, 10.0))
ax.set_extent((-20.0, 10.0, 52.0, 10.0))

ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

for name in bird_names:
    ix = ( birddata['bird_name'] == name )
    x, y = birddata.longitude[ix], birddata.latitude[ix]

    ## Geodetic seems essential here
    #ax.plot(x,y,'.', transform=ccrs.Geodetic(), label=name, ms=0.8)
    ax.plot( x, y, '.', ms=0.8, label=name,
             transform=ccrs.Geodetic() )
             #transform=ccrs.RotatedGeodetic() )
             
plt.legend(loc="upper left")
plt.show()

