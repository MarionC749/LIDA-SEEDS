#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 (Development Opportunities) - HELPER FUNCTIONS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import pandas as pd
import dash
from dash import html
import dash_leaflet as dl
import plotly.colors as pc
from dash_extensions.javascript import assign


from data_loading_n_config.load_data import(
    Leeds_wards,
    Leeds_outline,
)

from data_loading_n_config.config import(
    DVPT_DATASETS,
    LAYER_CONFIG,
    DVPT_SIDEBAR_CONFIG,
)


#Create Javascript function to read tooltip attributes
tooltip_function= assign("""
function(feature, layer){ 
    layer.bindTooltip(
        feature.properties.tooltip
    );
}
""")

#Create Javascript function to style each feature
categorical_style_function= assign("""
function(feature){
    return {
        color: "black",
        weight: 1,
        fillColor: feature.properties.colour,
        fillOpacity: 0.4
    };
}
""")

#Create Javascript function to style each feature
numeric_style_function= assign("""
function(feature){
    return {
        color: "black",
        weight: 1,
        fillColor: feature.properties.fillColor,
        fillOpacity: 0.4
    };
}
""")



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ CREATE BASE MAP FUNCTION ------
def dvpt_build_base_map():
    return dl.Map(
        id= "Future_CGSs_MAP",
        center= [53.83, -1.52],
        zoom= 11,
        style= {"width": "100%", "height": "100%"},
        children= [
            
            dl.TileLayer( #adds background map tiles from OpenStreetMap
                url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
                attribution='&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>'
                ), 
            
            #Add Leeds wards
            dl.GeoJSON(
                data= Leeds_wards.__geo_interface__,
                options={
                    "style": {
                        "color": "dimgray",
                        "weight": 1,
                        "fillOpacity": 0,
                    }
                },
                interactive= False
            ),
            
            #Add Leeds boundaries outline
            dl.GeoJSON(
                data= Leeds_outline.__geo_interface__,
                options= {
                    "style": {
                        "color": "black",
                        "weight": 3,
                        "fillOpacity": 0,
                    }
                },
                interactive= False
            ),
            
            #Create empty container for layer selected
            dl.LayerGroup(id= "dvpt-active-map-layers"),
            
            #Add point when user clicks location
            #opacity changes to 1 when location is clicked
            dl.CircleMarker(
                id= "dvpt-click-marker",
                center=[0, 0], #set coords somewhere outside map
                radius= 8,
                color= "black",
                fill= True,
                fillOpacity= 0, #dont fill circle, just show radius
                opacity= 1, #initially marker is invisible
                interactive= False,
            )
        ],
    )
              
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------ ADDING LAYER AND LEGEND FUNCTIONS ------
#Function to add a map layer to the basemap when selected from checklist, 
# with its corresponsing legend
def dvpt_add_layer(dataset, #name of dataset
                   layer # name of layer within that dataset to add
                   ):
    
    #Create copy of selected dataset
    subset= DVPT_DATASETS[dataset]["data"].copy()
    
    #Retrieve configuration settings for selected layer
    config = LAYER_CONFIG[dataset][layer]

    #Loop through the filter for that layer if one is defined
    for col, value in config.get("filter", {}).items():
        
        #Subset rows that match the filter (finding layer in dataset basically)
        subset= subset[subset[col] == value]
    
    #Map categorical layer
    if config["type"] == "categorical":
        
        return add_categorical_layer(
            subset,
            config["column"],
            config["palette"],
            config["legend"],
            f"{dataset}-{layer}",
        )

    #Map numerical layer
    else:
        return add_numeric_layer(
            subset,
            config["column"],
            config["colourscale"],
            config["legend"],
            f"{dataset}-{layer}",
        )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ MAP CATEGORICAL LAYERS FUNCTION ------
#Function to map one categorical layer (creates 1 GeoJSON + legend)

