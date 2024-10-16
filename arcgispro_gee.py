import ee
import geemap

ee.Authenticate()


# Initialize Earth Engine
ee.Initialize()

# Define the Map
Map = geemap.Map()

# Define the AOI using the provided coordinates (WGS 84)
#Not displaying the correct AOI
aoi_coordinates = [
    [-88.6388839, 34.9950848], 
    [-88.6758535, 35.4358305], 
    [-89.1999326, 34.9936731], 
    [-89.1820617, 35.4322600]
]


# Create an Earth Engine polygon from the AOI
aoi = ee.Geometry.Polygon(aoi_coordinates)

# Filter Sentinel-2 Harmonized collection using the AOI
collection = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(aoi)  # Filter to AOI
    .filterDate("2023-01-01", "2023-12-31")  # Example date range
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))  # Cloud cover < 20%
)

# Check if the collection has any images
if collection.size().getInfo() == 0:
    raise ValueError("No Sentinel-2 images found for the specified AOI and date range.")

# Select the first available image
image = collection.first()

# Calculate NDVI: (NIR - Red) / (NIR + Red)
ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")

# NDVI visualization parameters
ndvi_vis_params = {
    "min": -1,
    "max": 1,
    "palette": ["blue", "white", "green"],  # Low to high NDVI
}

# Add NDVI layer to the map
Map.addLayer(ndvi, ndvi_vis_params, "NDVI")

# Display the Map
Map

# user-defined bounding box 
bbox = Map.user_roi_coords()

# Export the NDVI image as a GeoTIFF to specified geodatabase path
export_path = r"C:\arcpy\streamgee\MyProject_streamgee\MyProject_streamgee.gdb\ndvi_harmonized.tif" #Not being displayed in the gdb.
geemap.ee_to_geotiff(ndvi, export_path, bbox=bbox, vis_params=ndvi_vis_params, resolution=10)
print(f"NDVI image exported as '{export_path}'.")



