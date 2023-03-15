import pymongo

# Descomentar para uso con mongodb server en local
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Creamos la conexión (modifica con tu usuario, contraseña y ruta a tu clúster
DB_conn = pymongo.MongoClient("mongodb+srv://usuario:password@cluster0.ruta_a_tu_cluster.mongodb.net/?retryWrites=true&w=majority")

# Listar todas las BD
for db_name in DB_conn.list_database_names():
	db = DB_conn[db_name]
	print(db_name)

# Listar todas las colecciones de todas las BD
for db_name in DB_conn.list_database_names():
	db = DB_conn[db_name]
	print("DataBase => {}".format(db_name))
	for coll_name in db.list_collection_names():
    	print("\t|-> Collection: {}".format(coll_name))

# Listar todos los elementos de una colección de una BD (¡¡¡OJO!!! si hay muchos datos puede ser un trabajo muy largo)
for db_name in DB_conn.list_database_names():
	db = DB_conn[db_name]
	for coll_name in db.list_collection_names():
    	print("db: {}, collection:{}".format(db_name, coll_name))
    	for r in db[coll_name].find({}):
			print(r)
    		print('\n\n')   
