# Spatial and Ecological Evaluation of Developing Spaces (SEEDS) 🌱

## Abstract:
Global soil degradation poses a critical challenge to future food security, with the Food and Agriculture Organization of the United Nations (FAO) estimating that 33% of soils are already degraded and over 90% may be at risk by 2050. As pressure on agricultural systems intensifies, cities are increasingly recognised as sites for food production. Community Growing Schemes (CGSs), including community gardens, allotments and informal urban agriculture, represent a key strategy to diversify and localize food production and utilise underused urban land.

Often led by grassroots groups, CGSs improve food security by increasing access to healthy, sustainable and affordable food, particularly for food insecure populations. They strengthen resilience to supply chain disruptions and support more democratic, local food systems. 

Beyond food provision, CGSs deliver wide-ranging social, economic and environmental benefits including: building community relations, increasing food literacy, supporting public health and encouraging waste recycling. Urban green spaces also provide ecosystem services, such as nutrients and organic carbon storage.
As urban soils are subject to numerous diverse anthropogenic activities, they may have high levels of pollution, posing risks to human and ecological health. Despite this, data on soil health and CGSs remain fragmented, limiting the ability to assess safe growing areas and target interventions.

This project, in partnership with Hyde Park Source and FoodWise Leeds, aims to assess and enhance the impact of CGSs in Leeds through spatial and statistical analysis. Using open-source socio-demographic and environmental datasets, the project will evaluate existing data, improve accessibility, identify areas for soil health interventions and determine suitable sites for new CGSs.

By improving reproducible data integration and accessibility, this research will support evidence-based urban planning, reduce exposure to contaminated soils, and promote sustainable land management. Ultimately, the project aims to strengthen local food systems, inform policy and contribute to healthier and more resilient urban communities.

## Run Instructions 💻

Acquire the datasets stored in the `Raw_Data` subfolder in the `Data` folder.
1. Run the `1-SEEDS_existingCGS_search.ipynb`, to collect, integrate and process the existing CGSs data.
2. Run the `2-SEEDS_soil_health.ipynb`, to collect, integrate and process the soil health data.
3. 2. Run the `3-SEEDS_potentialCGS_search.ipynb`, to collect, integrate and process the data on CGSs development opportunities.

4. Assets for the dashboard such as the `styles.css` and images are stored in the `assets` folder.

7. Older and exploratory versions of the dashboard are stored in the `app_versions` folder.


## Data 📊

The `Raw_Data` (in `Data`) folder contains all the raw datasets required for the cleaning and scraping steps. The cleaned datasets can be found in the `Processed_Data`.

Different datasets were collected, cleaned and joined to have the following variables ready for modelling:


