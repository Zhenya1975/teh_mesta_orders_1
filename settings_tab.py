from dash import dcc, html
import dash_bootstrap_components as dbc
import datetime

def settings_tab():
    settings_tab_block = dcc.Tab(
        label='Настройки',
        value='tab_settings',
        children=[
            dbc.Row([
                dbc.Col(
                    children=[

                        
                        html.Div([
                            html.P(),
                            dcc.DatePickerSingle(
                              id='my-date-picker-single',
                              # min_date_allowed=date(1995, 8, 5),
                              # max_date_allowed=date(2017, 9, 19),
                              initial_visible_month=datetime.datetime.now().date(),
                              date=datetime.datetime.now().date()
                          ),
                            html.P(),
                            dbc.Button("Выгрузить шаблон фильтров", id="btn_download_template", size="sm",
                                       style={'marginBottom': '3px',
                                              'marginTop': '3px',
                                              'backgroundColor': '#232632'}, ),
                            dcc.Download(id="download_template")
                        ]),

                        html.P("Загрузка файла"),
                        html.P("filters_template.xlsx, equipment_list.xlsx"),

                        html.Div([
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Перетащи или ',
                                    html.A('выбери файл')
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=True
                            ),
                            html.Div(id='output-data-upload'),
                        ]),


                    ])
                ])

        ])
    return settings_tab_block