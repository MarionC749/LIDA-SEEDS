#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 1 (Existing Community Growing Schemes) - COLOUR DICTIONARIES
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Define a color to map points/polygons of the same type
#color are color-blindness friendly
types_colors= {"Allotments": "#D55E00",
               "Community Growing Spaces": "#009E73",
               "Community Orchard": "#CC79A7",
               "Urban Farms": "#F0E442",
               "Composting Collective": "#0072B2"
}

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 (Imagining Future Growing Spaces) - DATASETS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from data_loading_n_config.load_data import(
    soil_health,
    heavy_metals,
    thresholds,
    flood,
    demographics
)


DVPT_DATASETS= {
    "soil_health":{
        "data": soil_health,
        "display_name": "🪱 Soil Health",
    },
    
    "heavy_metals":{
        "data": heavy_metals,
        "display_name": "🧪 Potential Toxic Elements",
    },
    
    "thresholds":{
        "data": thresholds,
        "display_name": "⚠️ Soil Health Thresholds Assessment"
    },
    
    "flood":{
            "data": flood,
            "display_name": "💧 Flood Risk",
        },
    
    "demographics":{
            "data": demographics,
            "display_name": "🏠 Socio-demographics",
        },
}


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 (Imagining Future Growing Spaces) - COLOUR DICTIONARIES
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

land_cover_colours= {
    "Acid grassland": "lightcoral",
    "Arable": "darkorange",
    "Calcareous grassland": "red",
    "Coniferous woodland": "darkgreen",
    "Deciduous woodland": "lime",
    "Fen": "yellowgreen",
    "Freshwater": "dodgerblue",
    "Heather": "yellow",
    "Heather grassland": "saddlebrown",
    "Improve grassland": "darkgoldenrod",
    "Inland rock": "tan",
    "Neutral grassland": "palegreen",
    "Suburban": "mediumvioletred",
    "Urban": "mediumorchid", 
}

soil_texture_colours= {
    "LIGHT(SILTY) TO MEDIUM(SILTY) TO HEAVY": '#1f77b4',
    "MEDIUM TO HEAVY": "#ff7f0e",
    "LIGHT(SILTY) TO MEDIUM(SILTY)": "#2ca02c",
    "MEDIUM TO LIGHT(SILTY) TO HEAVY": "#d62728",
    "LIGHT(SANDY) TO MEDIUM(SANDY)": "#9467bd",
    "HEAVY TO MEDIUM": "#8c564b",
    "ALL": "#e377c2",
    "MEDIUM(SILTY)": "#7f7f7f",
    "MEDIUM": "#bcbd22",
    "MEDIUM TO LIGHT(SILTY)": "#17becf",
}

grain_size_colours= {
    "ARGILLIC - ARENACEOUS": '#377eb8',
    "ARENACEOUS": '#ff7f00',
    "MIXED (ARGILLIC-RUDACEOUS)": '#4daf4a',
    "ARENACEOUS - RUDACEOUS": '#f781bf',
    "ARGILLACEOUS": '#a65628',
    "PEAT": '#984ea3',
}

flood_colours= {
    "Coastal - High Flood Potential": 'indigo',
    "Coastal - Secondary Flood Potential": 'blueviolet',
    "Fluvial - High Flood Potential": 'mediumblue',
    "Fluvial - Secondary Flood Potential": 'royalblue',
}

IMD_Decile_colours= {
    1: '#40039C',
    2: '#6A00A7',
    3: '#8F0DA3',
    4: '#B02A8F',
    5: '#CA4678',
    6: '#E06461',
    7: '#F1824C',
    8: '#FCA635',
    9: '#FCCC25',
    10: '#EFF821',
}

pp_dec_combined_colours= {
    1: '#40039C',
    2: '#6A00A7',
    3: '#8F0DA3',
    4: '#B02A8F',
    5: '#CA4678',
    6: '#E06461',
    7: '#F1824C',
    8: '#FCA635',
    9: '#FCCC25',
    10: '#EFF821',
}

