import pandas as pd
# import numpy as np
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
     Output("checklist_main_eo_class", "value"),
    Output("checklist_main_eo_class", "options"),
    Output('eo_table', 'children'),
    Output('number_of_rows_text', 'children'),
    Output('loading', 'parent_style')

],

    [
        Input('checklist_level_1', 'value'),
        Input('checklist_eo_class', 'value'),
        Input('checklist_main_eo_class', 'value'),

    ],
)
def teh_mesta(
        checklist_level_1,
        checklist_eo_class,
        checklist_main_eo_class
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

    ################## main_eo_class VALUES ###################################
    if checklist_main_eo_class == None:
      filter_main_eo_class = saved_filters_dict['main_eo_class']
    else:
      filter_main_eo_class = checklist_main_eo_class
      saved_filters_dict['main_eo_class'] = checklist_main_eo_class
     
      # записываем в json
      with open("saved_filters.json", "w") as jsonFile:
        json.dump(saved_filters_dict, jsonFile)
    checklist_main_eo_class_values = filter_main_eo_class

    
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

    # Список чек-боксов main_eo_class
    main_eo_class_df = pd.read_csv('data/main_eo_class.csv')
    checklist_main_eo_class_options = functions.main_eo_class_checklist_data(main_eo_class_df)[0]


    # Список чек-боксов level_2
    # eo_class_df = pd.read_csv('data/level_2_list.csv')

    # checklist_eo_class_options = functions.eo_class_checklist_data(eo_class_df)[0]

    ########### фильтр для таблицы по уровню main_eo ###################
    main_eo_all_values = functions.main_eo_class_checklist_data(main_eo_class_df)[1]
    
    # Если селект трогали но он пустой, то отдаем полный список
    if checklist_main_eo_class != None and len(checklist_main_eo_class) == 0:
      main_eo_table_filter = main_eo_all_values
    # если селект не трогали и в сохраненных ничего нет, то тоже отдаем полный список
    elif checklist_main_eo_class == None and len(saved_filters_dict['main_eo_class']) ==0:
      main_eo_table_filter = main_eo_all_values
    elif checklist_main_eo_class == None and len(saved_filters_dict['main_eo_class']) !=0:
      main_eo_table_filter = saved_filters_dict['main_eo_class']
    else:
      main_eo_table_filter=checklist_main_eo_class

    # print("checklist_main_eo_class", checklist_main_eo_class)
    # print("saved_filters_dict['main_eo_class']", saved_filters_dict['main_eo_class'])
    ########### фильтр для таблицы по уровню eo_class ###################
    eo_class_all_values = functions.eo_class_checklist_data(eo_class_df)[1]
    
    # Если селект трогали но он пустой, то отдаем полный список
    if checklist_eo_class != None and len(checklist_eo_class) == 0:
      eo_class_table_filter = eo_class_all_values
    # если селект не трогали и в сохраненных ничего нет, то тоже отдаем полный список
    elif checklist_eo_class == None and len(saved_filters_dict['eo_class']) ==0:
      eo_class_table_filter = eo_class_all_values
    elif checklist_eo_class == None and len(saved_filters_dict['eo_class']) !=0:
      eo_class_table_filter = saved_filters_dict['eo_class']

    else:
      eo_class_table_filter=checklist_eo_class

    
    ########### фильтр для таблицы по уровню level_1 ###################
    
    
    # если в фильтрах level_1 ничего нет, то в таблицу надо отдать все возможные значения
    level_1_all_values = ['first01', 'first05', 'first11']
    
    # Если селект не трогали и нет сохраненных фильтров, то отдаем полный список
    if checklist_level_1 != None and len(checklist_level_1)==0:
      level_1_table_filter = level_1_all_values
    elif checklist_level_1 == None and len(saved_filters_dict['level_1']) ==0:
      level_1_table_filter = level_1_all_values
    elif checklist_level_1 == None and len(saved_filters_dict['level_1']) !=0:
      level_1_table_filter = saved_filters_dict['level_1']
    else:
      level_1_table_filter = checklist_level_1_values
    
    
    ########### таблица с оборудованием ###################
    # отфильтровываем таблицу значениями из селектов
    # print("level_1_table_filter", level_1_table_filter)
    # print("main_eo_table_filter", main_eo_table_filter)
    # print("eo_class_table_filter", eo_class_table_filter)

    eo_df = pd.read_csv('data/full_eo_list.csv', dtype = str)
    
    eo_filtered_df = eo_df.loc[
    eo_df['level_1'].isin(level_1_table_filter) &
    eo_df['eo_class_code'].isin(eo_class_table_filter)&
    eo_df['eo_main_class_code'].isin(main_eo_table_filter)
    
    ]
    
    
    table_list = []
    for index,row in eo_filtered_df.iterrows():
        temp_dict = {}
        eo_code = row['eo_code']
        eo_description = row['eo_description']
        eo_class_description = row['eo_class_description']
        temp_dict['Код ЕО'] = eo_code
        temp_dict['Описание ЕО'] = eo_description
        temp_dict['Класс ЕО'] = eo_class_description
        temp_dict['Техместо'] = row['teh_mesto']

        table_list.append(temp_dict)
    table_df = pd.DataFrame(table_list)
    table_df.to_csv('data/eo_table.csv')
    number_of_rows = len(table_df)
    number_of_rows_text = 'Количество записей: {}'.format(number_of_rows)


    eo_table = dash_table.DataTable(
        # id='table',
        columns=[{"name": i, "id": i} for i in table_df.columns],
        data=table_df.to_dict('records'),
        filter_action='native',
        style_header={
            # 'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell={'textAlign': 'left'},
    )
    
    new_loading_style = loading_style
    return checklist_level_1_values, checklist_level_1_options, checklist_eo_class_values, checklist_eo_class_options, checklist_main_eo_class_values, checklist_main_eo_class_options, eo_table, number_of_rows_text, new_loading_style

############# выгрузка списка EO #################
@app.callback(
    Output("download-excel-eo", "data"),
    Input("btn-download-eo", "n_clicks"),
    prevent_initial_call=True,)
def funct(n_clicks_eo):
    if n_clicks_eo:
        df = pd.read_csv('data/eo_table.csv', dtype=str)
        return dcc.send_data_frame(df.to_excel, "список_ео.xlsx", index=False, sheet_name="список_ео")



if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=False)