#Experimenting with creating a dashboard using Plotly and Dash

import pandas as pd
import geopandas as gpd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc
import dash_bootstrap_components as dbc
import shapely
import dash_leaflet as dl
import json


import dash
from dash import Dash, html, dcc, Input, Output, State
from matplotlib.colors import to_hex
from shapely.geometry import Point

app = dash.Dash(__name__,
                suppress_callback_exceptions= True)
server= app.server



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 1- TAB 1 (Existing CGS) - LAYOUT
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
def existing_map_layout():
     return html.Div([
 
 # ------ Map and SideBar State Store ------
        dcc.Store(
            id= 'existing_map_state',
            data={'existing_layers': ['Allotments'], #initial state of map
                'existing_postcode': None,
                  'existing_sidebar': {
                      'open': False, 
                      'uid': None, #store uid of clicked feature
                      'lat': None, #store coordinates of clicked feature
                      'lon': None}
                  }
        ),
    
        # ------ Main Layout ------
        html.Div(
            className="main-content",
            children= [
                
                # ------ Left Panel ------
                
                html.Div([
                    
                    # ------ Postcode DropDown ------
                    dcc.Dropdown(
                        id='existing_postcode_search',
                        options= [],
                        placeholder= ('Search postcode...'),
                        searchable= True,
                        clearable= True,
                        style= {
                            'display': 'flex',
                            'justifyContent': 'center',
                            'width': '300px',
                            'padding': '10px'},
                    ),
                    
                    # ------ Layers Checklist ------
                    # Checklist component allows multiple layers selection simultaneously
                    dcc.Checklist(
                        id="existing_layer_selector",
                        className= "existing_custom_checklist",
                        options=[
                            {"label": html.Span([
                                html.Img(src='/assets/allotments.png', style={'height': '40px', 'margin': '5px', 'verticalAlign': 'middle'}),
                                "Allotments"
                                ]), "value": "Allotments"},
                            {"label": html.Span([
                                html.Img(src='/assets/community_growing_spaces.png', style={'height': '40px', 'margin': '5px', 'verticalAlign': 'middle'}),
                                "Community Growing Spaces"
                                ]), "value": "Community Growing Spaces"},
                            {"label": html.Span([
                                html.Img(src='/assets/orchard.png', style={'height': '40px', 'margin': '5px', 'verticalAlign': 'middle'}),
                                "Community Orchard"
                                ]), "value": "Community Orchard"},
                            {"label": html.Span([
                                html.Img(src='/assets/urban_farms.png', style={'height': '40px', 'margin': '5px', 'verticalAlign': 'middle'}),
                                "Urban Farms"
                                ]), "value": "Urban Farms"},
                            {"label": html.Span([
                                html.Img(src='/assets/compost.png', style={'height': '40px', 'margin': '5px', 'verticalAlign': 'middle'}),
                                "Composting Collective"
                                ]), "value": "Composting Collective"},
                        ],
                        value=["Allotments"], #initial value
                        ),
                    
                    html.Div(id="existing_output_container", style={
                        'textAlign': 'center',
                    }),
                    
                ]),
                

                # ------ Middle Map ------
                html.Div(
                    className= "existing_map_container",
                    children=[
                        #Empty placeholder where Plotly will display map
                        dcc.Graph(id='Existing_CGSs_MAP',
                                  style= {"height": "100%",
                                          "width": "100%"},
                                  config={'responsive': True},
                        )
                    ]
                ),
                
                # ------ SideBar ------
                html.Div(
                    id= 'existing_info_sidebar',
                    className= 'existing_info_sidebar existing_info_sidebar_collapsible',
                    children= [
                        html.Button(
                            'X',
                            id='existing_close_sidebar_btn',
                            n_clicks=0,
                            style={
                                'position': 'absolute',
                                'top': '10px',
                                'right': '10px',
                                'border': 'none',
                                'background': 'transparent',
                                'fontSize': '20px',
                                'cursor': 'pointer',
                                'zIndex': '9999',
                                'paddingTop': '10px'
                            }
                        ),
                        dbc.ButtonGroup(
                            [
                                dbc.Button(
                                    "Community",
                                    id="community-tab-btn",
                                    n_clicks= 0,
                                    className= "community-btn",
                                ),
                                dbc.Button(
                                    "Soil Health",
                                    id="soil-tab-btn",
                                    n_clicks= 0,
                                    className= "soil-btn",
                                ),
                            ],
                            className= "existing_sidebar_buttons",
                        ),
                       
                        html.Div(id='existing_sidebar_content', 
                                children='Click a feature to see details')
                    ]
                ),
                
                dcc.Store(
                    id="existing_sidebar_active_tab",
                    data="community"
                )
            ]
        ),
    ])


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 2- TAB 1 (Existing CGS) - IMPORTING THE DATA
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Prepare Data

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