pp_dec_domain_supermarket_proximity_colours= {
    1: '#40039C',
    2: '#6A00A7',
    3: '#8F0DA3',
    4: '#B02A8F',
    5: '#CA4678',
    6: '#E06461',
    7: '#F1824C',
    8: '#FCA635',
    9: '#FCCC25',
    10: '#EFF821',
}

pp_dec_domain_supermarket_accessibility_colours= {
    1: '#40039C',
    2: '#6A00A7',
    3: '#8F0DA3',
    4: '#B02A8F',
    5: '#CA4678',
    6: '#E06461',
    7: '#F1824C',
    8: '#FCA635',
    9: '#FCCC25',
    10: '#EFF821',
}

pp_dec_domain_socio_demographic_colours= {
    1: '#40039C',
    2: '#6A00A7',
    3: '#8F0DA3',
    4: '#B02A8F',
    5: '#CA4678',
    6: '#E06461',
    7: '#F1824C',
    8: '#FCA635',
    9: '#FCCC25',
    10: '#EFF821',
}

pp_dec_domain_nonsupermarket_proximity_colours= {
    1: '#40039C',
    2: '#6A00A7',
    3: '#8F0DA3',
    4: '#B02A8F',
    5: '#CA4678',
    6: '#E06461',
    7: '#F1824C',
    8: '#FCA635',
    9: '#FCCC25',
    10: '#EFF821',
}



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 (Imagining Future Growing Spaces) - LAYER CONFIGURATION
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

