### Autores:

- MC. Rodolfo Lopez
- Dr. Oscar de la Torre
- Dr. Felipe Andoni

### Descripcion:

- Libreria para la extraccion de precios de granos, frutas y hortalizas del SNIIM.

### Requerimientos:

- pip install pymongo

### Uso:

- import sniimapp
- sniim = sniimapp.SNIIM('granos', '01/01/2018', '22/01/2018')
- data = sniim.get_data()

- print(data[1])
- print(data.explain())

Para hacer una consulta se debe crear un objeto SNIIM(producto[fyh,granos], fecha_inicial, fecha_fina):
- sniim = sniimapp.SNIIM('fyh', '01/01/2018', '22/01/2018')

La funcion get_data() regresa un objeto cursor Mongo con el cual se puede interactur con los datos.
Para mas informaciion sobre cursor Mongo visite [Tools for iterating over MongoDB query results](https://pymongo.readthedocs.io/en/stable/api/pymongo/cursor.html#pymongo.cursor.Cursor.address)
