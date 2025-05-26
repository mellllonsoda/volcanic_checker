"""
Volcano Checker

This module checks for volcanic activity and provides alerts.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

json_path = "./volcanolist.json"
encoding = "utf-8"
with open(json_path, mode="rt", encoding="utf-8") as f:
	volcano_url_list = json.load(f)

def get_volcanic_alert_level_for_url(
        url: str = "https://www.data.jma.go.jp/vois/data/report/activity_info/314.html"
    ) -> int:"""
Volcano Checker

This module checks for volcanic activity and provides alerts.
"""

import requests
from bs4 import BeautifulSoup
import json

json_path = "./volcanolist.json"
encoding = "utf-8"
with open(json_path, mode="rt", encoding="utf-8") as f:
	volcano_url_list = json.load(f)

def get_volcanic_alert_level_for_url(
        url: str = "https://www.data.jma.go.jp/vois/data/report/activity_info/314.html"
    ) -> int:
    """
    URLに指定された火山の噴火警戒レベルを取得する

    Args:
        url (str): 噴火警戒レベルを取得する火山のページのURL。  
        デフォルトでは富士山の噴火警戒レベルを返す。

    Returns:
        int: 指定された火山の噴火警戒レベル。  
            取得できなかった場合は 0 を返す。
    """
    try:
        page_content = requests.get(url, timeout=3)
        page_content.encoding = 'UTF-8'
    except requests.exceptions.RequestException as e:
        print(f"通信エラーが発生しました: {e}")
        return 0

    bs_level_content = BeautifulSoup(page_content.text, 'html.parser')

    # 気象庁のサイトには噴火警戒レベルに応じたメッセージがあるのでそれを見る
    for level in range(1, 6):
        if bs_level_content.find(class_=f"level-keyword keyword{level}"):
            return level
    return 0

def get_volcanic_alert_level_for_name(name: str = "富士山") -> int:
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
    url = volcano_url_list.get(name)
    if url is None:
        print("指定された火山名がリストにありません。")
        return 0
    return get_volcanic_alert_level_for_url(url)
    """
    URLに指定された火山の噴火警戒レベルを取得する

    Args:
        url (str): 噴火警戒レベルを取得する火山のページのURL。  
        デフォルトでは富士山の噴火警戒レベルを返す。

    Returns:
        int: 指定された火山の噴火警戒レベル。  
            取得できなかった場合は 0 を返す。
    """
    try:
        page_content = requests.get(url, timeout=3)
        page_content.encoding = 'UTF-8'
    except requests.exceptions.RequestException as e:
        print(f"通信エラーが発生しました: {e}")
        return 0

    bs_level_content = BeautifulSoup(page_content.text, 'html.parser')

    # 気象庁のサイトには噴火警戒レベルに応じたメッセージがあるのでそれを見る
    for level in range(1, 6):
        if bs_level_content.find(class_=f"level-keyword keyword{level}"):
            return level
    return 0

def get_volcanic_alert_level_for_name(name: str = "富士山") -> int:
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
    url = volcano_url_list.get(name)
    if url is None:
        print("指定された火山名がリストにありません。")
        return 0
    return get_volcanic_alert_level_for_url(url)