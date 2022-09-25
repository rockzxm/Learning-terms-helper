import os
import random
from Browser import Browser
from Menu import ErrorMenu

# Card class
class Card:
    id = 0

    def __init__(self, term, definit, tags = [], search = True):
        """Initialization of menu card data"""
        self.id = Card.id
        Card.id += 1
        self.tags = tags
        self.br = Browser()
        self.term = term
        self.definit = definit
        if search:
            synonims = self.br.sinonym(self.term)
            self.alternative = list(map(lambda x: self.br.google(x + ' - это'), synonims[:10]))
            self.alternative = list(filter(lambda x: x[0].istitle() and x != "Нет" and not x.startswith("То же"), self.alternative))

    def __str__(self):
        """overloading the output of the menu card"""
        tags = "Теги: " + ", ".join(self.tags)
        return f"{self.id}. {self.term} - {self.definit}\n" + tags + "\n\n"


    def fin(self, inp):
        """Decrypting a string from a file to an object"""
        k = inp.split('\n')
        self.id = int(k[0])
        self.tags = k[1].split(';')
        self.term = k[2]
        self.definit = k[3]
        self.alternative = k[4].split(';')


    def fout(self):
        """Forming a string to save to a file"""
        ans = f"""{self.id}
{';'.join(self.tags)}
{self.term}
{self.definit}
{';'.join(self.alternative)}
"""
        return ans


    def input(self):
        """Entering a card from the console"""
        os.system("cls")
        self.term = input("Введите только термин:\n---> ")
        self.definit = input("Введите определение термина:\n---> ")
        self.tags = []
        choice = "1"
        while choice != "0":
            try:
                choice = input("Добавить тег? 1 - да, 0 - нет:\n---> ")
                if choice == "1":
                    self.tags.append(input("Введите тег:\n---> "))
                elif choice != "0":
                    raise ErrorMenu(choice)
            except ErrorMenu as e:
                e.reaction()
        self.alternative = list(map(self.br.google, map(lambda x: x + " - это", self.br.sinonym(self.term))))



    def playCard(self):
        """Playing a card to solve it as part of a test"""
        os.system('cls')
        print("Дайте у себя в голове определение следующему термину:")
        print(self.term)
        os.system("pause")
        os.system('cls')
        print(f"{self.term} - {self.definit}")
        ans = bool(not input("Введите что угодно, если вы ответили правильно, иначе 0\n---> ") == "0")
        os.system("pause")
        return ans

    def playTest(self):
        """Playing a card if it can be used as a test"""
        if len(self.alternative) < 3:
            return self.playCard()
        else:
            os.system('cls')
            print(f"{self.term} - это...")
            keys = random.choices(self.alternative, k = 3) + [self.definit]
            random.shuffle(keys)
            for i, key in enumerate(keys):
                print(f"{i + 1}. {key}")
            ans = int(input("Введите номер правильного ответа:\n---> "))
            if keys[ans - 1] == self.definit:
                print("Все верно")
                return True
            else:
                print(f"Нет, правильный ответ {keys.find(self.definit) + 1}")
                return False

# Test Class
class Quest:


    def __init__(self, cards, name):
        """Initialization"""
        self.cards = cards
        self.name = name


    def __str__(self):
        """Overloading the text output in the menu"""
        return self.name


    def fout(self):
        """The function of forming a string to save the test to a file"""
        ans = ""
        for to in self.cards:
            ans += f"{len(self.cards)}\n"
            ans += to.fout()
        return ans


    def playTest(self):
        """Playing the test"""
        random.shuffle(self.cards)
        questions = self.cards.copy()
        res = 0
        while questions:
            question = questions[-1]
            del questions[-1]
            ans = question.playTest()
            if not ans:
                res += 1
                questions.insert(0, question)
        print(f"{res} - столько ошибок вы совершили")
        
