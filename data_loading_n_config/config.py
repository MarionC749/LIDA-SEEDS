#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 1 (Existing Community Growing Schemes)) - COLOUR DICTIONARIES
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
# TAB 2 (Development Opportunities) - COLOUR DICTIONARIES
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
    "Heather grassland": "gold",
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

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TAB 2 (Development Opportunities) - LAYER CONFIGURATION
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

LAYER_CONFIG= {
    
    "Land Cover": {
        "filters": {"Soil_Metric": "Land Cover"},
        "column": "Land_Cover_Type",
        "type": "categorical",
        "palette": land_cover_colours,
        "legend": "Land Cover"
    },
    
    "Soil Texture": {
            "filters": {"Soil_Metric": "Soil Parent"},
            "column": "SOIL_GROUP",
            "type": "categorical",
            "palette": soil_texture_colours,
            "legend": "Soil Texture",
        },
    
    "Grain Size Class": {
            "filters": {"Soil_Metric": "Soil Parent"},
            "column": "GEN_GRAIN",
            "type": "categorical",
            "palette": grain_size_colours,
            "legend": "Grain Size Class",
        },
    
    "Soil pH": {
                "filters": {"Soil_Metric": "Soil pH"},
                "column": "PH_07",
                "type": "continuous",
                "colourscale": "inferno_r",
                "legend": "Soil pH (2007)",
            },
    
    "Soil SOM": {
                "filters": {"Soil_Metric": "Soil SOM"},
                "column": "LOI_07",
                "type": "continuous",
                "colourscale": "inferno_r",
                "legend": "Soil Organic Matter (SOM)",
            },

    "Nickel": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "Ni"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Nickel (mg/kg)",
        },
    "Arsenic": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "As"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Arsenic (mg/kg)",
        },
    "Lead": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "Pb"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Lead (mg/kg)",
        },
    "Zirconium": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "Zr"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Zirconium (mg/kg)",
        },
    "Selenium": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "Se"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Selenium (mg/kg)",
        },
    "Copper": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "Cu"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Copper (mg/kg)",
        },
    "Cadmium": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "Cd"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Cadmium (mg/kg)",
        },
    "Phosphorus": {
            "filters": {"Soil_Metric": "Heavy Metals",
                        "metal": "P2O5"},
            "column": "value",
            "type": "continuous",
            "colourscale": "inferno_r",
            "legend": "Phosphorus (w%)",
            },

}