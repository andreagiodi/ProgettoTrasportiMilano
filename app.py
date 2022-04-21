import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import folium
import contextily
import geopandas as gpd
import pandas as pd
import io
from flask import Flask, render_template, send_file, make_response, url_for, Response, request
app = Flask(__name__)


# pip install flask geopandas pandas contextily matplotlib folium

matplotlib.use('Agg')


quartieri = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/quartieri_milano.zip')
area_sosta_car_sharing = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/area_sosta_car_sharing.zip')
aree_velocita_lim = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/aree_velocita_lim.zip')
bike_sosta = gpd.read_file(
    '/workspace/ProgettoTrasportiMilano/filezip/bike_sosta.zip')
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


area_sosta_car_sharing = area_sosta_car_sharing.to_crs(4326)
area_sosta_car_sharing['lon'] = area_sosta_car_sharing['geometry'].x
area_sosta_car_sharing['lat'] = area_sosta_car_sharing['geometry'].y


@app.route('/test1', methods=['GET'])
def test():
    m = folium.Map(location=[45.46220047218434, 9.191121737490482],
                   zoom_start=12, tiles='CartoDB positron')
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

    m = folium.Map(location=[45.46220047218434, 9.191121737490482],zoom_start=12, tiles='openstreetmap')
    m1 = folium.Map(location=[45.46220047218434, 9.191121737490482], zoom_start=12, tiles='openstreetmap')

    if request.args.get('sel') == 'area_sosta':  # AREA_SOSTA
        zip = area_sosta_car_sharing['AREA_SOSTA']
        key='true'
        # prima pagina
        for _, row in area_sosta_car_sharing.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=row[['AREA_SOSTA', 'LOCALIZ']],
                icon=folium.map.Icon(color='green')
            ).add_to(m)
        # seconda pagina

    if request.args.get('sel') == 'aree_velocita':  # aree_velocita
        key='true'
        for _, r in aree_velocita_lim.iterrows():
            sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
            folium.Popup(r['nome_via']).add_to(geo_j)
            geo_j.add_to(m)

    return render_template('index2.html', map=m._repr_html_(), map1=m1._repr_html_(), area_sosta=area_sosta_car_sharing.to_html(), key=key ,zip=zip)


@app.route('/resultdrop1', methods=['GET'])
def resultdrop1():
    #dropdown di risposta delle (vie) di area_sosta e ogni altro dataframe (ancora da fare)
    m = folium.Map(location=[45.46220047218434, 9.191121737490482],zoom_start=12, tiles='openstreetmap')
    m1 = folium.Map(location=[45.46220047218434, 9.191121737490482], zoom_start=12, tiles='openstreetmap')

    

    return render_template('index2.html', map=m._repr_html_())


@app.route('/testresult', methods=['GET'])
def testresult():

    # dopo selezione returna cio(puo fare infinito da ora):
    if request.args['sel'] == 'aree_sosta':  # AREA_SOSTA
        #area_sosta_car_sharing = gpd.geodataframe(area_sosta_car_sharing, geometry= gpd.points_from_xy(area_sosta_car_sharing.LONG_X_4326, area_sosta_car_sharing.LAT_Y_4326))
        m = folium.Map(location=[y[0], x[0]],
                       zoom_start=40, tiles='openstreetmap')
        for index, row in area_sosta_car_sharing.iterrows():
            folium.Marker(
                #location=[row["LAT_Y_4326"], row["LONG_X_4326"]],
                popup=row['AREA_SOSTA'],
                icon=folium.map.Icon(color='green')
            ).add_to(m)

    return render_template('index.html', map=m._repr_html_(), table=ps)


@app.route('/test', methods=['GET'])
def test1():
    ps = area_sosta_car_sharing.to_html()

    return render_template('test.html', table=ps)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3245, debug=True)


# template di risposta a un dropdown
#lines = piste_ciclabili[piste_ciclabili['anagrafica']== request.args.get('sel')]
    #x, y = list(lines['geometry'])[0].coords.xy
    #m = folium.Map(location=[y[0], x[0]], zoom_start=40, tiles='openstreetmap')

    # for _, r in lines.iterrows():
    #sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
    #geo_j = sim_geo.to_json()
    #geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'blue'})
    # folium.Popup(r['anagrafica']).add_to(geo_j)
    # geo_j.add_to(m)
