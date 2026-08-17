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
    thresholds
)


DVPT_DATASETS= {
    "soil_health":{
        "data": soil_health,
        "display_name": "🪱 Soil Health",
    },
    
    "heavy_metals":{
        "data": heavy_metals,
        "display_name": "🧪 Heavy Metals",
    },
    
    "thresholds":{
        "data": thresholds,
        "display_name": "⚠️ Soil Health Thresholds Assessment"
    }
}
#Other Datasets TBC

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
    
    "Grain Size Class": {
            "filter": {"Soil_Metric": "Soil Parent"},
            "column": "GEN_GRAIN",
            "type": "categorical",
            "palette": grain_size_colours,
            "legend": "Grain Size Class",
        },
    
    "Soil pH": {
                "filter": {"Soil_Metric": "Soil pH"},
                "column": "PH_07",
                "type": "continuous",
                "colourscale": "inferno_r",
                "legend": "Soil pH (2007)",
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
    }
}
#Other Datasets TBC


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
    
    "Grain Size Class": {
            "filter":{"Soil_Metric": "Soil Parent"},
            "value_column": "GEN_GRAIN",
            "title": "Grain Size Class"
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
    }
    
    
#Other Datasets TBC
    
}