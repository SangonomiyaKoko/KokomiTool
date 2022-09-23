import requests
import json
import os
import configparser
import base64
import time
import sys


# class Token():
#     temp_dict = {}
#     string_temp = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#                    'abcdefghijklmnopqrstuvwxyz'
#                    '0123456789+/')
#     ascii_string = ''.join([chr(i) for i in range(4, 2 ** 7 - 1)])

#     def __init__(self, string):
#         self.string = string
#         for i in range(2 ** 6):
#             self.temp_dict[i] = self.string_temp[i]

#     def convert(self):
#         string_encode_byte = self.string.encode('utf-8')
#         string_digit_list = list(string_encode_byte)
#         string_bin_list = []
#         for item in string_digit_list:
#             string_bin_list.append(str(bin(item))[2:].zfill(8))
#         string_sum = ''.join(string_bin_list)
#         string_fill = self.fillIt(string_sum, factor=6, item='0')
#         string_bin_list2 = self.splitIt(string_fill, bits=6)
#         string_digit_list2 = []
#         for item in string_bin_list2:
#             string_digit_list2.append(int(item, 2))
#         string_base64_list = []
#         for item in string_digit_list2:
#             string_base64_list.append(self.temp_dict[item])
#         string_sum2 = ''.join(string_base64_list)
#         string_convert = self.fillIt(string_sum2, factor=4, item='=')
#         return string_convert

#     def fillIt(self, string, factor, item):
#         length = len(string)
#         remainder = length % factor
#         if remainder:
#             times = factor - remainder
#             string = string + times * item
#         return string

#     def splitIt(self, string, bits):
#         length = len(string)
#         new_list = []
#         for i in range(bits, length + 1, bits):
#             new_list.append(string[i - bits:i])
#             remain = length % bits
#         if remain != 0:
#             new_list.append(string[-remain:])
#         return new_list


# if __name__ == '__main__':
#     string = input()
#     myBase64 = Token(string)
#     enc_string = myBase64.convert()
#     print("测试字符串：{}".format(string))
#     print("base64：{}".format(enc_string))
# exit()


class OutputFormat():
    def space(num: int) -> str:
        out_msg = ''
        for i in range(num):
            out_msg += ' '
        return out_msg

    def string_format(message: str, all_len: int, keep_right: bool) -> str:
        if message == '0':
            message = '-'
        msg_len = len(message)
        if keep_right:
            return message + OutputFormat.space(all_len - msg_len)
        else:
            return OutputFormat.space(all_len - msg_len) + message

    def number_format(number: int) -> str:
        return '{:,}'.format(number)

    def out_of_range(message: str, max_len: int) -> str:
        if len(message) > max_len:
            message = message[:max_len-3]
            return message + '...'
        else:
            return message


def get_ship_info(ship_id: int):
    global APPLICATION_ID
    global sub_data
    request_url = 'https://api.worldofwarships.asia/wows/encyclopedia/ships/?application_id={}&ship_id={}'.format(
        APPLICATION_ID, str(ship_id))
    try:
        request_data = requests.get(url=request_url, timeout=10)
    except:
        print(f'请求数据失败，url:{request_url}\n请检查网络并重启程序')
        input('Press Enter to exit...')
        exit()
    data = json.loads(request_data.text)
    request_data.close()
    if data['data'][str(ship_id)] == None:
        if ship_id in sub_data:
            ship_tier = sub_data[ship_id]['tier']
            ship_type = 'Submarine'
            ship_name = sub_data[ship_id]['name']
        else:
            ship_tier = 0
            ship_type = 'Unknow'
            ship_name = 'Test Ship'
    else:
        ship_tier = data['data'][str(ship_id)]['tier']
        ship_type = data['data'][str(ship_id)]['type']
        ship_name = data['data'][str(ship_id)]['name']

    return (ship_tier, ship_type, ship_name, output_ship_name(ship_tier, ship_type, ship_name))


def output_ship_name(ship_tier: int, ship_type: str, ship_name: str):
    ship_type_code = {
        'AirCarrier': 'CV',
        'Battleship': 'BB',
        'Cruiser': 'CA',
        'Destroyer': 'DD',
        'Submarine': 'SS',
        'Unknow': 'UN'
    }
    if len(ship_name) > 17:
        out_shipname = OutputFormat.out_of_range(ship_name, 17)
    else:
        out_shipname = OutputFormat.string_format(ship_name, 17, True)
    output_msg = 'T{} {} {}'.format(OutputFormat.string_format(
        str(ship_tier), 2, True), ship_type_code[ship_type], out_shipname)
    return output_msg


