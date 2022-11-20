from sqlalchemy import create_engine

user = 'usr_owr_gestion_datos'
password = 'Mexico123'
host = '10.10.58.75'
port = 5432
database = 'GESTION_DATOS'


def get_connection():
    
	return create_engine(
		url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
			user, password, host, port, database
		)
	)