LAYER_CONFIG= {
    
    #Soil Health Dataset
    "soil_health":{
    
    "Land Cover": {
        "filter": {"Soil_Metric": "Land Cover"},
        "column": "Land_Cover_Type",
        "type": "categorical",
        "palette": land_cover_colours,
        "legend": "Land Cover"
    },
    
    "Soil Texture": {
            "filter": {"Soil_Metric": "Soil Parent"},
            "column": "SOIL_GROUP",
            "type": "categorical",
            "palette": soil_texture_colours,
            "legend": "Soil Texture",
        },
    
    "Soil Descriptor": {
            "filter": {"Soil_Metric": "Soil Parent"},
            "column": "GEN_GRAIN",
            "type": "categorical",
            "palette": grain_size_colours,
            "legend": "Soil Descriptor",
        },
    
    "Soil pH": {
                "filter": {"Soil_Metric": "Soil pH"},
                "column": "PH_07",
                "type": "continuous",
                "colourscale": "inferno_r",
                "legend": "Soil pH",
            },
    
    "Soil SOM": {
                "filter": {"Soil_Metric": "Soil SOM"},
                "column": "LOI_07",
                "type": "continuous",
                "colourscale": "inferno_r",
                "legend": "Soil Organic Matter (SOM) in %",
            },
    },
    
    #Heavy Metals Dataset
    "heavy_metals":{

    "Nickel": {
            "filter": {"HM_name": "Nickel"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Nickel (mg/kg)",
        },
    "Arsenic": {
            "filter": {"HM_name": "Arsenic"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Arsenic (mg/kg)",
        },
    "Lead": {
            "filter": {"HM_name": "Lead"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Lead (mg/kg)",
        },
    "Zirconium": {
            "filter": {"HM_name": "Zirconium"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Zirconium (mg/kg)",
        },
    "Selenium": {
            "filter": {"HM_name": "Selenium"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Selenium (mg/kg)",
        },
    "Copper": {
            "filter": {"HM_name": "Copper"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Copper (mg/kg)",
        },
    "Cadmium": {
            "filter": {"HM_name": "Cadmium"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Cadmium (mg/kg)",
        },
    "Phosphorus": {
            "filter": {"HM_name": "Phosphorus"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Phosphorus (w%)",
            },
    },
    
    #Flood Risk Dataset
        "flood":{
        
        "Flood Risk": {
            "column": "Class",
            "type": "categorical",
            "palette": flood_colours,
            "legend": "Flood Risk"
        },
    },

    #Socio-Demographics Dataset
    "demographics":{

    "IMD_Decile": {
            "column": "IMD_Decile",
            "type": "categorical",
            "palette": IMD_Decile_colours,
            "legend": "Index of Multiple Deprivation (decile)",
        },

    "pp_dec_combined": {
            "column": "pp_dec_combined",
            "type": "categorical",
            "palette": pp_dec_combined_colours,
            "legend": "Priority Places for Food Index (decile)",
        },
    
    "pp_dec_domain_supermarket_proximity": {
            "column": "pp_dec_domain_supermarket_proximity",
            "type": "categorical",
            "palette": pp_dec_domain_supermarket_proximity_colours,
            "legend": "Proximity to supermarket retail facilities (decile)",
        },
    
    "pp_dec_domain_supermarket_accessibility": {
            "column": "pp_dec_domain_supermarket_accessibility",
            "type": "categorical",
            "palette": pp_dec_domain_supermarket_accessibility_colours,
            "legend": "Accessibility to supermarket retail facilities (decile)",
        },
    
    "pp_dec_domain_socio_demographic": {
            "column": "pp_dec_domain_socio_demographic",
            "type": "categorical",
            "palette": pp_dec_domain_socio_demographic_colours,
            "legend": "Socio-economic barriers (decile)",
        },
    
    "pp_dec_domain_nonsupermarket_proximity": {
            "column": "pp_dec_domain_nonsupermarket_proximity",
            "type": "categorical",
            "palette": pp_dec_domain_nonsupermarket_proximity_colours,
            "legend": "Proximity to non-supermarket food provision (decile)",
        },
    }

}


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 (Imagining Future Growing Spaces) - SIDEBAR CONFIGURATION
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

DVPT_SIDEBAR_CONFIG = {
    
    #Soil Health Dataset
    "soil_health":{
        
    "Land Cover": {
            "filter":{"Soil_Metric": "Land Cover"},
            "value_column": "Land_Cover_Type",
            "title": "Land Cover"
        },
    
    "Soil Texture": {
            "filter":{"Soil_Metric": "Soil Parent"},
            "value_column": "SOIL_GROUP",
            "title": "Soil Texture"
        },
    
    "Soil Descriptor": {
            "filter":{"Soil_Metric": "Soil Parent"},
            "value_column": "GEN_GRAIN",
            "title": "Soil Descriptor",
            "description_column": "GEN_GRAIN_Desc",
        },
        
        
    "Soil pH": {
        "filter":{"Soil_Metric": "Soil pH"},
        "value_column": "PH_07",
        "title": "Soil pH"
    },
    
    "Soil SOM": {
                "filter":{"Soil_Metric": "Soil SOM"},
                "value_column": "LOI_07",
                "title": "Soil Organic Matter (SOM) in %"
            },
    
    },
    
    #Heavy Metals Dataset
    "heavy_metals":{

    "Nickel": {
            "filter": {"HM_name": "Nickel"},
            "value_column": "value",
            "title": "Nickel (Ni)",
            "unit_column": "HM_unit",
        },
    "Arsenic": {
            "filter": {"HM_name": "Arsenic"},
            "value_column": "value",
            "title": "Arsenic (As)",
            "unit_column": "HM_unit",
        },
    "Lead": {
            "filter": {"HM_name": "Lead"},
            "value_column": "value",
            "title": "Lead (Pb)",
            "unit_column": "HM_unit",
        },
    "Zirconium": {
            "filter": {"HM_name": "Zirconium"},
            "value_column": "value",
            "title": "Zirconium (Zr)",
            "unit_column": "HM_unit",
        },
    "Selenium": {
            "filter": {"HM_name": "Selenium"},
            "value_column": "value",
            "title": "Selenium (Se)",
            "unit_column": "HM_unit",
        },
    "Copper": {
            "filter": {"HM_name": "Copper"},
            "value_column": "value",
            "title": "Copper (Cu)",
            "unit_column": "HM_unit",
        },
    "Cadmium": {
            "filter": {"HM_name": "Cadmium"},
            "value_column": "value",
            "title": "Cadmium (Cd)",
            "unit_column": "HM_unit",
        },
    "Phosphorus": {
            "filter": {"HM_name": "Phosphorus"},
            "value_column": "value",
            "title": "Phosphorus (P2O5)",
            "unit_column": "HM_unit",
            },
    },
    
    #Flood Risk Dataset
    "flood":{

    "Flood Risk": {
            "value_column": "Class",
            "title": "Type",
            "description_column": "Legend"
        },
    },

    #Socio-demographics Dataset
    "demographics":{

    "IMD_Decile": {
            "value_column": "IMD_Decile",
            "title": "Index of Multiple Deprivation (decile)",
            "LSOA": "LSOA21NM"
        },

    "pp_dec_combined": {
            "value_column": "pp_dec_combined",
            "title": "Priority Places for Food Index (decile)",
            "LSOA": "LSOA21NM",
        },
    
    "pp_dec_domain_supermarket_proximity": {
            "value_column": "pp_dec_domain_supermarket_proximity",
            "title": "Proximity to supermarket retail facilities (decile)",
            "LSOA": "LSOA21NM",
        },
    
    "pp_dec_domain_supermarket_accessibility": {
            "value_column": "pp_dec_domain_supermarket_accessibility",
            "title": "Accessibility to supermarket retail facilities (decile)",
            "LSOA": "LSOA21NM",
        },
    
    "pp_dec_domain_socio_demographic": {
            "value_column": "pp_dec_domain_socio_demographic",
            "title": "Socio-economic barriers (decile)",
            "LSOA": "LSOA21NM",
        },
    
    "pp_dec_domain_nonsupermarket_proximity": {
            "value_column": "pp_dec_domain_nonsupermarket_proximity",
            "title": "Proximity to non-supermarket food provision (decile)",
            "LSOA": "LSOA21NM",
        }
    
    }

}

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# POP UP MESSAGES CONFIGURATION
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from dash import html

# ----- TAB 1 - Existing Community Growing Schemes -----

Existing_GUIDE_STEPS= [
    {
        "title": "Welcome to the SEEDS Dashboard !",
        "body": html.P(
            "The SEEDS Dashboard brings together environmental, soil and community data to support community food growing across Leeds.\nLet's take a quick tour to get you started."
                    ),
    },
    {
        "title": "Explore Existing Community Growing Schemes",
        "body": html.P([
            "Use the interactive map to explore existing Community Growing Schemes (CGSs) across Leeds.",
            html.Br(),
            html.Br(),
            "Use the checklist on the left to select different types of schemes.",
            ]),
    },
    {
        "title": "Explore a Community Growing Scheme",
        "body": html.P("Click on a scheme on the map to view information in the sidebar, including details about the scheme (location, activities, meeting times & places, contact details where available) and soil health information."
                    )
    },
    {
        "title": "Find Your Local Area",
        "body": html.P("Use the postcode search bar at the top to quickly locate and zoom onto an area of interest."
                    )
    },
    {
        "title": "Download the data",
        "body": html.P("Click on the 'Download the data' button to download the data displayed on the map."
                    )
    },
]



# ----- TAB 2 - Imagining Future Community Growing Schemes -----

Dvpt_GUIDE_STEPS= [
    {
        "title": "Imagining Future Growing Spaces",
        "body": html.P([
            "This tab provides a planning tool.",
            html.Br(),
            html.Br(),
            "Use the map to explore different areas across Leeds and consider where new Community Growing Schemes (CGSs) could potentially be developed.",
            ]),
    },
    {
        "title": "Select a Data Layer",
        "body": html.P([
            "Use the checklist on the left to select a data layer from the different categories. Only one layer can be selected at a time.",
            html.Br(),
            html.Br(),
            "Please refer to the 'User Guide' to learn more about each layer.",
            ]),
    },
    

    
    {
        "title": "Explore a Location",
        "body": html.P("Click anywhere on the map to explore information about the selected location in the sidebar."
                    )
    },
    {
        "title": "Find Your Local Area",
        "body": html.P("Use the postcode search bar at the top to quickly locate and zoom onto an area of interest."
                    )
    },
]