#Define a color to map points/polygons of the same type
#color are color-blindness friendly
types_colors= {"Allotments": "#D55E00",
               "Community Growing Spaces": "#009E73",
               "Community Orchard": "#CC79A7",
               "Urban Farms": "#F0E442",
               "Composting Collective": "#0072B2"
}

#-------------------------------------------------------------
#Import Leeds outline
Leeds_outline = gpd.read_file("Data/Processed_Data/Leeds_boundaries.gpkg")
#Ensure CRS is correct
Leeds_outline = Leeds_outline.to_crs(4326)

#Import Leeds wards
Leeds_wards = gpd.read_file("Data/Processed_Data/Leeds_Wards.gpkg")
#Ensure CRS is correct
Leeds_wards = Leeds_wards.to_crs(4326)

#-------------------------------------------------------------
#Import Leeds postcode geometries
Leeds_postcodes = gpd.read_file("Data/Processed_Data/leeds_postcodes.gpkg")
#Ensure postcodes are strings
Leeds_postcodes['Postcode'] = Leeds_postcodes['Postcode'].astype(str)
#Ensure CRS is correct
Leeds_postcodes  = Leeds_postcodes.to_crs(4326)

#-------------------------------------------------------------
#Import soil health data per CGS
soil_health_CGSs = gpd.read_file("Data/Processed_Data/soil_health_CGSs.csv")
print(soil_health_CGSs.columns)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 3- TAB 1 (Existing CGS) - CALLBACKS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------ Map State Callbacks ------

@app.callback(
    Output('existing_map_state', 'data'),
    Input('existing_layer_selector', 'value'),
    Input('existing_postcode_search', 'value'),
    Input('Existing_CGSs_MAP', 'clickData'),
    Input('existing_close_sidebar_btn', 'n_clicks'),
    State('existing_map_state', 'data'),
    prevent_initial_call= True
)

def existing_update_map_state(existing_layers, existing_postcode, clickData, close_clicks, existing_state):
    
    existing_state= existing_state or {
        'existing_layers': [],
        'existing_postcode': None,
        'existing_sidebar': {
            'open': False,
            'uid': None,
            'lat': None,
            'lon': None
        }
    }

    ctx= dash.callback_context
    trigger= ctx.triggered[0]['prop_id'].split('.')[0]
    
    # ------ LAYER SELECTION ------
    if trigger == 'existing_layer_selector':
        existing_state['existing_layers']= existing_layers or []
        
    # ------ POSTCODE ------
    elif trigger == 'existing_postcode_search':
        existing_state['existing_postcode'] = existing_postcode
        
    # ------ MAP CLICK ------
    elif trigger == 'Existing_CGSs_MAP' and clickData:
        point = clickData['points'][0]
        uid, lat, lon = point.get('customdata') #store the uid and coordinates of clicked feature
        
        existing_state['existing_sidebar']= {
            'open': True, 
            'uid': uid,
            'lat': lat,
            'lon': lon}
        
    # ------ CLOSE SIDEBAR BUTTON ------
    if trigger == 'existing_close_sidebar_btn':
        existing_state['existing_sidebar'] = {
            'open': False, 
            'uid': None,
            'lat': None,
            'lon': None}
    
    return existing_state

#------------------------------------------------------------------
# ------ Map Creation ------

# Connect the Plotly map with Dash Components
# Only one callback builds the map
@app.callback(
    Output('Existing_CGSs_MAP', 'figure'),
    Output('existing_output_container', 'children'),
    Input('existing_map_state', 'data'),
)

def existing_update_dashboard(existing_state):
    
    #Define what the state of the map should be
    existing_state = existing_state or {}
    layers = existing_state.get('existing_layers', [])
    postcode= existing_state.get('existing_postcode')
    sidebar= existing_state.get('existing_sidebar', {})
    
    #Apply base map creation function
    fig= existing_build_base_map()
    
    #If layers are selected, show points/polygons on map
    #Filter data
    filtered_points= points[points['Type'].isin(layers)].copy()
    filtered_polygons= polygons[polygons['Type'].isin(layers)].copy()
    
    #Apply the different map creation functions
    add_points(fig, filtered_points)
    add_polygons(fig, filtered_polygons)
    
    existing_apply_zoom_logic(fig, postcode, sidebar)
    
    count= len(filtered_points) + len(filtered_polygons)
    
    return fig, f"{count} sites displayed"
    