def get_ship_code(ship_info: tuple) -> int:
    type_list = {
        'AirCarrier': 8,
        'Battleship': 6,
        'Cruiser': 4,
        'Destroyer': 2,
        'Submarine': 0
    }
    ship_code = type_list[ship_info[1]]*10 + ship_info[0]
    return ship_code


def get_application_id(token: str) -> str:
    decode = base64.b64decode(token + '=')
    return decode.decode("utf-8")

# 获取服务器数据用于计算person rate


server_data = None
# 潜艇数据, 傻逼毛子的api接口没给
sub_data = {
    4179015472: {
        'tier': 10,
        'type': 'Submarine',
        'name': 'U_2501'
    },
    4179015664: {
        'tier': 10,
        'type': 'Submarine',
        'name': 'Balao'
    },
    4181112624: {
        'tier': 8,
        'type': 'Submarine',
        'name': 'U190'
    },
    4181112816: {
        'tier': 8,
        'type': 'Submarine',
        'name': 'Salmon'
    },
    4183209776: {
        'tier': 6,
        'type': 'Submarine',
        'name': 'U_69'
    },
    4183209968: {
        'tier': 6,
        'type': 'Submarine',
        'name': 'Cachalot'
    },
}


def get_pr_box(pr: int):
    if pr == -1:
        PR = "-          水平未知"
        diff = 0
    elif pr >= 0 and pr < 750:
        PR = "*          还需努力"
        diff = int(750-pr)
    elif pr >= 750 and pr < 1100:
        PR = "**         低于平均"
        diff = int(1100-pr)
    elif pr >= 1100 and pr < 1350:
        PR = "***        平均水平"
        diff = int(1350-pr)
    elif pr >= 1350 and pr < 1550:
        PR = "****       好"
        diff = int(1550-pr)
    elif pr >= 1550 and pr < 1750:
        PR = "*****      很好"
        diff = int(1750-pr)
    elif pr >= 1750 and pr < 2100:
        PR = "******     非常好"
        diff = int(2100-pr)
    elif pr >= 2100 and pr < 2450:
        PR = "*******    大佬平均"
        diff = int(2450-pr)
    elif pr >= 2450:
        PR = "********   神佬平均"
        diff = int(pr-2450)
    return (PR, diff)


def get_server_data():
    request_url = 'https://api.wows-numbers.com/personal/rating/expected/json/'
    try:
        request_data = requests.get(url=request_url, timeout=10)
    except:
        print(f'请求数据失败，url:{request_url}\n请检查网络并重启程序')
        input('Press Enter to exit...')
        exit()
    data = json.loads(request_data.text)
    request_data.close()
    return data

# temp文件路径


def get_temp_data_path() -> str:
    global WOWS_GAME_PATH
    global GAME_VERSON
    if os.path.exists(WOWS_GAME_PATH + '\\replays\\' + GAME_VERSON):
        return WOWS_GAME_PATH + '\\replays\\' + GAME_VERSON + '\\tempArenaInfo.json'
    else:
        return WOWS_GAME_PATH + '\\replays\\tempArenaInfo.json'

# 游戏文件路径


def get_game_exe_path() -> str:
    global WOWS_GAME_PATH
    return WOWS_GAME_PATH + '\\WorldOfWarships.exe'

# 测试网络


def test_netwoek(server: str):
    global APPLICATION_ID
    global server_data
    try:
        url_list = [
            'https://api.worldofwarships.{}/wows/account/list/?application_id={}&search={}'.format(
                server, APPLICATION_ID, '2030_1'),
            'http://vortex.worldofwarships.{}/api/accounts/{}/ships/{}/pvp/'.format(
                server, 2023619512, 4277090288,)
        ]
        for url in url_list:
            requests.get(url=url, timeout=5)
        server_data = get_server_data()

        return 0
    except:
        return -1


def get_user_camp(user_number: int) -> str:
    if user_number in [0, 1]:
        return 'teammate'
    else:
        return 'enemy'
