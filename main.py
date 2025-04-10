from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json


def init_driver():
    """Инициализация Chrome в Docker"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(
        executable_path='/usr/local/bin/chromedriver',
        options=chrome_options
    )
    return driver


def parse_f1_data():
    """Основная функция парсинга"""
    driver = init_driver()
    try:
        # Парсинг календаря
        driver.get('https://www.formula1.com/en/racing.html')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'event-item'))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        calendar = []

        for event in soup.find_all('div', class_='event-item'):
            try:
                name = event.find('p', class_='card-title').text.strip()
                date = event.find('p', class_='date').text.strip()
                location = event.find('p', class_='event-place').text.strip()
                calendar.append({
                    'name': name,
                    'date': date,
                    'location': location
                })
            except:
                continue

        # Парсинг последних результатов
        driver.get('https://www.formula1.com/en/results.html')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'resultsarchive-table'))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        last_race = soup.find('a', class_='resultsarchive-filter-item-link', href=True)

        results = []
        if last_race:
            race_url = f"https://www.formula1.com{last_race['href']}"
            driver.get(race_url)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'resultsarchive-table'))
            )

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for row in soup.select('table.resultsarchive-table tr')[1:6]:
                pos = row.find('td', class_='dark').text.strip()
                driver_name = row.find('span', class_='hide-for-tablet').text.strip()
                team = row.find('td', class_='semi-bold').text.strip()
                results.append({
                    'position': pos,
                    'driver': driver_name,
                    'team': team
                })

        return {
            'calendar': calendar,
            'last_race_results': results,
            'timestamp': int(time.time())
        }

    finally:
        driver.quit()


if __name__ == '__main__':
    data = parse_f1_data()
    print(json.dumps(data, indent=2))