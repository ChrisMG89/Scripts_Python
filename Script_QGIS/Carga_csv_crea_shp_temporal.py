import os
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsFields,
    QgsField,
    QgsVectorFileWriter,
)

# Define el directorio donde están los archivos CSV
directorio = r'C:\Users\chris\AEROTOOLS-UAV Dropbox\AEROTOOLS-UAV\Proyectos\PLANTAS_PV\JENCORE\CAROLINAS_I\2024\CSVs'

# Iterar sobre cada archivo en el directorio
for archivo in os.listdir(directorio):
    if archivo.endswith('_location.csv'):
        ruta_archivo = os.path.join(directorio, archivo)

        # Crear una capa de texto delimitado
        layer = QgsVectorLayer(f'file:///{ruta_archivo}?delimiter=,', archivo, 'delimitedtext')

        # Verificar si la capa se cargó correctamente
        if layer.isValid():
            # Crear una nueva capa con geometría de puntos
            new_layer = QgsVectorLayer('Point?crs=EPSG:4326', archivo, 'memory')
            new_provider = new_layer.dataProvider()

            # Definir los campos manualmente
            new_fields = QgsFields()
            new_fields.append(QgsField('imagen', QVariant.String))  # Nombre de la imagen
            new_fields.append(QgsField('latitud', QVariant.Double))  # Coordenada Y
            new_fields.append(QgsField('longitud', QVariant.Double))  # Coordenada X
            new_provider.addAttributes(new_fields)
            new_layer.updateFields()

            # Agregar las características a la nueva capa
            for feature in layer.getFeatures():
                # Obtener los valores de la fila actual
                imagen = feature[0]  # Nombre de la imagen (primer valor)
                latitud = feature[1]  # Coordenada Y (field_2)
                longitud = feature[2]  # Coordenada X (field_3)

                # Crear la geometría
                point = QgsPointXY(longitud, latitud)  # QGIS usa (X, Y)
                new_feature = QgsFeature()
                new_feature.setGeometry(QgsGeometry.fromPointXY(point))
                new_feature.setAttributes([imagen, latitud, longitud])  # Atributos de la imagen y coordenadas

                new_provider.addFeature(new_feature)

            # Actualizar la nueva capa
            new_layer.updateExtents()

            # Guardar la nueva capa como un shapefile
            shapefile_path = os.path.join(directorio, f"{os.path.splitext(archivo)[0]}.shp")
            error = QgsVectorFileWriter.writeAsVectorFormat(new_layer, shapefile_path, "UTF-8", new_layer.crs(), "ESRI Shapefile")

            if error[0] == QgsVectorFileWriter.NoError:
                print(f'Capa {archivo} guardada como shapefile en: {shapefile_path}')
                QgsProject.instance().addMapLayer(new_layer)  # Añadir la nueva capa al proyecto
            else:
                print(f'Error al guardar la capa {archivo}: {error}')

        else:
            print(f'Error al cargar la capa {archivo}.')

print('Carga de capas completada.')
