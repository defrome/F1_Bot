import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


def init_driver():
    """Инициализация Chrome в AWS Lambda"""
    options = Options()
    options.binary_location = './chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--remote-debugging-port=9222')

    driver = webdriver.Chrome(
        executable_path='./chromedriver',
        options=options
    )
    return driver


def parse_race_calendar(driver):
    """Парсинг календаря гонок"""
    driver.get('https://www.formula1.com/en/racing.html')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'event-item'))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    events = []

    for event in soup.find_all('div', class_='event-item'):
        try:
            name = event.find('p', class_='card-title').text.strip()
            date = event.find('p', class_='date').text.strip()
            location = event.find('p', class_='event-place').text.strip()
            events.append({
                'name': name,
                'date': date,
                'location': location
            })
        except:
            continue

    return events


def parse_last_results(driver):
    """Парсинг последних результатов"""
    driver.get('https://www.formula1.com/en/results.html')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'resultsarchive-table'))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    last_race = soup.find('a', class_='resultsarchive-filter-item-link', href=True)

    if not last_race:
        return None

    race_url = f"https://www.formula1.com{last_race['href']}"
    driver.get(race_url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'resultsarchive-table'))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = []

    for row in soup.select('table.resultsarchive-table tr')[1:6]:  # Топ-5
        pos = row.find('td', class_='dark').text.strip()
        driver_name = row.find('span', class_='hide-for-tablet').text.strip()
        team = row.find('td', class_='semi-bold').text.strip()
        results.append({
            'position': pos,
            'driver': driver_name,
            'team': team
        })

    return {
        'race_name': soup.find('h1', class_='ResultsArchiveTitle').text.strip(),
        'date': soup.find('span', class_='full-date').text.strip(),
        'results': results
    }


def lambda_handler(event, context):
    """Основная функция Lambda"""
    driver = None
    try:
        driver = init_driver()

        result = {
            'calendar': parse_race_calendar(driver),
            'last_race': parse_last_results(driver),
            'timestamp': int(time.time())
        }

        return {
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    finally:
        if driver:
            driver.quit()