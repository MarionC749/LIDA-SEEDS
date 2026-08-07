#Experimenting with creating a dashboard using Plotly and Dash

import pandas as pd
import geopandas as gpd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


import dash
from dash import Dash, html, dcc, Input, Output, State

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
            data={'layers': ['Allotments'], #initial state of map
                'postcode': None,
                  'sidebar': {
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
                        id="layer-selector",
                        className= "custom-checklist",
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
                    
                    html.Div(id="output_container", style={
                        'textAlign': 'center',
                    }),
                    
                ]),
                

                # ------ Middle Map ------
                html.Div(
                    className= "map-container",
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
                    id= 'info-sidebar',
                    className= 'info-sidebar info-sidebar-collapsible',
                    children= [
                        html.Button(
                            'X',
                            id='close-sidebar-btn',
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
                            className= "sidebar-buttons",
                        ),
                       
                        html.Div(id='sidebar_content', 
                                children='Click a feature to see details')
                    ]
                ),
                
                dcc.Store(
                    id="sidebar_active_tab",
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
    Input('layer-selector', 'value'),
    Input('existing_postcode_search', 'value'),
    Input('Existing_CGSs_MAP', 'clickData'),
    Input('close-sidebar-btn', 'n_clicks'),
    State('existing_map_state', 'data'),
    prevent_initial_call= True
)

def update_map_state(layers, postcode, clickData, close_clicks, state):
    
    state= state or {
        'layers': [],
        'postcode': None,
        'sidebar': {
            'open': False,
            'uid': None,
            'lat': None,
            'lon': None
        }
    }

    ctx= dash.callback_context
    trigger= ctx.triggered[0]['prop_id'].split('.')[0]
    
    # ------ LAYER SELECTION ------
    if trigger == 'layer-selector':
        state['layers']= layers or []
        
    # ------ POSTCODE ------
    elif trigger == 'existing_postcode_search':
        state['postcode'] = postcode
        
    # ------ MAP CLICK ------
    elif trigger == 'Existing_CGSs_MAP' and clickData:
        point = clickData['points'][0]
        uid, lat, lon = point.get('customdata') #store the uid and coordinates of clicked feature
        
        state['sidebar']= {
            'open': True, 
            'uid': uid,
            'lat': lat,
            'lon': lon}
        
    # ------ CLOSE SIDEBAR BUTTON ------
    if trigger == 'close-sidebar-btn':
        state['sidebar'] = {
            'open': False, 
            'uid': None,
            'lat': None,
            'lon': None}
    
    return state

#------------------------------------------------------------------
# ------ Map Creation ------

# Connect the Plotly map with Dash Components
# Only one callback builds the map
@app.callback(
    Output('Existing_CGSs_MAP', 'figure'),
    Output('output_container', 'children'),
    Input('existing_map_state', 'data'),
)

def update_dashboard(state):
    
    #Define what the state of the map should be
    state = state or {}
    layers = state.get('layers', [])
    postcode= state.get('postcode')
    sidebar= state.get('sidebar', {})
    
    #Apply base map creation function
    fig= build_base_map()
    
    #If layers are selected, show points/polygons on map
    #Filter data
    filtered_points= points[points['Type'].isin(layers)].copy()
    filtered_polygons= polygons[polygons['Type'].isin(layers)].copy()
    
    #Apply the different map creation functions
    add_points(fig, filtered_points)
    add_polygons(fig, filtered_polygons)
    
    apply_zoom_logic(fig, postcode, sidebar)
    
    count= len(filtered_points) + len(filtered_polygons)
    
    return fig, f"{count} sites displayed"
    
#------------------------------------------------------------------
# Helper functions for map creation
    
#------ CREATE BASE MAP FUNCTION ------
def build_base_map():
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
              
  
#Function to get coloring
def hex_to_rgba(hex_color, alpha):
    hex_color= hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
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
                customdata= list(zip(subset['uid'], subset.geometry.y, subset.geometry.x)), #used for sidebar infor + zoom + halo
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
            
            centroid= geom.centroid
            
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
                    customdata= [(row['uid'], centroid.y, centroid.x)]* len(list(x)),
                )
            )
    

# ------ Priority Zoom System ------
def apply_zoom_logic(fig, postcode, sidebar):
    
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
                    marker= dict(size=40, 
                                 color='yellow', 
                                 opacity=0.5, 
                                 symbol='circle'),
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
    Output('sidebar_active_tab', 'data'),
    Input('community-tab-btn', 'n_clicks'),
    Input('soil-tab-btn', 'n_clicks'),
    prevent_initial_call= True
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
    Input('sidebar_active_tab', 'data'),
)

#Change opacity of sidebar buttons depending on selection
def update_button_style(active_tab):
    
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
    Output('sidebar_content', 'children'),
    Output('info-sidebar', 'className'),
    Input('existing_map_state', 'data'),
    Input('sidebar_active_tab', 'data')
)

#Create Opening/Closing logic
def render_sidebar(state, active_tab):
    
    sidebar= (state or {}).get('sidebar', {})
    
    if not sidebar.get('open'):
        return (
            'Click a feature to see details',
            'info-sidebar info-sidebar-collapsible'
        )
    
    uid= sidebar['uid']
    row= gdf[gdf['uid'] == uid]
    
    if row.empty:
        return (
            'Feature not found',
            'info-sidebar info-sidebar-collapsible'
        )
    
    row = row.iloc[0]
    
    #Build Sidebar content, depending on chosen tab
    if active_tab== "community":
        sidebar_content = build_community_tab(row)
    elif active_tab == "soil":
        sidebar_content= build_soil_tab(row)
    else:
        sidebar_content= html.Div("No information available")
    
    return sidebar_content, 'info-sidebar info-sidebar-open'


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

def update_postcodes(search):
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
            data={'layers': ['BLA'], #initial state of map
                'postcode': None,
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
                        id='dvlpt_postcode_search',
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
                        id="layer-selector",
                        className= "custom-checklist",
                        options=[
                        ],
                        value=["BLA"], #initial value
                        ),
                    
                    html.Div(id="output_container", style={
                        'textAlign': 'center',
                    }),
                    
                ]),
                

                # ------ Middle Map ------
                html.Div(
                    className= "map-container",
                    children=[
                        #Empty placeholder where Plotly will display map
                        dcc.Graph(id='Future_CGSs_MAP',
                                  style= {"height": "100%",
                                          "width": "100%"},
                                  config={'responsive': True},
                        )
                    ]
                ),
                
                # ------ SideBar ------
                html.Div(
                    id= 'info-sidebar',
                    className= 'info-sidebar info-sidebar-collapsible',
                    children= [
                        html.Button(
                            'X',
                            id='close-sidebar-btn',
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
                        html.Div(id='sidebar_content', 
                                children='Click a feature to see details')
                    ]
                ),
                
                dcc.Store(
                    id="sidebar_active_tab",
                    data="community"
                )
            ]
        ),
    ])



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 5- TAB 2 (Development Opportunities) - IMPORT DATA
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 6- TAB 2 (Development Opportunities) - CALLBACKS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 7- OVERALL APP LAYOUT
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
            value="existing-CGS-map-tab",
            children= [
                dcc.Tab(
                    label= "Existing Community Growing Schemes",
                    value= "existing-CGS-map-tab",
                    children= existing_map_layout(),
                ),
                dcc.Tab(
                    label="Development Opportunities",
                    value= "dvlp-map-tab",
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
    app.run(debug= False)