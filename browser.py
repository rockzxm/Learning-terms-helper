import requests
from bs4 import BeautifulSoup

# A class for searching for auxiliary results on the Internet
class Browser:


    def __init__(self, 
                 user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"):
        """Initializing the browser"""
        self.headers = {}
        # Формально - устройство, с которого, якобы, будет происходить поиск
        self.headers["user-agent"] = user_agent


    def google(self, query):
        """Search for the definition of a certain word in Google"""
        query = query.replace(' ', '+')
        URL = f"https://google.com/search?q={query}"
        resp = requests.get(URL, headers = self.headers)

        # Если запрос прошел успешно
        if resp.status_code == 200:
            # Получить ответ
            soup = BeautifulSoup(resp.content, "html.parser")
            # Получить все блоки спан
            rc = soup.find_all('span', recursive = True)
            # Оставить только те, содержимое которых начинается со слова Словарь
            newkey = list(filter(lambda x: x.startswith("Словарь"), map(lambda x: x.text, rc)))
            # Если такие есть
            if newkey:
                # Выделим блок с определением и вернем само определение
                newkey = newkey[0]
                newkey = newkey[newkey.find("род") + 3:]
                if newkey[0].isdigit():
                    while newkey[0].isdigit():
                        newkey = newkey[1:]
                    newkey = newkey[1:]
                newkey = newkey[:newkey.find(".")]
                newkey = " ".join(newkey.split())
                return newkey
            else:
                # Иначе вернем нет
                return "Нет"


    def sinonym(self, phrase):
        """A function for searching for synonyms of a word"""
        URL = f"https://sinonim.org/s/{phrase}#f"
        resp = requests.get(URL, headers = self.headers)
        soup = BeautifulSoup(resp.content, "html.parser")
        # Фильтруем таблицу с синонимами до только тех слов, которые мы бы реально названияяя
        rc = map(lambda x: x.text.replace(".", ""), soup.find_all('td'))
        rc = filter(lambda x: x.find(" ") == -1, rc)
        rc = list(filter(lambda x: x and x != '-' and \
                                     not x.endswith(")") and\
                                     not x.isdigit() and\
                                     x.find(phrase) == -1 and\
                                     not x.istitle(), rc))
        return rc
