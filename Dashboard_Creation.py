#Experimenting with creating a dashboard using Plotly and Dash

import pandas as pd
import geopandas as gpd
import plotly
import plotly.express as px
import plotly.graph_objects as go


import dash
from dash import Dash, html, dcc, Input, Output, State

app = dash.Dash(__name__,
                suppress_callback_exceptions= True)

print("VERSION 8")

#------------------------------------------------------------------
#Prepare Data

#Import data
gdf = gpd.read_file("Data/Processed_Data/Existing_CGSs.gpkg")
print(gdf.columns)
#create unique identifier
gdf= gdf.reset_index().rename(columns={'index':'uid'})

#Ensure CRS is correct
gdf = gdf.to_crs(4326)

#Separate points and polygons
points = gdf[gdf.geometry.geom_type.isin(["Point", "MultiPoint"])]
polygons = gdf[gdf.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]

#Define a color to map points/polygons of the same type
#color are color-blindness friendly
types_colors= {"Allotments": "#D55E00",
               "Community Growing Projects": "#009E73",
               "Community Growing Spaces": "#56B4E9",
               "Community Orchard": "#CC79A7",
               "Urban Farms": "#F0E442" 
}

#Import Leeds outline
Leeds_outline = gpd.read_file("Data/Processed_Data/Leeds_boundaries.gpkg")
#Ensure CRS is correct
Leeds_outline = Leeds_outline.to_crs(4326)

#-------------------------------------------------------------
#App layout

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
        
        # ------ SideBar State ------
        dcc.Store(
            id= 'sidebar_state',
            data={'open': False, 
                  'uid': None, #store uid of clicked feature
                  'lat': None, #store coordinates of clicked feature
                  'lon': None}
        ),
    
        # ------ Main Layout ------
        html.Div(
            className="main-content",
            children= [
                
                # ------ Left Panel ------
                # Checklist component allows multiple layers selection simultaneously
                html.Div([
                    dcc.Checklist(
                        id="layer-selector",
                        className= "custom-checklist",
                        options=[
                            {"label": html.Span([
                                html.Img(src='/assets/allotments.png', style={'height': '40px', 'margin': '5px', 'verticalAlign': 'middle'}),
                                "Allotments"
                                ]), "value": "Allotments"},
                            {"label": html.Span([
                                html.Img(src='/assets/community_growing_projects.png', style={'height': '40px', 'margin': '5px', 'verticalAlign': 'middle'}),
                                "Community Growing Projects"
                                ]), "value": "Community Growing Projects"},
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
                        ],
                        value=["Allotments"], #initial value
                        ),
                    
                    html.Div(id="output_container")
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
                        html.Div(id='sidebar_content', 
                                children='Click a feature to see details')
                    ]
                )
            ]
        ),
        
        # ------ BOTTOM NAVBAR ------
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

#-------------------------------------------------------------------------------------------------------------
# ------ Map Creation ------


# Connect the Plotly map with Dash Components
# Only map, no sidebar
@app.callback(
    Output('output_container', 'children'),
    Output('Existing_CGSs_MAP', 'figure'),
    Input('layer-selector', 'value'),
    Input('sidebar_state', 'data') #for zoom and halo on clicked feature
)

def update_dashboard(slctd_layers, sidebar_state):
    
    # ------ Create basemap ------
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
    
    # ------ No layers selected - display empty map ------
    #add invisble dummy marker to ensure map shows
    if not slctd_layers:
        fig.add_trace(
            go.Scattermap(
                lat=[53.8],
                lon=[-1.55],
                mode="markers",
                marker=dict(size=1, opacity=0),
            )
        )
        return ("No layers selected", 
                fig)
              
                
    # ------ Layers Selection ------
    
    #If layers are selected, show points/polygons on base map
    #Filter data
    filtered_points= points[points['Type'].isin(slctd_layers)].copy()
    filtered_polygons= polygons[polygons['Type'].isin(slctd_layers)].copy()
    
    def hex_to_rgba(hex_color, alpha):
        hex_color= hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f'rgba({r},{g}, {b}, {alpha})'
    
    # POINTS
    #Add points (each category/layer having a different color on map)
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

    # POLYGONS
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
    
    # Add zoom + halo on clciked feature
    if sidebar_state and sidebar_state.get('open'):
        lat = sidebar_state.get('lat')
        lon = sidebar_state.get('lon')
        
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
    
    
    return f"{len(filtered_points)+len(filtered_polygons)} sites displayed", fig