#------------------------------------------------------------------
# Helper functions for map creation
    
#------ CREATE BASE MAP FUNCTION ------
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
    
#------ POINTS FUNCTION ------
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

#------ POLYGONS FUNCTION ------
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
    

# ------ Priority Zoom System ------
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
                zoom= 12,
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

#------------------------------------------------------------------
# ------ Sidebar Tabs Callback ------
@app.callback(
    Output('existing_sidebar_active_tab', 'data'),
    Input('community-tab-btn', 'n_clicks'),
    Input('soil-tab-btn', 'n_clicks'),
    prevent_initial_call= True,
)

def change_sidebar_tab(community_clicks, soil_clicks):
    ctx = dash.callback_context #contains info about current callback execution
    
    #By default show the community tab
    if not ctx.triggered:
        return "community"
    
    button= ctx.triggered_id
    
    if button == "community-tab-btn":
        return "community"
    
    elif button == "soil-tab-btn":
        return "soil"

# ------ Sidebar Tabs Button Style Callback ------
@app.callback(
    Output("community-tab-btn", "style"),
    Output("soil-tab-btn", "style"),
    Input('existing_sidebar_active_tab', 'data'),
)

#Change opacity of sidebar buttons depending on selection
def existing_update_button_style(active_tab):
    
    community_style= {
        "opacity": 1 if active_tab == "community" else "0.5",
    }
    soil_style= {
        "opacity": 1 if active_tab == "soil" else "0.5",
    }
    return community_style, soil_style


#------------------------------------------------------------------
# ------ Feature Clicking and Sidebar RENDER ------
    
# Open sidebar with feature information when clicked
# Zoom and create halo around feature when clicked

# Sidebar render callback
@app.callback(
    Output('existing_sidebar_content', 'children'),
    Output('existing_info_sidebar', 'className'),
    Input('existing_map_state', 'data'),
    Input('existing_sidebar_active_tab', 'data'),
)

#Create Opening/Closing logic
def existing_render_sidebar(existing_state, active_tab):
    
    sidebar= (existing_state or {}).get('existing_sidebar', {})
    
    if not sidebar.get('open'):
        return (
            'Click a feature to see details',
            'existing_info_sidebar existing_info_sidebar_collapsible'
        )
    
    uid= sidebar['uid']
    row= gdf[gdf['uid'] == uid]
    
    if row.empty:
        return (
            'Feature not found',
            'existing_info_sidebar existing_info_sidebar_collapsible'
        )
    
    row = row.iloc[0]
    
    #Build Sidebar content, depending on chosen tab
    if active_tab== "community":
        sidebar_content = build_community_tab(row)
    elif active_tab == "soil":
        sidebar_content= build_soil_tab(row)
    else:
        sidebar_content= html.Div("No information available")
    
    return sidebar_content, 'existing_info_sidebar existing_info_sidebar_open'


#Define function to display text in sidebar 
# only if cell contains a value
def info_show(label, value):
    if pd.isna(value) or value== "":
        return None
    return html.P([
        (f'{label}: '), str(value)
        ])

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
    

#------------------------------------------------------------------
# ------ Postcode Selection Dropdown ------

#Postcode dropdown callback
@app.callback(
    Output('existing_postcode_search', 'options'),
    Input('existing_postcode_search', 'search_value'),
)

