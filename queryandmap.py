# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 16:53:15 2018

@author: jeremy azzopardi
"""

import psycopg2
import shapely
import shapely.wkt
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import os


def connect():
    connection = psycopg2.connect(database="HeritageSites",user="postgres", password="admin", port=5433)
    return connection
    
#Import development site for querying
def import_dev_site(connection, fname):
    development_site = gpd.read_file(fname).set_index('id')['geometry']
    dev_site_wkt=shapely.wkt.dumps(development_site[1])
    SQL="SELECT geom, name_mt_1, name_en, type_1, location, id  FROM cultural_map_20_nov_2014_2 WHERE ST_DWithin(cultural_map_20_nov_2014_2.geom, ST_GeomFromText('{}'),4000)".format(dev_site_wkt)

    gdf1 = gpd.read_postgis(SQL, connection, geom_col='geom',crs={'init': u'epsg:3857'}, coerce_float=False)
    gdf2 = gpd.read_file(fname)
    connection.close()
    
    return gdf1,gdf2

# Add basemap
def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    # restore original x/y limits
    ax.axis((xmin, xmax, ymin, ymax))
        
        
    
  # Create output map
def produce_outmap(geodataframe, title, intervention_code, archaeologist):
    fig, ax = plt.subplots()
    # set aspect to equal. This is done automatically
    # when using *geopandas* plot on it's own, but not when
    # working with pyplot directly.
    
    sites_of_interest = geodataframe[0]
    dev_site = geodataframe[1]
    ax = sites_of_interest.plot(color='Red', figsize= (35, 60))
    add_basemap(ax, zoom=15, url=ctx.sources.OSM_A)
    ax.axis('off')
    dev_site.plot(ax=ax, color='blue', edgecolor='black')
    ax.set_title('{} \n {} \n {}'.format(title, intervention_code, archaeologist))
    
    
 
    plt.savefig(title)
    

    
def main():
    connection = connect()
    gdf1, gdf2 = import_dev_site(connection, r'C:\Users\xazzje\Desktop\docAserv\data\study area buffer site.geojson')
      
    # Input parameters
    t = 'test title'
    i = 'M200/19'
    a = 'Jeremy Azzopardi'
    
    produce_outmap([gdf1,gdf2],t, i, a)
    
    print(t.join('.png'))
        
if __name__ == '__main__':
    main()
    
    

    

 


    

'''
# Create a Map instance
m = folium.Map(location=[35.92, 14.41], tiles='Stamen Terrain',
                   zoom_start=15, control_scale=True)


outfp= "./data/base_map.html"
m.save(outfp)
'''

    
    
    