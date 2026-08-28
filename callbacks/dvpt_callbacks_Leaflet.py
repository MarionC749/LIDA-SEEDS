#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 (Imaginging Future Growing) - CALLBACKS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import dash
from dash import html, Input, Output, State
from shapely.geometry import Point
from dash import ALL
import dash_leaflet as dl


from functions.dvpt_helpers_Leaflet import(
    dvpt_add_layer,
    get_dvpt_sidebar_info,
)

from data_loading_n_config.load_data import(
    Leeds_postcodes,
)

from data_loading_n_config.config import (
    Dvpt_GUIDE_STEPS
)


#Function to create all the callbacks of the tab 2 (Imaginging Future Growing Spaces)
def create_dvpt_callbacks(app):

#----------------------------------------------------------------------------------------------------------------------------------------------        
    # ------ Map State Callbacks ------
    @app.callback(
        Output("dvpt_map_state", "data"),
        
        Output({"type": "layer-selector",
                "dataset": "soil_health"},
               "value"),
        
        Output({"type": "layer-selector",
                "dataset": "heavy_metals"},
                "value"),
        
        Output({"type": "layer-selector",
                        "dataset": "flood"},
                        "value"),
        
        Output({"type": "layer-selector",
                        "dataset": "demographics"},
                        "value"),
        
        Input({"type": "layer-selector",
               "dataset": ALL },
              "value"),
        
        Input("dvpt_postcode_search", "value"),
        
        Input("Future_CGSs_MAP", "clickData"),
        
        Input("dvpt_close_sidebar_btn", "n_clicks"),
        
        State("dvpt_map_state", "data"),
        prevent_initial_call= True
    )

    def dvpt_update_map_state(active_layer, #from layer RadioItems
                              postcode, #from postcode dropdown
                              click_data, #from map click
                              close_clicks, #from sidebar close button
                              dvpt_state): #stored state
        
        #Define default state
        dvpt_state= dvpt_state or {
            "active_layer": {
                "soil_health": None,
                "heavy_metals": None,
                "flood": None,
                "demographics": None,
                },
            "dvpt_postcode": None,
            "dvpt_sidebar": {"open": False},
            "dvpt_clicked_point": {"lat": None, "lon": None}
        }
            
        trigger= dash.ctx.triggered_id    
        
        # ------ LAYER SELECTION ------
        #Check if a layer selector was triggered
        if isinstance(trigger, dict):
            triggered_dataset= trigger["dataset"]
            
            #RadioItems values
            soil_layer= active_layer[0]
            heavy_metal_layer= active_layer[1]
            flood_layer= active_layer[2]
            demo_layer= active_layer[3]
            
            #If a soil health layer is selected
            if triggered_dataset == "soil_health":
                #Store layer
                dvpt_state["active_layer"]= {
                    "soil_health": soil_layer,
                    "heavy_metals": None,
                    "flood": None,
                    "demographics": None,
                }
                
                return(dvpt_state,
                       soil_layer,
                       None,
                       None,
                       None)
            
            #If heavy metal layer is selected
            elif triggered_dataset == "heavy_metals":
                #Store layer
                dvpt_state["active_layer"]= {
                    "soil_health": None,
                    "heavy_metals": heavy_metal_layer,
                    "flood": None,
                    "demographics": None,
                }
                
                return(dvpt_state,
                        None,
                        heavy_metal_layer,
                        None,
                        None)

            #If flood layer is selected
            elif triggered_dataset == "flood":
                #Store layer
                dvpt_state["active_layer"]= {
                    "soil_health": None,
                    "heavy_metals": None,
                    "flood": flood_layer,
                    "demographics": None,
                }
                
                return(dvpt_state,
                        None,
                        None,
                        flood_layer,
                        None)
                
            #If socio-demo layer is selected
            elif triggered_dataset == "demographics":
                #Store layer
                dvpt_state["active_layer"]= {
                    "soil_health": None,
                    "heavy_metals": None,
                    "flood": None,
                    "demographics": demo_layer,
                }
                
                return(dvpt_state,
                        None,
                        None,
                        None,
                        demo_layer)

            
        # ------ POSTCODE ------
        #If postcode dropdown is selected, store postocde
        elif trigger == 'dvpt_postcode_search':
            dvpt_state['dvpt_postcode'] = postcode
            
        # ------ MAP CLICK ------
        elif trigger == 'Future_CGSs_MAP':
            
            #Clicking map stores coordinates of location clicked and opens sidebar
            lat= click_data["latlng"]["lat"]
            lon= click_data["latlng"]["lng"]
            
            dvpt_state["dvpt_clicked_point"]= {
                "lat": lat,
                "lon": lon
            }
            
            dvpt_state['dvpt_sidebar']= {'open': True}
            
        # ------ CLOSE SIDEBAR BUTTON ------
        #Clicking button closes the sidebar and clears the clicked map location
        if trigger == 'dvpt_close_sidebar_btn':
            dvpt_state['dvpt_sidebar'] = {'open': False}
            dvpt_state['dvpt_clicked_point']= {
                        'lat':  None,
                        'lon':  None
                        }
        
        #Return updated state
        return (
            dvpt_state,
            active_layer[0],
            active_layer[1],
            active_layer[2],
            active_layer[3],
        )