def existing_update_postcodes(search):
    if not search:
        return dash.no_update
    
    pc_filter= Leeds_postcodes[Leeds_postcodes['Postcode'].str.contains(search, case=False, na=False)]['Postcode'].unique()
    
    return [
        {'label': pc, 'value': pc}
    for pc in pc_filter[:20]
    ]



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 4- TAB 2 (Development Opportunities) - LAYOUT
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def dvpt_map_layout():
    return html.Div([
 
 # ------ Map and SideBar State Store ------
        dcc.Store(
            id= 'dvpt_map_state',
            data={'dvpt_layers': [], #initial state of map
                'dvpt_postcode': None,
                'dvpt_sidebar': {
                    'open': False,
                },
                'dvpt_clicked_point': {
                    'lat': None,
                    'lon': None
                }
            }
        ),
    
        # ------ Main Layout ------
        html.Div(
            className="main-content",
            children= [
                
                # ------ Left Panel ------
                
                html.Div([
                    
                    # ------ Postcode DropDown ------
                    dcc.Dropdown(
                        id='dvpt_postcode_search',
                        options= [],
                        placeholder= ('Search postcode...'),
                        searchable= True,
                        clearable= True,
                        style= {
                            'display': 'flex',
                            'justifyContent': 'center',
                            'width': '300px',
                            'padding': '10px'},
                    ),
                    
                    # ------ Layers Checklist ------
                    
                    html.Details(
                        className= "dvpt_layer_box",
                        children=[
                            html.Summary("Soil Health"),
                        
                            dcc.Checklist(
                                id= "soil_health_selector",
                                className= "dvpt_custom_checklist",
                                options=[
                                    {"label": "Land Cover", "value": "Land Cover"},
                                    {"label": "Soil Texture", "value": "Soil Texture"},
                                    {"label": "Grain Size Class", "value": "Grain Size Class"},
                                    {"label": "Soil pH", "value": "Soil pH"},
                                    {"label": "Soil SOM", "value": "Soil SOM"},
                                ],
                                value= []
                            ),
                    
                            html.Details(
                                className= "dvpt_layer_box",
                                children=[
                                    html.Summary("Heavy Metals"),

                                    dcc.Checklist(
                                        id="heavy_metals_selector",
                                        className= "dvpt_custom_checklist",
                                        options=[
                                            {"label": "Nickel", "value": "Nickel"},
                                            {"label": "Arsenic", "value": "Arsenic"},
                                            {"label": "Lead", "value": "Lead"},
                                            {"label": "Zirconium", "value": "Zirconium"},
                                            {"label": "Selenium", "value": "Selenium"},
                                            {"label": "Copper", "value": "Copper"},
                                            {"label": "Cadmium", "value": "Cadmium"},
                                            {"label": "Phosphorus", "value": "Phosphorus"},
                                        ],
                                        value= [] #initial value
                                    )
                                ]
                            )
                        ]
                    ),
                    
                    html.Div(id="dvpt_output_container", style={
                        'textAlign': 'center',
                    }),
                    
                ]),
                

                # ------ Middle Map ------
                html.Div(
                    className= "dvpt_map_container",
                    children=[
                        #Empty placeholder where Plotly will display map
                        dl.Map(id='Future_CGSs_MAP',
                               style= {"height": "100%",
                                          "width": "100%"},
                               center= [53.83, "lon": -1.55],
                               zoom= 9.8,
                               children= [
                                   dl.TileLayer()
                                ]
                        )
                    ]
                ),
                
                # ------ SideBar ------
                html.Div(
                    id= 'dvpt_info_sidebar',
                    className= 'dvpt_info_sidebar dvpt_info_sidebar_collapsible',
                    children= [
                        html.Button(
                            'X',
                            id='dvpt_close_sidebar_btn',
                            n_clicks=0,
                            style={
                                'position': 'absolute',
                                'top': '10px',
                                'right': '10px',
                                'border': 'none',
                                'background': 'transparent',
                                'fontSize': '20px',
                                'cursor': 'pointer',
                                'zIndex': '9999',
                                'paddingTop': '10px'
                            }
                        ),
                        html.Div(id='dvpt_sidebar_content', 
                                children='Click a feature to see details')
                    ]
                ),
            ]
        ),
    ])


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 5- TAB 2 (Development Opportunities) - IMPORT DATA
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Import Leeds outline
Leeds_outline = gpd.read_file("Data/Processed_Data/Leeds_boundaries.gpkg")
#Ensure CRS is correct
Leeds_outline = Leeds_outline.to_crs(4326)

#-------------------------------------------------------------
#Import Leeds postcode geometries
Leeds_postcodes = gpd.read_file("Data/Processed_Data/leeds_postcodes.gpkg")
#Ensure postcodes are strings
Leeds_postcodes['Postcode'] = Leeds_postcodes['Postcode'].astype(str)
#Ensure CRS is correct
Leeds_postcodes  = Leeds_postcodes.to_crs(4326)

