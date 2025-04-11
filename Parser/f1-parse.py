from bs4 import BeautifulSoup
import requests

class Parser():
    def __init__(self) -> None:
        self.link = ''



    def _parse_table(self, html_table) -> list:


        def extract_cell_data(cell) -> list:
            colspan = int(cell.get('colspan', 1))
            rowspan = int(cell.get('rowspan', 1))

            return [cell.text] * colspan, rowspan
        
        


        table = []

        for row in html_table.find_all('tr'):

            row_data = []
            row_spans = []

            for cell in row.find_all(['th', 'td']):
                cell_data, cell_rowspan = extract_cell_data(cell)
                row_data.extend(cell_data)
                row_spans.extend([cell_rowspan] * len(cell_data))
            
            for i, span in enumerate(row_spans):
                if span > 1:
                    row_spans[i] -= 1
                    if len(table) > 0:
                        row_data.insert(i, table[-1][i])

            table.append(row_data[1:])
        
        return table[1:]



    def _get_html(self, link: str | None = None) -> BeautifulSoup:
        link = link or self.link

        response = requests.get(link)
        response.raise_for_status()

        return BeautifulSoup(response.text, "html.parser")
    



    def get_team_status(self):
        soup = self._get_html()
        ...



    def get_calendar(self) -> list:
        soup = self._get_html('https://f1calendar.com/')

        html_table = soup.find('table')

        calendar = self._parse_table(html_table)

        return [calendar[i:i+6] for i in range(0, len(calendar), 6)]




    def __del__(self) -> None:
        ...

if __name__ == '__main__':
    obj = Parser()
    for i in obj.get_calendar():
        print(i)
        print()