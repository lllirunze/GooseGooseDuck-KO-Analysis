# import pandas as pd
# import json
# import matplotlib.pyplot as plt
# import numpy as np

# roles_path = 'data/roles.json'
# with open(roles_path, 'r', encoding='utf-8') as roles_file:
#     roles = json.load(roles_file)

# duck_roles = set(roles["duck_roles"])
# goose_roles = set(roles["goose_roles"])

# # duck_roles = {"鸭子", "间谍", "专业杀手", "刺客", "告密者", "静语者", "派对狂", "爆炸王", "身份窃贼", "忍者", "连环杀手", "小丑", "食鸟鸭", "丧葬者", "传教士", "超能力者", "雇佣杀手", "变形者"}
# # goose_roles = {"鹅", "肉汁", "通灵者", "正义使者", "警长", "加拿大鹅", "工程师", "模仿者", "侦探", "观鸟者", "政治家", "锁匠", "殡仪员", "网红", "冒险家", "复仇者", "星界行者", "说客", "生存主义者", "跟踪者", "预言家", "科学家", "流浪儿童", "追踪者", "保镖"}

# # Function to calculate the win rate for each player based on their selected role and the winner
# def calculate_win_rate_curve(player):
#     player_data = data[["time", '胜方', player]]
#     # print(player_data)
#     player_data['time'] = pd.to_datetime(player_data['time'])  # 转换为日期时间格式
#     player_data['day'] = player_data['time'].dt.date          # 提取日期部分

#     total_rounds = 0
#     wins = 0
#     date = str(player_data.iloc[0]['day'])

#     winRateCurve = []
#     winsCurve = []
#     totalCurve = []

#     for _, row in player_data.iterrows():
#         selected_role = row[player]
#         winner = row['胜方']
#         today = str(row['day'])

#         if today != date:
#             if (total_rounds == 0):
#                 winRateCurve.append(0)
#                 winsCurve.append(0)
#                 totalCurve.append(0)
#             else:
#                 winRateCurve.append(wins / total_rounds)
#                 winsCurve.append(wins)
#                 totalCurve.append(total_rounds)
#             date = today

#         # print(winner)
#         # if winner == "":
#         #     continue

#         if pd.isna(selected_role):
#             continue

#         if winner == '鹅' and selected_role in goose_roles:
#             wins += 1
#         elif winner == '鸭子' and selected_role in duck_roles:
#             wins += 1
#         elif selected_role == winner:
#             wins += 1
#         total_rounds += 1

#     if (total_rounds == 0):
#         winRateCurve.append(0)
#         winsCurve.append(0)
#         totalCurve.append(0)
#     else:
#         winRateCurve.append(wins / total_rounds)
#         winsCurve.append(wins)
#         totalCurve.append(total_rounds)

#     # if total_rounds == 0:
#     #     return 0, 0, 0  # If the player did not participate in any rounds
    
#     # # print("{}: {} ({}/{})".format(player, wins / total_rounds, wins, total_rounds))
#     # win_rate = wins / total_rounds
#     # return round(win_rate, 3), wins, total_rounds
#     return winRateCurve, winsCurve, totalCurve

# # Load the dataset to examine its structure
# file_path = 'data/data - Sheet1.csv'
# data = pd.read_csv(file_path)

# # 获取日期列表
# # days = sorted(pd.to_datetime(data['time']).dt.date.unique())  # 确保日期按时间排序
# # days

# plt.figure(figsize=(20, 12))

# days = sorted(pd.to_datetime(data['time']).dt.date.unique())  # 确保日期按时间排序
# players = data.columns

# # 创建唯一颜色映射
# num_lines = len(players[2: -1])
# colors = plt.cm.get_cmap('tab20', num_lines)  # 使用 'tab20' 调色盘

# for i, player in enumerate(players[2: -1]):
#     win_rate, _, _ = calculate_win_rate_curve(player)
#     plt.plot(days, win_rate, marker='o', linestyle='-', label=player, color=colors(i))

# plt.xlabel('Days', fontsize=14)
# plt.ylabel('Win Rate', fontsize=14)
# plt.xticks(rotation=45)  # 设置 x 轴刻度
# plt.yticks(fontsize=12)
# plt.grid(True)  # 添加网格
# plt.legend(fontsize=12)  # 添加图例
# # plt.show()

# plt.savefig("image/winCurve.png")

import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# 加载角色数据
roles_path = 'data/roles.json'
with open(roles_path, 'r', encoding='utf-8') as roles_file:
    roles = json.load(roles_file)

duck_roles = set(roles["duck_roles"])
goose_roles = set(roles["goose_roles"])

# Function to calculate the win rate for each player based on their selected role and the winner
def calculate_win_rate_curve(player):
    player_data = data[["time", '胜方', player]]
    player_data['time'] = pd.to_datetime(player_data['time'])  # 转换为日期时间格式
    player_data['day'] = player_data['time'].dt.date          # 提取日期部分

    total_rounds = 0
    wins = 0
    date = str(player_data.iloc[0]['day'])

    winRateCurve = []
    winsCurve = []
    totalCurve = []

    for _, row in player_data.iterrows():
        selected_role = row[player]
        winner = row['胜方']
        today = str(row['day'])

        if today != date:
            if total_rounds == 0:
                winRateCurve.append(0)
            else:
                winRateCurve.append(wins / total_rounds)
            date = today

        if pd.isna(selected_role):
            continue

        if winner == '鹅' and selected_role in goose_roles:
            wins += 1
        elif winner == '鸭子' and selected_role in duck_roles:
            wins += 1
        elif selected_role == winner:
            wins += 1
        total_rounds += 1

    if total_rounds == 0:
        winRateCurve.append(0)
    else:
        winRateCurve.append(wins / total_rounds)

    return winRateCurve

# 加载数据
file_path = 'data/data - Sheet1.csv'
data = pd.read_csv(file_path)

# 获取日期列表
days = sorted(pd.to_datetime(data['time']).dt.date.unique())  # 确保日期按时间排序
players = data.columns[2:-1]  # 去掉非玩家列

# 创建动画
fig, ax = plt.subplots(figsize=(20, 12))
num_lines = len(players)
colors = plt.cm.get_cmap('tab20', num_lines)  # 使用 'tab20' 调色盘
lines = {player: ax.plot([], [], marker='o', linestyle='-', label=player, color=colors(i))[0] for i, player in enumerate(players)}

def init():
    """初始化动画，清空所有曲线"""
    ax.set_xlim(days[0], days[-1])
    ax.set_ylim(0, 0.6)
    ax.set_xlabel('Days', fontsize=14)
    ax.set_ylabel('Win Rate', fontsize=14)
    ax.legend(fontsize=12)
    return list(lines.values())

def update(frame):
    """更新动画帧"""
    current_day = days[:frame + 1]
    for player, line in lines.items():
        win_rate = calculate_win_rate_curve(player)[:frame + 1]
        line.set_data(current_day, win_rate)
    return list(lines.values())

ani = FuncAnimation(fig, update, frames=len(days), init_func=init, blit=True, interval=200)

# 保存或展示动画
ani.save("image/winCurve.gif", writer='pillow')  # 保存为 GIF
# plt.show()