# 获取请求数据的服务器


def get_request_server(server: str) -> str:
    if server == 'na':
        return 'com'
    else:
        return server

# 获取战斗类型代码,请求数据用


def get_match_group(match_group: str) -> str:
    global gametype
    global battles_type
    group_list = {
        'ranked': 'rank_solo',
        'pvp': 'pvp'
    }
    if match_group not in group_list:
        gametype = True
        return 'pvp'
    else:
        battles_type = group_list[match_group]
        return group_list[match_group]

# 获取用户account_id


def get_user_account_id(user_name: str, server: str) -> int:
    global APPLICATION_ID
    request_url = 'https://api.worldofwarships.{}/wows/account/list/?application_id={}&language=en&search={}'.format(
        get_request_server(server), APPLICATION_ID, user_name)
    try:
        request_data = requests.get(url=request_url, timeout=10)
    except:
        try:
            request_data = requests.get(url=request_url, timeout=10)
        except:
            print(f'请求数据失败\n请检查网络并重启程序')
            input('Press Enter to exit...')
            exit()
    data = json.loads(request_data.text)
    request_data.close()
    return data['data'][0]['account_id']

# 获取用户的clan信息


def get_clan_name(account_id: int, server: str):
    global APPLICATION_ID
    clan_id_url = 'http://api.worldofwarships.{}/wows/clans/accountinfo/?application_id={}&language=en&account_id={}'.format(
        get_request_server(server), APPLICATION_ID, str(account_id))
    try:
        clan_id_original_data = requests.get(url=clan_id_url, timeout=10)
    except:
        try:
            clan_id_original_data = requests.get(url=clan_id_url, timeout=10)
        except:
            print(f'请求数据失败\n请检查网络并重启程序')
            input('Press Enter to exit...')
            exit()
    clan_id_processed_data = json.loads(clan_id_original_data.text)
    clan_id_original_data.close()
    if clan_id_processed_data["data"][str(account_id)] != None:
        clan_id = clan_id_processed_data["data"][str(account_id)]["clan_id"]
        if clan_id == None:
            clan_name = ""
        elif clan_id == "":
            clan_name = ""
        else:
            clan_name_url = 'http://api.worldofwarships.{}/wows/clans/info/?application_id={}&language=en&clan_id={}'.format(
                get_request_server(server), APPLICATION_ID, str(clan_id))
            try:
                clan_name_original_data = requests.get(
                    url=clan_name_url, timeout=10)
            except:
                try:
                    clan_name_original_data = requests.get(
                        url=clan_name_url, timeout=10)
                except:
                    print(f'请求数据失败\n请检查网络并重启程序')
                    input('Press Enter to exit...')
                    exit()
            clan_name_processed_data = json.loads(clan_name_original_data.text)
            clan_name_original_data.close()
            if clan_name_processed_data["status"] == "error":
                clan_name = ""
            else:
                clan_name = clan_name_processed_data["data"][str(
                    clan_id)]["tag"]

            return clan_name
    return ""

# 获取用户船只数据，并写入user_data


