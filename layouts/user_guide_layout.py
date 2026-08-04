from dash import html, dcc
import dash_bootstrap_components as dbc


# ------ HELPER FUNCTION ------
def create_accordion_item(title, image, description):
    title_children= []
    
    if image is not None:
        title_children.append(
            html.Img(
                src= f"/assets/{image}",
                style={
                    "height": "30px",
                    "marginRight": "10px",
                    "verticalAlign": "middle"
                }
            ),
        )
    
    title_children.append(
        html.Span(title,
                  style= {"fontSize": "15px"}
        ),
    )
        
    return dbc.AccordionItem(
        children= [
            dcc.Markdown(description),
        ],
        title= html.Div(
            title_children,
            style= {
                "display": "flex",
                "alignItems": "center",  
            }
        )
    )

# ------ CREATE USER GUIDE LAYOUT FUNCTION ------
def create_user_guide_layout():
     return html.Div(
         className= "user_guide_container",
         children=[
             
             html.H1("How to use"),
             
             html.Br(),
             
             html.H2("Existing Community Growing Schemes"),
             
             dcc.Markdown("""
                #### What is this page?
            
                This page provides an overview of existing Community Growing Schemes (CGSs) across Leeds, making it easier to discover and explore local schemes. Users can view five different types of CGSs (allotments, community growing spaces, community orchards, urban farms and composting collectives) and select individual schemes to access more detailed information. Data on the map were last updated in September 2026.

                Clicking on a CGS opens a sidebar menu with two sections:
                * **Community**: Provides information about the scheme, including its location, activities, meeting times and places and contact details where available.
                * **Soil Health**: Summarises soil health information for the area covered by the CGS, helping users understand the conditions of the growing environment.
            
                #### What are Community Growing Schemes (CGS) ?
                Community Growing Schemes are shared spaces, often open to the public, where people collectively grow food and plants for community benefit and personal use rather than private profit.

                """),
             
             html.H4("Data Layer Guidance"),
             
             dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Allotments",
                        image= "allotments.png",
                        description= """
                        #### What is this layer?
                            
                        Allotments are individual plots of land rented by individuals to grow vegetables, fruits and other plants for personal or family consumption. In Leeds, allotments may be managed by the council or by independent associations.
                        
                        **Important note:** Allotments are not generally publicly accessible. Access is usually limited to plot holders and authorised visitors.

                        #### Where is the data from?
                        
                        Allotments were identified using [Ordnance Survey](https://osdatahub.os.uk/data/downloads/open/OpenGreenspace), [OpenStreetMap](https://www.openstreetmap.org/#map=13/53.81089/-1.58512), [Leeds Green Activity Provider (LGAP)](https://www.arcgis.com/apps/mapviewer/index.html?layers=6afec02763ab4f87887939ed4d073c70) and [Leeds City Council](https://www.leeds.gov.uk/parks-and-countryside/grow-your-own/allotments) datasets.
                        """
                    ),

                ],
                start_collapsed= True
             ),
             dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Community Growing Spaces",
                        image= "community_growing_spaces.png",
                        description= """
                        #### What is this layer?
                            
                        Community growing spaces are shared pieces of land where people come together to grow food and plants. These spaces may be managed by volunteers, community groups or professional organisations.

                        #### Where is the data from?
                        
                        Community growing spaces were identified using [Ordnance Survey]( https://osdatahub.os.uk/data/downloads/open/OpenGreenspace), [OpenStreetMap]( https://www.openstreetmap.org/#map=13/53.81089/-1.58512), and [Leeds Green Activity Provider (LGAP)](https://www.arcgis.com/apps/mapviewer/index.html?layers=6afec02763ab4f87887939ed4d073c70) datasets.
                        """
                    ),

                ],
                start_collapsed= True
             ),
             dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Community Orchards",
                        image= "orchards.png",
                        description= """
                        #### What is this layer?
                            
                        Community orchards are shared, publicly accessible collections of fruit and nut trees planted and cared for by communities.
                        
                        #### Where is the data from?
                        
                        Community orchards were identified using [OpenStreetMap]( https://www.openstreetmap.org/#map=13/53.81089/-1.58512) and [Fruit Works Co-Operative]( https://www.fruitworks.org.uk/) datasets.
                        """
                    ),

                ],
                start_collapsed= True
             ),
             dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Urban Farms",
                        image= "urban_farms.png",
                        description= """
                        #### What is this layer?
                            
                        Urban farms are spaces within the city where people grow food and may also raise animals. They will typically own their land or rent it from the council. They can support local food production, education and community engagement.
                        
                        #### Where is the data from?
                        
                        Urban farms were identified using [Leeds Green Activity Provider (LGAP)](https://www.arcgis.com/apps/mapviewer/index.html?layers=6afec02763ab4f87887939ed4d073c70) datasets.
                        """
                    ),

                ],
                start_collapsed= True
             ),
             dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Composting Collectives",
                        image= "compost.png",
                        description= """
                        #### What is this layer?
                            
                        Composting collectives are shared composting facilities, such as drop-off composting bins, that allow residents to reduce food waste by recycling food scraps. The compost produced provides a free source of nutrient-rich soil to grow food, flowers and other plants.
                        
                        #### Where is the data from?
                        
                        Urban farms were identified using [FoodWiseLeeds]( https://foodwiseleeds.org/project/ccl/) datasets.
                        """
                    ),

                ],
                start_collapsed= True
             ),
                        
             dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Basemap",
                        image= "basemap.png",
                        description= """
                        #### What is this layer?
                        
                        A background map that provides visual context for the CGSs and its surroundings. It shows roads, buildings, green spaces, and water in a simple map.
                        
                        #### How to use this information
                        
                        * Understanding surroundings: Identifying nearby streets, buildings, and green spaces around the CGS boundary.
                        * Orientation: Locating yourself within the dashboard before exploring other layers.
                        * Cross-referencing: Comparing layers with the area’s overall layout.

                        #### Where is the data from?
                        
                        This layer uses OpenStreetMap data, styled by Carto.
                        """
                    ),

                ],
                start_collapsed= True
             ),
             
             html.Br(),
             html.Br(),
             html.Hr(),  
             html.H2("Imagining Future Growing Spaces"),
                          
            dcc.Markdown("""
                        #### What is this page?
                        
                        This page provides a planning tool, allowing to imagine where growing spaces could be created in the future across Leeds. Users can select layers from a variety of categories (soil health, TBC) to get a general view of these over Leeds, and select specific locations to access more detailed information. Data on the map were last updated in September 2026.

            """),
                        
            html.H4("Data Layer Guidance"),
            html.Br(),
            html.H5("Soil Health"),
            
            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Land Cover",
                        image= None,
                        description= """
                            #### What is this layer?
                            
                            The land cover layer displays the different types of surfaces covering the land, such as woodland, grassland or urban areas. It includes 14 land cover classes in Leeds, based on the UKCEH Aggregate Class system.
                            
                            #### How to use this information?
                            
                            The layer helps to identify what is currently covering the land and understand the character of an area.
                                        
                            #### Where is the data from?
                            
                            The land cover data comes from [Digimap]( https://digimap.edina.ac.uk/roam/map/environment) datasets.
                                    
                        """
                    ),
            
                ],
                start_collapsed= True
            ),
            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Soil Texture",
                        image= None,
                        description= """
                            #### What is this layer?
                            
                            The soil texture layer displays the general texture of soils based on their mix of sand, silt and clay. Soils are grouped as light (sand/silt rich), medium (loams) or heavy (clay-rich). These groups are indicative and may vary locally.
                                        
                            #### How to use this information?
                            
                            The layer helps to understand soil conditions, such as drainage water retention and suitability for different types of plants and growing.
                                                    
                            #### Where is the data from?
                            
                            The soil texture data comes from [Digimap]( https://digimap.edina.ac.uk/roam/map/environment) datasets.
                                                
                        """
                    ),
                        
                ],
                start_collapsed= True
            ),
            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Grain Size Class",
                        image= None,
                        description= """
                            #### What is this layer?
                            
                            The grain size class layer displays the classes describing the particle size and composition of the underlying material parent material. The classes describe whether the material is mainly sand, clay and silt, gravel, pear or a mixture of these materials.
                                        
                            #### How to use this information?
                            
                            The layer helps to understand soil conditions, such as drainage water retention and suitability for different types of plants and growing.
                                                    
                            #### Where is the data from?
                            
                            The grain size class data comes from [Digimap]( https://digimap.edina.ac.uk/roam/map/environment) datasets.                 
                        """
                    ),
                        
                ],
                start_collapsed= True
            ),
            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Soil pH",
                        image= None,
                        description= """
                            #### What is this layer?
                            
                            The soil pH layer displays the topsoil pH (0-15cm) which shows how acidic or alkaline the top layer of soil is. The values are estimated from a 2007 model using information about soil type and calcium carbonate content.
                                        
                            #### How to use this information?
                            
                            This layer helps indicate how suitable the soil may be for different plants and growing conditions.
                                                    
                            #### Where is the data from?
                            
                            The soil pH data comes from [UK Soil Observatory]( https://catalogue.ceh.ac.uk/documents/5dd624a9-55c9-4cc0-b366-d335991073c7) datasets.                  
                        """
                    ),
                        
                ],
                start_collapsed= True
            ),
            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Soil SOM",
                        image= None,
                        description= """
                            #### What is this layer?
                            
                            The soil SOM layer displays the topsoil organic matter (0-15 cm) which shows the amount of organic material in the top layer of the soil. High organic matter can improve soil health by helping it hold water and nutrients, supporting plant growth. The values are estimated from a 2007 model using information about soil type and texture.
                                        
                            #### How to use this information?
                                                    
                            #### Where is the data from?
                            
                            The soil SOM data comes from [UK Soil Observatory]( https://catalogue.ceh.ac.uk/documents/5dd624a9-55c9-4cc0-b366-d335991073c7) datasets.               
                        """
                    ),
                        
                ],
                start_collapsed= True
            ),
            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Heavy Metals",
                        image= None,
                        description= """
                            #### What is this layer?
                            
                            The Heavy Metals layers display the concentrations of different metals found in the topsoil (5-20 cm). The layers include eight metals: nickel, arsenic, lead, zirconium, selenium, copper, cadmium and phosphorus.
                                       
                            #### How to use this information?
                            
                            This information helps understand soil conditions and identify areas where metal concentrations may affect land use and growing suitability.
                                                    
                            #### Where is the data from?
                            
                            The heavy metals data comes from [UK Soil Observatory](https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html) datasets.              
                        """
                    ),
                        
                ],
                start_collapsed= True
            ),
            html.Br(),
            html.Br(),
            html.Hr(),  
            html.H2("References"),
            dcc.Markdown("""
                        For more information on data collection and the dashboard building, refer to the [project's GitHub repository](https://github.com/MarionC749/LIDA-SEEDS).
            """),
         ]
     )

