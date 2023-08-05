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

La clase devuelve un diccionario con los datos.

- from precios_sniim import SNIIM
- sniim     = SNIIM('fyh', '2023-06-22', '2023-06-22')
- resultado = sniim.get_data()

**Para formatear la fecha**
- resultado[0]['fecha'].strftime("%Y-%m-%d")
