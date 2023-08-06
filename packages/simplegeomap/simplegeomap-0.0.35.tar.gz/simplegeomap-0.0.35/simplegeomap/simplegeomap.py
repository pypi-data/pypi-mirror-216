from simplegeomap.util import gltiles, find_tile, get_quad, conv2d, initialize_kernel, padding
from pygeodesy.sphericalNvector import LatLon
import pandas as pd, zipfile, sys, os, csv, io
import matplotlib.pyplot as plt
import numpy as np, json, shapefile

GWIDTH = 200

def plot_water_df(df,clat,clon,zoom,ax):
    MAX = 60
    CENTER_DIST = (40000. / MAX)*(zoom+1)
    p1 = LatLon(clat,clon) 
    dist = df.apply(lambda x: p1.distanceTo(LatLon(x['lat'],x['lon']))/1000.0, axis=1)
    df2 = df[dist < CENTER_DIST]
    for idx,row in df2.iterrows():
        geo = np.array(json.loads(row['polygon']))
        if 'lake' in row['type']: 
            ax.fill(geo[:,1],geo[:,0],'blue',alpha=0.4)
        if 'river' in row['type']: 
            ax.plot(geo[:,1],geo[:,0],'blue',alpha=0.4)
    
def plot_water(clat,clon,zoom,ax=None):
    if not ax: fig, ax = plt.subplots()
    data_dir = os.path.dirname(__file__)    
    with zipfile.ZipFile(data_dir + '/lake_river.zip', 'r') as z:
        df =  pd.read_csv(z.open('lake_river.csv'))
        plot_water_df(df,clat,clon,zoom=zoom,ax=ax)

    df =  pd.read_csv(data_dir + '/lake_river_addn.csv')
    plot_water_df(df,clat,clon,zoom,ax=ax)
        
   
def plot_countries(clat,clon,zoom=7,incolor='lightyellow',outcolor='lightblue',country_color={},ax=None,force_include=['']):
    if not ax: fig, ax = plt.subplots()
    data_dir = os.path.dirname(__file__)
    MAX = 20    
    CENTER_DIST = (40000. / MAX)*(zoom+1)
    xlims = (clon+(-180./MAX)*zoom, clon+(180./MAX)*zoom)
    ylims = (clat+(-90./MAX)*zoom, clat+(90./MAX)*zoom)
    p1 = LatLon(clat, clon)
    ax.set_facecolor(color=outcolor)
    sf = shapefile.Reader(data_dir + "/TM_WORLD_BORDERS-0.3.shp", encoding = "ISO8859-1")
    r = sf.records()
    countries = sf.shapes()
    for idx in range(len(countries)):
        country = countries[idx]
        name = r[idx]
        iso3 = r[idx][2]
        lat,lon = name[10],name[9] # middle point of country
        p2 = LatLon(lat, lon)
        d = p1.distanceTo(p2)/1000.0
        # skip if a country is too far and not in force_include list
        if d > CENTER_DIST and iso3 not in force_include: continue 
        bounds = list(country.parts) + [len(country.points)]        
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)        
        for previous, current in zip(bounds, bounds[1:]):    
            geo = [[x[0],x[1]] for x in country.points[previous:current]]
            if len(geo) < 1: continue
            geo = np.array(geo)
            if geo.shape[0] > 0:
                if iso3 in country_color: 
                    ax.fill(geo[:,0],geo[:,1],country_color[iso3],alpha=0.5)
                else:
                    ax.fill(geo[:,0],geo[:,1],incolor,alpha=0.5)
                ax.plot(geo[:,0],geo[:,1],'b')

def plot_continents(clat,clon,zoom=7,incolor='lightyellow',outcolor='lightblue',len_thres=10,fill=True,ax=None):
    if not ax: fig, ax = plt.subplots()
    data_dir = os.path.dirname(__file__)
    zip_file    = zipfile.ZipFile(data_dir + "/continents.zip")
    fin  = zip_file.open('continents.json')
    res = json.loads(fin.read())

    MAX = 20    
    CENTER_DIST = (40000. / MAX)*(zoom+1)
    xlims = (clon+(-180./MAX)*zoom, clon+(180./MAX)*zoom)
    ylims = (clat+(-90./MAX)*zoom, clat+(90./MAX)*zoom)
    
    ax.set_facecolor(color=outcolor)
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    
    for i in range(8):
        for x in res['features'][i]['geometry']['coordinates']:
            if len(x[0]) > len_thres:
                arr = np.array(x[0])
                if fill:
                   ax.fill(arr[:,0],arr[:,1],incolor,alpha=0.5)
                else:
                   ax.plot(arr[:,0],arr[:,1],incolor)
                
