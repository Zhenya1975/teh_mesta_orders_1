import pandas as pd
# import numpy as np
from dash import Dash, dcc, html, Input, Output, callback_context, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import datetime
import functions
import eo_tab
import messages_orders_tab
import messages_orders
import orders_moved_tab
import settings_tab
# import orders_tab
from dash import dash_table
import base64
import io
import json
import plotly.graph_objects as go
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
                                messages_orders_tab.messages_orders_tab(),
                                orders_moved_tab.orders_moved_tab(),
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
    Output("checklist_level_upper", "value"),
    Output("checklist_level_upper", "options"),

    Output('eo_table', 'children'),
    Output('number_of_rows_text', 'children'),
    Output('loading', 'parent_style')

],

    [
        Input('checklist_level_1', 'value'),
        Input('checklist_eo_class', 'value'),
        Input('checklist_main_eo_class', 'value'),
        Input('checklist_level_upper', 'value'),

    ],
)
def teh_mesta(
        checklist_level_1,
        checklist_eo_class,
        checklist_main_eo_class,
        checklist_level_upper
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
    
    ################## level_upper VALUES ###################################
    if checklist_level_upper == None:
      filter_level_upper = saved_filters_dict["level_upper"]
      
    else:
      filter_level_upper = checklist_level_upper
      saved_filters_dict["level_upper"] = checklist_level_upper
      # записываем в json
      with open("saved_filters.json", "w") as jsonFile:
        json.dump(saved_filters_dict, jsonFile)
    checklist_level_upper_values = filter_level_upper
    
    ################## eo_class VALUES ###################################
    if checklist_eo_class == None:
      filter_eo_class = saved_filters_dict["eo_class"]
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
    
    ########### фильтр для таблицы по уровню level_upper ###################
    level_upper = pd.read_csv('data/level_upper.csv')
    level_upper.rename(columns={'teh_mesto': 'level_upper'}, inplace=True)
    upper_level_all_values = functions.level_upper_checklist_data(level_upper)[1]
    
    # Если селект трогали но он пустой, то отдаем полный список
    if checklist_level_upper != None and len(checklist_level_upper) == 0:
      level_upper_table_filter = upper_level_all_values
    # если селект не трогали и в сохраненных ничего нет, то тоже отдаем полный список
    elif checklist_level_upper == None and len(saved_filters_dict['level_upper']) ==0:
       level_upper_table_filter = upper_level_all_values
    elif checklist_level_upper == None and len(saved_filters_dict['level_upper']) !=0:
      level_upper_table_filter = saved_filters_dict['level_upper']

    else:
      level_upper_table_filter=checklist_level_upper
    
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

    eo_df = pd.read_csv('data/full_eo_list.csv', dtype = str)
    eo_df["operation_start_date"] = eo_df["operation_start_date"].astype("datetime64[ns]")
    eo_upper_level_df = pd.merge(eo_df, level_upper, on='level_upper', how='left')
    
    level_1 = pd.read_csv('data/level_1.csv')
    
    eo_upper_level_level_1_df = pd.merge(eo_upper_level_df, level_1, on='level_1', how='left')        

    eo_filtered_df = eo_upper_level_level_1_df.loc[
    eo_df['level_1'].isin(level_1_table_filter) &
    eo_df['eo_class_code'].isin(eo_class_table_filter)&
    eo_df['eo_main_class_code'].isin(main_eo_table_filter)&
    eo_df['level_upper'].isin(level_upper_table_filter)    
    ]
    

    table_list = []
    for index,row in eo_filtered_df.iterrows():
        temp_dict = {}
        eo_code = row['eo_code']
        eo_description = row['eo_description']
        eo_class_description = row['eo_class_description']
        temp_dict['Завод'] = row['level_1_description']
        temp_dict['ЕО код'] = eo_code
        temp_dict['ЕО описание'] = eo_description
        temp_dict['Основной Класс ЕО код'] = row['eo_main_class_code']
        temp_dict['Основной Класс ЕО описание'] = row['eo_main_class_description']
        temp_dict['Класс ЕО'] = row['eo_class_code'] + "; " + eo_class_description
        temp_dict['Техместо код'] = row['teh_mesto']
        temp_dict['Техместо описание'] = row['teh_mesto_description']
        temp_dict['Вышестоящее техместо'] = row['level_upper'] + "; " + row['Название технического места']
        
        operation_start_date = row['operation_start_date'].strftime("%d.%m.%Y")
        # print(operation_start_date)
        temp_dict['Дата начала эксплуатации'] = operation_start_date
       

        table_list.append(temp_dict)
    table_df = pd.DataFrame(table_list)
    table_df.to_csv('data/eo_table.csv')
    number_of_rows = len(table_df)
    number_of_rows_text = 'Количество записей: {}'.format(number_of_rows)


    eo_table = dash_table.DataTable(
        # id='table',
        # editable=True,
        columns=[{"name": i, "id": i} for i in table_df.columns],
        data=table_df.to_dict('records'),
        # filter_action='native',
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
    
    eo_class_droplist_options_list = functions.depending_checklists(level_1_table_filter, main_eo_table_filter)

    checklist_eo_class_options = eo_class_droplist_options_list

    level_upper_droplist_option_list = functions.depending_level_upper_checklist(level_1_table_filter, main_eo_table_filter)
    checklist_level_upper_options = level_upper_droplist_option_list

    new_loading_style = loading_style
    
    return checklist_level_1_values, checklist_level_1_options, checklist_eo_class_values, checklist_eo_class_options, checklist_main_eo_class_values, checklist_main_eo_class_options, checklist_level_upper_values, checklist_level_upper_options, eo_table, number_of_rows_text, new_loading_style

############# выгрузка списка EO #################
@app.callback(
    Output("download-excel-eo", "data"),
    Input("btn-download-eo", "n_clicks"),
    prevent_initial_call=True,)
def funct(n_clicks_eo):
    if n_clicks_eo:
        df = pd.read_csv('data/eo_table.csv', dtype=str)
        return dcc.send_data_frame(df.to_excel, "список_ео.xlsx", index=False, sheet_name="список_ео")



@app.callback([
    Output("checklist_basis_start_month_year", "value"),
    Output("checklist_basis_start_month_year", "options"),
    Output('orders_table', 'children'),
    Output('number_of_rows_text_orders', 'children'),
    Output('loading_messages_orders_tab', 'parent_style')
],

    [
        Input('checklist_basis_start_month_year', 'value'),

    ],
)
def orders_messages_tab(checklist_basis_start_month_year):
  with open('saved_filters_messages_orders.json', 'r') as openfile:
      # Reading from json file
      saved_filters_messages_orders_dict = json.load(openfile)
  ########### фильтр для таблицы заказов по фильтру "месяц и год в поле Базисный срок начала" ###################
    
  # если в фильтрах ничего нет, то в таблицу надо отдать все возможные значения
  basis_start_date_all_values = messages_orders.order_data_prepare()[2]
  
  # Список чек-боксов Level_1
  month_year_2022_df = pd.read_csv('data/month_year_2022.csv')
  checklist_month_year_2022_options = functions.month_year_2022_checklist_data(month_year_2022_df)[0]
  
  ################## month_year_2022 VALUES ###################################
  if checklist_basis_start_month_year == None:
    filter_month_year_2022 = saved_filters_messages_orders_dict['basis_start_date_month_year']
  else:
    filter_month_year_2022 = checklist_basis_start_month_year
    saved_filters_messages_orders_dict['basis_start_date_month_year'] = checklist_basis_start_month_year
    
  # записываем в json
  with open("saved_filters_messages_orders.json", "w") as jsonFile:
    json.dump(saved_filters_messages_orders_dict, jsonFile)
  
  # присваиваем значения фильтра в output функции
  checklist_month_year_2022_values = filter_month_year_2022



  # Если селект не трогали и нет сохраненных фильтров, то отдаем полный список
  # print('длина в сохраненном фильтре', len(saved_filters_messages_orders_dict['basis_start_date_month_year']))
  # print('checklist_basis_start_month_year', checklist_basis_start_month_year)
  if checklist_basis_start_month_year != None and len(checklist_basis_start_month_year)==0:
    # print("первый")
    basis_start_month_date_table_filter = basis_start_date_all_values
  elif checklist_basis_start_month_year == None and len(saved_filters_messages_orders_dict['basis_start_date_month_year']) ==0:
    # print("второй")
    basis_start_month_date_table_filter = basis_start_date_all_values
  elif checklist_basis_start_month_year == None and len(saved_filters_messages_orders_dict['basis_start_date_month_year']) !=0:
    # print("третий")
    basis_start_month_date_table_filter = saved_filters_messages_orders_dict['basis_start_date_month_year']
  else:
    # print("четвертый")
    basis_start_month_date_table_filter = checklist_basis_start_month_year

  # print("basis_start_month_date_table_filter", basis_start_month_date_table_filter)
  ############ Фильтруем таблицу с заказами ###############
  orders_df = messages_orders.order_data_prepare()[0]
  # print(basis_start_month_date_table_filter)
  orders_filtered_df = orders_df.loc[
  orders_df['basis_start_month_year'].isin(basis_start_month_date_table_filter)
    ]

  ######### подготовка таблицы для вывода ######################
  table_list = []
  for index,row in orders_filtered_df.iterrows():
    temp_dict = {}
    order_id = row['Заказ']
    basis_start_date = row['БазисСрокНачала']
    plan_date = row['Плановая дата']
    order_user_status = row['ПользСтатус']
    order_system_status = row['СистСтатус']
    tk_downtime_total = row['ОбщееВремяПростояТК']
    order_description = row['Краткий текст']
    message_system_status = row['СистСтатСообщТОРО']
    eo_id = row['Ед. оборудов.']
    teh_mesto_id = row['Техместо']
    spp_order_title = row['СПП-ЗаголЗаказа']

    temp_dict['Заказ'] = order_id
    temp_dict['БазисСрокНачала'] = basis_start_date
    temp_dict['Плановая дата'] = plan_date
    temp_dict['ПользСтатус (заказа)'] = order_user_status
    temp_dict['СистСтатус'] = order_system_status
    temp_dict['ОбщееВремяПростояТК'] = tk_downtime_total
    temp_dict['Краткий текст'] = order_description
    temp_dict['СистСтатСообщТОРО'] = message_system_status
    temp_dict['ЕО; teh_mesto; СПП-ЗаголЗаказа'] = str(eo_id) + "\n" + str(teh_mesto_id) + "\n" + str(spp_order_title)


    table_list.append(temp_dict)
  order_table_df = pd.DataFrame(table_list)
  order_table_df.to_csv('data/order_table_df.csv')
  number_of_rows = len(order_table_df)
  number_of_rows_text_orders = 'Количество записей: {}'.format(number_of_rows)


  orders_table = dash_table.DataTable(
        # id='table',
        columns=[{"name": i, "id": i} for i in order_table_df.columns],
        data=order_table_df.to_dict('records'),
        # filter_action='native',
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

  orders_new_loading_style = loading_style

  return checklist_month_year_2022_values, checklist_month_year_2022_options, orders_table, number_of_rows_text_orders, orders_new_loading_style


############# Обработчик вкладки Переносы заказов ########################
@app.callback([
    Output("checklist_basis_start_date_orders_moved_tab", "value"),
    Output("checklist_basis_start_date_orders_moved_tab", "options"),
    Output('loading_orders_moved_tab', 'parent_style'),
    Output('orders_moved_from_jan', 'figure')
],

    [
        Input('checklist_basis_start_date_orders_moved_tab', 'value'),

    ],
)
def orders_moved_tab(checklist_basis_start_date_orders_moved_tab):
  with open('saved_filters_orders_moved.json', 'r') as openfile:
      # Reading from json file
      saved_filters_orders_moved_dict = json.load(openfile)
  ########### фильтр для таблицы заказов по фильтру "месяц и год в поле Базисный срок начала" ###################
    
  # если в фильтрах ничего нет, то в таблицу надо отдать все возможные значения
  # basis_start_date_all_values = messages_orders.order_data_prepare()[2]
  
  
  month_year_2022_df = pd.read_csv('data/month_year_2022.csv')
  checklist_orders_moved_tab_month_year_2022_options = functions.month_year_2022_checklist_data(month_year_2022_df)[0]
  
  ################## month_year_2022 VALUES ###################################
  if checklist_basis_start_date_orders_moved_tab == None:
    filter_month_year_2022_orders_moved_tab = saved_filters_orders_moved_dict['target_period_month_year']
  else:
    filter_month_year_2022_orders_moved_tab = checklist_basis_start_date_orders_moved_tab
    saved_filters_orders_moved_dict['target_period_month_year'] = checklist_basis_start_date_orders_moved_tab
    
  # записываем в json
  with open("saved_filters_orders_moved.json", "w") as jsonFile:
    json.dump(saved_filters_orders_moved_dict, jsonFile)
  
  # присваиваем значения фильтра в output функции
  checklist_month_year_2022_orders_moved_tab_values = filter_month_year_2022_orders_moved_tab



  orders_moved_new_loading_style = loading_style

  x = ['январь', 'февраль', 'март', 'апрель']
  y1 = [20, 0, 0, 0]
  y2 = [12, 0, 0, 0]
  y3 = [0, 3, 2, 7]

  fig = go.Figure()
  fig = go.Figure(data=[
    go.Bar(name='Запланированные на январь и оставшиеся в январе', x=x, y=y1, marker_color='green', text=y1,textposition='auto',),
    go.Bar(name='Перенесенные с января. В январском столбике', x=x, y=y2, marker_color='red', text=y2,textposition='auto'),
    go.Bar(name='Перенесенные с января', x=x, y=y3, marker_color='#ffcccb', text=y3, textposition='auto')
  ])


  fig.update_layout(
      barmode='stack',
      yaxis = {'range':[0, 50]},
      legend=dict(
          orientation="h",
          yanchor="bottom",
          y=1.02,
          xanchor="right",
          x=1
      )
      
      # template=graph_template,
      # xaxis={'range': [start_quarter_date, finish_quarter_date]},
      # title='Завершено: {}<br><sup>c {} по {}</sup> '.format(fact_at_current_date, start_date, finish_date),
  )

  return checklist_month_year_2022_orders_moved_tab_values, checklist_orders_moved_tab_month_year_2022_options, orders_moved_new_loading_style, fig







if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=False)