def add_categorical_layer(gdf, #geodataframe in EPSG:4326
                          column, #column containing categories
                          palette, #dictionary mapping categories to colours
                          legend_title, #text used in tooltip label
                          layer_id): 
    
    # ----- Create Map Layer -----
    
    gdf= gdf.copy()
    #Create colour column based on dict value
    gdf["colour"]= gdf[column].map(palette)
    #Create text for hover information
    gdf["tooltip"]= (legend_title + ": " + gdf[column].astype(str))
    
    geojson = dl.GeoJSON(
        id= layer_id,
        data= gdf.__geo_interface__,
        options= {
            "style": categorical_style_function,
            "onEachFeature": tooltip_function,
            "interactive": False
        },
    )
    
    # ----- Create Categorical Legend -----
    
    legend_items= []
    
    for label, colour in palette.items():
        legend_items.append(
            html.Div(
                children=[
                    html.Span(
                        className= "dvpt-cat-legend-box",
                        style={"backgroundColor": colour,
                               "opacity": 0.4}
                    ),
                    html.Span(
                        label,
                        className= "dvpt-cat-legend-label"
                    )
                ],
                className="dvpt-cat-legend-item"
            )
        )
    
    legend = html.Div(
        children=[
            html.H4(
                legend_title,
                className="dvpt-cat-legend-title"
            ),
            html.Div(
                children=legend_items,
                className="dvpt-cat-legend-items"
            )
        ],
        className="dvpt-cat-legend"
    )
    
    #Return map layer + legend 
    return geojson, legend


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ MAP NUMERICAL LAYERS FUNCTION ------

#Function to map one numerical layer (creates 1 GeoJSON + legend)

def add_numeric_layer(gdf, #geodataframe in EPSG:4326
                      column, #numerical column
                      colourscale,
                      legend_title,
                      layer_id):
    
    # ----- Preparation -----
    
    #Avoid crash when NaN values
    #Remove NaNs only in the column/layer being mapped
    gdf= gdf.dropna(subset=[column]).copy()
    
    if gdf.empty:
        return None, None
    
    #Get min and max values for the column
    vmin= gdf[column].min()
    vmax= gdf[column].max()
    
    #Calculate colours for each feature
    colours= []
    
    for value in gdf[column]:
        
        #Normalise value
        if vmax == vmin:
            scaled= 0.5 #if all values are the same, get middle color
        else:
            scaled= (value - vmin)/(vmax - vmin) #convert values between 0 and 1
        
        #Look up colour corresponding to scaled value
        colours.append(pc.sample_colorscale(colourscale, scaled)[0])
        
    #Add display properties to GeoDataFrame
    gdf["fillColor"] = colours
        
    #Add hover/tooltip info
    gdf["tooltip"] = (
        legend_title
        + ": "
        + gdf[column].round(2).astype(str)
    )
    
    # ----- Create Map Layer -----

    geojson= dl.GeoJSON(
        id= layer_id,
        data= gdf.__geo_interface__,
        options= {
            "style": numeric_style_function,
            "onEachFeature": tooltip_function,
            "interactive": False,
            },
    )
    
    # ----- Create Numerical Legend -----
    
    #Get colours from named plotly colourscale
    colour_list= pc.get_colorscale(colourscale)
    
    #Convert Plotly colourscale into CSS gradient
    gradient= ", ".join(
        f"{colour} {position * 100}%"
        for position, colour in colour_list
    )
    
    legend = html.Div(
        children=[
            html.H4(
                legend_title,
                className= "dvpt-num-legend-title"
            ),
            
            #Colour gradient
            html.Div(
                className= "dvpt-num-legend-gradient",
                style={"background": f"linear-gradient(to right, {gradient})"}
            ),
            #Min / max labels
            html.Div(
                children=[
                    html.Span(str(round(vmin, 2)), className="dvpt-num-legend-min"),
                    html.Span(str(round(vmax, 2)), className="dvpt-num-legend-max"),
                ],
                className="dvpt-num-legend-scale-labels"
            ),
        ],
        className="dvpt-num-legend"
    )
    
    # ----- Return Layer + Legend -----
    return geojson, legend
        
 
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ LOOKUP SOIL HEALTH and HEAVY METALS THRESHOLD ------
def get_threshold_row(dataset, layer, row):
    
    thresholds= DVPT_DATASETS["thresholds"]["data"]
    
    #Soil health threshold lookup
    if dataset == "soil_health":
        thresholds_match= thresholds[thresholds["Soil_Metric"]== layer]

    #Heavy metals thresholds lookup
    elif dataset == "heavy_metals":
        thresholds_match= thresholds[thresholds["HM_name"]== row["HM_name"]]

    else:
        return None
    
    if thresholds_match.empty:
        return None
    
    return thresholds_match.iloc[0]
    