#-------------------------------------------------------------
#Import overall soil health data
soil_health = gpd.read_file("Data/Processed_Data/soil_health.gpkg")
soil_health = soil_health.to_crs(4326)

#-------------------------------------------------------------
#Import soil health thresholds
thresholds= pd.read_excel("Data/Raw_Data/Soil_health_Thresholds.xlsx")


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 6- TAB 2 (Development Opportunities) - COLOUR DICTIONARIES
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

land_cover_colours= {
    "Acid grassland": "lightcoral",
    "Arable": "darkorange",
    "Calcareous grassland": "red",
    "Coniferous woodland": "darkgreen",
    "Deciduous woodland": "lime",
    "Fen": "yellowgreen",
    "Freshwater": "dodgerblue",
    "Heather": "yellow",
    "Heather grassland": "gold",
    "Improve grassland": "darkgoldenrod",
    "Inland rock": "tan",
    "Neutral grassland": "palegreen",
    "Suburban": "mediumvioletred",
    "Urban": "mediumorchid", 
}

soil_texture_colours= {
    "LIGHT(SILTY) TO MEDIUM(SILTY) TO HEAVY": '#1f77b4',
    "MEDIUM TO HEAVY": "#ff7f0e",
    "LIGHT(SILTY) TO MEDIUM(SILTY)": "#2ca02c",
    "MEDIUM TO LIGHT(SILTY) TO HEAVY": "#d62728",
    "LIGHT(SANDY) TO MEDIUM(SANDY)": "#9467bd",
    "HEAVY TO MEDIUM": "#8c564b",
    "ALL": "#e377c2",
    "MEDIUM(SILTY)": "#7f7f7f",
    "MEDIUM": "#bcbd22",
    "MEDIUM TO LIGHT(SILTY)": "#17becf",
}

grain_size_colours= {
    "ARGILLIC - ARENACEOUS": '#377eb8',
    "ARENACEOUS": '#ff7f00',
    "MIXED (ARGILLIC-RUDACEOUS)": '#4daf4a',
    "ARENACEOUS - RUDACEOUS": '#f781bf',
    "ARGILLACEOUS": '#a65628',
    "PEAT": '#984ea3',
}

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 7- TAB 2 (Development Opportunities) - LAYER CONFIGURATION
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
LAYER_CONFIG= {
    
    "Land Cover": {
        "filters": {"Soil_Metric": "Land Cover"},
        "column": "Land_Cover_Type",
        "type": "categorical",
        "palette": land_cover_colours,
        "legend": "Land Cover"
    },
    
    "Soil Texture": {
            "filters": {"Soil_Metric": "Soil Parent"},
            "column": "SOIL_GROUP",
            "type": "categorical",
            "palette": soil_texture_colours,
            "legend": "Soil Texture",
        },
    
    "Grain Size Class": {
            "filters": {"Soil_Metric": "Soil Parent"},
            "column": "GEN_GRAIN",
            "type": "categorical",
            "palette": grain_size_colours,
            "legend": "Grain Size Class",
        },
    
    "Soil pH": {
                "filters": {"Soil_Metric": "Soil pH"},
                "column": "PH_07",
                "type": "continuous",
                "colourscale": "inferno_r",
                "legend": "Soil pH (2007)",
            },
    
    "Soil SOM": {
                "filters": {"Soil_Metric": "Soil SOM"},
                "column": "LOI_07",
                "type": "continuous",
                "colourscale": "inferno_r",
                "legend": "Soil Organic Matter (SOM)",
            },

    "Nickel": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "Ni"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Nickel (mg/kg)",
        },
    "Arsenic": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "As"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Arsenic (mg/kg)",
        },
    "Lead": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "Pb"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Lead (mg/kg)",
        },
    "Zirconium": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "Zr"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Zirconium (mg/kg)",
        },
    "Selenium": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "Se"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Selenium (mg/kg)",
        },
    "Copper": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "Cu"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Copper (mg/kg)",
        },
    "Cadmium": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "Cd"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Cadmium (mg/kg)",
        },
    "Phosphorus": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "P2O5"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Phosphorus (w%)",
            },

}

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 8- TAB 2 (Development Opportunities) - HELPER FUNCTIONS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#------ CONVERT to GEOJSON  ------
#Leaflet works with GeoJSON, not plotly traces
def gdf_to_geojson(gdf):
    return json.loads(gdf.to_json())

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
              

# #------ ADDING LAYERS FUNCTIONS ------

