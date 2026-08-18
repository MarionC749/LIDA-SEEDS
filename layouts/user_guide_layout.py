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
        children= [description],
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
                #### What is this page ?
            
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
                        description= html.Div([
                            html.H4("What is this layer ?"),
                            
                            html.P("Allotments are individual plots of land rented by individuals to grow vegetables, fruits and other plants for personal or family consumption. In Leeds, allotments may be managed by the council or by independent associations."
                            ),
                             html.P("Important note: Allotments are not generally publicly accessible. Access is usually limited to plot holders and authorised visitors."
                            ),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "Allotments were identified using ",
                                html.A(
                                    "Ordnance Survey",
                                    href="https://osdatahub.os.uk/data/downloads/open/OpenGreenspace",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                ", ",
                                html.A(
                                    "OpenStreetMap",
                                    href="https://www.openstreetmap.org/#map=13/53.81089/-1.58512",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                ", ",
                                html.A(
                                    "Leeds Green Activity Provider (LGAP)",
                                    href="https://lgap.co.uk/",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " and ",
                                html.A(
                                    "Leeds City Council",
                                    href="https://www.leeds.gov.uk/parks-and-countryside/grow-your-own/allotments",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " datasets."
                            ]),
                        ])
                    )
                ],
                start_collapsed= True
             ),
            
            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Community Growing Spaces",
                        image= "community_growing_spaces.png",
                        description= html.Div([
                            html.H4("What is this layer ?"),
                            
                            html.P("Community growing spaces are shared pieces of land where people come together to grow food and plants. These spaces may be managed by volunteers, community groups or professional organisations."
                            ),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "Community growing spaces were identified using ",
                                html.A(
                                    "Ordnance Survey",
                                    href="https://osdatahub.os.uk/data/downloads/open/OpenGreenspace",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                ", ",
                                html.A(
                                    "OpenStreetMap",
                                    href="https://www.openstreetmap.org/#map=13/53.81089/-1.58512",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " and ",
                                html.A(
                                    "Leeds Green Activity Provider (LGAP)",
                                    href="https://lgap.co.uk/",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " datasets."
                            ]),
                        ])
                    )
                ],
                start_collapsed= True
             ),

            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Community Orchards",
                        image= "orchards.png",
                        description= html.Div([
                            html.H4("What is this layer ?"),
                            
                            html.P("Community orchards are shared, publicly accessible collections of fruit and nut trees planted and cared for by communities."
                            ),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "Community orchards were identified using ",
                                html.A(
                                    "OpenStreetMap",
                                    href="https://www.openstreetmap.org/#map=13/53.81089/-1.58512",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " and ",
                                html.A(
                                    "Fruit Works Co-Operative",
                                    href="https://www.fruitworks.org.uk/",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " datasets."
                            ]),
                        ])
                    )
                ],
                start_collapsed= True
             ),

            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Urban Farms",
                        image= "urban_farms.png",
                        description= html.Div([
                            html.H4("What is this layer ?"),
                            
                            html.P("Urban farms are spaces within the city where people grow food and may also raise animals. They will typically own their land or rent it from the council. They can support local food production, education and community engagement."
                            ),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "Urban farms were identified using ",
                                html.A(
                                    "Leeds Green Activity Provider (LGAP)",
                                    href="https://lgap.co.uk/",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " datasets."
                            ]),
                        ])
                    )
                ],
                start_collapsed= True
             ),

            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Composting Collectives",
                        image= "compost.png",
                        description= html.Div([
                            html.H4("What is this layer ?"),
                            
                            html.P("Composting collectives are shared composting facilities, such as drop-off composting bins, that allow residents to reduce food waste by recycling food scraps. The compost produced provides a free source of nutrient-rich soil to grow food, flowers and other plants."
                            ),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "Composting collectives were identified using ",
                                html.A(
                                    "FoodWiseLeeds",
                                    href="https://foodwiseleeds.org/project/ccl/",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " datasets."
                            ]),
                        ])
                    )
                ],
                start_collapsed= True
             ),

            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Basemap",
                        image= "basemap.png",
                        description= html.Div([
                            html.H4("What is this layer ?"),
                            
                            html.P("A background map that provides visual context for the CGSs and its surroundings. It shows roads, buildings, green spaces, and water in a simple map."
                            ),
                            
                            html.H4("How to use this information ?"),
                            html.Li("Understanding surroundings: Identifying nearby streets, buildings, and green spaces around the CGS boundary."),
                            html.Li("Orientation: Locating yourself within the dashboard before exploring other layers."),
                            html.Li("Cross-referencing: Comparing layers with the area’s overall layout.."),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "This layer uses ",
                                html.A(
                                    "OpenStreetMap",
                                    href="https://www.openstreetmap.org/#map=13/53.81089/-1.58512",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " data, styled by Carto.",
                            ])
                        ])
                    )
                ],
                start_collapsed= True
             ),
             
             html.Br(),
             html.Br(),
             html.Hr(),  
             html.H2("Imagining Future Growing Spaces"),
                          
            dcc.Markdown("""
                        #### What is this page ?
                        
                        This page provides a planning tool, allowing to imagine where growing spaces could be created in the future across Leeds. Users can select layers from a variety of categories (soil health, heavy metals, TBC) to get a general view of these over Leeds, and select specific locations to access more detailed information. Data on the map were last updated in September 2026.

            """),
                        
            html.H4("Data Layer Guidance"),
            html.Br(),
            html.H5("Soil Health"),

            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Land Cover",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer ?"),
                            
                            html.P("The land cover layer displays the different types of surfaces covering the land, such as woodland, grassland or urban areas. It includes 14 land cover classes in Leeds, based on the UKCEH Aggregate Class system."
                            ),
                            
                            html.H4("How to use this information ?"),
                            
                            html.P("The layer helps to identify what is currently covering the land and understand the character of an area."),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "The land cover data comes from ",
                                html.A(
                                    "Digimap",
                                    href="https://digimap.edina.ac.uk/roam/map/environment",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " datasets."
                            ]),
                        ])
                    ),   
                ],
                start_collapsed= True
            ),
            
            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Soil Texture",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer ?"),
                            
                            html.P("The soil texture layer displays the general texture of soils based on their mix of sand, silt and clay. Soils are grouped as light (sand/silt rich), medium (loams) or heavy (clay-rich). These groups are indicative and may vary locally."
                            ),
                            
                            html.H4("How to use this information ?"),
                            
                            html.P("The layer helps to understand soil conditions, such as drainage water retention and suitability for different types of plants and growing."),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "The soil texture data comes from ",
                                html.A(
                                    "Digimap",
                                    href="https://digimap.edina.ac.uk/roam/map/environment",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " datasets."
                            ]),
                        ])
                    ),   
                ],
                start_collapsed= True
            ),

            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Grain Size Class",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer ?"),
                            
                            html.P("The grain size class layer displays the classes describing the particle size and composition of the underlying material parent material. The classes describe whether the material is mainly sand, clay and silt, gravel, pear or a mixture of these materials."
                            ),
                            
                            html.H4("How to use this information ?"),
                            
                            html.P("The layer helps to understand soil conditions, such as drainage water retention and suitability for different types of plants and growing."),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "The grain size class data comes from ",
                                html.A(
                                    "Digimap",
                                    href="https://digimap.edina.ac.uk/roam/map/environment",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " datasets."
                            ]),
                        ])
                    ),   
                ],
                start_collapsed= True
            ),

            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Soil pH",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer ?"),
                            
                            html.P("The soil pH layer displays the topsoil pH (0-15cm) which shows how acidic or alkaline the top layer of soil is. The values are estimated from a 2007 model using information about soil type and calcium carbonate content."
                            ),
                            
                            html.H4("How to use this information ?"),
                            
                            html.P("This layer helps indicate how suitable the soil may be for different plants and growing conditions."),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "The soil pH data comes from the ",
                                html.A(
                                    "UK Soil Observatory",
                                    href="https://catalogue.ceh.ac.uk/documents/5dd624a9-55c9-4cc0-b366-d335991073c7",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " datasets."
                            ]),
                            
                            html.H4("How were the pH assessment thresholds determined ?"),
                            
                            html.P([
                                "The pH thresholds were sourced from the ",
                                html.A(
                                    "Royal Horticultural Society",
                                    href="https://www.rhs.org.uk/soil-composts-mulches/ph-and-testing-soil",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                "."
                            ]),
                            
                            html.P("The measured soil pH is compared with these reference thresholds to see whether it falls within, above or below the healthy range."
                                   ),
                        ])
                    ),   
                ],
                start_collapsed= True
            ),
            
            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Soil SOM",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer?"),
                            
                            html.P("The soil SOM layer displays the topsoil organic matter (0-15 cm) which shows the amount of organic material in the top layer of the soil. High organic matter can improve soil health by helping it hold water and nutrients, supporting plant growth. The values are estimated from a 2007 model using information about soil type and texture."
                            ),
                            
                            html.H4("How to use this information?"),
                            
                            html.H4("Where is the data from?"),
                            
                            html.P([
                                "The soil SOM data comes from the ",
                                html.A(
                                    "UK Soil Observatory",
                                    href="https://catalogue.ceh.ac.uk/documents/9e4451f8-23d3-40dc-9302-73e30ad3dd76",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " datasets."
                            ]),
                            
                            html.H4("How were the Soil Organic Matter (SOM) assessment thresholds determined ?"),
                            
                            html.P([
                                "The soil organic matter thresholds were sourced from the ",
                                html.A(
                                    "Royal Horticultural Society",
                                    href="https://www.rhs.org.uk/soil-composts-mulches/organic-matter-how-to-use-in-garden",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                "."
                            ]),
                            
                            html.P("The measured soil organic matter is compared with these reference thresholds to see whether it falls within, above or below the healthy range."
                            )
                        ])
                    ),   
                ],
                start_collapsed= True
            ),
            
            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Heavy Metals",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer?"),
                            
                            html.P("The Heavy Metals layers display the concentrations of different metals found in the topsoil (5-20 cm). The layers include eight metals: nickel, arsenic, lead, zirconium, selenium, copper, cadmium and phosphorus."
                            ),
                            
                            html.H4("How to use this information?"),
                            
                            html.P("This information helps understand soil conditions and identify areas where metal concentrations may affect land use and growing suitability."),
                            
                            html.H4("Where is the data from?"),
                            
                            html.P([
                                "The heavy metals data comes from ",
                                html.A(
                                    "UK Soil Observatory",
                                    href="https://www.ukso.org/static-maps/uk-topsoil-geochemistry.html",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                " datasets."
                            ]),
                            
                            html.H4("How were the heavy metals assessment thresholds determined ?"),
                            html.P("The heavy metals threshold assessment uses three types of reference thresholds:"),
                            html.Li([
                                html.Strong("SVG (Soil Guideline Values)"),
                                " - represent concentrations of chemicals in soil below which the long-term human health risks are likely to be minimal."]),
                            html.Li([
                                html.Strong("C4SL (Category 4 Screening Levels)"),
                                " - represent soil screening values for assessing potential risks to human health."]),
                            html.Li([
                                html.Strong("NBC (Normal Background Concentrations)"),
                                " - represent the upper limit of 'normal' levels of contaminants in soils, as described by the Part 2A contaminated land statutory guidance (SG7)."]),
                            html.Br(),
                            html.P([
                                "The SVG for allotment land use values were sourced from reports published by ",
                                html.A(
                                    "CL:AIRE",
                                    href="https://claire.co.uk/information-centre/water-and-land-library-wall.html?view=article&id=178:soil-guideline-values&catid=417&start=1",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                "."
                            ]),
                            html.P([
                                "The C4SLs values for allotments land use were sourced from the following ",
                                html.A(
                                    "peer-reviewed research paper",
                                    href="https://www.sciencedirect.com/science/article/pii/S0269749121015426#bib137",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                "."
                            ]),
                            html.P([
                                "The NBC values (principal) were sourced from the  ",
                                html.A(
                                    "British Geological Survey (BGS)",
                                    href="https://www.bgs.ac.uk/geology-projects/applied-geochemistry/g-base-environmental-geochemistry/nbc-defra-project/#table",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                "."
                            ]),
                            
                            html.P("These reference thresholds are used to compare the measured heavy metal concentrations with the relevant soil assessment criteria and determine whether concentrations fall above the threshold values."
                            )
                        ])
                    ),   
                ],
                start_collapsed= True
            ),
            
            html.Br(),
            html.Br(),
            html.Hr(),  
            html.H2("References"),
            
            
            html.P([
                "For more information on data collection and the dashboard building, refer to the  ",
                html.A(
                    "SEEDS project GitHub repository",
                    href="https://github.com/MarionC749/LIDA-SEEDS",
                    target="_blank",
                    rel="noopener noreferrer"
                ),
                "."
            ]),
         ]
     )

