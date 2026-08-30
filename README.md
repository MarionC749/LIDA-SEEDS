# Spatial and Ecological Evaluation of Developing Spaces (SEEDS) 🌱

## Abstract
Global soil degradation poses a critical challenge to future food security, with the Food and Agriculture Organization of the United Nations (FAO) estimating that 33% of soils are already degraded and over 90% may be at risk by 2050. As pressure on agricultural systems intensifies, cities are increasingly recognised as sites for food production. Community Growing Schemes (CGSs), including community gardens, allotments and informal urban agriculture, represent a key strategy to diversify and localize food production and utilise underused urban land.

Often led by grassroots groups, CGSs improve food security by increasing access to healthy, sustainable and affordable food, particularly for food insecure populations. They strengthen resilience to supply chain disruptions and support more democratic, local food systems. 

Beyond food provision, CGSs deliver wide-ranging social, economic and environmental benefits including: building community relations, increasing food literacy, supporting public health and encouraging waste recycling. Urban green spaces also provide ecosystem services, such as nutrients and organic carbon storage.
As urban soils are subject to numerous diverse anthropogenic activities, they may have high levels of pollution, posing risks to human and ecological health. Despite this, data on soil health and CGSs remain fragmented, limiting the ability to assess safe growing areas and target interventions.

This project, in partnership with Hyde Park Source and FoodWise Leeds, aims to assess and enhance the impact of CGSs in Leeds through spatial and statistical analysis. Using open-source socio-demographic and environmental datasets, the project will evaluate existing data, improve accessibility, identify areas for soil health interventions and determine suitable sites for new CGSs.

By improving reproducible data integration and accessibility, this research will support evidence-based urban planning, reduce exposure to contaminated soils, and promote sustainable land management. Ultimately, the project aims to strengthen local food systems, inform policy and contribute to healthier and more resilient urban communities.

## SEEDS Dashboard - Setup and Usage 💻

Follow the steps below to prepare the data and run the SEEDS dashboard application.

### 1. Acquire the Raw Datasets
Obtain the datasets stored in the `Raw_Data` subfolder within the `Data` folder.

### 2. Process the Data
Run the 3 Jupyter Notebooks located in the `Data Processing` folder. These notebooks process the raw datasets and generate the `Processed_Data` datasets required to build and run the SEEDS dashboard app.

### 3. Install the Requirements
Install the required Python dependencies listed in the `requirements.txt` file.

### 4. Run the Dashboard

The application is organised into the following components:
* `layouts/` - contains the 4 files that define the layouts for the main application and each of its 3 tabs.
* `callbacks/` - contains 2 files responsible for the callbacks used for the "Existing Community Growing Schemes" and the "Imagining Future Growing Spaces" tabs.
* `functions/` - contains 2 files containing the functions required by the "Existing Community Growing Schemes" and the "Imagining Future Growing Spaces" tabs.
* `data_loading_n_config/` - contains the 2 files responsible for loading the data and configuring the data used across the different tabs of the app.
* `assets/` - contains the dashboard assets, including `styles.css` and the images used by the app.

### 5. Previous Dashboard Versions
Older and exploratory versions of the dashboard are stored in the `app_versions` folder. These versions are retained for reference and are not required to run the current dashboard.

## Data 📊

The `Raw_Data` (in `Data`) folder contains all the raw datasets required for the collecting, integrating and cleaning steps. The processed datasets can be found in the `Processed_Data` folder.

The following datasets were collected:

