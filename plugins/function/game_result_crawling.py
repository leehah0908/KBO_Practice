def game_result():
    import warnings
    warnings.filterwarnings(action="ignore")

    import time
    from datetime import datetime
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    today_dt = str(datetime.today()).split(' ')[0]

    game_id_list = []
    date_list = []
    home_team_list = []
    away_team_list = []
    home_score_list = []
    away_score_list = []
    status_list = []
    winner_team_list = []

    gmae_center_url = 'https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx'

    driver = webdriver.Chrome()
    driver.get(gmae_center_url)
    driver.maximize_window()
    time.sleep(1)

    game_cnt = driver.find_elements(By.XPATH, f'//*[@id="contents"]/div[3]/div/div[1]/ul/li')

    for index, game_th in enumerate(game_cnt, start = 1):
        away_score = home_score = winner_team = ''

        date = game_th.get_attribute('g_dt')
        status = game_th.get_attribute('class').split(' ')[-1]
        game_id = game_th.get_attribute('g_id')
        away_team = game_th.get_attribute('away_nm')
        home_team = game_th.get_attribute('home_nm')

        if status == 'cancel':
            continue

        away_score = game_th.find_element(By.XPATH, f'//*[@id="contents"]/div[3]/div/div[1]/ul/li[{index}]/div[2]/div[2]/div[1]/div[2]').text
        home_score = game_th.find_element(By.XPATH, f'//*[@id="contents"]/div[3]/div/div[1]/ul/li[{index}]/div[2]/div[2]/div[3]/div[2]').text

        if int(away_score) > int(home_score):
            winner_team = away_team
        elif int(away_score) < int(home_score):
            winner_team = home_team
        elif int(away_score) == int(home_score):
            winner_team = 'Draw'

        date_list.append(date)
        status_list.append(status)
        game_id_list.append(game_id)
        away_team_list.append(away_team)
        home_team_list.append(home_team)
        away_score_list.append(away_score)
        home_score_list.append(home_score)
        winner_team_list.append(winner_team)

        # 더블헤더
        if len(game_cnt) > 5 and index == 5:
            try:
                driver.find_element(By.XPATH, '//*[@id="contents"]/div[3]/div/div[2]/div/a[2]').click()
                driver.implicitly_wait(1)
            except:
                continue

    driver.quit()

    game_df = pd.DataFrame({'date' : date_list,
                       'status' : status_list,
                       'game_id' : game_id_list,
                       'away_team' : away_team_list,
                       'home_team' : home_team_list,
                       'away_score' : away_score_list,
                       'home_score' : home_score_list,
                       'winner_team' : winner_team_list})

    game_df.to_csv(f'/opt/airflow/files/game_detail_{today_dt}.csv', encoding = 'utf-8', index = False)