def dvpt_add_layer(fig, layer):
    
    print(f"Adding layer: {layer}")
    config = LAYER_CONFIG[layer]
    
    subset= soil_health.copy()
    
    for col, value in config["filters"].items():
        
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
# 9- TAB 2 (Development Opportunities) - CALLBACKS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------ Map State Callbacks ------
@app.callback(
    Output('dvpt_map_state', 'data'),
    Input('soil_health_selector', 'value'),
    Input('heavy_metals_selector', 'value'),
    Input('dvpt_postcode_search', 'value'),
    Input('Future_CGSs_MAP', 'click_lat_lng'),
    Input('dvpt_close_sidebar_btn', 'n_clicks'),
    State('dvpt_map_state', 'data'),
    prevent_initial_call= True
)

def dvpt_update_map_state(soil_layers,
                          metal_layers,
                          dvpt_postcode, 
                          clickData, 
                          close_clicks, 
                          dvpt_state):
    
    dvpt_state= dvpt_state or {
        'dvpt_layers': [],
        'dvpt_postcode': None,
        'dvpt_sidebar': {
            'open': False
        },
        'dvpt_clicked_point': {
            'lat': None,
            'lon': None 
        }
    }

    ctx= dash.callback_context
    trigger= ctx.triggered[0]['prop_id'].split('.')[0]
    
    # ------ LAYER SELECTION ------
    if trigger in [
        'soil_health_selector',
        'heavy_metals_selector'
    ]:
        dvpt_state['dvpt_layers']= (
            (soil_layers or []) +
            (metal_layers or [])
        )
        
    # ------ POSTCODE ------
    elif trigger == 'dvpt_postcode_search':
        dvpt_state['dvpt_postcode'] = dvpt_postcode
        
    # ------ MAP CLICK ------
    elif trigger == 'Future_CGSs_MAP' and clickData:
        
        #Clicking map stores coordinates of point clicked and opens sidebar
        
        dvpt_state['dvpt_sidebar']= {
            'open': True}
        dvpt_state['dvpt_clicked_point']= {
            'lat':  clickData["lat"],
            'lon':  clickData["lng"]
            }
        
    # ------ CLOSE SIDEBAR BUTTON ------
    if trigger == 'dvpt_close_sidebar_btn':
        dvpt_state['dvpt_sidebar'] = {
            'open': False
        }
        dvpt_state['dvpt_clicked_point']= {
                    'lat':  None,
                    'lon':  None
                    }
    
    return dvpt_state

# #------------------------------------------------------------------
# ------ Map Creation ------

# Connect the Plotly map with Dash Components
# Only one callback builds the map
@app.callback(
    Output('Future_CGSs_MAP', 'children'),
    Output('dvpt_output_container', 'children'),
    Input('dvpt_map_state', 'data'),
)

def dvpt_update_dashboard(dvpt_state):
    
#Define what the state of the map should be
    dvpt_state = dvpt_state or {}
    layers = dvpt_state.get('dvpt_layers', [])
    postcode= dvpt_state.get('dvpt_postcode')
    sidebar= dvpt_state.get('dvpt_sidebar', {})
    clicked_point= dvpt_state.get('dvpt_clicked_point', {})
    
    print("Dashboard layers:", layers)
    
    #Apply base map creation function
    fig= dvpt_build_base_map()
    
    #If layers are selected, show polygons on map
    #Apply the different map creation functions
    for layer in layers:
        dvpt_add_layer(fig, layer)
    
    dvpt_apply_zoom_logic(fig, postcode, sidebar, clicked_point)
    
    print("Total traces:", len(fig.data))
    
    return fig, f"{len(layers)} layers displayed"
    

# ------ Priority Zoom System ------
def dvpt_apply_zoom_logic(fig, postcode, sidebar, clicked_point):
    
    # 1- SIDEBAR (strongest)
    # Add zoom on clicked area
    if sidebar.get('open'):
        lat = clicked_point.get('lat')
        lon = clicked_point.get('lon')
        
        if lat is not None and lon is not None:
            
            #Zoom on clicked area (clicked point coordinates)
            fig.update_layout(
                map=dict(
                center={'lat': lat, 'lon': lon},
                zoom= 14,
            ))
            
            #Halo (black circle) on clicked point
            fig.add_trace(
                go.Scattermap(
                    lat= [lat],
                    lon= [lon],
                    mode= 'markers',
                    marker= dict(size=20, 
                                 color='black',
                                 symbol='circle',
                    ),
                    showlegend= False,
                    hoverinfo= 'skip',
                )
            )

            
    # 2- POSTCODE (only if no sidebar)
     
    elif postcode:
        row= Leeds_postcodes[Leeds_postcodes['Postcode'] == str(postcode)]
        if not row.empty:
            centroid= row.iloc[0].geometry.centroid
            fig.update_layout(map=dict(center={'lat': centroid.y, 'lon': centroid.x}, zoom=14))


