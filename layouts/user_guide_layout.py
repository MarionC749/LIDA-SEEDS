from dash import html, dcc
import dash_bootstrap_components as dbc


# ------ HELPER FUNCTION ------
def create_accordion_item(title, image, description):
    return dbc.AccordionItem(
        dcc.Markdown(description),
        title= html.Div(
        [
            html.Img(
                src= f"/assets/{image}",
                style={
                    "height": "35px",
                    "marginRight": "5px",
                    "verticalAlign": "middle"
                }
            ),
            html.Span(title)
        ],
        style= {
            "display": "flex",
            "alignItems": "center"
        }
        )
    )

# ------ CREATE USER GUIDE LAYOUT FUNCTION ------
def create_user_guide_layout():
     return html.Div(
         className= "user_guide_container",
         children=[
             
             html.H1("SEEDS Dashboard User Guide"),
             
             html.H2("Existing Community Growing Schemes"),
             
             dcc.Markdown("""
                ### What is this page?
            
                This page provides an overview of existing Community Growing Schemes (CGSs) across Leeds, making it easier to discover and explore local schemes. Users can view five different types of CGSs (allotments, community growing spaces, community orchards, urban farms and composting collectives) and select individual schemes to access more detailed information. Data on the map were last updated in September 2026.

                Clicking on a CGS opens a sidebar menu with two sections:
                * **Community**: Provides information about the scheme, including its location, activities, meeting times and places and contact details where available.
                * **Soil Health**: Summarises soil health information for the area covered by the CGS, helping users understand the conditions of the growing environment.
            
                ### What are Community Growing Schemes (CGS) ?
                Community Growing Schemes are shared spaces, often open to the public, where people collectively grow food and plants for community benefit and personal use rather than private profit.

                """),
             
             html.H3("Data Layer Guidance"),
             
             dbc.Accordion(
                [
                    create_accordion_item(
                        title= "Allotments",
                        image= "allotments.png",
                        description= """
                        ### What is this layer?
                            
                        Allotments are individual plots of land rented by individuals to grow vegetables, fruits and other plants for personal or family consumption. In Leeds, allotments may be managed by the council or by independent associations.
                        **Important note:** Allotments are not generally publicly accessible. Access is usually limited to plot holders and authorised visitors.

                        ### Where is the data from?
                        Allotments were identified using [Ordnance Survey](https://osdatahub.os.uk/data/downloads/open/OpenGreenspace), [OpenStreetMap](https://www.openstreetmap.org/#map=13/53.81089/-1.58512), [Leeds Green Activity Provider (LGAP)](https://www.arcgis.com/apps/mapviewer/index.html?layers=6afec02763ab4f87887939ed4d073c70) and [Leeds City Council](https://www.leeds.gov.uk/parks-and-countryside/grow-your-own/allotments) datasets.
                        """
                    ),

                ],
                start_collapsed= True
             )
         ]
     )

