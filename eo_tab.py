from dash import dcc, html
import dash_bootstrap_components as dbc
loading_style = {
    # 'position': 'absolute',
    # 'align-self': 'center'
                 }
def eo_tab():
    select_filters_tab_block = dcc.Tab(
        label='Выбор параметров техмест',
        value='tab_select_parameters',
        children=[
            dcc.Loading(id='loading', parent_style=loading_style),
            dbc.Row(justify="start",
            children = [
              
              html.Div([
                dbc.Button("Выгрузить список EO xlsx", id="btn-download-eo", size="sm",
                                    style={'marginBottom': '3px',
                                            'marginTop': '3px',
                                            'backgroundColor': '#232632'},),
                dcc.Download(id="download-excel-eo")
              ])


            ]),

            dbc.Row([
                # колонка с фильтрами
                dbc.Col(width=4,
                  children=[
                    
                    html.P(),
                    html.Div([
                      "Техместа. Уровень 1",
                      dcc.Dropdown(id="checklist_level_1", multi=True),
                  ]),


                    html.P(),
                    html.Div([
                      "EO Основной Класс",
                      dcc.Dropdown(id="checklist_main_eo_class", multi=True),
                  ]),
                    
                    html.P(),
                    html.Div([
                      "EO Класс",
                      dcc.Dropdown(id="checklist_eo_class", multi=True),
                  ]),
                    
                    
                    
                    html.P(),
                    html.Div([
                      "Техместа. Уровень 2",
                      dcc.Dropdown(id="checklist_level_2", multi=True),
                  ]),

                  #html.P(),
                  #  html.Div([
                  #    "Уровень 3",
                  #    dcc.Dropdown(id="checklist_level_3", multi=True),
                  #]),

                  # html.P(),
                  #  html.Div([
                  #    "Уровень 4",
                  #    dcc.Dropdown(id="checklist_level_4", multi=True),
                  #]),

                  #html.P(),
                  #  html.Div([
                  #    "Уровень 5",
                  #    dcc.Dropdown(id="checklist_level_5", multi=True),
                  #]),

                  html.P(),
                    html.Div([
                      "Уровень Вышестоящее техместо",
                      dcc.Dropdown(id="checklist_level_upper", multi=True),
                  ]),
                  ]
                ),
                dbc.Col(width=8,
                    children=[
                        html.P(id='number_of_rows_text'),
                        
                        html.P(),
                        html.Div(
                            children=[
                                html.Div(id='eo_table'),
                                # dcc.Loading(id='loading', parent_style=loading_style)
                            ], style={
                                # 'position': 'relative',
                                # 'display': 'flex',
                                'justify-content': 'center'
                                      }
                            ),


                    ]),
                
            ]),
            #dbc.Row([
                
            #]),
        
        ]
    )
    return select_filters_tab_block