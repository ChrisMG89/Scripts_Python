import os
from qgis.core import (
    QgsProject,
    QgsVectorLayer
)

# Define el directorio donde están los archivos CSV
directorio = r'C:\Users\chris\AEROTOOLS-UAV Dropbox\AEROTOOLS-UAV\Proyectos\PLANTAS_PV\JENCORE\MIRANDA\2024\CSVs'

# Iterar sobre cada archivo en el directorio
for archivo in os.listdir(directorio):
    if archivo.endswith('_location.csv'):
        ruta_archivo = os.path.join(directorio, archivo)

        # Crear una capa de texto delimitado directamente desde el CSV sin encabezados
        uri = f'file:///{ruta_archivo}?delimiter=,&xField=field_3&yField=field_2&crs=EPSG:4326&useHeader=no'
        layer = QgsVectorLayer(uri, archivo, 'delimitedtext')

        # Verificar si la capa se cargó correctamente
        if layer.isValid():
            # Añadir la capa directamente al proyecto de QGIS
            QgsProject.instance().addMapLayer(layer)
            print(f'Capa {archivo} añadida al proyecto desde: {ruta_archivo}')
        else:
            print(f'Error al cargar la capa {archivo} desde el CSV.')

print('Carga de capas completada.')
