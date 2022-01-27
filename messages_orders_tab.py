from dash import dcc, html
import dash_bootstrap_components as dbc
loading_style = {
    # 'position': 'absolute',
    # 'align-self': 'center'
                 }
def messages_orders_tab():
    messages_orders_tab_block = dcc.Tab(
        label='Сообщения. Заказы',
        value='tab_messages_orders',
        children=[
            dcc.Loading(id='loading_messages_orders_tab', parent_style=loading_style),
            dbc.Row([
              # колонка с фильтрами
                dbc.Col(width=3,
                  children=[
                    html.Div(
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    html.P(),
                                    html.Div([
                                      "Техместа. Уровень 1",
                                      dcc.Dropdown(id="checklist_level_1_messages_orders_tab", multi=True),
                                  ]),


                                    html.P(),
                                    html.Div([
                                      "EO Основной Класс",
                                      dcc.Dropdown(id="checklist_main_eo_class_messages_orders_tab", multi=True),
                                  ]),
                                    
                                    html.P(),
                                    html.Div([
                                      "EO Класс",
                                      dcc.Dropdown(id="checklist_eo_class_messages_orders_tab", multi=True),
                                  ]),
                                    
                                    
                                    
                                    html.P(),
                                    html.Div([
                                      "Техместа. Уровень 2",
                                      dcc.Dropdown(id="checklist_level_2_messages_orders_tab", multi=True),
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
                                      dcc.Dropdown(id="checklist_level_upper_messages_orders_tab", multi=True),
                                  ]),
                                ],
                                title="EO",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("This is the content of the second section"),
                                    dbc.Button("Don't click me!", color="danger"),
                                ],
                                title="Item 2",
                            ),
                            dbc.AccordionItem(
                                "This is the content of the third section",
                                title="Item 3",
                            ),
                        ],
                    )
                )

                    
                  ]
                ),
            ])
            
        ]

    )        
            
        

    return messages_orders_tab_block