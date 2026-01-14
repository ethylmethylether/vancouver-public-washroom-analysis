# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 17:57:19 2026

@author: PC
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

#Loading Files
land = gpd.read_file("data/local-area-boundary.geojson")
parks = gpd.read_file("data/parks-polygon-representation.geojson")
pw = gpd.read_file("data/public-washrooms.geojson")
transit = gpd.read_file("data/rapid-transit-lines.geojson")
stations = gpd.read_file("data/rapid-transit-stations.geojson")



land = land.to_crs(epsg=3857)
parks = parks.to_crs(epsg=3857)
pw = pw.to_crs(epsg=3857)
transit = transit.to_crs(epsg=3857)
stations = stations.to_crs(epsg=3857)

color_map = {'Expo Line': 'navy',
             'Canada Line': 'deepskyblue',
             'Millennium Line' : 'gold'
             }
transit['color'] = transit['line'].map(color_map)


# Identifying parks with least number of washrooms according to their area

#pw = park_name_left
#parks = park_name_right


#This will create a new geofile which has pw included in parks with
# attributes of pw and parks

      
pw_in_parks = gpd.sjoin(pw, parks, how ='inner',predicate='within')



#this counts the number of washrooms per park and outputs
#Index(['park_name_right', 'pw_count'], dtype='object')
washroom_counts = pw_in_parks.groupby('park_name_right').size().reset_index(name='pw_count')

parks_with_pw = parks.merge(
    washroom_counts,
    left_on = 'park_name',
    right_on = 'park_name_right',
    how='left'
    )
parks_with_pw['pw_count'] = parks_with_pw['pw_count'].fillna(0).astype(int)

# calculating washroom density

parks_with_pw['pw_per_ha'] = parks_with_pw['pw_count']/parks_with_pw['area_ha']
parks_with_pw = parks_with_pw.drop(columns=['park_name_right', 'park_id'])


# Sorting Parks in ascending order
parks_least_pw = parks_with_pw.sort_values('pw_per_ha', ascending = True)


# Tp 5 parks by washroom counts

top5_parks = (
    parks_with_pw
    .sort_values('pw_count', ascending = False)
    .head(5)
    )


#---------------MAP---------------

ax = land.plot(color='none', edgecolor='black', figsize=(10,10))
transit.plot(ax=ax, color=transit['color'], linewidth=3, legend=False, zorder=1)
parks.plot(ax=ax, color='green', markersize=20, zorder=2, label='Parks')
pw.plot(ax=ax, color='grey', edgecolor='black', markersize=15, zorder=3, label='Public Washrooms')
stations.plot(ax=ax, color='white', edgecolor='black', markersize=25, zorder=4, label='Stations')


#---------Base Map-----------------
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=13)

#------------PLOT 1----------------
ax.set_title("Vancouver: Parks, Transit Lines & Stations", fontsize=16)
ax.set_axis_off()
plt.tight_layout()
ax.legend()
plt.savefig("vancouver_map.png", dpi=600, bbox_inches='tight')
plt.show()

#------------------BAR PLOT--------------------


# Tp 5 parks by washroom counts

top5_parks = (
    parks_with_pw
    .sort_values('pw_count', ascending = False)
    .head(5)
    )

plt.figure(figsize=(10,10))

plt.bar(
        top5_parks['park_name'],
        top5_parks['pw_count'],
        color='green'
        )
plt.title("Top 5 Parks with Most Public Washrooms")
plt.xlabel("Park Name")
plt.ylabel("Number of Public Washrooms")

for i, value in enumerate(top5_parks['pw_count']):
    plt.text(i, value + 0.1, int(value), ha='center')

plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.show()

#-----------------TABLE-----------

parks_table = parks_with_pw[
    ['park_name','area_ha', 'pw_count','pw_per_ha']
].copy()

# Sort first
parks_table = parks_table.sort_values('pw_count', ascending=False).round(2)

# Convert area from ha → m² (keep NaN for missing)
parks_table['area_m2'] = parks_table['area_ha'] * 10000

# Use pandas "nullable integer" type to allow NaN
parks_table['area_m2'] = parks_table['area_m2'].round(0).astype('Int64')

parks_table['pw_per_m2'] = parks_table['pw_count'] / parks_table['area_m2']
parks_table['pw_per_m2'] = parks_table['pw_per_m2'].round(6)


# Drop original ha column if you want
parks_table = parks_table.drop(columns=['area_ha','pw_per_ha'])

parks_table

# Save to CSV
parks_table.to_csv("parks_washroom_analysis_m2.csv", index=False)


