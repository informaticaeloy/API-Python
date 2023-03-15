import pymongo
from bson.objectid import ObjectId

# Descomentar para uso con mongodb server en local
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Creamos la conexión
DB_conn = pymongo.MongoClient("mongodb+srv://usuario:password@cluster0.tu_ruta.mongodb.net/?retryWrites=true&w=majority")

# Listar todas las BD
# Crear una bd

nueva_DB = DB_conn["nombre_nueva_BD"]

# Crear una colección
nueva_coleccion = nueva_DB["prueba_nueva_coleccion"]

# Preparar una query
myquery = { "Campo41": "datos del campo 41","Campo51": "datos del campo 51","Campo61": "datos del campo 61","Campo71": "datos del campo 71" }

# Insertar una query. Guardamos en x los datos del nuevo documento insertado
x = nueva_coleccion.insert_one(myquery)
# Imprimimos el ID del nuevo documento insertado
print("El _id del nuevo elemento insertado es:")
print(x.inserted_id)

# Buscamos con find_one -> nos devuelve el primer elemento que encuentre que cumpla (en este caso, todos, no hay filtro)
# y nos imprime el valor de '_id' y el de 'Campo4'
item_detalle = nueva_coleccion.find_one()
print("El _id y Campo41 del primer elemento encontrado sin filtro es:")
print(item_detalle['_id'])
print(item_detalle['Campo4'])

# Buscamos con find_one -> nos devuelve el primer elemento que encuentre que cumpla que contenga {"Campo41": "datos del campo 41"}
# y nos imprime el valor de '_id' y el de 'Campo41'
item_detalle = nueva_coleccion.find_one({"Campo41": "datos del campo 41"})
print("El _id y Campo41 del primer elemento encontrado con filtro ""Campo41"": ""datos del campo 41"" es:")
print(item_detalle['_id'])
print(item_detalle['Campo41'])

# Buscamos con find -> nos devuelve todos los elementos que encuentre que cumpla (en este caso, todos, no hay filtro)
# y nos imprime el valor de '_id' 
item_detalle = nueva_coleccion.find()
print("El _id de todos los elementos encontrados sin filtro es:")
for documento_actual in item_detalle:
    print(documento_actual['_id'])

# Buscamos con find -> nos devuelve todos los elementos que encuentre que cumplan {"Campo41": "datos del campo 41"}
# y nos imprime el valor de '_id' y 'Campo41'
item_detalle = nueva_coleccion.find({"Campo41": "datos del campo 41"})
print("El _id de todos los elementos encontrados con filtro {""Campo41"": ""datos del campo 41""} es:")
for documento_actual in item_detalle:
    print(documento_actual['_id'])
    print(documento_actual['Campo41'])

# Buscamos con find_one -> nos devuelve todos los elementos que encuentre que cumplan, pero buscando por el campo '_id'
# que es un poco especial, y se define de esta forma
id_buscado = "6411aea07032e989bfadb83b"
objeto_del_id_buscado = ObjectId(id_buscado)
# Buscamos con find_one -> nos devuelve el primer elemento que encuentre que cumpla (en este caso, todos, no hay filtro)
item_detalle = nueva_coleccion.find_one({'_id': objeto_del_id_buscado})
print("EL elemento encontrado por id -> " + str(item_detalle['_id']) + "contiene estos datos:")
print(item_detalle)
