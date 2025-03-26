"""
Volcano Checker

This module checks for volcanic activity and provides alerts.
"""

import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

def get_volcanic_alart_level_for_url(
        url: str="https://www.data.jma.go.jp/"
        "vois/data/report/activity_info/314.html") -> int:

    """URLに指定された火山の噴火警戒レベルを取得する

    Args:
        url (str): 噴火警戒レベルを取得する火山のページのURL。  
                   URLが指定されていない場合、または情報を取得できない場合は、  
                   富士山の噴火警戒レベルを取得する。

    Returns:
        int: 指定された火山の噴火警戒レベル。  
             取得できなかった場合は 0 を返す。
    """

    try:
        page_content = requests.get(url,timeout=3)
        page_content.encoding = 'UTF-8'
    except requests.exceptions.ConnectionError:
        print("Please check your internet connection.")
        exit()

    bs_level_content = BeautifulSoup(page_content.text,'html.parser')

    #気象庁のサイトには噴火警戒レベルに応じたメッセージがあるのでそれを見る
    if bs_level_content.find(class_="level-keyword keyword1"):
        return 1
    elif bs_level_content.find(class_="level-keyword keyword2"):
        return 2
    elif bs_level_content.find(class_="level-keyword keyword3"):
        return 3
    elif bs_level_content.find(class_="level-keyword keyword4"):
        return 4
    elif bs_level_content.find(class_="level-keyword keyword5"):
        return 5
    #Returns "0" if no match is found.
    else:
        return "0"

def get_volcanic_alart_level_for_name(name: str="Fujisan") -> int:
    """
    指定された活火山の噴火警戒レベルを取得する。

    Args:
        name (str): 噴火警戒レベルを取得する火山の正式名称。  
                    名称が指定されていない、または情報を取得できない場合は、  
                    富士山の噴火警戒レベルを取得する。

    Returns:
        int: 指定された火山の噴火警戒レベル。  
             取得できなかった場合は 0 を返す。
    """
    volcano_url_list ={
        "アトサヌプリ":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/104.html",
        "雌阿寒岳":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/105.html",
        "大雪山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/107.html",
        "十勝岳":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/108.html",
        "樽前山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/109.html",
        "倶多楽":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/111.html",
        "有珠山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/112.html",
        "北海道駒ヶ岳":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/113.html",
        "恵山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/114.html",
        "岩木山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/202.html",
        "八甲田山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/203.html",
        "十和田":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/204.html",
        "秋田焼山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/205.html",
        "岩手山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/207.html",
        "秋田駒ヶ岳":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/208.html",
        "鳥海山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/209.html",
        "栗駒山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/210.html",
        "蔵王山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/212.html",
        "吾妻山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/213.html",
        "安達太良山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/214.html",
        "磐梯山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/215.html",
        "那須岳":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/301.html",
        "日光白根山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/302.html",
        "草津白根山（白根山（湯釜付近））":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/350.html",
        "草津白根山（本白根山）":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/351.html",
        "浅間山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/306.html",
        "新潟焼山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/307.html",
        "弥陀ヶ原":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/309.html",
        "焼岳":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/310.html",
        "乗鞍岳":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/311.html",
        "御嶽山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/311.html",
        "白山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/313.html",
        "富士山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/314.html",
        "箱根山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/315.html",
        "伊豆東部火山群":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/316.html",
        "伊豆大島":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/317.html",
        "新島":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/318.html",
        "神津島":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/319.html",
        "三宅島":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/320.html",
        "八丈島":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/321.html",
        "青ヶ島":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/322.html",
        "鶴見岳・伽藍岳":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/513.html",
        "九重山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/502.html",
        "阿蘇山":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/503.html",
        "雲仙岳":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/504.html",
        "霧島山（えびの高原（硫黄山）周辺）":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/552.html",
        "霧島山（大幡池）":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/553.html",
        "霧島山（新燃岳）":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/551.html",
        "霧島山（御鉢）":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/550.html",
        "桜島":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/506.html",
        "薩摩硫黄島":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/508.html",
        "口永良部島":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/509.html",
        "諏訪之瀬島":
        "https://www.data.jma.go.jp/vois/data/report/activity_info/509.html"
        }
    try:
        return get_volcanic_alart_level_for_url(volcano_url_list[name])
    except KeyError:
        print("No volcanoes were found with the volcanic alart level.")

def update_display():
    volcanic_level = get_volcanic_alart_level_for_name(volcano_name)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 火山レベルに応じてのメッセージ
    if 1 == volcanic_level:
        message="活火山である事に留意してください"
    elif 2 == volcanic_level:
        message="火口周辺規制が行われています。"
    elif 3 == volcanic_level:
        message="入山規制が行われています。"
    elif 4 == volcanic_level:
        message="高齢者等は避難してください。"
    elif 5 == volcanic_level:
        message="直ちに危険区域から避難しなさい。"
    else:
        message="エラー。管理者に知らせて下さい。"

    label.config(text=f"{volcano_name} \nの噴火警戒レベル情報\n\n現在の噴火警戒レベル:{volcanic_level}\n\n{message}\n\n更新時刻: {timestamp}")

    # 火山レベルに応じて背景色を変更
    if 1 == volcanic_level:
        bgcolor="#FFFFFF"
        textcolor="black"
    elif 2 == volcanic_level:
        bgcolor="#F2E700"
        textcolor="black"
    elif 3 == volcanic_level:
        bgcolor="#F6AA00"
        textcolor="black"
    elif 4 == volcanic_level:
        bgcolor="#FF4B00"
        textcolor="white"
    elif 5 == volcanic_level:
        bgcolor="#990099"
        textcolor="white"
    else:
        bgcolor="black"
        textcolor="white"

    root.configure(bg=bgcolor)
    label.configure(bg=bgcolor,foreground=textcolor,font=("Helvetica",80))

    root.after(1000, update_display)  # 3秒ごとに更新

# GUIの設定
root = tk.Tk()
root.withdraw()  # メインウィンドウを非表示にする

# ユーザーに質問を表示し、入力を取得
volcano_name = simpledialog.askstring("表示したい火山", "表示したい火山の名前は何ですか？")
if volcano_name == "":
    exit()
else:
    pass

root.deiconify()

root.title(f"{volcano_name} 火山情報")
root.attributes('-fullscreen', True)  # フルスクリーン表示
root.configure(bg="black")

label = tk.Label(root, text="データ取得中...", font=("Helvetica", ), fg="white", bg="black")
label.pack(expand=True)

# 初回データ取得
update_display()

# キーボードのEscキーで終了
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()