def get_user_shipdata(account_id: int, ship_id: int, server: str, match_group: str):
    global user_data
    global is_end
    request_url = 'http://vortex.worldofwarships.{}/api/accounts/{}/ships/{}/{}/'.format(
        get_request_server(server), account_id, ship_id, get_match_group(match_group))
    try:
        request_data = requests.get(url=request_url, timeout=10)
    except:
        try:
            request_data = requests.get(url=request_url, timeout=10)
        except:
            print(f'请求数据失败，url:{request_url}\n请检查网络并重启程序')
            input('Press Enter to exit...')
            exit()
    data = json.loads(request_data.text)
    request_data.close()
    if 'hidden_profile' in data['data'][str(account_id)]:      # 判断是否隐藏战绩
        dict_data = {
            'hidden': True,
            'data': None
        }
        user_data[account_id] = dict_data
    else:       # 写入数据
        try:
            ship_data = data['data'][str(account_id)]['statistics'][str(
                ship_id)][get_match_group(match_group)]
            dict_data = {
                'hidden': False,
                'data': {
                    'battles_count': ship_data['battles_count'],
                    'art_agro': ship_data['art_agro'],
                    'original_exp': ship_data['original_exp'],
                    'frags': ship_data['frags'],
                    'wins': ship_data['wins'],
                    'hits_by_main': ship_data['hits_by_main'],
                    'shots_by_main': ship_data['shots_by_main'],
                    'planes_killed': ship_data['planes_killed'],
                    'survived': ship_data['survived'],
                    'ships_spotted': ship_data['ships_spotted'],
                    'control_captured_points': ship_data['control_captured_points'],
                    'control_dropped_points': ship_data['control_dropped_points'],
                    'damage_dealt': ship_data['damage_dealt'],
                    'scouting_damage': ship_data['scouting_damage']
                }
            }
            if is_end == {}:
                temp_dict = {
                    'account_id': account_id,
                    'server': get_request_server(server),
                    'ship_id': ship_id,
                    'type': get_match_group(match_group),
                    'battles': ship_data['battles_count']
                }
                is_end = temp_dict
        except:
            dict_data = {
                'hidden': False,
                'data': {
                    'battles_count': 0,
                    'art_agro': 0,
                    'original_exp': 0,
                    'frags': 0,
                    'wins': 0,
                    'hits_by_main': 0,
                    'shots_by_main': 0,
                    'planes_killed': 0,
                    'survived': 0,
                    'ships_spotted': 0,
                    'control_dropped_points': 0,
                    'control_captured_points': 0,
                    'damage_dealt': 0,
                    'scouting_damage': 0
                }
            }
        user_data[account_id] = dict_data


def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)
# 计算船只的评级（Person Rate）,计算公式及数据来自wows number


def get_pvp_pr(average_damage_dealt: float, average_wins: float, average_kd: float, ship_id: int):
    global server_data
    userserverdata = server_data
    if str(ship_id) not in userserverdata['data']:
        return (-1, 0, 0)
    if userserverdata['data'][str(ship_id)] == []:
        return (-1, 0, 0)
    server_damage_dealt = userserverdata['data'][str(
        ship_id)]['average_damage_dealt']
    server_frags = userserverdata['data'][str(ship_id)]['average_frags']
    server_wins = userserverdata['data'][str(ship_id)]['win_rate']
    if average_damage_dealt > server_damage_dealt*0.4:
        n_damage = (average_damage_dealt-server_damage_dealt *
                    0.4)/(server_damage_dealt*0.6)
    else:
        n_damage = 0
    if average_wins > server_wins*0.7:
        n_win_rate = (average_wins-server_wins*0.7) / \
            (server_wins*0.3)
    else:
        n_win_rate = 0
    if average_kd > server_frags*0.1:
        n_kd = (average_kd-server_frags*0.1)/(server_frags*0.9)
    else:
        n_kd = 0
    pr = 700*n_damage+300*n_kd+150*n_win_rate
    return (pr, n_damage, n_kd)

# 获取并写入数据


def begin_battle():
    global SET_SERVER
    global player_id
    global user_data
    global player_info
    file_data = open(get_temp_data_path(), "r", encoding="utf-8")
    temp_data = json.load(file_data)
    file_data.close()
    match_group = temp_data['matchGroup']
    for i in range(len(temp_data['vehicles'])):
        user_name = temp_data['vehicles'][i]['name']
        account_id = get_user_account_id(user_name, SET_SERVER)
        ship_id = temp_data['vehicles'][i]['shipId']
        user_number = temp_data['vehicles'][i]['relation']
        if user_number == 0:
            player_id == account_id
        get_user_shipdata(account_id, ship_id, SET_SERVER, match_group)
        clan_name = get_clan_name(account_id, SET_SERVER)
        ship_info = get_ship_info(ship_id)
        ship_code = get_ship_code(ship_info)
        dict_data = {
            'user_name': user_name,
            'ship_id': ship_id,
            'clan_name': clan_name,
            'ship_tier': ship_info[0],
            'ship_type': ship_info[1],
            'ship_name': ship_info[2],
            'out_ship_name': ship_info[3]
        }
        if get_user_camp(user_number) == 'teammate':
            teammate_ship_code[account_id] = ship_code
        else:
            enemy_ship_code[account_id] = ship_code
        player_info[get_user_camp(user_number)][account_id] = dict_data


