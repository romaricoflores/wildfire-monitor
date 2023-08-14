import ee
import folium

# Authenticate and initialize the Earth Engine API
ee.Authenticate()
ee.Initialize()

# Define the study area (e.g., Kamloops, BC)
study_area = ee.Geometry.Point(-121.597, 50.448)

# Load a Landsat image
landsat = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA') \
    .filterBounds(study_area) \
    .filterDate('2022-01-01', '2022-12-31') \
    .sort('CLOUD_COVER') \
    .first()

# Visualize the Landsat image
landsat_vis_params = {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 0.3}
landsat_map = folium.Map(location=[50.448, -121.597], zoom_start=10)
landsat_map.add_ee_layer(landsat, landsat_vis_params, 'Landsat Image')
display(landsat_map)

# Perform a simple analysis (calculate NDVI)
def calculate_ndvi(image):
    ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI')
    return image.addBands(ndvi)

landsat_with_ndvi = calculate_ndvi(landsat)

# Visualize NDVI
ndvi_params = {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'green']}
ndvi_map = folium.Map(location=[50.448, -121.597], zoom_start=10)
ndvi_map.add_ee_layer(landsat_with_ndvi.select('NDVI'), ndvi_params, 'NDVI')
display(ndvi_map)
