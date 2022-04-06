from flask import Flask, render_template, send_file, make_response, url_for, Response, request
app = Flask(__name__)

import io
import pandas as pd
import geopandas as gpd
import contextily
import folium
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


quartieri = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/quartieri_milano.zip')
area_sosta_car_sharing = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/area_sosta_car_sharing.zip')
aree_velocita_lim = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/aree_velocita_lim.zip')
bike_sosta = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/bike_sosta.zip')
comuni = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/comuni.zip')
comuni = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/comuni.zip')
fermate_metro = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/fermate_metro.zip')
fermate_superficie = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/fermate_superifcie.zip')
fontanelle = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/Fontanelle.zip')
parcheggi_pubblici = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/parcheggi_pubblici.zip')
pedoni_ztl = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/pedoni_ztl.zip')
percorsi_metro = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/percorsi_metro.zip')
percorsi_superficie = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/percorsi_superficie.zip')
piste_ciclabili = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/piste_ciclabili.zip')
province = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/province.zip')
quartieri_milano = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/quartieri_milano.zip')
sosta_turistici = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/sosta_turistici.zip')
stazioni_bikemi = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/stazioni_bikemi.zip')
stazioni_milano = gpd.read_file('/workspace/ProgettoTrasportiMilano/filezip/stazioni_milano.csv')



@app.route('/test', methods=['GET'])
def test():
    m = folium.Map(location=[45.46220047218434, 9.191121737490482], zoom_start=12, tiles='CartoDB positron')
    for _, r in quartieri_milano.iterrows():
        
    
        sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'none'})
        folium.Popup(r['NIL']).add_to(geo_j)
        geo_j.add_to(m)
    for _, r in piste_ciclabili.iterrows():
        
    
        sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'black'})
        folium.Popup(r['anagrafica']).add_to(geo_j)
        geo_j.add_to(m)
    return render_template('test.html', test=m._repr_html_())



@app.route('/', methods=['GET'])
def index():


    #ps = percorsi_superficie[['linea', 'nome']].sort_values(['nome'], ascending=True)                       
    #ps = ps.to_html(index=False)
    global ps #globale per altra route
    ps = piste_ciclabili['anagrafica'].drop_duplicates().to_list()
    ps = sorted(ps)  
    #ps = ps.to_html(index=False)

    #folium mappa for per creare comune
    m = folium.Map(location=[45.46220047218434, 9.191121737490482], zoom_start=12, tiles='openstreetmap') #CartoDB positron
    for _, r in quartieri_milano.iterrows():
        
        sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
        folium.Popup(r['NIL']).add_to(geo_j)
        geo_j.add_to(m)
    return render_template('index.html', table=ps, map=m._repr_html_())


@app.route('/resultdrop', methods=['GET'])
def resultdrop():

    #dopo selezione returna cio(puo fare infinito da ora):
    lines = piste_ciclabili[piste_ciclabili['anagrafica']== request.args.get('sel')]
    x, y = list(lines['geometry'])[0].coords.xy
    m = folium.Map(location=[y[0], x[0]], zoom_start=40, tiles='openstreetmap')
    
    
    for _, r in lines.iterrows():
        sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
        folium.Popup(r['anagrafica']).add_to(geo_j)
        geo_j.add_to(m)
    
    return render_template('index.html', map=m._repr_html_(), table=ps)




@app.route('/testresult', methods=['GET'])
def testresult():

    #dopo selezione returna cio(puo fare infinito da ora):
    lines = piste_ciclabili[piste_ciclabili['anagrafica']== request.args.get('sel')]
    x, y = list(lines['geometry'])[0].coords.xy
    m = folium.Map(location=[y[0], x[0]], zoom_start=40, tiles='openstreetmap')
    
    
    for _, r in lines.iterrows():
        sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
        folium.Popup(r['anagrafica']).add_to(geo_j)
        geo_j.add_to(m)
    
    return render_template('index.html', map=m._repr_html_(), table=ps)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)