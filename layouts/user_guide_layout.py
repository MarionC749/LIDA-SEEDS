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
                            
                            html.P("This layer displays the different types of surfaces covering the land, such as woodland, grassland or urban areas. It includes 14 land cover classes in Leeds, based on the UKCEH Aggregate Class system."
                            ),
                            
                            html.H4("How to use this information ?"),
                            
                            html.P("The layer helps to identify what is currently covering the land and understand the character of an area."),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "The data comes from ",
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
                            
                            html.P("This layer displays the general texture of soils based on their mix of sand, silt and clay. Soils are grouped as light (sand/silt rich), medium (loams) or heavy (clay-rich). These groups are indicative and may vary locally."
                            ),
                            
                            html.H4("How to use this information ?"),
                            
                            html.P("The layer helps to understand soil conditions, such as drainage water retention and suitability for different types of plants and growing."),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "The data comes from ",
                                html.A(
                                    "Digimap",
                                    href="https://digimap.edina.ac.uk/geology",
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
                            
                            html.P("This layer displays the classes describing the particle size and composition of the underlying material parent material. The classes describe whether the material is mainly sand, clay and silt, gravel, pear or a mixture of these materials."
                            ),
                            
                            html.H4("How to use this information ?"),
                            
                            html.P("The layer helps to understand soil conditions, such as drainage water retention and suitability for different types of plants and growing."),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "The data comes from ",
                                html.A(
                                    "Digimap",
                                    href="https://digimap.edina.ac.uk/geology",
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
                            
                            html.P("This layer displays the topsoil pH (0-15cm) which shows how acidic or alkaline the top layer of soil is. The values are estimated from a 2007 model using information about soil type and calcium carbonate content."
                            ),
                            
                            html.H4("How to use this information ?"),
                            
                            html.P("This layer helps indicate how suitable the soil may be for different plants and growing conditions."),
                            
                            html.H4("Where is the data from ?"),
                            
                            html.P([
                                "The data comes from the ",
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
                            
                            html.P("This layer displays the topsoil organic matter (0-15 cm) which shows the amount of organic material in the top layer of the soil. High organic matter can improve soil health by helping it hold water and nutrients, supporting plant growth. The values are estimated from a 2007 model using information about soil type and texture."
                            ),
                            
                            html.H4("How to use this information?"),
                            
                            html.H4("Where is the data from?"),
                            
                            html.P([
                                "The data comes from the ",
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
            
            html.Br(),
            html.H5("Heavy Metals"),
            
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
                                "The data comes from ",
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
            html.H5("Flood Risk"),
            
            
            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Flood Risk",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer?"),
                            
                            html.P("This layer displays the likely susceptibility to flooding, either from coastal inundation or fluvial (inland) water flow."
                            ),
                            
                            html.H4("How to use this information?"),
                            
                            html.P("This information helps to understand where safer locations for community growing are and inform measures to protect crops, soil and infrastructures from flooding."
                                   ),
                            
                            html.H4("Where is the data from?"),
                            
                            html.P([
                                "The data comes from the ",
                                html.A(
                                    "Digimap",
                                    href="https://digimap.edina.ac.uk/geology",
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

            html.Br(),
            html.H5("Socio-Demographics"),

            dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Index of Multiple Deprivation (decile)",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer?"),
                            
                            html.P(
                            "This layer displays the Index of Multiple Deprivation, also referred to as IMD (2025), which is a composite index formed of data compiled across 7 domains, to produce an overall relative measure of deprivation. Deciles are calculated by ranking the 33,755 small areas in England, from most deprived to least deprived, and dividing them into 10 equal groups. These range from the most deprived 10% of small areas nationally to the least deprived 10% of small areas nationally, where 1 represents the 10% most deprived areas and 10 represents the 10% least deprived areas."
                            ),
                            html.H5("Domain definitions"),
                            html.Li("Income Deprivation (22.5% of composite index)"),
                            html.Li("Employment Deprivation  (22.5% of composite index)"),
                            html.Li("Education, Skills and Training Deprivation (13.5% of composite index)"),
                            html.Li("Health Deprivation and Disability (13.5% of composite index)"),
                            html.Li("Crime (9.3% of composite index)"),
                            html.Li("Barriers to Housing and Services (9.3% of composite index)"),
                            html.Li("Living Environment Deprivation (9.3% of composite index)"),
                            html.Br(),
                            html.P([
                                "To learn more about the Index of Multiple Deprivation (IMD) refer to ",
                                html.A(
                                    "this page",
                                    href="https://www.gov.uk/government/statistics/english-indices-of-deprivation-2025",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                "."
                            ]),
                            
                            html.H4("How to use this information?"),
                            
                            html.P(""
                                   ),
                            
                            html.H4("Where is the data from?"),
                            
                            html.P([
                                "The  data comes from the ",
                                html.A(
                                    "UK Government",
                                    href="https://www.gov.uk/government/statistics/english-indices-of-deprivation-2025",
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
                        title= "Priority Places for Food Index (decile)",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer?"),
                            
                            html.P("This layer displays the Priority Places for Food Index, which is a composite index formed of data compiled across seven domains. Its goal is to identify neighbourhoods that are most vulnerable to increases in the cost of living and which have a lack of accessibility to cheap, healthy, and sustainable sources of food—making them a Priority Place for Food. Deciles are calculated by ranking the 33,755 small areas in England, from most deprived to least deprived, and dividing them into 10 equal groups. These range from the most deprived 10% of small areas nationally to the least deprived 10% of small areas nationally, where 1 represents the 10% most deprived areas and 10 represents the 10% least deprived areas."
                            ),
                            html.H5("Domain definitions"),
                            html.Li("Proximity to supermarket retail facilities (12.5% of composite index)"),
                            html.Li("Accessibility to supermarket retail facilities (12.5% of composite index)"),
                            html.Li("Access to online deliveries (12.5% of composite index)"),
                            html.Li("Proximity to non-supermarket food provision (12.5% of composite index)"),
                            html.Li("Socio-economic barriers (16.7% of composite index)"),
                            html.Li("Need for family food support (16.7% of composite index)"),
                            html.Li("Fuel Poverty (16.7% of composite index)"),
                            html.Br(),
                            html.P([
                                "To learn more about the Priority Places for Food Index refer to ",
                                html.A(
                                    "this page",
                                    href="https://priorityplaces.cdrc.ac.uk/",
                                    target="_blank",
                                    rel="noopener noreferrer"
                                ),
                                "."
                            ]),
                            
                            html.H4("How to use this information?"),
                            
                            html.P(""
                                   ),
                            
                            html.H4("Where is the data from?"),
                            
                            html.P([
                                "The  data comes from the ",
                                html.A(
                                    "Healthy and Sustainable Places (HASP)",
                                    href="https://data.hasp.ac.uk/browser/dataset/5276/0",
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
                        title= "Proximity to supermarket retail facilities (decile)",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer?"),
                            
                            html.P("This layer displays the Proximity to supermarket retail facilities (decile). The indicator was based on:"
                            ),
                            html.Li("Average distance to nearest large grocery store (Geolytix Retail Points v28)."),
                            html.Li("Average count of stores within 1km (Geolytix Retail Points v28)."),
                            
                            
                            html.H4("How to use this information?"),
                            
                            html.P(""
                                   ),
                            
                            html.H4("Where is the data from?"),
                            
                            html.P([
                                "The  data comes from the ",
                                html.A(
                                    "Healthy and Sustainable Places (HASP)",
                                    href="https://data.hasp.ac.uk/browser/dataset/5276/0",
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
                        title= "Accessibility to supermarket retail facilities (decile)",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer?"),
                            
                            html.P("This layer displays the Accessibility to supermarket retail facilities (decile). The indicator was based on:"
                            ),
                            html.Li("Average travel distance (based on a custom built spatial interaction model)."),
                            html.Li("Accessibility via public transport (Govt Journey Time Statistics 2019)."),
                            
                            html.H4("How to use this information?"),
                            
                            html.P(""
                                   ),
                            
                            html.H4("Where is the data from?"),
                            
                            html.P([
                                "The  data comes from the ",
                                html.A(
                                    "Healthy and Sustainable Places (HASP)",
                                    href="https://data.hasp.ac.uk/browser/dataset/5276/0",
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
                        title= "Socio-economic barriers (decile)",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer?"),
                            
                            html.P("This layer displays the Socio-economic barriers (decile). The indicator was based on:"
                            ),
                            html.Li("Proportion of population experiencing income deprivation (UK Govt Index of Multiple Deprivation 2017-2020). "),
                            html.Li("Proportion of population with no car access (UK Census 2021)."),
                            
                            html.H4("How to use this information?"),
                            
                            html.P(""
                                   ),
                            
                            html.H4("Where is the data from?"),
                            
                            html.P([
                                "The  data comes from the ",
                                html.A(
                                    "Healthy and Sustainable Places (HASP)",
                                    href="https://data.hasp.ac.uk/browser/dataset/5276/0",
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
                        title= "Proximity to non-supermarket food provision (decile)",
                        image= None,
                        description= html.Div([
                            html.H4("What is this layer?"),
                            
                            html.P("This layer displays the Proximity to non-supermarket food provision (decile). The indicator was based on:"
                            ),
                            html.Li("Distance to nearest non-supermarket retail food store (Food Standards Agency, accessed 2022-08-23 and Geolytix Retail Points v28)."),
                            html.Li("Count of non-supermarket retail food stores within 1km (Food Standards Agency, accessed 2023-11-02)."),
                            html.Li("Average distance to nearest market (CDRC data from National Market Traders Federation 2016-2019)."),
                            html.Li("Average count of markets within 1km (CDRC data from National Market Traders Federation 2016-2019)."),
                            
                            html.H4("How to use this information?"),
                            
                            html.P(""
                                   ),
                            
                            html.H4("Where is the data from?"),
                            
                            html.P([
                                "The  data comes from the ",
                                html.A(
                                    "Healthy and Sustainable Places (HASP)",
                                    href="https://data.hasp.ac.uk/browser/dataset/5276/0",
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

