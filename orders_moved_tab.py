from dash import dcc, html
import dash_bootstrap_components as dbc
loading_style = {
    # 'position': 'absolute',
    # 'align-self': 'center'
                 }
def orders_moved_tab():
    orders_moved_tab_block = dcc.Tab(
        label='Заказы. Переносы',
        value='tab_orders_moved',
        children=[
            dcc.Loading(id='loading_orders_moved_tab', parent_style=loading_style),
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
                                    html.P(),
                                    html.Div([
                                      "Базисный срок начала. Месяц, год",
                                      dcc.Dropdown(id="checklist_basis_start_date_orders_moved_tab", multi=True),
                                  ]),
                                ],
                                title="Заказы",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P(),
                                    html.Div([
                                      "Техместа. Уровень 1",
                                      dcc.Dropdown(id="checklist_level_1_orders_moved_tab", multi=True),
                                  ]),


                                    html.P(),
                                    html.Div([
                                      "EO Основной Класс",
                                      dcc.Dropdown(id="checklist_main_eo_class_orders_moved_tab", multi=True),
                                  ]),
                                    
                                    html.P(),
                                    html.Div([
                                      "EO Класс",
                                      dcc.Dropdown(id="checklist_eo_class_orders_moved_tab", multi=True),
                                  ]),
                                    
                                    
                                    
                                    html.P(),
                                    html.Div([
                                      "Техместа. Уровень 2",
                                      dcc.Dropdown(id="checklist_level_2_orders_moved_tab", multi=True),
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

                                 
                                ],
                                title="EO",
                            ),
                            
                            
                        ],
                    )
                )

                    
                  ]
                ),
                dbc.Col(width=9,
                    children=[
                      html.P('Выборка: "arm_planir_new_plan_date_2.csv" группа: Самосвалы карьерные HD1500-8 в "03. Полюс Вернинское" из АРМ Планировщик с данными от 31.01.2022'),
                      html.P(),
                      html.P(id='total_number_of_orders_in_january'), # Общее количество заказов, которые были запланированы в январе
                     
                        


                    ]),
                
            ])
            
        ]

    )        
            
        

    return orders_moved_tab_block