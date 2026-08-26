#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 1 (Existing CGS) - LAYOUT
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import dash_bootstrap_components as dbc
from dash import html, dcc
 
 
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
                
                html.Div(
                    className= "existing_left_panel",
                    children= [
                    
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
                        
                        # ------ Loading Message ------
                        html.P("Please note: Loading times may vary. Please allow a few moments for the map to update.", className="existing-loading-time-message"),
                        
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
                                    "Community Orchards"
                                    ]), "value": "Community Orchard"},
                                {"label": html.Span([
                                    html.Img(src='/assets/urban_farms.png', style={'height': '40px', 'margin': '5px', 'verticalAlign': 'middle'}),
                                    "Urban Farms"
                                    ]), "value": "Urban Farms"},
                                {"label": html.Span([
                                    html.Img(src='/assets/compost.png', style={'height': '40px', 'margin': '5px', 'verticalAlign': 'middle'}),
                                    "Composting Collectives"
                                    ]), "value": "Composting Collective"},
                            ],
                            value=["Allotments"], #initial value
                            ),
                        
                        html.Div(id="existing_output_container", style={
                            'textAlign': 'center',
                        }),
                        
                        # ------ Download Data Button ------
                        dcc.Download(id="existing-download-data"),
                        html.Button(
                            "Download the data",
                            id= "existing-CGSs-download-button",
                            className="existing-CGSs-download-button"
                        ),
                    ]
                ),
                

                # ------ Middle Map ------
                
                html.Div(
                    className= "existing_map_container",
                    children=[
                        #Loading indicator
                        dcc.Loading(
                            id="existing-map-loading",
                            className= "existing-map-loading",
                            type="circle",
                            overlay_style={"visibility": "visible", "opacity": 0.5},
                            parent_style={"width": "100%", "height": "100%"},
                            children=[
                            
                                #Empty placeholder where Plotly will display map
                                dcc.Graph(
                                    id='Existing_CGSs_MAP',
                                    className= "existing-map-graph",
                                    style= {"height": "100%", "width": "100%"},
                                    config={'responsive': True},
                                )
                            ]
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
        
        # ------ Tab Walkthrough PopUps Messages ------
        dcc.Store(
            id= "existing-guide-step",
            data=0
        ),
        
        dbc.Modal([
            dbc.ModalHeader(
                dbc.ModalTitle(
                    id="existing-guide-modal-title"
                )
            ),
            
            dbc.ModalBody(
                id="existing-guide-modal-body"
            ),
            
            dbc.ModalFooter([
                
                #Back Button
                html.Div(
                    dbc.Button(
                        "Back",
                        id= "existing-guide-back",
                        n_clicks=0,
                    ),
                    className= "existing-guide-footer-back"
                ),
                    
                #Progress Indicator
                html.Div(
                    html.Small(
                        id="existing-guide-progress",
                        className= "existing-guide-progress"
                    ),
                    className= "existing-guide-footer-progress"
                ),
                    
                #Next and Finish Buttons
                html.Div([
                    dbc.Button(
                        "Next",
                        id="existing-guide-next",
                        n_clicks=0
                    ),
                    dbc.Button(
                        "Finish",
                        id="existing-guide-finish",
                        n_clicks=0,
                        style={"display": "none"}
                    ),
                ],
                className="existing-guide-footer-nextfinish"
                ),

            ],
            className="existing-guide-footer"
            )
        
        ],
        id="existing-guide-modal",
        className= "existing-guide-modal",
        is_open= True,
        centered= True,
        backdrop= "static",
    )
])
