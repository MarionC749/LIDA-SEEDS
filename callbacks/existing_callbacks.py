#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 1 (Existing CGS) - CALLBACKS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import dash
from dash import html, dcc
from dash import Input, Output, State


from functions.existing_helpers import(
    existing_build_base_map,
    add_points,
    add_polygons,
    existing_apply_zoom_logic,
    build_community_tab,
    build_soil_tab
)

from data_loading_n_config.load_data import(
    points,
    polygons,
    gdf,
    Leeds_postcodes
)



def create_existing_callbacks(app):
    
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
    
    #------------------------------------------------------------------
    # ------ Data Download Button ------
    @app.callback(
        Output("existing-download-data", "data"),
        Input("existing-CGSs-download-button", "n_clicks"),
        prevent_initial_call= True
    )
    
    def existing_download_data(n_clicks):
        return dcc.send_data_frame(
            gdf.to_csv,
            "Existing_CGSs.csv",
            index=False
        )
        