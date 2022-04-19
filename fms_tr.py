import pandas as pd

# в regs_df - бойцы, которые находятся в категории
regs_df = pd.read_csv('temp_files/fghtrs.csv')
# кол-во регистраций в категории
number_of_regs = len(regs_df)

# id соревнования
comp_id = 1
# id весовой категории
wc_id = 14

fight_category_data = []

############ ДАННЫЕ О РАУНДЕ ###########
round_no = 0
need_additional_round = False
number_of_fighters = number_of_regs
while number_of_fighters>2:
  # кол-во боев в раунде
  round_fights_qty = number_of_fighters // 2
  # кол-во бойцов в раунде
  number_of_fighters = round_fights_qty * 2
  round_no = round_no + 1  # счетчик кругов в категории
  
  
  
  
  ############## ЕСЛИ ПРОИСХОДИТ ГРУППОВОЙ ТУРНИР, ТО КОЛ_ВО равно предыдущему раунду
  # next_round_fighter_qty = round_fighter_qty
  
  ############ ДАННЫЕ О МЕСТАХ В РАУНДЕ ###########
  round_place = 0
  while round_place < number_of_fighters:
    for color in ["red", "blue"]:  
      round_dict = {}
      round_dict['comp_id'] = comp_id
      round_dict["wc_id"] = wc_id
      round_place = round_place + 1
      round_dict['round_place_no'] = round_place
      round_fighter_place_identifier = "round_place_" +  str(round_place) + "_comp_" + str(comp_id) + "_wc_" + str(wc_id) + "_rndid_" + str(round_no) + "_" + color
      round_dict['round_fighter_place_identifier'] = round_fighter_place_identifier
      round_dict['fighter_occupation_status'] = 'free'
      round_dict['fighter_id'] = 0
      fight_category_data.append(round_dict)
  
  fight_category_df = pd.DataFrame(fight_category_data)
  
  # итерируемся по бойцам и ищем в круге свободной место
  
  for row in regs_df.itertuples():
    fighter_id = getattr(row, "fighter_id")
    # ищем свободное место в списке круга
    fight_category_free_row = fight_category_df.loc[fight_category_df['fighter_occupation_status']=='free'].head(1)
    if len(fight_category_free_row)>0:
      # индекс строки: 
      index_fight_category_free_row = fight_category_free_row.index.values[0]
      # записываем индекс бойца в таблицу круга
      fight_category_df.loc[index_fight_category_free_row, 'fighter_id'] =  fighter_id
      fight_category_df.loc[index_fight_category_free_row, 'fighter_occupation_status'] =  'occupied'
  
  ############ ПРЕДПОЛОЖИМ ЧТО ОЛИМПИЙСКАЯ СИСТЕМА
  # кол-во бойцов в категории в следующем круге - это половина от текущего кол-ва
  number_of_fighters = number_of_fighters / 2  

fight_category_df.to_csv('temp_files/fight_category_df.csv')

