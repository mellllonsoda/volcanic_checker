"""
Volcano Checker

This module checks for volcanic activity and provides alerts.
"""

import json
import requests
from bs4 import BeautifulSoup


class VolcanoAlertChecker:
    def __init__(
        self,
        volcanolist_path: str = "./volcanolist.json",
        encoding: str = "utf-8"
    ):
        with open(volcanolist_path, mode="rt", encoding=encoding) as f:
            self.volcano_url_map = json.load(f)

    def get_alert_level_by_url(self, volcano_url: str) -> int:
        """
        指定されたURLから火山の噴火警戒レベルを取得する

        Args:
            volcano_url (str): 火山情報ページのURL

        Returns:
            int: 噴火警戒レベル（取得できなかった場合は0）
        """
        try:
            response = requests.get(volcano_url, timeout=3)
            response.encoding = "UTF-8"
        except requests.exceptions.RequestException as e:
            print(f"通信エラーが発生しました: {e}")
            return 0

        soup = BeautifulSoup(response.text, "html.parser")
        for level in range(1, 6):
            if soup.find(class_=f"level-keyword keyword{level}"):
                return level
        return 0

    def get_alert_level_by_name(self, volcano_name: str = "富士山") -> int:
        """
        指定された火山名から噴火警戒レベルを取得する

        Args:
            volcano_name (str): 火山の正式名称

        Returns:
            int: 噴火警戒レベル（取得できなかった場合は0）
        """
        url = self.volcano_url_map.get(volcano_name)
        if url is None:
            print("指定された火山名がリストにありません。")
            return 0
        return self.get_alert_level_by_url(url)


if __name__ == "__main__":
    checker = VolcanoAlertChecker()
    volcano_name = input("火山名を入力してください: ")
    print(checker.get_alert_level_by_name(volcano_name))