# #------------------------------------------------------------------
# # ------ Sidebar Tabs Callback ------

# Sidebar render callback
@app.callback(
    Output('dvpt_sidebar_content', 'children'),
    Output('dvpt_info_sidebar', 'className'),
    Input('dvpt_map_state', 'data'),
)

def dvpt_render_sidebar(dvpt_state):
    
    print("DVPT STATE:", dvpt_state)
    
    sidebar= (dvpt_state or {}).get('dvpt_sidebar', {})
    print("SIDEBAR:", sidebar)
    
    if not sidebar.get('open'):
        return (
            'Click an area to see details',
            'dvpt_info_sidebar dvpt_info_sidebar_collapsible'
        )
    
    #Sidebar retrieves geometry of clicked point
    clicked= dvpt_state.get('dvpt_clicked_point', {})
    
    if (clicked.get("lat") is None or clicked.get("lon") is None):
        return (
            'No area selected',
            'dvpt_info_sidebar dvpt_info_sidebar_collapsible'
        )
        
    soil_health_layers= [
        "Land Cover",
        "Soil Texture",
        "Grain Size Class",
        "Soil pH",
        "Soil SOM",
        "Nickel",
        "Arsenic",
        "Lead",
        "Zirconium",
        "Selenium",
        "Copper",
        "Cadmium",
        "Phosphorus",
    ]
    
    selected_layers= dvpt_state.get('dvpt_layers', [])
    pt = Point(clicked["lon"], clicked["lat"])
    
    content= []
    
    #Sidebar title
    content.extend([
        html.H2("Location Information"),
        html.Br(),
    ])
    
    #Add soil health subtitle only if soil health layers selected
    if any(layer in selected_layers for layer in soil_health_layers):
        content.append(html.H3("🪱 Soil Health"))
        
    assessment_results= []
    
    # LAND COVER
    if "Land Cover" in selected_layers:
        land= soil_health[(soil_health["Soil_Metric"]== "Land Cover")]
        row= land[land.geometry.intersects(pt)]
        
        if not row.empty:
            content.extend([
                html.H4('Land Cover'),
                info_show(
                    'Type',
                    row.iloc[0]['Land_Cover_Type']
                )
            ])
    
    # Soil Parent: Soil Texture
    if "Soil Texture" in selected_layers:
        soilT= soil_health[(soil_health["Soil_Metric"]== "Soil Parent")]
        row= soilT[soilT.geometry.intersects(pt)]
        
        if not row.empty:
            content.extend([
                html.H4('Soil Parent'),
                info_show(
                    'Soil Texture',
                    row.iloc[0]['SOIL_GROUP']
                )
            ])
    
    # Soil Parent: Grain Size Class
    if "Grain Size Class" in selected_layers:
        grain = soil_health[(soil_health["Soil_Metric"]== "Soil Parent")]
        row= grain[grain.geometry.intersects(pt)]
        
        if not row.empty:
            content.extend([
                html.H4('Soil Parent'),
                info_show(
                    'Grain Size Class',
                    row.iloc[0]['GEN_GRAIN']
                )
            ])

    
    # Soil PH
    if "Soil pH" in selected_layers:
        ph = soil_health[soil_health["Soil_Metric"]== "Soil pH"]
        row= ph[ph.geometry.intersects(pt)]
            
        if not row.empty:
            value= row.iloc[0]['PH_07']
            
            content.extend([
                html.H4('Soil pH'),
                info_show(
                    'Soil pH',
                    f"{value:.2f}"
                )
            ])
            
            #Threshold check
            threshold_row= thresholds[(thresholds["Soil_Metric"]== "Soil pH")]
            if not threshold_row.empty:
                exceedances= check_threshold(value, threshold_row.iloc[0])
                if exceedances:
                    assessment_results.append(
                        f"Soil pH above: {', '.join(exceedances)}"
                    )
                
    # SOIL SOM
    if "Soil SOM" in selected_layers:
        som = soil_health[soil_health["Soil_Metric"]== "Soil SOM"]
        row= som[som.geometry.intersects(pt)]
            
        if not row.empty:
            content.extend([
                html.H4('Soil Organic Matter (SOM)'),
                info_show(
                    'Soil SOM',
                    f"{row.iloc[0]['LOI_07']:.2f}"
                )
            ])
        
    # HEAVY METALS
    metals_lookup= {
        "Nickel": "Ni",
        "Arsenic": "As",
        "Lead": "Pb",
        "Zirconium": "Zr",
        "Selenium": "Se",
        "Copper": "Cu",
        "Cadmium": "Cd",
        "Phosphorus": "P2O5",
    }

    
    selected_metals= [
        metals_lookup[layer]
        for layer in selected_layers
        if layer in metals_lookup
    ]
    
    if selected_metals:
        metals = soil_health[
            (soil_health["Soil_Metric"]== "Heavy Metals") &
            (soil_health["metal"].isin(selected_metals))]
        rows= metals[metals.geometry.intersects(pt)]
    
        if not rows.empty:
            content.append(html.H4('Heavy Metals'))
            content.append(
                html.Ul([
                    html.Li(
                        f"{row.HM_name}: {row.value:.2f} {row.HM_unit}"
                    )
                    for _, row in rows.iterrows()
                ])
            )
            
            #Threshold checks
            for _, row in rows.iterrows():
                threshold_row= thresholds[
                    (thresholds["Soil_Metric"]== "Heavy Metals")
                    &
                    (thresholds["metal"] == row["metal"])
                ]
                if not threshold_row.empty:
                    exceedances= check_threshold(row["value"], threshold_row.iloc[0])
                    if exceedances:
                        assessment_results.append(
                            f"{row.HM_name} above: {', '.join(exceedances)}"
                        )
    
    #Add Soil Health Threshold Assessment
    if assessment_results:
        content.extend([
            html.Hr(),
            html.H3("⚠️ Threshold Assessment"),
            html.Ul([
                html.Li(item) for item in assessment_results
            ]),
        ])
    else:
        content.append(
            html.P("No threshold exceedances detected")
        )
    
    
    #Default content
    if not content:
        content.append(html.P("No data available at this location"))
        
    return content, 'dvpt_info_sidebar dvpt_info_sidebar_open'


