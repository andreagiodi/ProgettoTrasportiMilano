from flask import Flask, render_template, send_file, make_response, url_for, Response, request
app = Flask(__name__)

import io
import pandas as pd
import geopandas as gpd
import contextily
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
#milano = comuni[comuni.NOME == 'Milano']
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
    
    return render_template('test.html')



@app.route('/', methods=['GET'])
def index():
    ps = percorsi_superficie[['linea', 'nome']].sort_values(['nome'], ascending=True)                        #.set_index('nome')
    ps = ps.to_html(index=False)







    return render_template('index.html', table=ps)





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)