# Tesi_2024

Per il corretto funzionamento dell'applicativo:

Importare il database Postgres, passaggi su Windows:


1) avere installato postgres, verifica da terminale

psql --version



2) crea un database con lo stesso nome

psql -h localhost -U postgres

CREATE DATABASE farm_db;

conferma creazione



3) ripristino backup

psql -U postgres -d farm_db -f C:\pathToBackup\..\Tesi_2024\farm_db_backup.sql

psql -U [postgres] -d [farm_db] -f database_export.sql


Installare dipendenze sul nuovo computer

pip install -r requirements.txt


4) Se necessario modificare le password in db_handler.py


conn_params = {
    "host": "localhost",
    "dbname": "farm_db",
    "user": "postgres",
    "password": "TuaPassword",
    "port": "5432"
}


engine = create_engine('postgresql+psycopg2://postgres:TuaPassword@localhost/farm_db')


5) Eseguire l'applicazione

flask run --host=0.0.0.0
o
...\tesi_2024\track_1.6_dashboard\code python app.py  +  ctr click su  http://127.0.0.1:8050/