#------------------------------------------------------------------
# ------ Postcode Selection Dropdown ------

#Postcode dropdown callback
@app.callback(
    Output('dvpt_postcode_search', 'options'),
    Input('dvpt_postcode_search', 'search_value'),
)

def dvpt_update_postcodes(search):
    if not search:
        return dash.no_update
    
    pc_filter= Leeds_postcodes[Leeds_postcodes['Postcode'].str.contains(search, case=False, na=False)]['Postcode'].unique()
    
    return [
        {'label': pc, 'value': pc}
    for pc in pc_filter[:20]
    ]

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 10- OVERALL APP LAYOUT
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# APP LAYOUT

app.layout= html.Div(
    className= 'app-shell', 
    children=[
        
        # ------ TOP NAVBAR ------
        html.Header(
            className="navbar",
            children=[
                html.Div([
                    html.Div("SEEDS Dashboard", className="brand-title"),
                    html.Div("Spatial & Ecological Evaluation of Developing Spaces", className="brand-subtitle")
                ])
            ]
        ),
        
        # ------ TWO MAIN TABS ------
        dcc.Tabs(
            id= "main-tabs",
            className= "main-tabs",
            value="existing_CGS_map_tab",
            children= [
                dcc.Tab(
                    label= "Existing Community Growing Schemes",
                    value= "existing_CGS_map_tab",
                    children= existing_map_layout(),
                ),
                dcc.Tab(
                    label="Development Opportunities",
                    value= "dvlp_map_tab",
                    children= dvpt_map_layout(),
                ),
            ]
        ),
       
        # ------ FOOTER BOTTOM NAVBAR ------
        html.Footer(
            className='footer-navbar',
            children=[
                html.Img(
                    src='/assets/University-of-Leeds_logo.png',
                    style={'height': '120px'}
                    ),
                html.Img(
                    src='/assets/lida_logo.png',
                    style={'height': '40px'}
                )
            ]
        )
    ]
)



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# For local development, debug=True
# When deploying, debug=False
if __name__ == '__main__':
    app.run(debug= True)