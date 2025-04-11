from bs4 import BeautifulSoup
import requests

class Parser():
    def __init__(self) -> None:
        self.link = ''



    def _parse_table(self, html_table) -> list:
        # обработка таблицы html

        def extract_cell_data(cell) -> list:
            # достаёт данные из частитаблицы

            colspan = int(cell.get('colspan', 1)) # столбцы
            rowspan = int(cell.get('rowspan', 1)) # строки

            return [cell.text] * colspan, rowspan # возвращает элемент таблицы из строк и столбцов


        table = [] # объявление возвращаемой таблицы
        hash_table = {} # словарь

        counter = 0
        for row in html_table.find_all('tr'): # tr строка
            
            row_data = []
            row_spans = []

            for cell in row.find_all(['th', 'td']): # th и td столбцы, на сайте используется только td
                
                cell_data, cell_rowspan = extract_cell_data(cell)
                row_data.extend(cell_data)
                row_spans.extend([cell_rowspan] * len(cell_data))

            if counter == 0:
                counter += 1 
                continue
            
            if counter % 6 == 1:
                hash_table[row_data[1]] = list()
            

            hash_table[list(hash_table.keys())[-1]].append(row_data[1:])

            # добавление в таблицу данных
            table.append(row_data[1:])
            
            counter += 1
        
        return hash_table



    def _get_html(self, link: str | None = None) -> BeautifulSoup:
        # создаёт объект парсера

        link = link or self.link # если ссылка None, то использует self.link (она пока не определена)

        response = requests.get(link) # GET запрос на сайт
        response.raise_for_status() # обработка ошибок как 403 и тп

        return BeautifulSoup(response.text, "html.parser") # объект bs4 для парса по коду
    



    def get_team_status(self):
        soup = self._get_html()
        ...



    def get_calendar(self) -> list:
        # функция получает календарь и возвращает список из элементов календаря

        soup = self._get_html('https://f1calendar.com/') # _get_html возвращает код страницы и тут же создаёт объект для парсера

        html_table = soup.find('table') # ищет в html коде элементы класса <table>  

        calendar = self._parse_table(html_table) # отправляет в парсер таблицу начиная с <table> заканчивая </table>

        return calendar # возвращает словарь




    def __del__(self) -> None:
        ...

if __name__ == '__main__':
    obj = Parser()
    
    hash = obj.get_calendar()
    
    for key in hash.keys():
        print(key, hash[key])
        print('\n')