def data_reset():
    global user_data
    global player_info
    global end_player_info
    global teammate_ship_code
    global enemy_ship_code
    global teammate_xp_code
    global enemy_xp_code
    global is_end
    global player_id
    global gametype
    global battles_type

    user_data = {}
    player_info = {
        'teammate': {},
        'enemy': {}
    }
    end_player_info = {
        'teammate': {},
        'enemy': {}
    }
    teammate_ship_code = {}
    enemy_ship_code = {}
    teammate_xp_code = {}
    enemy_xp_code = {}
    is_end = {}
    player_id = None
    gametype = False
    battles_type = 'pvp'


def battles_info():
    # 队友数据
    for camp_name in ['teammate', 'enemy']:
        all_battles = 0
        all_value_battles = 0
        all_damage_dealt = 0
        all_wins = 0
        all_frags = 0
        all_pr = 0
        teammate_data = player_info[camp_name]
        if camp_name == 'teammate':
            acc_data = sorted(teammate_ship_code.items(),
                              key=lambda x: x[1], reverse=True)
            print('''---------------------------------------------------------------------   您的队伍   ---------------------------------------------------------------------------------------
           Ship                             ID                       战斗场数       胜率            伤害          击杀         评级            PR''')
        else:
            acc_data = sorted(enemy_ship_code.items(),
                              key=lambda x: x[1], reverse=True)
            print(f'''---------------------------------------------------------------------   您的对手   ---------------------------------------------------------------------------------------
           Ship                             ID                       战斗场数       胜率            伤害          击杀         评级            PR''')
        for acc in acc_data:
            account_id = acc[0]
            value = teammate_data[account_id]
            if value['clan_name'] == "":
                user_outname = value['user_name']
            else:
                user_outname = '[' + value['clan_name'] + \
                    ']' + value['user_name']
            if len(user_outname) > 25:
                user_outname = OutputFormat.out_of_range(user_outname, 25)
            else:
                user_outname = OutputFormat.string_format(
                    user_outname, 25, True)
            if user_data[account_id]['hidden'] == True:
                str_battles = '    -  '
                str_damage_dealt = '    -'
                str_wins = '-    '
                str_kd = ' -     '
                pr_info = '用户隐藏了战绩'
            else:
                ship_id = teammate_data[account_id]['ship_id']
                battles = user_data[account_id]['data']['battles_count']
                damage_dealt = user_data[account_id]['data']['damage_dealt']
                wins = user_data[account_id]['data']['wins']
                frags = user_data[account_id]['data']['frags']
                if battles != 0:
                    average_damage_dealt = damage_dealt/battles
                    average_wins = wins/battles
                    average_kd = frags/battles
                    pr = get_pvp_pr(average_damage_dealt, average_wins,
                                    average_kd, ship_id)[0]
                else:
                    average_damage_dealt = 0
                    average_wins = 0
                    average_kd = 0
                    pr = -1
                all_battles += battles
                all_value_battles += battles
                all_damage_dealt += damage_dealt
                all_wins += wins
                all_frags += frags
                all_pr += pr*battles

                pr_name, pr_diff = get_pr_box(pr)
                pr_info = pr_name + '(+' + str(pr_diff) + ')'
                str_battles = OutputFormat.string_format(
                    OutputFormat.number_format(battles), 5, False)
                str_wins = OutputFormat.string_format(
                    str(round(average_wins*100, 2))+'%', 6, True)
                str_damage_dealt = OutputFormat.string_format(
                    OutputFormat.number_format(int(average_damage_dealt)), 7, False)
                str_kd = OutputFormat.string_format(
                    str(round(average_kd, 2)), 4, True)
            user_message = f"         {value['out_ship_name']}   {user_outname}       {str_battles}       {str_wins}           {str_damage_dealt}         {str_kd}         {pr_info}"
            print(user_message)
        all_average_damage_dealt = all_damage_dealt/all_battles
        all_average_wins = all_wins/all_battles
        all_average_kd = all_frags/all_battles
        all_average_pr = all_pr/all_value_battles
        pr_name, pr_diff = get_pr_box(all_average_pr)
        pr_info = pr_name + '(+' + str(pr_diff) + ')'
        str_wins = OutputFormat.string_format(
            str(round(all_average_wins*100, 2))+'%', 6, True)
        str_damage_dealt = OutputFormat.string_format(
            OutputFormat.number_format(int(all_average_damage_dealt)), 7, False)
        str_kd = OutputFormat.string_format(
            str(round(all_average_kd, 2)), 4, True)                                       #
        user_message = f"\n                队伍平均水平                                                      {str_wins}         {str_damage_dealt}         {str_kd}         {pr_info}"
        print(user_message)
        # print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------')


