#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 1 (Existing CGS) - HELPER FUNCTIONS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from dash import html
import pandas as pd
import plotly.graph_objects as go
from matplotlib.colors import to_hex

from data_loading_n_config.config import types_colors
from data_loading_n_config.load_data import(
    Leeds_wards,
    Leeds_outline,
    Leeds_postcodes,
    soil_health_CGSs
)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ BASE MAP CREATION FUNCTION ------
def existing_build_base_map():
    fig= go.Figure()
    
    fig.update_layout(
        margin=dict(l=0, r=10, t=10, b=10),
        map=dict(
            style= "carto-positron",
            center={"lat": 53.83, "lon": -1.55},
            zoom= 9.8),
        showlegend= False,
        autosize= True,
        clickmode= 'event',
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
#------ POINTS MAPPING FUNCTION ------
#Add points (each category/layer having a different color on map)
def add_points(fig, filtered_points):
    if not filtered_points.empty:
        for category in filtered_points['Type'].unique():
            subset= filtered_points[filtered_points["Type"] == category]
            color= types_colors.get(category, 'gray')
            fig.add_trace(
                go.Scattermap(
                lat= subset.geometry.y,
                lon= subset.geometry.x,
                mode= "markers",
                marker=dict(size= 10, color= color, opacity=0.8),
                text= subset["Name"],
                hoverinfo= "text",
                customdata= list(zip(subset['uid'], subset.geometry.y, subset.geometry.x)), #used for sidebar info + zoom + halo
                )
            )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ POLYGONS MAPPING FUNCTION ------
def add_polygons(fig, filtered_polygons):
    for _, row in filtered_polygons.iterrows():
        geom= row.geometry
        color= types_colors.get(row['Type'], "gray")
        
        if geom.geom_type == "Polygon":
            polys= [geom]
        elif geom.geom_type== "MultiPolygon":
            polys= geom.geoms
        else:
            continue
        
        for poly in polys:
            x, y= poly.exterior.xy
            
            centroid= poly.centroid
            
            #Add the polygons
            fig.add_trace(
                go.Scattermap(
                    lon= list(x),
                    lat= list(y),
                    mode="lines",
                    fill= "toself",
                    line= dict(color=color, width=2),
                    fillcolor= hex_to_rgba(color, 0.4),
                    text= row["Name"],
                    hoverinfo="text",
                    customdata= [[row['uid'], centroid.y, centroid.x]]* len(x),
                )
            )
                
            #Add polygon centroid marker
            #Visually cleaner and avoids bias
            fig.add_trace(
                go.Scattermap(
                    lon= [centroid.x],
                    lat= [centroid.y],
                    mode="markers",
                    marker=dict(size= 10, color= color, opacity=0.8),
                                text= row["Name"],
                                hoverinfo= "text",
                                customdata= [[row['uid'], centroid.y, centroid.x]], #used for sidebar info + zoom + halo
                            )     
            )
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------ PRIORITY ZOOM SYSTEM FUNCTION ------
def existing_apply_zoom_logic(fig, postcode, sidebar):
    
    # 1- SIDEBAR (strongest)
    # Add zoom + halo on clicked feature
    if sidebar.get('open'):
        lat = sidebar.get('lat')
        lon = sidebar.get('lon')
        
        if lat is not None and lon is not None:
            
            #Zoom on clicked feature
            fig.update_layout(
                map=dict(
                center={'lat': lat, 'lon': lon},
                zoom= 14,
            ))
    
            #Halo on clicked feature
            fig.add_trace(
                go.Scattermap(
                    lat=[lat],
                    lon=[lon],
                    mode= 'markers',
                    marker= dict(size=50, 
                                 color='yellow', 
                                 opacity=0.5, 
                                 symbol='circle'
                                 ),
                    showlegend= False,
                    hoverinfo= 'skip',
                    )
                )
            
    # 2- POSTCODE (only if no sidebar)
     
    if postcode:
        row= Leeds_postcodes[Leeds_postcodes['Postcode'] == str(postcode)]
        if not row.empty:
            geom= row.iloc[0].geometry
            fig.update_layout(map=dict(center={'lat': geom.y, 'lon':geom.x}, zoom=12))

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
#------ COMMUNITY TAB FUNCTION ------
#Build 'Community tab' layout function
def build_community_tab(row):
    return html.Div([
    
            #Build Sidebar Information Display
            html.H3(row['Name']),
            html.Hr(),
            html.H4('🌱 Quick Information'),
            info_show("Type", row['Type']),
            info_show("Management", row['Management']),
            info_show("Organisation", row['Organisation']),
            html.Br(),
            html.Hr(),
            html.H4('🥕 Activity'),
            info_show("Description", row['Activity_Description']),
            html.Br(),
            html.Hr(),
            html.H4('📍 About the Venue'),
            info_show("Entry Conditions", row['Entry_Conditions']),
            info_show("Day and Time", row['Day_and_Time_(LGAP)']),
            info_show("Ongoing or set programs?", row['Ongoing_or_set_programs?_(LGAP)']),
            info_show("All year or seasonal?", row['All_year_or_seasonal?_(LGAP)']),
            info_show("Seasonal Details", row['Seasonal_details_(LGAP)']),
            info_show("One location?", row['one_location_(LGAP)']),
            info_show("Location Description", row['Location_Description']),
            info_show("Postcode", row['Postcode_(FWC)']),
            info_show("Site Accessibility", row['Site_Accessibility_(LGAP)']),
            info_show("Toilets", row['Toilets_(LGAP)']),
            info_show("Indoor Space", row['Indoor_Space_(LGAP)']),
            info_show("Indoor Type", row['Indoor_Type_(LGAP)']),
            info_show("Transport support available", row['Transport_Support_(LGAP)']),
            html.Br(),
            html.Hr(),
            html.H4('📞 Contact'),
            info_show("Contact", row['Contact_Name']),
            info_show("Email", row['Email']),
            info_show("Phone number", row['Phone_Number_(LGAP)']),
            info_show("Website", row['Website_Link']),
            info_show("Facebook", row['Facebook_(FWC)']),
            ])

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------ SOIL HEALTH TAB FUNCTION ------
#Build Soil tab layout function
def build_soil_tab(row):
    uid = row['uid']
    soil_rows = soil_health_CGSs[soil_health_CGSs['id'] == uid]
    
    if soil_rows.empty:
        return html.Div([
            html.H3('Soil Health'),
            html.Br(),
            html.P('No soil data available for this site.')
        ])
        
    land_cover= soil_rows[soil_rows['Soil_Metric'] == 'Land Cover']
    soil_parent= soil_rows[soil_rows['Soil_Metric'] == 'Soil Parent']
    soil_ph= soil_rows[soil_rows['Soil_Metric'] == 'Soil pH']
    soil_som= soil_rows[soil_rows['Soil_Metric'] == 'Soil SOM']
    metals = soil_rows[soil_rows['Soil_Metric'] == 'Heavy Metals']
    
    children= []
    
    if not land_cover.empty:
        children.extend([
            html.H4("Land Cover"),
            info_show("Type", land_cover.iloc[0]['Land_Cover_Type']),
            html.Hr(),
        ])
        
    if not soil_parent.empty:
            children.extend([
                html.H4("Soil Parent"),
                info_show("Soil Texture", soil_parent.iloc[0]['SOIL_GROUP']),
                info_show("Grain Size Class", soil_parent.iloc[0]['GEN_GRAIN']),
                html.Hr(),
            ])
    
    if not soil_ph.empty:
            children.extend([
                html.H4("Soil pH"),
                info_show("Value (2007)", soil_ph.iloc[0]['PH_07']),
                html.Hr(),
            ])
    
    if not soil_som.empty:
            children.extend([
                html.H4("Soil Organic Matter (SOM)"),
                info_show("Soil Loss-in-Ignition (2007)", f"{soil_som.iloc[0]['LOI_07']} %"),
                html.Hr(),
            ])
            
    if not metals.empty:
            children.extend([
                html.H4("Heavy Metals"),
                html.Ul([ #unordered list
                    html.Li( #list items
                        f"{row['HM_name']} ({row['metal']}):"
                        f"{row['value']} {row['HM_unit']}"
                    )
                    for _, row in metals.iterrows()
                ])
            ])
    
    return html.Div([
        html.H3(row['Name']),
        html.Hr(),
        *children
    ]) 