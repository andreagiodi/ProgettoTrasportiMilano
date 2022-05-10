import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import folium
import contextily
import geopandas as gpd
import pygeos
import pandas as pd
import io
from flask import Flask, render_template, send_file, make_response, url_for, Response, request
app = Flask(__name__)


# pip install flask geopandas pandas contextily matplotlib folium pygeos

matplotlib.use('Agg')


quartieri = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/quartieri_milano.zip')
area_sosta_car_sharing = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/area_sosta_car_sharing.zip')
aree_velocita_lim = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/aree_velocita_lim.zip')
comuni = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/comuni.zip')
fermate_metro = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/fermate_metro.zip')
fermate_superficie = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/fermate_superifcie.zip')
fontanelle = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/Fontanelle.zip')
parcheggi_pubblici = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/parcheggi_pubblici.zip')
pedoni_ztl = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/pedoni_ztl.zip')
percorsi_metro = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/percorsi_metro.zip')
percorsi_superficie = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/percorsi_superficie.zip')
piste_ciclabili = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/piste_ciclabili.zip')
province = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/province.zip')
quartieri_milano = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/quartieri_milano.zip')
sosta_turistici = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/sosta_turistici.zip')
stazioni_bikemi = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/stazioni_bikemi.zip')
stazioni_milano = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/stazioni_milano.csv')
bike_sosta = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/bike_sosta.zip')

area_sosta_car_sharing = area_sosta_car_sharing.to_crs(4326)
area_sosta_car_sharing['lon'] = area_sosta_car_sharing['geometry'].x
area_sosta_car_sharing['lat'] = area_sosta_car_sharing['geometry'].y
bike_sosta['lon'] = bike_sosta['geometry'].x
bike_sosta['lat'] = bike_sosta['geometry'].y
bike_sosta.dropna(inplace=True)
fontanelle['lon'] = fontanelle['geometry'].x
fontanelle['lat'] = fontanelle['geometry'].y
parcheggi_pubblici = parcheggi_pubblici.to_crs(4326)
parcheggi_pubblici['lon'] = parcheggi_pubblici['geometry'].x
parcheggi_pubblici['lat'] = parcheggi_pubblici['geometry'].y
piste_ciclabili = gpd.overlay(piste_ciclabili, piste_ciclabili, how='union').sort_values(ascending=True, by='anagrafica_1')
fermate_metro = fermate_metro.to_crs(4326)
fermate_metro['lon'] = fermate_metro['geometry'].x
fermate_metro['lat'] = fermate_metro['geometry'].y
fermate_superficie = fermate_superficie.set_crs(4326)
fermate_superficie['lon'] = fermate_superficie['geometry'].x
fermate_superficie['lat'] = fermate_superficie['geometry'].y

@app.route('/test1', methods=['GET'])
def test():
    m = folium.Map(location=[45.46220047218434, 9.191121737490482],zoom_start=12, tiles='CartoDB positron')
    for _, r in quartieri_milano.iterrows():

        sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'gray'})
        folium.Popup(r['NIL']).add_to(geo_j)
        geo_j.add_to(m)
    for _, r in piste_ciclabili.iterrows():

        sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {
                               'fillColor': 'black'})
        folium.Popup(r['anagrafica']).add_to(geo_j)
        geo_j.add_to(m)
    return render_template('test.html', test=m._repr_html_())


@app.route('/', methods=['GET'])
def index():

    # folium mappa for per creare comune
    m = folium.Map(location=[45.46220047218434, 9.191121737490482],zoom_start=12, tiles='openstreetmap')  # CartoDB positron
    for _, r in quartieri_milano.iterrows():
        sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
        folium.Popup(r['NIL']).add_to(geo_j)
        geo_j.add_to(m)

    return render_template('index2.html', map=m._repr_html_())