### Existing Community Growing Schemes Data
Variable | Description | Data Scale | File Type | Publication Year | Acquisition Date | Source
---------|-------------|------------|-----------|------------------|------------------|-------
Leeds Local Authority Boundaries | Polygon outlining Leeds LA boundaries | UK | Shapefile | 2024 | 20/04/2026 | [ONS, Local Authority Districts (May 2024) Boundaries UK BFE](https://geoportal.statistics.gov.uk/datasets/ons::local-authority-districts-may-2024-boundaries-uk-bfe-2/explore?location=53.495068%2C-0.354857%2C7)
Leeds Wards Boundaries | Polygons of wards| Leeds | Web scraped - CSV | 2018 | Live | [Leeds City Council](https://www.leeds.gov.uk/councillors-and-democracy/ward-maps)
Leeds Postcodes | Postcode centroids | UK | GeoPackage | 2026 | 07/05/2026 | [Ordnance Survey CodePointOpen](https://osdatahub.os.uk/data/downloads/open/CodePointOpen)
Urban Green Spaces | CGSs under the function 'Allotments Or Community Growing Spaces' | UK| GeoPackage | Updated every 6 months | 20/04/26 | [Ordnance Survey - Open Greenspace](https://osdatahub.os.uk/data/downloads/open/OpenGreenspace)
Urban Green Spaces | CGSs, see notebook table for API OSM keys and values | Chosen LA (Leeds) | Shapefile | Updated live | Live | [OpenStreetMap API](https://www.openstreetmap.org/#map=13/53.81089/-1.58512)
CGSs | CGSs from the 'Gardening' and 'Gardening and Animal Care' categories | Leeds | Web scraped - CSV | Updated live | Live | [Leeds Green Activity Provider (LGAP) Hyde Park Source](https://lgap.co.uk/)
Allotments | Allotments managed by council or associations  | Leeds | Web scraped - CSV | Not known | Live | [Leeds City Council](https://www.leeds.gov.uk/parks-and-countryside/grow-your-own/allotments)
Community Orchards | Orchards, location is postcode centroid | Leeds | Excel | 2026 | 23/07/2026 | [Fruit Works Co-operative](https://www.fruitworks.org.uk/)
Composting Collectives | Composting sites, location is postcode centroid | Leeds | Excel | 2026 | 25/06/2026 | [FoodWiseLeeds](https://foodwiseleeds.org/project/ccl/)


### Soil Health Data
Variable | Description | Data Scale | File Type | Data Type | Resolution | Publication Year | Acquisition Date | Source
---------|-------------|------------|-----------|-----------|------------|------------------|------------------|--------
Land Cover |  | SE Tile | GeoPackage | Vector | | 2024 | 05/05/2026 | [Digimap](https://digimap.edina.ac.uk/roam/map/environment)
Soil Texture |  | SE Tile | GeoPackage | Vector | | 2019 | 20/04/2026 | [Digimap](https://digimap.edina.ac.uk/geology)
Grain Size Class |  | SE Tile | GeoPackage | Vector | | 2019 | 05/05/2026 | [Digimap](https://digimap.edina.ac.uk/geology)
Soil pH | Topsoil (0-15cm) pH, based on 'Mean value for total soil nitrogen concentration in 2007 modelled by LCM_CLASS and CACO3_RANK' | UK | Shapefile | Raster | 1km x 1km | 2007 | 05/05/2026 | [UKSO](https://catalogue.ceh.ac.uk/documents/5dd624a9-55c9-4cc0-b366-d335991073c7)
Soil SOM | Topsoil (0-15 cm depth) organic matter content , estimated using the loss-on-ignition method (in %), based on 'Mean value for soil loss-on-ignition in 2007 modelled by LCM_CLASS and DOM_GRAIN' | UK | Shapefile | Raster | 1km x 1km | 2007 | 06/05/2026 | [UKSO](https://catalogue.ceh.ac.uk/documents/9e4451f8-23d3-40dc-9302-73e30ad3dd76)
Nickel (Ni) | Topsoil (5-20 cm depth) concentration in mg/kg,  | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Arsenic (As) | Topsoil (5-20 cm depth) concentration in mg/kg | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Lead (Pb) | Topsoil (5-20 cm depth) concentration in mg/kg | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Zirconium (Zi) | Topsoil (5-20 cm depth) concentration in mg/kg | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Selenium (Se) | Topsoil (5-20 cm depth) concentration in mg/kg | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Copper (Cu) | Topsoil (5-20 cm depth) concentration in mg/kg | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Cadmium (Cd) | Topsoil (5-20 cm depth) concentration in mg/kg | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Phosphorus (P2O5) | Topsoil (5-20 cm depth) concentration in w% | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Soil Health Thresholds | Author created dataset by combining thresholds from various sources. | UK | Excel | NA | NA |  |  | [Royal Horticultural Society pH](https://www.rhs.org.uk/soil-composts-mulches/ph-and-testing-soil), [Royal Horticultural Society SOM](https://www.rhs.org.uk/soil-composts-mulches/organic-matter-how-to-use-in-garden), [CL:AIRE](https://claire.co.uk/information-centre/water-and-land-library-wall.html?view=article&id=178:soil-guideline-values&catid=417&start=1), [Research Paper](https://www.sciencedirect.com/science/article/pii/S0269749121015426#bib137), [British Geological Survey (BGS)](https://www.bgs.ac.uk/geology-projects/applied-geochemistry/g-base-environmental-geochemistry/nbc-defra-project/#table)


### Development Opportunities Data
Variable | Description | Data Scale | File Type | Publication Year | Acquisition Date | Source
---------|-------------|------------|-----------|------------------|------------------|-------
Leeds LSOA boundaries | Polygons outlining Leeds LSOA boundaries | UK | GeoJSON | 2021 | 24/08/26 | [ONS](https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2021-boundaries-ew-bsc-v4-2/about)
Urban Green Spaces | CGSs under the OS Function 'Public Park Or Garden' | UK| GeoPackage | Updated every 6 months | 20/04/2026 | [Ordnance Survey - Open Greenspace](https://osdatahub.os.uk/data/downloads/open/OpenGreenspace)
Urban Green Spaces | Greenspaces, see notebook table for API OSM keys and values | Chosen LA (Leeds) | Shapefile | Updated live | Live | [OpenStreetMap API](https://www.openstreetmap.org/#map=13/53.81089/-1.58512)
Brownfields |   | Leeds | Web scraped - CSV | Not known | Live | [Leeds City Council](https://mapservices.leeds.gov.uk/arcgis/rest/services/Public/Strategic_Planning/MapServer/14)
Flood Risk | Likelihood of flooding. | UK | ShapeFile | 2010 | 20/04/26 | [Digimap](https://digimap.edina.ac.uk/geology)
PPFI and subdomains | Priority Places for Food Index and subdomains | UK | CSV | 2024 | 24/08/26 | [HASP](https://data.hasp.ac.uk/browser/dataset/5276/0)
IMD | Index of Multiple Deprivation | UK | Excel | 2025 | 24/08/26 | [UK Government](https://www.gov.uk/government/statistics/english-indices-of-deprivation-2025)

## Project Worflow ⚙️

### <ins> 1. Existing Community Growing Schemes - Processing </ins> 

This notebook `1-SEEDS_existingCGS_search.ipynb` involves collecting,  integrating and cleaning the raw data on existing CGSs. As datasets may have overlapping CGSs, several cleaning processes are included to avoid having duplicates that refer to the same CGS but have different names and geometries.
The notebook also collects and processes datasets related to Leeds such as the local authority boundaries, wards boundaries and postcode centroids.

The output files from this notebook are:
* `Existing_CGSs.gpkg`
* `Leeds_boundaries.gpkg`
* `leeds_postcodes.gpkg`
* `Leeds_Wards.gpkg`

### <ins> 2. Soil Health - Processing </ins> 

This notebook `2-SEEDS_soil_health.ipynb` involves collecting,  integrating and cleaning the raw data on soil health (land cover, soil texture, grain size class, heavy metals concentrations). The first cleaned dataset links the existing CGSs to their corresponding soil health metrics, while the second cleaned dataset contains soil health metrics for the entire Leeds local authority area

The output files from this notebook are:
* `soil_health_CGSs.csv`
* `soil_health.gpkg`


### <ins> 3. CGSs Development Opportunities - Processing </ins>

This notebook `3-SEEDS_potentialCGS_search.ipynb` involves collecting,  integrating and cleaning various raw datasets to build the dashboard planning tool, enabling to identify future potential CGS sites.

The output files from this notebook are:
* `TO_BE_CONTINUED.csv`


### <ins> 4. Dashboard Building </ins> 💻

The `seeds_app.py` file contains the main structure and layout of the dashboard. It is linked to the `assets` folder, which contains the `styles.css` stylesheet and the images required for the dashboard's styling and overall appearance.

