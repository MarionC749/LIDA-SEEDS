#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 (Development Opportunities) - LAYOUT
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from dash import html, dcc


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
                        dcc.Graph(id='Future_CGSs_MAP',
                                  style= {"height": "100%",
                                          "width": "100%"},
                                  config={'responsive': True},
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

