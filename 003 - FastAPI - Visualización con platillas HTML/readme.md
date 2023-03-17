### Visualización de QUERYs a MongoDB y visualización en plantillas HTML

La idea de este desarrollo es crear un fichero HTML dinámico con tablas de datos que iremos rellenando según las Querys generadas en los .py de modo dinámico, controlando la logitud de los datos mostrados y la paginación, botones para realizar acciones sobre las búsquedas, ... utilizando Bootstrap y con diseño responsive.

### Funcionamiento

* El fichero .env contiene los datos de acceso a tu clúster de Mongo DB Atlas

![image](https://user-images.githubusercontent.com/20743678/225888717-5fd66b79-d81c-4b22-be30-73bdb0ab007c.png)

* En la carpeta "templates" están los ficheros "indexXX.html", que son los que lee la API y los devuelve modificados como respuesta. Todos estos fichero funcionan con la API, y todos son distintos diseños HTML con Bootstrap y FontAwesome. Simplemente renombra la plantilla que te interese a "index.html" y el fichero "/static/styleXX.css" a "style.css". El fichero index03.html necesita del fichero /static/style03.css, el index05.html necesita del fichero /static/style05.css, etc.

Renombra pues la plantilla y el css deseados a "index.html" y "style.css" y la API ya hará uso de ellas, o modifica en el código del fichero main.py la llamada a estos ficheros con el nombre deseado.

![image](https://user-images.githubusercontent.com/20743678/225890639-802f87c2-3f90-4cef-b354-f1d2c9fbb5f5.png)

![image](https://user-images.githubusercontent.com/20743678/225890903-62ca4fe9-f647-41f3-9faa-ff6987413f64.png)

La función list_books de main.py, llama a TEMPLATES.TemplateResponse pasándole como argumento "index.html", la variable "request" y los datos almacenados en la lista "lista_de_books". 

```python
@app.get("/", response_description="List all books", response_model=List[Book])
def list_books(request: Request):
    books = collection.find(limit=10)
    lista_de_books = []
    for book in books:
        book_actual = {"_id":str(book["_id"]), "st": str(book["st"])}
        lista_de_books.append(book_actual)
       
    return TEMPLATES.TemplateResponse("index.html",{"request": request, "recipes": lista_de_books})
 ```
 
 Está última variable, "lista_de_books", es utilizada dentro de index.html con la construcción
 
 ```sell
 {% for recipe in recipes %}
      {{ recipe.id }}
      {{ recipe.st }}
 {% endfor %}
 ```
 
 De esta forma dentro de index.html:
 
 ```html
{% for recipe in recipes %}

    <div class="card mb-3">
     <div class="card-body">
      <div class="d-flex flex-column flex-lg-row">
       <span class="avatar avatar-text rounded-3 me-4 bg-info mb-2">{{ recipe.id }}</span>
        <div class="row flex-fill">
         <div class="col-sm-5">
          <h4 class="h5">{{ recipe.st }}</h4>
          <span class="badge bg-secondary">WORLDWIDE</span> <span class="badge bg-success">$150K - $210K</span>
         </div>
        <div class="col-sm-4 py-2">
        <span class="badge bg-secondary">PRODUCT MARKETING</span>
        <span class="badge bg-secondary">MARKETING</span>
        <span class="badge bg-secondary">EXECUTIVE</span>
        <span class="badge bg-secondary">ECOMMERCE</span>
       </div>
      <div class="col-sm-3 text-lg-end">
       <a href="#" class="btn btn-primary stretched-link">Apply</a>
      </div>
     </div>
    </div>
        </div>
{% endfor %}
```
    
El funcionamiento es el siguiente:

{% for recipe in recipes %} indica el comienzo de un bucle, que recorrerá la lista "recipes" que hemos declarado en la llamada TEMPLATES.TemplateResponse y que hemos establecido que su valor era la lista "lista_de_books". Para cada uno de los elemento de dicha lista (recipe in recipes), inssertará en el código HTML todo lo que esté debajo del bucle, hasta el código {% endfor %}. De esta forma, indicamos que se cree una fila (tr) y tantas colunmnas como necesitemos (td) para imprimir en el HTML los datos de las variables, en este ejemplo, con {{ recipe.id }} y {{ recipe.st }}, que son los dos elementos que componen cada uno de los elementos de "recipe".

Un ejemplo más sencillo sería este:

```html
<table border=1> 
{% for recipe in recipes %}
    <tr>
        <td>
            Voy a imprimir el primer valor que es el ID almacenado en recipe.id
        </td>
        <td>
            {{ recipe.id }}
        </td>
        <td>
            Aquí meto el valor de recipe.st
        </td>
        <td>
            {{ recipe.st }}
        </td>
    </tr>
 {% endfor %}
</table>
```

![image](https://user-images.githubusercontent.com/20743678/225895235-f07503fb-6e29-40ea-8f3e-c85e83753ddb.png)
