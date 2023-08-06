### Autores:

- MC. Rodolfo Lopez
- Dr. Oscar de la Torre
- Dr. Felipe Andoni

### Descripcion:

- Extraccion de datos del SNIIM.

### Requerimientos:

- pip install SNIIM_2
- pip install mysql-connector-Python

### Uso:

- from sniimapp_2 import sniimapp_2
- sniim = sniimapp_2.SNIIM('fyh', '2018-01-01', '2018-01-22', 'mongo')
- data = sniim.get_data()
- print(data.count())
- print(data[1])

Para formatear la fecha
- data[1]['fecha'].strftime("%Y-%m-%d")
