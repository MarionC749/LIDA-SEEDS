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