### Existing Community Growing Schemes Data
Variable | Description | Data Scale | File Type | Publication Year | Acquisition Date | Source
---------|-------------|------------|-----------|------------------|------------------|-------
Leeds Local Authority Boundaries | Polygon of Leeds LA boundaries | UK | Shapefile | 2024 | 20/04/2026 | [ONS, Local Authority Districts (May 2024) Boundaries UK BFE](https://geoportal.statistics.gov.uk/datasets/ons::local-authority-districts-may-2024-boundaries-uk-bfe-2/explore?location=53.495068%2C-0.354857%2C7)
Urban Green Spaces | Polygons of green spaces in Leeds | UK| Shapefile | Updated every 6 months | Live | [Ordnance Survey](https://osdatahub.os.uk/data/downloads/open/OpenGreenspace)
Urban Green Spaces | Polygons of green spaces in Leeds | Chosen LA (Leeds) | Shapefile | Updated live | Live | OpenStreetMap API
CGSs |  | Leeds | Webscraped - CSV | Updated live | Live | [ArcGIS Online - Leeds Green Activity Provider Hyde Park Source](https://www.arcgis.com/apps/mapviewer/index.html?layers=6afec02763ab4f87887939ed4d073c70)
Community Orchards |  | Leeds | Excel | 2026 | 23/07/2026 | Fruit Works Co-operative
Allotments | Allotments managed by council or associations  | Leeds | Webscraped - CSV | Not known | Live | [Leeds City Council](https://www.leeds.gov.uk/parks-and-countryside/grow-your-own/allotments)


### Soil Health Data
Variable | Description | Data Scale | File Type | Data Type | Resolution | Publication Year | Acquisition Date | Source
---------|-------------|------------|-----------|-----------|------------|------------------|------------------|--------
Land Cover |  | SE Tile | GeoPackage | Vector | | 2024 | 05/05/2026 | [Digimap](https://digimap.edina.ac.uk/roam/map/environment)
Soil Texture |  | SE Tile | GeoPackage | Vector | | 2019 | 20/04/2026 | [Digimap](https://digimap.edina.ac.uk/roam/map/environment)
Grain Size Class |  | SE Tile | GeoPackage | Vector | | 2019 | 05/05/2026 | [Digimap](https://digimap.edina.ac.uk/roam/map/environment)
Soil pH |  | UK | Shapefile | Raster | 1km x 1km | 2007 | 05/05/2026 | [UKSO](https://catalogue.ceh.ac.uk/documents/5dd624a9-55c9-4cc0-b366-d335991073c7)
Soil SOM |  | UK | Shapefile | Raster | 1km x 1km | 2007 | 06/05/2026 | [UKSO](https://catalogue.ceh.ac.uk/documents/9e4451f8-23d3-40dc-9302-73e30ad3dd76)
Nickel (Ni) |  | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Arsenic (As) |  | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Lead (Pb) |  | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Zirconium (Zi) |  | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Selenium (Se) |  | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Copper (Cu) |  | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Cadmium (Cd) |  | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)
Phosphorus (P2O5) |  | UK | GeoTIFF | Raster | 500m x 500m | 1978 to 2014 | 29/04/2026 | [UKSO](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html)


### Development Opportunities Data
Variable | Description | Data Scale | File Type | Publication Year | Acquisition Date | Source
---------|-------------|------------|-----------|------------------|------------------|-------



## Project Worflow ⚙️

### <ins> 1. Exploratory Data Analysis </ins> 📊

This notebook involves cleaning the raw footfall data and conducting exploratory data analysis, as well as creating visualizations which can be used for a dashboard.

The ouput files from this are:
* `footfall_map.html`
* `footfall_plots.html`

### <ins> 2. Clean data </ins> ✨

This notebook involves cleaning the raw footfall data and creating contextual temporal variables.

The ouput files from this are:
* `missing_days_counts.csv`
* `footfall_Mix_Clean.csv`

### <ins> 3. Data Scraping </ins> ⛏️

This notebook involves adding more contextual variables by scraping data for weather (with API), UK bank holidays, school holidays and covid times. The notebook ends by separating data for the 2019-2024 period and the 2025 period, and removing outliers in the 2019-2024 data using the Median Average Distance technique.

The ouput files from this are:
* `footfall_cleaned.csv` (all years)
* `footfall_cleaned_19_24.csv` (2019-2024)
* `footfall_cleaned_2025.csv` (just 2025)

### <ins> 4. Data Modelling </ins> 🤖

This notebook is the continuity of the data cleaning and scraping by modelling the footfall data. The model is selected, tuned and fitted using the footfall data between 2019 and 2024. The model is then used later on to predict the 2025 footfall, to allow Bradford City of Culture programem impact evaluation.

The below steps are followed:

#### 1) Model selection

The performance of four different machine learning models is tested using 10-fold cross validation. The models include:

* Linear regression
* Random Forest
* XGBoost
* Extra Trees Regressor

The outputs of the 10-fold cross validation with TimeSeriesSplit process are used to calculate the error metric scores associated with that model (averaged over all folds). The MAE, the MAPE, the R2 and the RMSE metrics are compared to find the model that will best fit the data.

**Conclusion:** Random Forest Regression is the best performing model.

#### 2) Model Evaluation

The performance of the Random Forest Regression model is tested, using a 80-20 test split with the chronological order of the data preserved using TimeSeriesSplit. The model performance is evaluated using the error metrics of MAE, MAPE, R2 and RMSE.

#### 3) Hyperparameter Tuning

Hyperparameter tuning is performed as it allows to find the best set of hyperparameters to maximise the model's efficiency and accuracy. 

#### 4) Fitting the Final Model

Using the optimal hyperparameters found during the tuning, the model is fitted again, this time using the whole dataset (no training and test splits).

#### 5) Feature Importance

The feature importance of the model predictor variables is investigated.

#### 6) Cross-Validated SHAP for Feature Importance

The feature importance of the model predictor variables is investigated using SHAP.

#### 7) Using Model Forecast to Evaluate Events

The final model is used to quantify the change in footfall that would otherwise been predicted in 2025.


## Other Work Included ℹ️

The `Other Notebooks` folder includes other notebooks which were not part of the modelling analysis but contributed to the project work.
* `Footfall Insights` folder contains 3 notebooks which were built to create various insights for different stakeholders (NCDO and Bradford 2025) on footfall but also demographics, dwell time and sales.
* `SARIMAX Attempt` folder contains the notebooks used to try building a SARIMA model to predict footfall in 2025. The analysis was not used in the end as the performance of the Random Forest Regression was better and more appropriate to incorporate footfall from different locations.
