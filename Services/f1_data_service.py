from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from datetime import datetime


class F1DataService:
    pass


class F1ScraperService(F1DataService):
    def __init__(self):
        self.driver = None
        self.timeout = 10
        self.base_url = "https://www.formula1.com"

    async def start(self):
        """Запуск браузера"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        return self

    async def stop(self):
        """Закрытие браузера"""
        if self.driver:
            self.driver.quit()

    async def _get_page(self, url):
        """Загрузка страницы и получение HTML"""
        if not self.driver:
            await self.start()

        self.driver.get(url)
        time.sleep(3)  # Ожидание загрузки
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    async def get_race_calendar(self, season=None):
        """Парсинг календаря гонок"""
        try:
            url = f"{self.base_url}/en/racing/{season}.html" if season else f"{self.base_url}/en/racing.html"
            soup = await self._get_page(url)

            events = soup.find_all('div', class_='event-item')
            if not events:
                return ["No races found"]

            calendar = []
            for event in events:
                name = event.find('p', class_='card-title').text.strip()
                date = event.find('p', class_='date').text.strip()
                location = event.find('p', class_='event-place').text.strip()
                calendar.append(f"🏁 {name}\n📅 {date}\n📍 {location}")

            return calendar

        except Exception as e:
            return [f"⚠️ Parsing error: {str(e)}"]

    async def get_last_results(self):
        """Парсинг последних результатов"""
        try:
            soup = await self._get_page(f"{self.base_url}/en/results.html")

            # Находим последнюю гонку
            last_race = soup.find('a', class_='resultsarchive-filter-item-link', href=True)
            if not last_race:
                return {'error': 'No race data found'}

            race_url = f"{self.base_url}{last_race['href']}"
            race_soup = await self._get_page(race_url)

            # Извлекаем данные
            race_name = race_soup.find('h1', class_='ResultsArchiveTitle').text.strip()
            date = race_soup.find('span', class_='full-date').text.strip()
            results = []

            for row in race_soup.select('table.resultsarchive-table tr')[1:6]:  # Топ-5
                pos = row.find('td', class_='dark').text.strip()
                driver = row.find('span', class_='hide-for-tablet').text.strip()
                team = row.find('td', class_='semi-bold').text.strip()
                results.append(f"{pos}. {driver} ({team})")

            return {
                'race_name': race_name,
                'date': date,
                'results': results,
                'circuit': race_soup.find('span', class_='circuit-info').text.strip() if race_soup.find('span',
                                                                                                        class_='circuit-info') else 'Unknown'
            }

        except Exception as e:
            return {'error': f"⚠️ Parsing error: {str(e)}"}

    async def get_drivers(self, season=None):
        """Парсинг списка гонщиков"""
        try:
            url = f"{self.base_url}/en/drivers.html"
            soup = await self._get_page(url)

            drivers = []
            for driver in soup.select('div.col-12.col-md-6.col-xl-4'):
                name = driver.find('span', class_='d-block f1--xxs').text.strip()
                team = driver.find('p', class_='f1--s').text.strip()
                number = driver.find('span', class_='f1-bold--xs').text.strip()
                drivers.append(f"🏎 {number} {name}\n🏁 {team}")

            return drivers[:20]  # Возвращаем топ-20 гонщиков

        except Exception as e:
            return [f"⚠️ Parsing error: {str(e)}"]

    async def get_teams(self):
        """Парсинг списка команд"""
        try:
            url = f"{self.base_url}/en/teams.html"
            soup = await self._get_page(url)

            teams = []
            for team in soup.select('div.col-12.col-md-6.col-xl-3'):
                name = team.find('span', class_='d-block f1--xxs').text.strip()
                drivers = team.find_all('p', class_='f1--s')
                driver_list = " & ".join([d.text.strip() for d in drivers])
                teams.append(f"🏁 {name}\n🏎 {driver_list}")

            return teams

        except Exception as e:
            return [f"⚠️ Parsing error: {str(e)}"]

    async def get_standings(self):
        """Парсинг турнирной таблицы"""
        try:
            soup = await self._get_page(f"{self.base_url}/en/standings.html")

            # Парсинг гонщиков
            drivers = []
            for row in soup.select('table.f1-standing-table--driver tr')[1:11]:  # Топ-10
                pos = row.find('td', class_='f1-bold--xs').text.strip()
                name = row.find('span', class_='d-block f1-bold--s').text.strip()
                points = row.find('td', class_='f1-bold--end').text.strip()
                drivers.append(f"{pos}. {name} - {points} pts")

            # Парсинг команд
            teams = []
            for row in soup.select('table.f1-standing-table--team tr')[1:6]:  # Топ-5
                pos = row.find('td', class_='f1-bold--xs').text.strip()
                name = row.find('span', class_='d-block f1-bold--s').text.strip()
                points = row.find('td', class_='f1-bold--end').text.strip()
                teams.append(f"{pos}. {name} - {points} pts")

            return {
                'drivers': drivers,
                'teams': teams
            }

        except Exception as e:
            return {'error': f"⚠️ Parsing error: {str(e)}"}


async def create_f1_service():
    """Фабричная функция для создания сервиса"""
    service = F1ScraperService()
    await service.start()
    return service