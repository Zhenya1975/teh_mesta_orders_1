import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, callback_context, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import datetime
import functions
import eo_tab
import settings_tab
# import orders_tab
from dash import dash_table
import base64
import io
import json
# import plotly.graph_objects as go
# import result_df_prep
# import clean_messages_raw_file

# select the Bootstrap stylesheet2 and figure template2 for the theme toggle here:
# template_theme1 = "sketchy"
template_theme1 = "flatly"
template_theme2 = "darkly"
# url_theme1 = dbc.themes.SKETCHY
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY


loading_style = {
    # 'position': 'absolute',
                 # 'align-self': 'center'
                 }

templates = [
    "bootstrap",
    "minty",
    "pulse",
    "flatly",
    "quartz",
    "cyborg",
    "darkly",
    "vapor",
]

load_figure_template(templates)

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
)
app = Dash(__name__, external_stylesheets=[url_theme1, dbc_css])

"""
===============================================================================
Layout
"""
app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H4("ТЕХНИЧЕСКИЕ МЕСТА, ЗАКАЗЫ"),
                    ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2], ),

                    html.Div([
                        dcc.Tabs(
                            id="tabs-all",
                            style={
                                # 'width': '50%',
                                # 'font-size': '200%',
                                # 'height':'5vh'
                            },
                            value='tab_select_parameters',
                            # parent_className='custom-tabs',
                            # className='custom-tabs-container',
                            children=[
                                eo_tab.eo_tab(),
                                # orders_tab.orders_tab(),
                                settings_tab.settings_tab()

                                # tab2(),
                                # tab3(),
                            ]
                        ),
                    ]),

                ]
            )
        ]
    ),
    className="m-4 dbc",
    # fluid=True,
)


@app.callback([
    Output("checklist_level_1", "value"),
    Output("checklist_level_1", "options"),
    Output("checklist_eo_class", "value"),
    Output("checklist_eo_class", "options"),
    
    Output('loading', 'parent_style')

],

    [
        Input('checklist_level_1', 'value'),
        Input('checklist_eo_class', 'value'),
        
    ],
)
def teh_mesta(
        checklist_level_1,
        checklist_eo_class
      ):
    # changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    
    # читаем файл с дефолтными фильтрами
    # Opening JSON file
    with open('saved_filters.json', 'r') as openfile:
      # Reading from json file
      saved_filters_dict = json.load(openfile)

    ################## level_1 VALUES ###################################
    if checklist_level_1 == None:
      filter_level_1 = saved_filters_dict['level_1']
    else:
      filter_level_1 = checklist_level_1
      saved_filters_dict['level_1'] = checklist_level_1
     
      # записываем в json
      with open("saved_filters.json", "w") as jsonFile:
        json.dump(saved_filters_dict, jsonFile)
    checklist_level_1_values = filter_level_1
    
    ################## eo_class VALUES ###################################
    if checklist_eo_class == None:
      filter_eo_class = saved_filters_dict['eo_class']
    else:
      filter_eo_class = checklist_eo_class
      saved_filters_dict['eo_class'] = checklist_eo_class
     
      # записываем в json
      with open("saved_filters.json", "w") as jsonFile:
        json.dump(saved_filters_dict, jsonFile)
    checklist_eo_class_values = filter_eo_class

    
    selected_items_df = pd.read_csv('data/selected_items.csv', dtype=str)
    selected_items_df = selected_items_df.astype({"level_no": int})

    # Список чек-боксов Level_1
    level_1_df = selected_items_df.loc[selected_items_df['level_no'] == 1]
    checklist_level_1_options = []
    if len(level_1_df)>0:
        checklist_level_1_options = functions.level_checklist_data(level_1_df)[0]

   
    # Список чек-боксов eo_class
    eo_class_df = pd.read_csv('data/eo_class.csv')

    
    checklist_eo_class_options = functions.eo_class_checklist_data(eo_class_df)[0]


    new_loading_style = loading_style
    return checklist_level_1_values, checklist_level_1_options, checklist_eo_class_values, checklist_eo_class_options, new_loading_style





if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=False)