#------ CHECK SOIL HEALTH THRESHOLD ------
def check_threshold(metric_name, value, thresholds_row):
    
    #Store warning messages
    warnings= []
    
    unit= thresholds_row["threshold_unit"]
    if pd.isna(unit):
        unit= ""
    
    threshold_names= {
        "RHS": "RHS (Royal Horticultural Society)",
        "NBC": " NBC (Normal Background Concentrations)",
        "C4SL": "C4SL (Category 4 Screening Levels)",
        "SGV": "SGV (Soil Guideline Values)",
    }
    
    #Upper thresholds
    for threshold_type in [
        "RHS_upper",
        "NBC_threshold",
        "C4SL_threshold",
        "SGV_threshold",
    ]:
        limit= thresholds_row[threshold_type]
        
        if pd.notna(limit) and value > limit:
            name= threshold_type.replace("_threshold", "").replace("_upper", "")
            display_name= threshold_names[name]
            
            warnings.append(
                f"{metric_name} is above the {limit}{unit} threshold established by the {display_name}")
    
    #Lower thresholds
    for threshold_type in [
            "RHS_lower",
        ]:
            limit= thresholds_row[threshold_type]
            
            if pd.notna(limit) and value < limit:
                name= threshold_type.replace("_lower", "")
                display_name= threshold_names[name]
                warnings.append(
                    f"{metric_name} is below the {limit}{unit} threshold established by the {display_name}")
    
    return warnings

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ DISPLAY SIDEBAR TEXT FUNCTION ------
#Define function to display text in sidebar 
# only if cell contains a value
def info_show(label, value):
    if pd.isna(value) or value== "":
        return None
    return html.P([
        (f'{label}: '), str(value)
        ])

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ CREATE SIDEBAR CONTENT FUNCTION ------

def get_dvpt_sidebar_info(active_layers, #dict of selected dataset and layer
                          clicked_point): #map location the user clicked
    
    content= []
    
    #Loop through every dataset currently has selected layers
    for dataset, layer in active_layers.items():
        #Skip dataset if no layer is selected
        if layer is None:
            continue
        
        #Retrieve GeoDataFrame for current dataset
        gdf= DVPT_DATASETS[dataset]["data"]
        #Get display name
        dataset_heading= DVPT_DATASETS[dataset]["display_name"]
        #Get sidebar config for this dataset
        config= DVPT_SIDEBAR_CONFIG.get(dataset, {})
        
        dataset_items= [] #store bullet point for this dataset
        threshold_warnings= [] #store all warnings for dataset
            
        #Skip if selected layer has no sidebar info in config
        if layer not in config:
            continue
            
        layer_config= config[layer]
            
        #Start with full dataset
        subset= gdf
            
        #Apply layer filter (layer only represents a subset of dataset) if one is defined
        for col, value in layer_config.get("filter", {}).items():
            subset= subset[subset[col] == value]
        
        #Find polygon that contains/intersects with clicked point
        match= subset[subset.geometry.intersects(clicked_point)]

        #If clicked point isnt inside any polygons of this layer, skip it
        if match.empty:
            continue
            
        for _, row in match.iterrows():
            value = row[layer_config["value_column"]]
                
            #Round numerical values
            if isinstance(value, (int, float)):
                value= round(value, 2)
                    
            #Add unit if available
            unit= ""
                
            if "unit_column" in layer_config:
                unit= row[layer_config["unit_column"]]
                    
                if pd.isna(unit):
                    unit= ""
                
            #Create bullet point
            text= f"{layer_config['title']}: {value}"
            if unit:
                text += f" {unit}"
                
            dataset_items.append(html.Li(text))
            
            #Add description if provided
            description_column= layer_config.get("description_column")
            if description_column:
                description= row[description_column]
                
                if pd.notna(description):
                    dataset_items.append(html.Li(f"Description: {description}"))
            
            #Add LSOA name if provided
            lsoa_column= layer_config.get("LSOA")
            if lsoa_column:
                lsoa= row[lsoa_column]
                            
                if pd.notna(lsoa):
                    dataset_items.append(html.Li(f"LSOA (Lower layer Super Output Area): {lsoa}"))
                
            #Threshold checking
            threshold_row= get_threshold_row(dataset, layer, row)
                
            if threshold_row is not None:
                warnings= check_threshold(layer_config["title"], value, threshold_row)
                threshold_warnings.extend(warnings)
                    
        #Add dataset information to sidebar
        if dataset_items:
            content.extend([
                html.Br(),
                html.H3(dataset_heading),
                html.Ul(dataset_items)
            ])
                    
        #Add threshold warnings
        if threshold_warnings:
            content.extend([
                html.H3("⚠️ Threshold Assessment"),
                html.Ul([
                    html.Li(warning)
                    for warning in threshold_warnings
                ])
            ])
                
    return content


