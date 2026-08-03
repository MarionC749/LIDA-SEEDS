#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 (Development Opportunities) - CALLBACKS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import dash
from dash import html, Input, Output, State
from shapely.geometry import Point
import plotly.graph_objects as go


from functions.dvpt_helpers import(
    dvpt_build_base_map,
    dvpt_add_layer,
    info_show,
    check_threshold
    
)

from data_loading_n_config.load_data import(
    Leeds_postcodes,
    soil_health,
    thresholds
)



def create_dvpt_callbacks(app):

    # ------ Map State Callbacks ------
    @app.callback(
        Output('dvpt_map_state', 'data'),
        Input('soil_health_selector', 'value'),
        Input('heavy_metals_selector', 'value'),
        Input('dvpt_postcode_search', 'value'),
        Input('Future_CGSs_MAP', 'clickData'),
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
            point_c = clickData['points'][0]
            
            dvpt_state['dvpt_sidebar']= {
                'open': True}
            dvpt_state['dvpt_clicked_point']= {
                'lat':  point_c["lat"],
                'lon':  point_c["lon"]
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
        Output('Future_CGSs_MAP', 'figure'),
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


