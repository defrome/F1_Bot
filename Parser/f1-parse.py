from bs4 import BeautifulSoup
import requests

class Parser():
    def __init__(self) -> None:
        self.link = ''

    
    def _get_html(self, link: str | None = None) -> BeautifulSoup:
        link = link or self.link

        response = requests.get(link)
        response.raise_for_status()

        return BeautifulSoup(response.text, "html.parser")
    

    def get_team_status(self):
        soup = self._get_html()
        ...


    def get_calendar(self):
        soup = self._get_html('https://f1calendar.com/')
        ...


    def __del__(self) -> None:
        ...