def end_battles():
    for camp in ['teammate', 'enemy']:
        for key, value in player_info[camp].items():
            account_id = key
            ship_id = value['ship_id']
            if user_data[account_id]['hidden'] == True:
                end_player_info[camp][account_id] = {
                    'hidden': True,
                    'data': {
                        'art_agro': 0,
                        'original_exp': 0,
                        'frags': 0,
                        'wins': 0,
                        'hits_by_main': 0,
                        'shots_by_main': 0,
                        'planes_killed': 0,
                        'survived': 0,
                        'ships_spotted': 0,
                        'control_captured_points': 0,
                        'control_dropped_points': 0,
                        'damage_dealt': 0,
                        'scouting_damage': 0
                    }
                }
                continue
            request_url = 'http://vortex.worldofwarships.{}/api/accounts/{}/ships/{}/{}/'.format(
                get_request_server(SET_SERVER), account_id, ship_id, battles_type)
            try:
                request_data = requests.get(url=request_url, timeout=10)
            except:
                try:
                    request_data = requests.get(url=request_url, timeout=10)
                except:
                    print(f'请求数据失败，url:{request_url}\n请检查网络并重启程序')
                    input('Press Enter to exit...')
                    exit()
            data = json.loads(request_data.text)
            request_data.close()
            ship_data = data['data'][str(account_id)]['statistics'][str(
                ship_id)][battles_type]
            try:
                dict_data = {
                    'hidden': False,
                    'data': {
                        'art_agro': ship_data['art_agro'] - user_data[account_id]['data']['art_agro'],
                        'original_exp': ship_data['original_exp'] - user_data[account_id]['data']['original_exp'],
                        'frags': ship_data['frags'] - user_data[account_id]['data']['frags'],
                        'wins': ship_data['wins'] - user_data[account_id]['data']['wins'],
                        'hits_by_main': ship_data['hits_by_main'] - user_data[account_id]['data']['hits_by_main'],
                        'shots_by_main': ship_data['shots_by_main'] - user_data[account_id]['data']['shots_by_main'],
                        'planes_killed': ship_data['planes_killed'] - user_data[account_id]['data']['planes_killed'],
                        'survived': ship_data['survived'] - user_data[account_id]['data']['survived'],
                        'ships_spotted': ship_data['ships_spotted'] - user_data[account_id]['data']['ships_spotted'],
                        'control_captured_points': ship_data['control_captured_points'] - user_data[account_id]['data']['control_captured_points'],
                        'control_dropped_points': ship_data['control_dropped_points'] - user_data[account_id]['data']['control_dropped_points'],
                        'damage_dealt': ship_data['damage_dealt'] - user_data[account_id]['data']['damage_dealt'],
                        'scouting_damage': ship_data['scouting_damage'] - user_data[account_id]['data']['scouting_damage']
                    }
                }
            except:
                dict_data = {
                    'hidden': False,
                    'data': {
                        'art_agro': 0,
                        'original_exp': 0,
                        'frags': 0,
                        'wins': 0,
                        'hits_by_main': 0,
                        'shots_by_main': 0,
                        'planes_killed': 0,
                        'survived': 0,
                        'ships_spotted': 0,
                        'control_captured_points': 0,
                        'control_dropped_points': 0,
                        'damage_dealt': 0,
                        'scouting_damage': 0
                    }
                }

            end_player_info[camp][account_id] = dict_data