#----------------------------------------------------------------------------------------------------------------------------------------------
    # ------ UPDATE MAP WITH SELECTED/ACTIVE LAYER AND ITS LEGEND ------

    @app.callback(
        Output('dvpt-active-map-layers', 'children'), #map displays selected layer
        Output('dvpt-map-legend', 'children'), #map displays corresponding legend to layer selected
        Input('dvpt_map_state', 'data'),
    )

    def dvpt_update_layers(dvpt_state):

        print("ACTIVE STATE:", dvpt_state)
        
        #Empty map and legend if no state
        if not dvpt_state:
            return [], None
        
        #Store geojson layers
        components= []
        #Default is no legend
        legend= None
        
        active_layer= dvpt_state.get("active_layer", {})
        
        #Loop through each selected dataset
        for dataset, layer in active_layer.items():
            
            #Skip if no layer selected
            if layer is None:
                continue
            
            #Create map layer and corresponding legend
            geojson, layer_legend = dvpt_add_layer(dataset= dataset, layer= layer)
                
            print("CREATED LAYER:", dataset, layer, type(geojson))
            
            if geojson is not None:
                components.append(geojson) #add layer to list
            
            #Store corresponding legend
            legend= layer_legend
        
        return components, legend
             
        
#----------------------------------------------------------------------------------------------------------------------------------------------

    # ------ Updating map view with postcode and clicked point Callback ------
    
    @app.callback(
        Output('Future_CGSs_MAP', 'viewport'), #update center and zoom of map
        Output('dvpt-click-marker-layer', 'children'), #update click marker position
        Input('dvpt_map_state', 'data'),
        prevent_initial_call= True
        )

    # ------ Priority Zoom System ------
    def dvpt_apply_zoom_logic(dvpt_state):
        
        #If no change in state state
        if not dvpt_state:
            return (dash.no_update, #no change in map
                    []) #no marker
        
        # First priority: clicked location
        
        #Retrieve clicked location coords
        clicked= dvpt_state["dvpt_clicked_point"]
        
        #Check sidebar is open and if coords is valid
        if (dvpt_state['dvpt_sidebar']['open'] 
            and clicked["lat"] is not None):
            
            lat= clicked["lat"]
            lon= clicked["lon"]
            
            #Create marker
            marker = dl.CircleMarker(
                id= "dvpt-click-marker",
                center=[lat, lon], #set coords to location clicked + shift a bit to fit sidebar
                radius= 8,
                color= "black",
                fill= False, #only keep outline of circle
                interactive= False,
            )
            
            
            #Move map to clicked point and zoom
            return(
                dict(center=[lat, lon + 0.015], zoom=14, transition="flyto"), #map centers and zooms (shift a bit to account for sideabar)
                [marker], #move marker to clicked position
            )
            
        
        # Second priority: postcode
        
        #Retrieve selected postcode
        postcode= dvpt_state["dvpt_postcode"]
        
        if postcode:
            row= Leeds_postcodes[Leeds_postcodes['Postcode'] == str(postcode)] #find postcode in GeoDataFrame
            if not row.empty:
                centroid= row.iloc[0].geometry.centroid #get postcode center
                #Move to postcode center and zoom
                return (
                    dict(center=[centroid.y, centroid.x], zoom=14, transition="flyto"), #map centers and zooms
                        [], #no clicked marker
                )
        
        #If no map click and no postcode, no map change
        return (dash.no_update, #no map change
                []) # no marker



