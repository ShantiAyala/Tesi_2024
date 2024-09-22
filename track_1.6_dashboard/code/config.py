#Questo file contiene le configurazioni per l'applicazione, come le impostazioni del database e altre variabili.
import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://postgres:pollo54@localhost/farm_db'