def battles_data_info():
    for camp in ['teammate', 'enemy']:
        all_damage = 0
        for key, value in end_player_info[camp].items():
            account_id = key
            if camp == 'teammate':
                teammate_xp_code[account_id] = end_player_info[camp][account_id]['data']['original_exp']
                all_damage += end_player_info[camp][account_id]['data']['damage_dealt']
            else:
                enemy_xp_code[account_id] = end_player_info[camp][account_id]['data']['original_exp']
                all_damage += end_player_info[camp][account_id]['data']['damage_dealt']

        if camp == 'teammate':
            acc_data = sorted(teammate_xp_code.items(),
                              key=lambda x: x[1], reverse=True)
            print('''---------------------------------------------------------------------   您的队伍   ---------------------------------------------------------------------------------------
    Ship                          ID                  存活       伤害&占比           经验      击杀  飞机击落     潜在伤害   侦查伤害 占领点数  船只侦查     主炮命中率        ''')
        else:
            acc_data = sorted(enemy_xp_code.items(),
                              key=lambda x: x[1], reverse=True)
            print('''---------------------------------------------------------------------   您的对手   ---------------------------------------------------------------------------------------
    Ship                          ID                  存活       伤害&占比           经验      击杀  飞机击落     潜在伤害   侦查伤害 占领点数  船只侦查     主炮命中率        ''')
        for acc in acc_data:
            account_id = acc[0]
            teammate_data = player_info[camp]
            value = teammate_data[account_id]
            user_outname = '[' + value['clan_name'] + ']' + value['user_name']
            if len(user_outname) > 30:
                user_outname = OutputFormat.out_of_range(user_outname, 30)
            else:
                user_outname = OutputFormat.string_format(
                    user_outname, 30, True)
            survived = end_player_info[camp][account_id]['data']['survived']
            damage_dealt = end_player_info[camp][account_id]['data']['damage_dealt']
            xp = end_player_info[camp][account_id]['data']['original_exp']
            frag = end_player_info[camp][account_id]['data']['frags']
            plane_kill = end_player_info[camp][account_id]['data']['planes_killed']
            art_agro = end_player_info[camp][account_id]['data']['art_agro']
            socuting_damage = end_player_info[camp][account_id]['data']['scouting_damage']
            point = end_player_info[camp][account_id]['data']['control_captured_points']
            define = end_player_info[camp][account_id]['data']['control_dropped_points']
            ship_spotted = end_player_info[camp][account_id]['data']['ships_spotted']
            main_shot = end_player_info[camp][account_id]['data']['shots_by_main']
            main_hit = end_player_info[camp][account_id]['data']['hits_by_main']
            if survived == 1:
                str_survived = '1'
            else:
                str_survived = '-'
            str_damage_dealt = OutputFormat.string_format(
                OutputFormat.number_format(int(damage_dealt)), 7, False)
            str_point_damage = OutputFormat.string_format(
                str(round(damage_dealt/all_damage*100, 2)) + '%', 7, True)
            str_xp = OutputFormat.string_format(
                OutputFormat.number_format(int(xp)), 5, False)
            str_frag = OutputFormat.string_format(
                OutputFormat.number_format(int(frag)), 2, False)
            str_plane_kill = OutputFormat.string_format(
                OutputFormat.number_format(int(plane_kill)), 2, False)
            str_art_agro = OutputFormat.string_format(
                OutputFormat.number_format(int(art_agro)), 9, False)
            str_socuting_damage = OutputFormat.string_format(
                OutputFormat.number_format(int(socuting_damage)), 7, False)
            str_ship_spotted = OutputFormat.string_format(
                OutputFormat.number_format(int(ship_spotted)), 2, False)
            str_point = OutputFormat.string_format(
                OutputFormat.number_format(int(point)), 3, False)
            if main_shot == 0:
                str_hit_rate = OutputFormat.string_format('0.0%', 7, True)
            else:
                str_hit_rate = OutputFormat.string_format(
                    str(round(main_hit/main_shot*100, 2)) + '%', 7, True)

            user_message = f"{value['out_ship_name']}{user_outname} {str_survived}     {str_damage_dealt} | {str_point_damage}      {str_xp}      {str_frag}       {str_plane_kill}       {str_art_agro}   {str_socuting_damage}    {str_point}       {str_ship_spotted}       {str_hit_rate} ({main_hit}\{main_shot})    {define}"
            print(user_message)


# 导入配置文件
try:
    config = configparser.ConfigParser()  # 类实例化
    config_path = (os.getcwd()+'\config.ini').replace('\\', '\\\\')
    config.read(config_path)

    APPLICATION_ID = get_application_id(config.get('select', 'TOKEN'))
    SET_SERVER = config.get('select', 'SET_SERVER')
    WOWS_GAME_PATH = config.get('select', 'WOWS_GAME_PATH')
    GAME_VERSON = config.get('select', 'GAME_VERSON')
