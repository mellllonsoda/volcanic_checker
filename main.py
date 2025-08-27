"""
Volcano Checker

This module checks for volcanic activity and provides alerts.
"""

from dataclasses import dataclass
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup

@dataclass
class VolcanoAlert:
    """
    Data class for volcano alert level information.

    Attributes:
        name (str): Volcano name
        url (str): Volcano info page URL
        level (int): Volcano alert level (0 if unavailable)
        retrieved_at (datetime): Datetime when info was retrieved
    """
    name: str
    url: str
    level: int
    retrieved_at: datetime


class VolcanoAlertChecker:
    """
    Class to retrieve volcano alert levels.

    Loads volcano name-URL mapping from a JSON file and fetches alert levels from the JMA website.

    Attributes:
        volcano_url_map (dict[str, str]): Mapping of volcano names to info page URLs.
    """

    def __init__(
        self,
        volcanolist_path: str = "./volcanolist.json",
        encoding: str = "utf-8"
    ):
        self.volcano_url_map = self._load_volcano_url_map(volcanolist_path, encoding)

    @staticmethod
    def _load_volcano_url_map(path: str, encoding: str) -> dict:
        try:
            with open(path, mode="rt", encoding=encoding) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Failed to load volcano list: {e}")
            return {}

    def get_alert_level_by_url(self, volcano_name: str, volcano_url: str) -> VolcanoAlert:
        """
        Fetches volcano alert level from the specified URL.

        Args:
            volcano_name (str): Volcano name
            volcano_url (str): Info page URL

        Returns:
            VolcanoAlert: Alert level info (level=0 if unavailable)
        """
        level = 0
        try:
            response = requests.get(volcano_url, timeout=3)
            response.encoding = "UTF-8"
            soup = BeautifulSoup(response.text, "html.parser")
            for lvl in range(1, 6):
                if soup.find(class_=f"level-keyword keyword{lvl}"):
                    level = lvl
                    break
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")

        return VolcanoAlert(
            name=volcano_name,
            url=volcano_url,
            level=level,
            retrieved_at=datetime.now()
        )

    def get_alert_level_by_name(self, volcano_name: str = "富士山") -> VolcanoAlert:
        """
        Fetches volcano alert level by volcano name.

        Args:
            volcano_name (str): Volcano name

        Returns:
            VolcanoAlert: Alert level info (level=0 if unavailable)
        """
        url = self.volcano_url_map.get(volcano_name)
        if not url:
            print("Volcano name not found in list.")
            return VolcanoAlert(
                name=volcano_name,
                url="",
                level=0,
                retrieved_at=datetime.now()
            )
        return self.get_alert_level_by_url(volcano_name, url)


def main():
    """
    Fetches and displays the volcano alert level based on user input.

    Prompts the user for a volcano name, retrieves its alert level using
    VolcanoAlertChecker, and prints the result.
    """

    checker = VolcanoAlertChecker()
    input_volcano_name = input("火山名を入力してください: ")
    alert = checker.get_alert_level_by_name(input_volcano_name)
    print(alert)


if __name__ == "__main__":
    main()