@app.route('/resultdrop', methods=['GET'])
def resultdrop():
    #primo risultato dopo la selezione della categoria nel dropdown
    m = folium.Map(location=[45.46220047218434, 9.191121737490482],zoom_start=12, tiles='openstreetmap')
    m1 = folium.Map(location=[45.46220047218434, 9.191121737490482], zoom_start=12, tiles='openstreetmap')
    if request.args.get('sel') == 'area_sosta':  # AREA_SOSTA
        global zip
        zip = area_sosta_car_sharing['AREA_SOSTA'].sort_values()
        global zipg
        zipg = area_sosta_car_sharing
        global a
        a = 'area_sosta_car_sharing'
        key='true'
        #popup1 = zip.values[0]
        # prima pagina
        for _, row in area_sosta_car_sharing.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=row['AREA_SOSTA'],
                icon=folium.map.Icon(color='green')
            ).add_to(m)
        # seconda pagina
    if request.args.get('sel') == 'aree_velocita':  # aree_velocita
        
        zip = aree_velocita_lim['nome_via'].sort_values()

        zipg = aree_velocita_lim
   
        a = 'aree_velocita_lim'
        key='true'
        
        for _, r in aree_velocita_lim.iterrows():
            sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
            folium.Popup(r['nome_via']).add_to(geo_j)
            geo_j.add_to(m)
    if request.args.get('sel') == 'aree_sosta_bike':  # aree_sostaBike
        
        zip = bike_sosta['categoriev']

        zipg = bike_sosta
   
        a = 'bike_sosta'
        key='false'
        
        for _, row in bike_sosta.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=row['categoriev'],
                icon=folium.map.Icon(color='green')
            ).add_to(m)
    if request.args.get('sel') == 'fontanelle':  # fontanelle
        
        zip = fontanelle

        zipg = fontanelle
   
        a = 'fontanelle'
        key='false'
        
        for _, row in fontanelle.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                icon=folium.map.Icon(color='green')
            ).add_to(m)
    if request.args.get('sel') == 'parcheggi_pubblici':  # parcheggi_pubblici
        
        zip = parcheggi_pubblici['indirizzo'].sort_values()

        zipg = parcheggi_pubblici
   
        a = 'parcheggi_pubblici'
        key='true'
        
        for _, row in parcheggi_pubblici.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=row['indirizzo'],
                icon=folium.map.Icon(color='green')
            ).add_to(m)
    if request.args.get('sel') == 'pedoni_ztl':  # parcheggi_pubblici
        
        zip = pedoni_ztl['nome'].sort_values()

        zipg = pedoni_ztl

        zip1 = pedoni_ztl[pedoni_ztl['tipo'] == 'AREA_B']
        zip2 = pedoni_ztl[pedoni_ztl['tipo'] == 'AREA_C']

        a = 'pedoni_ztl'
        key='false'

        for _, r in zip1.iterrows():
            sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'yellow', 'color' : 'yellow'})
            folium.Popup(r['nome']).add_to(geo_j)
            geo_j.add_to(m)
        for _, r in zip2.iterrows():
            sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'red', 'color' : 'red'})
            folium.Popup(r['nome']).add_to(geo_j)
            geo_j.add_to(m)
    if request.args.get('sel') == 'piste_ciclabili':  # piste_ciclabili 
        
        zip = piste_ciclabili['anagrafica_1'].sort_values()

        zipg = piste_ciclabili


        a = 'piste_ciclabili'
        key='false'

        
        for _, r in piste_ciclabili.iterrows():
            sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
            folium.Popup(r['anagrafica_1']).add_to(geo_j)
            geo_j.add_to(m)


    if request.args.get('sel') == 'percorsi_metro':  # fermate_metro DA FINIRE
        
        zip = fermate_metro['nome'].sort_values()

        zipg = fermate_metro


        a = 'fermate_metro'
        key='false'

        
        for _, row in fermate_metro.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=row['nome'],
                icon=folium.map.Icon(color='green')
            ).add_to(m)
        for _, r in percorsi_metro.iterrows():
            sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.000001)
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
            folium.Popup(r['linea']).add_to(geo_j)
            geo_j.add_to(m)


    if request.args.get('sel') == 'percorsi_superficie':  # percorsi_superficie 
        
        zip = percorsi_superficie['nome'].sort_values()

        zipg = percorsi_superficie


        a = 'percorsi_superficie'
        key='false'

        
        for _, row in fermate_superficie.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=row['ubicazione'],
                icon=folium.map.Icon(color='green')
            ).add_to(m)
        for _, r in percorsi_superficie.iterrows():
            sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.000001) 
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
            folium.Popup(r['linea']).add_to(geo_j)
            geo_j.add_to(m)
        


    return render_template('index2.html', map=m._repr_html_(), percorsi_superficie=percorsi_superficie.to_html(), key=key ,zip=zip)


@app.route('/resultdrop1', methods=['GET'])
def resultdrop1():
    #dropdown di risposta delle (vie) di area_sosta e ogni altro dataframe (ancora da fare)
    m = folium.Map(location=[45.46220047218434, 9.191121737490482],zoom_start=12, tiles='openstreetmap')
    key='true'
    value = request.args.get('sel1')
    if a == 'area_sosta_car_sharing':
        value1 = zipg[zipg.AREA_SOSTA == value]
        folium.Marker(
            location=[value1["lat"], value1["lon"]],
            popup=value1['AREA_SOSTA'].values[0],
            icon=folium.map.Icon(color='green')
        ).add_to(m)
        
    if a == 'aree_velocita_lim':
        value1 = zipg[zipg.nome_via == value]
        sim_geo = gpd.GeoSeries(value1['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
        folium.Popup(value1['nome_via'].values[0]).add_to(geo_j)
        geo_j.add_to(m)
    if a == 'parcheggi_pubblici':
        value1 = zipg[zipg.indirizzo == value].sort_values(by='indirizzo')
        folium.Marker(
            location=[value1["lat"], value1["lon"]],
            popup=value1['indirizzo'].values[0],
            icon=folium.map.Icon(color='green')
        ).add_to(m)
    
        
    
    #m1 = folium.Map(location=[45.46220047218434, 9.191121737490482], zoom_start=12, tiles='openstreetmap')
    
    return render_template('index2.html', map=m._repr_html_(), key=key, zip=zip)


@app.route('/testresult', methods=['GET'])
def testresult():

    # dopo selezione returna cio(puo fare infinito da ora):
    if request.args['sel'] == 'aree_sosta':  # AREA_SOSTA
        
        m = folium.Map(location=[y[0], x[0]],
                       zoom_start=40, tiles='openstreetmap')
        for index, row in area_sosta_car_sharing.iterrows():
            folium.Marker(
                popup=row['AREA_SOSTA'],
                icon=folium.map.Icon(color='green')
            ).add_to(m)

    return render_template('index.html', map=m._repr_html_(), table=ps)


@app.route('/test', methods=['GET'])
def test1():
    ps = fermate_superficie
    ps = ps.to_html()

    return render_template('test.html', table=ps)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)