except:
    print(f'导入配置文件失败！\nPATH:{config_path}')
    input('Press Enter to exit...')
    exit()

user_data = {}
player_info = {
    'teammate': {},
    'enemy': {}
}
end_player_info = {
    'teammate': {},
    'enemy': {}
}
teammate_ship_code = {}
enemy_ship_code = {}
teammate_xp_code = {}
enemy_xp_code = {}
is_end = {}
player_id = None
gametype = False
battles_type = 'pvp'


def main():
    global SET_SERVER
    try:
        # 运行前检测
        if os.path.exists(get_game_exe_path()):
            print('> 检测到游戏文件,获取数据中')
        else:
            print(f'未检测到游戏路径\n请检查游戏路径 {get_game_exe_path()} 是否正确')
            input('Press Enter to exit...')
            exit()
        if test_netwoek(get_request_server(SET_SERVER)) == -1:
            print('网络异常，请检查网络或者使用加速器')
            input('Press Enter to exit...')
            exit()
        print('> KokomiTool加载成功！')
        print('''-------------------------------------------------------------
|      __ __   ____     __ __   ____     __  ___    ____    |
|     / //_/  / __ \   / //_/  / __ \   /  |/  /   /  _/    |
|    / ,<    / / / /  / ,<    / / / /  / /|_/ /    / /      |
|   / /| |  / /_/ /  / /| |  / /_/ /  / /  / /   _/ /       |
|  /_/ |_|  \____/  /_/ |_|  \____/  /_/  /_/   /___/       |
|                                                           |
-------------------------------------------------------------
|                 Tips:只支持随机和排位                     |
|             作者:MaoYu   交流群:164933984                 |
|                     Verson:1.0.0                          |
-------------------------------------------------------------
''')
        # 监听本地文件
        print('> 等待游戏数据中~')
        while True:
            while True:
                # 查询temp文件是否存在
                if os.path.exists(get_temp_data_path()) == False:
                    # 文件不存在，休眠5s后再次查询
                    time.sleep(5)
                    continue
                else:
                    # 判断游戏类型，若非pvp或rank则继续监听
                    file_data = open(get_temp_data_path(),
                                     "r", encoding="utf-8")
                    temp_data = json.load(file_data)
                    file_data.close()
                    match_group = temp_data['matchGroup']
                    # 若符合条件则跳出循环
                    if match_group in ['pvp', 'ranked']:
                        print(f'\n检测到{match_group}对局，开始数据计算，可能需要一段时间')
                        break
                    else:
                        time.sleep(5)
                        continue
            # 计算数据
            file_data = open(get_temp_data_path(), "r", encoding="utf-8")
            temp_data = json.load(file_data)
            file_data.close()
            match_group = temp_data['matchGroup']
            if match_group not in ['pvp', 'ranked']:
                print()
            begin_battle()
            battles_info()
            # 监听接口

            print('\n> 等待结算数据中~\n')
            while True:
                request_url = 'http://vortex.worldofwarships.{}/api/accounts/{}/ships/{}/{}/'.format(
                    is_end['server'], is_end['account_id'], is_end['ship_id'], is_end['type'])
                try:
                    request_data = requests.get(url=request_url, timeout=10)
                except:
                    try:
                        request_data = requests.get(
                            url=request_url, timeout=10)
                    except:
                        print(f'请求数据失败，url:{request_url}\n请检查网络并重启程序')
                        continue
                data = json.loads(request_data.text)
                request_data.close()
                battles = data['data'][str(is_end['account_id'])]['statistics'][str(
                    is_end['ship_id'])][is_end['type']]['battles_count']
                if battles != is_end['battles']:
                    print('> 对局已结算，开始计算结算数据')
                    break
                else:
                    time.sleep(5)

            # 计算结算数据
            end_battles()
            battles_data_info()
            data_reset()
            print('\n等待新的游戏数据中~\n')
    except Exception as e:
        error_mag = str(e)
        print(f'呜呜呜~好像发生了无法解决的错误\nError_Message:{error_mag}')
        input('Press Enter to exit...')
        exit()


if __name__ == '__main__':
    main()
