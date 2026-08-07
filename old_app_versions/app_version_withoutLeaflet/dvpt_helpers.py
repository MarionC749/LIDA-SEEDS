#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 (Development Opportunities) - HELPER FUNCTIONS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import pandas as pd
import plotly.graph_objects as go
from dash import html


from data_loading_n_config.load_data import(
    Leeds_wards,
    Leeds_outline,
    soil_health,
)
from data_loading_n_config.config import(
    LAYER_CONFIG,
)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ CREATE BASE MAP FUNCTION ------
def dvpt_build_base_map():
    fig= go.Figure()
    
    fig.update_layout(
        margin=dict(l=0, r=10, t=10, b=10),
        map=dict(
            style= "carto-positron",
            center={"lat": 53.83, "lon": -1.55},
            zoom= 9.8),
        showlegend= False,
        autosize= True,
        clickmode= 'event+select',
        uirevision= 'keep' #avoid zoom reset every callback
    )
    
    #Add Leeds wards
    for ward in Leeds_wards.geometry:
        x, y = ward.exterior.xy
        fig.add_trace(
                go.Scattermap(
                    lat= list(y),
                    lon= list(x),
                    mode= "lines",
                    fill= None,
                    line= dict(color= 'dimgray', width=1),
                    hoverinfo= 'skip',
                )
            )

    #Add Leeds boundary
    geom_Leeds = Leeds_outline.geometry.iloc[0]
    x, y = geom_Leeds.exterior.xy
    fig.add_trace(
            go.Scattermap(
            lat= list(y),
            lon= list(x),
            mode= "lines",
            fill= None,
            line= dict(color= 'black', width=3),
            hoverinfo= 'skip',
            )
        )
    
    return fig
              
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------ ADDING LAYERS FUNCTIONS ------

def dvpt_add_layer(fig, layer):
    
    print(f"Adding layer: {layer}")
    config = LAYER_CONFIG[layer]
    
    subset= soil_health.copy()
    
    for col, value in config["filter"].items():
        
        subset= subset[subset[col] == value]
        
        print("Subset rows:", len(subset))
        print("Columns:", subset.columns.tolist())
    
    if config["type"] == "categorical":
        
        add_categorical_layer(
            fig,
            subset,
            config["column"],
            config["palette"],
            config["legend"],
        )
        
    else:
        add_numeric_layer(
            fig,
            subset,
            config["column"],
            config["colourscale"],
            config["legend"],
        )
    
    print("Figure traces after filtering:", len(fig.data))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------  COLOURING FUNCTION ------
#Function to get coloring (works with hex values, color names, or rgb)
def hex_to_rgba(colour, alpha):
    
    colour= colour.strip() if isinstance(colour, str) else colour
    
    #Handle plotly rgb() strings
    if isinstance(colour, str) and colour.strip().startswith("rgb"):
        
       values= colour.replace("rgba(", "").replace("rgb(", "").replace(")", "")
       values = values.split(",")
       
       r= int(float(values[0].strip()))
       g= int(float(values[1].strip()))
       b= int(float(values[2].strip()))
       
       return f"rgba({r}, {g}, {b}, {alpha})" 
    
    #Handle named colours
    if not colour.startswith("#"):
        colour= to_hex(colour)
        
    #Remove #
    colour= colour.lstrip('#')
    r, g, b = tuple(int(colour[i:i+2], 16) for i in (0, 2, 4))
    
    return f'rgba({r},{g}, {b}, {alpha})'

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ MAP CATEGORICAL LAYERS FUNCTION ------
#Function to map categorical layers
def add_categorical_layer(fig, #map
                          gdf, #geodataframe in EPSG:4326
                          column,
                          palette,
                          legend_title):
    
    categories= gdf[column].dropna().unique() #find all unique categories
    
    for category in categories:
        subset= gdf[gdf[column]== category]
        
        lons= []
        lats= []
        
        for _, row in subset.iterrows():
                
                    geom= row.geometry
                
                    if geom.geom_type == "Polygon":
                        polys= [geom]
                    elif geom.geom_type== "MultiPolygon":
                        polys= geom.geoms
                    else:
                        continue
        
                    for poly in polys:
                        x, y= poly.exterior.xy
                        
                        #Add polygon
                        lons.extend(list(x))
                        lats.extend(list(y))
                        
                        #Separator between polygons
                        lons.append(None)
                        lats.append(None)
        
        colour = palette.get(category, "gray")
            
        fig.add_trace(
            go.Scattermap(
            lon= lons,
            lat= lats,
            mode="lines",
            fill= "toself",
            line= dict(color= 'black', width=0.5),
            fillcolor= hex_to_rgba(colour, 0.3),
            name= category,
            legendgroup= legend_title,
            hovertemplate=(
                f"{legend_title}: {category}"
                "<extra></extra>"
            ),
            showlegend= True,
            )
         )


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ MAP NUMERICAL LAYERS FUNCTION ------
#Function to map numerical layers
def add_numeric_layer(fig, #map
                      gdf, #geodataframe in EPSG:4326
                      column, #numerical column
                      colourscale,
                      legend_title):
    
    #Avoid crash when NaN values
    gdf= gdf.dropna(subset=[column])
    
    vmin= gdf[column].min()
    vmax= gdf[column].max()
    
    #Loop through each row
    for _, row in gdf.iterrows():
        
        value= row[column]
        #Normalise value
        if vmax == vmin:
            scaled= 0.5 #if all values are the same, get middle color
        else:
            scaled= (value - vmin)/(vmax - vmin) #comvert values between 0 and 1
        
        #Look up colour corresponding to scaled value
        colour= pc.sample_colorscale(colourscale, scaled)[0]
        
        geom= row.geometry
        
        if geom.geom_type == "Polygon":
            polys= [geom]
        elif geom.geom_type== "MultiPolygon":
            polys= geom.geoms
        else:
            continue
        
        for poly in polys:
            x, y= poly.exterior.xy
            
            fig.add_trace(
                go.Scattermap(
                    lon= list(x),
                    lat= list(y),
                    mode="lines",
                    fill= "toself",
                    line= dict(color= 'black', width=1),
                    fillcolor= hex_to_rgba(colour, 0.3),
                    hovertemplate=(
                        f"{legend_title}: {value:.2f}"
                        "<extra></extra>"
                    ),
                )
            )
            
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ CHECK SOIL HEALTH THRESHOLD ------
def check_threshold(value, thresholds_row):
    
    #Store warning messages
    warnings= []
    
    for threshold_type in [
        "AHDB_threshold",
        "NBC_threshold",
        "C4SL_threshold",
        "SVG_threshold",
    ]:
        limit= thresholds_row[threshold_type]
        unit= thresholds_row["threshold_unit"]
        if pd.isna(unit):
            unit= ""
        
        if pd.notna(limit) and value > limit:
            warnings.append(f"{threshold_type.replace('_threshold', '')} ({limit} {unit})")
    
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