#----------------------------------------------------------------------------------------------------------------------------------------------
    # # ------ Sidebar Tabs Callback ------

    #Check whether side should be open
    #Find the clicked map location
    #Ask helper function what information exists there
    #Build HTML content
    #Control whether sidebar is visible or hidden

    # Sidebar render callback
    @app.callback(
        Output('dvpt_sidebar_content', 'children'), #update sidebar content
        Output('dvpt_info_sidebar', 'className'), #change CSS class of sidebar container, open and close
        Input('dvpt_map_state', 'data'),
    )

    #Function creates sidebar
    def dvpt_render_sidebar(dvpt_state):
        sidebar= dvpt_state.get('dvpt_sidebar', {})

        #Check whether sidebar is open
        if not sidebar.get('open'):
            return (
                'Click a location to see details',
                'dvpt_info_sidebar dvpt_info_sidebar_collapsible', #keep sidebar collapsed
            )

        #Sidebar retrieves coords stored from map click
        clicked= dvpt_state.get('dvpt_clicked_point', {})
        
        #Check user has actually clicked map
        if clicked.get("lat") is None:
            return ("Click a location to see details",
                    "dvpt_info_sidebar dvpt_info_sidebar_collapsible", #keep sidebar collapsed
            )


        #Get active layer
        active_layer= dvpt_state.get('active_layer', {})
        
        #Check whether at least one layer has been selected
        layer_selected= any(
            bool(layer)
            for layer in active_layer.values()
        )
        
        #Start of sidebar content
        content= [html.H2("Location Information"),
                  html.Hr(),]
        
        #If no layer selected
        if not layer_selected:
            content.append(html.P("Select a layer on the left checklist to see location information."))
        
        #if layer is selected
        else:
            #Create Shapely Point (convert lat & lon to geometry)
            point= Point(clicked["lon"], clicked["lat"])
        
            #Call helper function
            # loops through checklist selected datasets
            # applies filter
            # finds polygons containing point
            # creates HTML components (sidebar content)
            sidebar_info= get_dvpt_sidebar_info(active_layer, point)
            
            #If information found
            if sidebar_info:
                content.extend(sidebar_info)
            #Layer selected, but no information at clicked location
            else:
                content.append(
                    html.P("No information available for this location."))
        
        return (content, 
                "dvpt_info_sidebar dvpt_info_sidebar_open",
                )




#----------------------------------------------------------------------------------------------------------------------------------------------
    # ------ Postcode Selection Dropdown Callback ------

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

#----------------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------
    # ------ PopUp Walkthrough Messages Callback ------
    @app.callback(
        Output("dvpt-guide-modal", "is_open"),
        Output("dvpt-guide-modal-title", "children"),
        Output("dvpt-guide-modal-body", "children"),
        Output("dvpt-guide-progress", "children"),
        Output("dvpt-guide-back", "style"),
        Output("dvpt-guide-next", "style"),
        Output("dvpt-guide-finish", "style"),
        Output("dvpt-guide-step", "data"),
        
        Input("dvpt-guide-next", "n_clicks"),
        Input("dvpt-guide-back", "n_clicks"),
        Input("dvpt-guide-finish", "n_clicks"),
        
        State("dvpt-guide-step", "data"),
        
        prevent_initial_call= False
    )
    
    def update_dvpt_guide(next_clicks, 
                          back_clicks,
                          finish_clicks,
                          step):
        
        #Identify which button was clicked
        ctx= dash.callback_context
        
        if ctx.triggered:
            button= ctx.triggered[0]["prop_id"].split(".")[0]
            
            if button == "dvpt-guide-next":
                step += 1
            
            elif button == "dvpt-guide-back":
                step -= 1
            
            elif button == "dvpt-guide-finish":
                return(
                    False, #close modal
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    step
                )
        
        #Keep step within valid range
        step= max(0, min(step, len(Dvpt_GUIDE_STEPS) -1))
        
        #Get current guide content
        current = Dvpt_GUIDE_STEPS[step]
        progress= f"Step {step + 1} of {len(Dvpt_GUIDE_STEPS)}"
        
        #Button visibility
        back_style = {"display": "none"} if step == 0 else {}
        
        next_style= {"display": "none"} if step == len(Dvpt_GUIDE_STEPS) - 1 else {}
        
        finish_style= {} if step == len(Dvpt_GUIDE_STEPS) - 1 else {"display": "none"}
        
        return(
            True,
            current["title"],
            current["body"],
            progress,
            back_style,
            next_style,
            finish_style,
            step
        )