def game_detail_result():
    import warnings
    warnings.filterwarnings(action="ignore")

    import time
    from datetime import datetime
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    today_dt = str(datetime.today()).split(' ')[0]

    game_id_list = []
    field_list = []
    nth_list = []
    broadcast_list = []
    game_time_list = []
    away_team_starting_pitcher_list = []
    home_team_starting_pitcher_list = []
    winning_pitcher_list = []
    losing_pitcher_list = []
    save_pitcher_list = []
    hitting_key_player_list = []
    pitching_key_player_list = []
    runtime_list = []
    crowd_list = []

    # 경기 디테일 내용
    winning_hit_list = []
    home_run_list = []
    double_list = []
    triple_list = []
    error_list = []
    double_play_list = []
    stolen_base_list = []
    caught_stealing_list = []
    run_out_list = []
    pickoff_list = []
    passed_ball_list = []
    wild_pitch_list = []
    umpire_list = []

    detail_mapping = {'결승타': winning_hit_list,
                    '홈런': home_run_list,
                    '2루타': double_list,
                    '3루타': triple_list,
                    '실책': error_list,
                    '병살타': double_play_list,
                    '도루': stolen_base_list,
                    '도루자': caught_stealing_list,
                    '주루사': run_out_list,
                    '견제사': pickoff_list,
                    '포일': passed_ball_list,
                    '폭투': wild_pitch_list,
                    '심판': umpire_list
                    }

    gmae_center_url = 'https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx'

    driver = webdriver.Chrome()
    driver.get(gmae_center_url)
    driver.maximize_window()
    time.sleep(1)

    game_cnt = driver.find_elements(By.XPATH, f'//*[@id="contents"]/div[3]/div/div[1]/ul/li')

    for index, game_th in enumerate(game_cnt, start = 1):
        game_id = game_th.get_attribute('g_id')
        status = game_th.get_attribute('class').split(' ')[-1]

        field = game_th.get_attribute('s_nm')
        nth = game_th.get_attribute('vs_game_cn')
        broadcast = game_th.find_element(By.XPATH, './div[2]/div[1]').text
        game_time = game_th.find_element(By.XPATH, './div[1]/ul/li[2]').text

        # 정보가 없으면 null값을 넣어야 하기 때문에 초기화
        winning_pitcher = losing_pitcher = save_pitcher = hitting_key_player = pitching_key_player = runtime = crowd = ''

        detail_dic = {key: None for key in detail_mapping.keys()}

        if status == 'cancel':
            away_team_starting_pitcher = game_th.find_element(By.XPATH, f'./div[2]/div[2]/div[1]/div[2]/p').text.replace("선", "")
            home_team_starting_pitcher = game_th.find_element(By.XPATH, f'./div[2]/div[2]/div[3]/div[2]/p').text.replace("선", "")

        elif status == 'end':
            game_th.click()
            driver.implicitly_wait(1)
            pitching_key_player = driver.find_element(By.XPATH, f'//*[@id="gameCenterContents"]/div[3]/dl[1]/dd[2]').text

            driver.find_element(By.XPATH, '//*[@id="gameCenterContents"]/div[1]/ul/li[2]/a').click()
            driver.implicitly_wait(1)
            hitting_key_player = driver.find_element(By.XPATH, f'//*[@id="gameCenterContents"]/div[3]/dl[1]/dd[2]').text

            driver.find_element(By.XPATH, '//*[@id="tabDepth2"]/li[2]').click()
            driver.implicitly_wait(1)

            tmp_pitcher_list = game_th.find_elements(By.XPATH, f'./div[2]/div[2]/div/div[3]/p')

            if len(tmp_pitcher_list) == 3:
                for tmp_pitcher_th in tmp_pitcher_list:
                    if tmp_pitcher_th.text[0] == '승':
                        winning_pitcher = tmp_pitcher_th.text[1:]
                    elif tmp_pitcher_th.text[0] == '패':
                        losing_pitcher = tmp_pitcher_th.text[1:]
                    elif tmp_pitcher_th.text[0] == '세':
                        save_pitcher = tmp_pitcher_th.text[1:]
            elif len(tmp_pitcher_list) == 2:
                for tmp_pitcher_th in tmp_pitcher_list:
                    if tmp_pitcher_th.text[0] == '승':
                        winning_pitcher = tmp_pitcher_th.text[1:]
                    elif tmp_pitcher_th.text[0] == '패':
                        losing_pitcher = tmp_pitcher_th.text[1:]
                    elif tmp_pitcher_th.text[0] == '무':
                        winning_pitcher = ''
                        losing_pitcher = ''
                save_pitcher = ''

            runtime_hour = int(game_th.find_element(By.XPATH, f'//*[@id="txtRunTime"]').text.split(' ')[2].split(':')[0])
            runtime_min = int(game_th.find_element(By.XPATH, f'//*[@id="txtRunTime"]').text.split(' ')[2].split(':')[1])
            runtime = (runtime_hour*60) + runtime_min
            crowd = int(game_th.find_element(By.XPATH, f'//*[@id="txtCrowd"]').text.split(' ')[2].replace(",", ""))

            away_team_starting_pitcher = driver.find_element(By.XPATH, f'//*[@id="tblAwayPitcher"]/tbody/tr[1]/td[1]').text
            home_team_starting_pitcher = driver.find_element(By.XPATH, f'//*[@id="tblHomePitcher"]/tbody/tr[1]/td[1]').text

            list = game_th.find_elements(By.XPATH, '//*[@id="tblEtc"]/tbody/tr')
            for tmp_detail in list:
                tmp_detail_item = tmp_detail.find_element(By.XPATH, './th').text
                tmp_detail_contents = tmp_detail.find_element(By.XPATH, './td').text

                if tmp_detail_item in detail_mapping:
                    detail_dic[tmp_detail_item] = tmp_detail_contents
        
        game_id_list.append(game_id)
        field_list.append(field)
        nth_list.append(nth)
        broadcast_list.append(broadcast)
        game_time_list.append(game_time)
        away_team_starting_pitcher_list.append(away_team_starting_pitcher)
        home_team_starting_pitcher_list.append(home_team_starting_pitcher)
        winning_pitcher_list.append(winning_pitcher)
        losing_pitcher_list.append(losing_pitcher)
        save_pitcher_list.append(save_pitcher)
        hitting_key_player_list.append(hitting_key_player)
        pitching_key_player_list.append(pitching_key_player)
        runtime_list.append(runtime)
        crowd_list.append(crowd)

        for key, lst in detail_mapping.items():
            try:
                lst.append(detail_dic[key])
            except:
                lst.append('')
        
        if len(game_cnt) > 5 and index == 5:
            try:
                driver.find_element(By.XPATH, '//*[@id="contents"]/div[3]/div/div[2]/div/a[2]').click()
                driver.implicitly_wait(1)
            except:
                continue

    driver.quit()

    game_detail_df = pd.DataFrame({'game_id_list' : game_id_list,
                                   'field_list' : field_list,
                                   'nth_list' : nth_list,
                                   'broadcast_list' : broadcast_list,
                                   'game_time_list' : game_time_list,
                                   'away_team_starting_pitcher_list' : away_team_starting_pitcher_list,
                                   'home_team_starting_pitcher_list' : home_team_starting_pitcher_list,
                                   'winning_pitcher_list' : winning_pitcher_list,
                                   'losing_pitcher_list' : losing_pitcher_list,
                                   'save_pitcher_list' : save_pitcher_list,
                                   'hitting_key_player_list' : hitting_key_player_list,
                                   'pitching_key_player_list' : pitching_key_player_list,
                                   'runtime_list' : runtime_list,
                                   'crowd_list' : crowd_list})

    game_detail_df.to_csv(f'/opt/airflow/files/game_detail_{today_dt}.csv', encoding = 'utf-8', index = False)