#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# OVERALL APP LAYOUT
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from dash import html, dcc

from layouts.existing_layout import existing_map_layout
from layouts.dvpt_layout_Leaflet import dvpt_map_layout
from layouts.user_guide_layout import create_user_guide_layout

def create_main_layout():
    return html.Div(
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
            
            # ------ THREE MAIN TABS ------
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
                        label="Imagining Future Growing Spaces",
                        value= "dvlp_map_tab",
                        children= dvpt_map_layout(),
                    ),
                    dcc.Tab(
                        label="User Guide",
                        value= "user_guide_tab",
                        children= [
                            html.Div(
                                className= "user-guide-tab",
                                children= create_user_guide_layout(),
                            )
                        ]
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