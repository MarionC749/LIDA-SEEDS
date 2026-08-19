#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 (Imagining Future Grwoing Spaces) - LAYOUT
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from dash import html, dcc
from functions.dvpt_helpers_Leaflet import dvpt_build_base_map


def dvpt_map_layout():
    
    return html.Div([
 
 # ------ Map and SideBar State Store ------
        dcc.Store(
            id= 'dvpt_map_state',
            #Initial state of map
            data={'active_layer': {
                    "soil_health": None,
                    "heavy_metals": None
                },  
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
                
                html.Div(
                    className= "dvpt_left_panel",
                    children= [
                    
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
                        
                            dcc.RadioItems(
                                id= {
                                    "type": "layer-selector",
                                    "dataset": "soil_health",
                                },
                                className= "dvpt_custom_checklist",
                                options=[
                                    {"label": "Land Cover", "value": "Land Cover"},
                                    {"label": "Soil Texture", "value": "Soil Texture"},
                                    {"label": "Grain Size Class", "value": "Grain Size Class"},
                                    {"label": "Soil pH", "value": "Soil pH"},
                                    {"label": "Soil Organic Matter (SOM)", "value": "Soil SOM"},
                                ],
                                value= None
                            ),
                        ]
                    ),
                    
                    html.Details(
                        className= "dvpt_layer_box",
                        children=[
                            html.Summary("Heavy Metals"),

                            dcc.RadioItems(
                                id= {
                                    "type": "layer-selector",
                                    "dataset": "heavy_metals",
                                },
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
                                value= None
                            )
                        ]
                    ),
                ]),
                

                # ------ Middle Map with Loading Indicator ------
                html.Div(
                    className= "dvpt_map_container",
                    children=[
                        #Loading indicator
                        dcc.Loading(
                            id="dvpt-map-loading",
                            className= "dvpt-map-loading",
                            type="circle",
                            overlay_style={"visibility": "visible", "opacity": 0.5},
                            parent_style={"width": "100%", "height": "100%"},
                            children=[
                            
                                html.Div(
                                    className= "dvpt_map_content",
                                    children=[
                                        dvpt_build_base_map(),
                                        #Map Legend
                                        html.Div(
                                            id="dvpt-map-legend",
                                            className="dvpt_map_legend"
                                        )
                                    ]
                                ),
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
                                children='Click a location to see details')
                    ]
                ),
            ]
        ),
    ])

