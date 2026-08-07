import pandas as pd
import geopandas as gpd

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 1 (Existing CGS) - IMPORTING THE DATA
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#------ EXISTING CGS DATA ------

#Prepare CGS Data

#Import data
gdf = gpd.read_file("Data/Processed_Data/Existing_CGSs.gpkg")
print(gdf.columns)
#Set the 'id' column as unique identifier
gdf= gdf.rename(columns={'id':'uid'})


#Ensure CRS is correct
gdf = gdf.to_crs(4326)

#Separate points and polygons
points = gdf[gdf.geometry.geom_type.isin(["Point", "MultiPoint"])]
polygons = gdf[gdf.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]


#------ BASE MAP DATA ------

#Import Leeds outline
Leeds_outline = gpd.read_file("Data/Processed_Data/Leeds_boundaries.gpkg")
#Ensure CRS is correct
Leeds_outline = Leeds_outline.to_crs(4326)


#Import Leeds wards
Leeds_wards = gpd.read_file("Data/Processed_Data/Leeds_Wards.gpkg")
#Ensure CRS is correct
Leeds_wards = Leeds_wards.to_crs(4326)

#------ POSTCODES DATA ------

#Import Leeds postcode geometries
Leeds_postcodes = gpd.read_file("Data/Processed_Data/leeds_postcodes.gpkg")
#Ensure postcodes are strings
Leeds_postcodes['Postcode'] = Leeds_postcodes['Postcode'].astype(str)
#Ensure CRS is correct
Leeds_postcodes  = Leeds_postcodes.to_crs(4326)

#------ EXISTING CGS SOIL DATA ------

#Import soil health data per CGS
soil_health_CGSs = gpd.read_file("Data/Processed_Data/soil_health_CGSs.csv")
print(soil_health_CGSs.columns)



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 (Imagining Future Growing Spaces) - IMPORT DATA
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#------ OVERALL SOIL HEALTH DATA ------

soil_health = gpd.read_file("Data/Processed_Data/soil_health.gpkg")
soil_health = soil_health.to_crs(4326)

#------ OVERALL HEAVY METALS DATA ------

heavy_metals = gpd.read_file("Data/Processed_Data/heavy_metals.gpkg")
heavy_metals = heavy_metals.to_crs(4326)

#------ SOIL HEALTH THRESHOLDS DATA ------

thresholds= pd.read_excel("Data/Raw_Data/Soil_health_Thresholds.xlsx")