#----------------------------------------------------------------------------------------------------------
# ------ Feature Clicking and Sidebar ------
    
# Open sidebar with feature information when clicked
# Zoom and create halo around feature when clicked

#Sidebar controller (open + close)
@app.callback(
    Output('sidebar_state', 'data'),
    Input('Existing_CGSs_MAP', 'clickData'),
    Input('close-sidebar-btn', 'n_clicks'),
    State('sidebar_state', 'data'),
    prevent_initial_call= True
    )
    
def update_sidebar_state(clickData, _close_clicks, state):
        
    ctx= dash.callback_context
    trigger= ctx.triggered[0]['prop_id'].split('.')[0]
    
    # CLOSE Button
    if trigger == 'close-sidebar-btn':
        return {'open': False, 
                'uid': None,
                'lat': None,
                'lon': None}
    
    # Map click
    if trigger == 'Existing_CGSs_MAP' and clickData:
        point = clickData['points'][0]
        uid, lat, lon = point.get('customdata') #store the uid and coordinates of clicked feature
        
        return {'open': True, 
                'uid': uid,
                'lat': lat,
                'lon': lon}
    
    return state


#Define function to show text only if cell contains a value
def info_show(label, value):
    if pd.isna(value) or value== "":
        return None
    return html.P([
        (f'{label}: '), str(value)
        ])


# Sidebar render callback
@app.callback(
    Output('sidebar_content', 'children'),
    Output('info-sidebar', 'className'),
    Input('sidebar_state', 'data')
)


def render_sidebar(state):
    
    if not state or not state['open']:
        return (
            'Click a feature to see details',
            'info-sidebar info-sidebar-collapsible'
        )
    
    uid= state['uid']
    row= gdf[gdf['uid'] == uid]
    
    if row.empty:
        return (
            'Feature not found',
            'info-sidebar info-sidebar-collapsible'
        )
    
    row = row.iloc[0]
    
    #Build Sidebar content
    sidebar_content = html.Div([
    
            #Build Sidebar Information Display
            html.Br(),
            html.H3(row['Name']),
            info_show("Type", row['Type']),
            html.Br(),
            info_show("Management", row['Management']),
            info_show("Organisation", row['Organisation_(LGAP)']),
            info_show("Activity Description", row['Activity_Description_(LGAP)']),
            html.Br(),
            html.H4('About the venue:'),
            info_show("Entry Conditions", row['Entry_Conditions']),
            info_show("Day and Time", row['Day_and_Time_(LGAP)']),
            info_show("Ongoing or set programs?", row['Ongoing_or_set_programs?_(LGAP)']),
            info_show("All year or seasonal?", row['All_year_or_seasonal?_(LGAP)']),
            info_show("Seasonal Details", row['Seasonal_details_(LGAP)']),
            info_show("One location?", row['one_location_(LGAP)']),
            info_show("Location Description", row['Location_Description_(LGAP)']),
            info_show("Postcode", row['Postcode_(FWC)']),
            info_show("Site Accessibility", row['Site_Accessibility_(LGAP)']),
            info_show("Toilets", row['Toilets_(LGAP)']),
            info_show("Indoor Space", row['Indoor_Space_(LGAP)']),
            info_show("Indoor Type", row['Indoor_Type_(LGAP)']),
            info_show("Transport support available", row['Transport_Support_(LGAP)']),
            html.Br(),
            info_show("Contact", row['Contact_name_(LGAP)']),
            info_show("Email", row['Email']),
            info_show("Phone number", row['Phone_Number_(LGAP)']),
            info_show("Website", row['Website_Link_(LGAP)']),
            ])
    
    return sidebar_content, 'info-sidebar info-sidebar-open'


# For local development, debug=True
if __name__ == '__main__':
    app.run(debug= False)