def plot_elevation(clat,clon,zoom,levels=None,lleft=None,uright=None,ax=None):
    if not ax: fig, ax = plt.subplots()    
    tkeys = np.array(list(gltiles.keys()))
    CENTER_DIST = 2000 * zoom
    print ('dist',CENTER_DIST)

    if not lleft:
        p1 = LatLon(clat,clon)
        EARTH_RAD = 6371
        upright = p1.destination (CENTER_DIST, bearing=45, radius=EARTH_RAD)
        lowleft = p1.destination (CENTER_DIST, bearing=225, radius=EARTH_RAD)
        latmin = np.min([lowleft.lat, upright.lat])
        latmax = np.max([lowleft.lat, upright.lat])
        lonmin = np.min([lowleft.lon, upright.lon])
        lonmax = np.max([lowleft.lon, upright.lon])
    else:
        latmin = np.min([lleft[0],uright[0]])
        latmax = np.max([lleft[0],uright[0]])
        lonmin = np.min([lleft[1],uright[1]])
        lonmax = np.max([lleft[1],uright[1]])

    N = 15
    x = np.linspace(lonmin,lonmax,N)
    y = np.linspace(latmin,latmax,N)
    newx,newy =  np.meshgrid(x,y)
    latints = np.unique(y.astype(int))
    lonints = np.unique(x.astype(int))
    
    skip = len(latints)
    tile = tkeys[find_tile(clat,clon)]    
    q = get_quad(tuple(latints),tuple(lonints),tile)
    interp = np.vectorize(q.interpolate,otypes=[np.float64])
    newz = interp(newx,newy)
    newz[newz<0] = 0
    #newz = conv2d(padding(newz),initialize_kernel((3,3),1))    
    CS=plt.contour(newx,newy,newz,cmap=plt.cm.binary,levels=levels)
    plt.clabel(CS, fontsize=10, inline=1)

def elev_at(clat,clon):    
    clats = [int(clat)-1, int(clat), int(clat)+1]
    clons = [int(clon)-1, int(clon), int(clon)+1]
    tkeys = np.array(list(gltiles.keys()))
    tile = tkeys[find_tile(clat,clon)]    
    q = get_quad(tuple(clats),tuple(clons),tile)
    res = q.interpolate(clon,clat)
    return res
    
def plot_line(regarr,ax,color='black',linestyle='solid'):
    ax.plot(regarr[:,1],regarr[:,0],color=color,linestyle=linestyle)
       
def plot_region(regarr,ax,color='lightgray',alpha=0.5):
    ax.fill(regarr[:,1],regarr[:,0],color=color,alpha=alpha)
    
def find_city(name,country):
    data_dir = os.path.dirname(__file__)
    zip_file    = zipfile.ZipFile(data_dir + '/cities.zip')
    items_file  = zip_file.open('cities.csv')
    items_file  = io.TextIOWrapper(items_file)
    rd = csv.reader(items_file)
    headers = {k: v for v, k in enumerate(next(rd))}
    res = []
    for row in rd:
        if name.lower() == row[headers['nameascii']].lower().strip() and \
           country.lower() == row[headers['country_name']].lower().strip():
            res.append(row[:])
    return res

def get_country_name_iso3():
    data_dir = os.path.dirname(__file__)
    sf = shapefile.Reader(data_dir + "/TM_WORLD_BORDERS-0.3.shp", encoding = "ISO8859-1")
    r = sf.records()
    countries = sf.shapes()
    name_iso3_dict = {}
    for idx in range(len(countries)):
        country = countries[idx]
        iso3,name = r[idx][2],r[idx][4]
        name_iso3_dict[name] = iso3
    return name_iso3_dict

def get_country_geo():
    data_dir = os.path.dirname(__file__)
    sf = shapefile.Reader(data_dir + "/TM_WORLD_BORDERS-0.3.shp", encoding = "ISO8859-1")
    r = sf.records()
    countries = sf.shapes()
    country_geo = {}
    for idx in range(len(countries)):
        iso3 = r[idx][2]
        lat,lon = r[idx][10],r[idx][9] # middle point of country
        country_geo[iso3] = (lat,lon)
    return country_geo
