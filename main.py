from Browser import Browser
import Menu
from cards import Card
from cards import Quest
import os


# Список, хранящий все вопросы, с которыми предстоит работать пользователю
cards = []
# Список тестов, которые может пройти пользователь
quests = []
# Проверяем, существует ли файл с предзаписанными данными и не пуст ли он
if os.path.exists("config.txt") and os.path.getsize("config.txt"):
    # Если это так, то открываем его для чтения
    # Данные в нем записаны следующим образом
    with open("config.txt", "r", encoding='utf-8') as fp:
        # Количество карточек с вопросами
        n = int(fp.readline())
        for i in range(n):
            # Вспомогательные переменные для записи
            card = ""
            cardReal = Card("", "", search = False)
            # Считываем 5 полей карточки
            # id, tags, term, definit, alternative
            for j in range(5):
                card += fp.readline()
            # Расшифровываем полученную строку в объект
            cardReal.fin(card)
            # Добавляем егов список
            cards.append(cardReal)

        # Считываем кол-во тестов
        n = int(fp.readline())
        for i in range(n):
            # Считываем имя теста
            name = fp.readline()
            # Кол-во вопросов в тесте
            m = int(fp.readline())
            questCards = []
            # Сохраняем карточки вопросов в тесте по тем же правилам, что и простые карточки
            for j in range(m):
                card = ""
                cardReal = Card("", "", search = False)
                for k in range(5):
                    card += fp.readline()
                fp.readline()
                cardReal.fin(card)
                questCards.append(cardReal)
            # Сохраняем тест
            quests.append(Quest(questCards, name))

# Те карты вопросов, которые будут показаны в меню редактирования
openCards = [cards.copy()]
# Номер версии карточек в меню редактирования
stepCard = 0
# Флаг, отвечающий за показ карт в меню редактирования
showOpenCardsFlag = False
# Те тесты, которые показаны в меню тестирования
openQuests = [quests.copy()]
# Флаг, отвечающий за показ тестов в меню тестирования
showOpenQuestsFlag = False
# Номер версии списка тестов в меню тестирования
stepQuest = 0


def exitEditMenu():
    """Функция меню, сохраняющая все необходимые данные при 
    переходе из меню редактирования в основное меню"""
    global openCards
    global stepCard
    openCards = [cards.copy()]
    stepCard = 0


def newCond():
    """A menu function that filters question cards by
    the condition entered by the user"""
    global openCards
    global stepCard
    openCards = openCards[:stepCard + 1]
    cond = input("Введите условие:\n---> ")
    openCards.append(list(filter(lambda x: eval(cond), openCards[stepCard])))
    stepCard += 1


def back():
    """A menu function that returns the user to 
    to the previous list of cards with questions"""
    global stepCard
    stepCard = max(0, stepCard - 1)


def forward():
    """A menu function that returns the user to
    to the next list of question cards"""
    global stepCard
    stepCard = min(stepCard + 1, len(openCards) - 1)


def tagging():
    """A menu function that adds a given tag to
    all found question cards"""
    global cards
    global openCards 
    global stepCard
    tag = input("Введите новый тег:\n---> ")
    for to in openCards[stepCard]:
        cards[cards.index(to)].tags.append(tag)


def edit():
    """Menu function that implements editing 
    found cards with questions"""
    global cards
    global openCards 
    for to in openCards[stepCard]:
        cards[cards.index(to)].input()
    openCards = [cards.copy()]
        

def showHide():
    """Menu function that implements hiding and showing 
    question cards in the edit menu"""
    global showOpenCardsFlag
    showOpenCardsFlag = not showOpenCardsFlag


def makeTest():
    """Menu function that creates a test based on the found 
    questions in the edit menu"""
    global quests
    name = input("Дайте название тесту:\n---> ")
    quests.append(Quest(openCards[stepCard], name))


def delete():
    """Menu function that deletes all found 
    question cards in the edit menu"""
    global cards
    global openCards 
    for to in openCards[stepCard]:
        del cards[cards.index(to)]
    openCards = [cards.copy()]
    step = 0


# Фиксируем команды и функции, их реализующие
editMenu = {"Вернуться": exitEditMenu,
            "Добавить условие": newCond,
            "Показать/Скрыть карточки": showHide,
            "Назад": back,
            "Вперед": forward,
            "Добавить к найденным элементам тег": tagging,
            "Редактировать найденные карточки": edit,
            "Удалить найденные карточки": delete,
            "Создать тест по найденным карточкам": makeTest,
            "Сброс": exitEditMenu}

# Вспомогательная функция, показывающа или скрывающая карточки с вопросами
def displayEditMenu():
    if showOpenCardsFlag:
        if openCards[stepCard]:
            print(*openCards[stepCard], sep = '\n')
        else:
            print("Не подходит ни одна карта")

# Создаем меню с заданным функционалом
editMenu = Menu.Menu(editMenu, displayEditMenu)


def exitTestMenu():
    """Menu function that saves all the necessary data 
    when switching from the test menu to the main menu"""
    global openQuests
    global stepQuest
    openQuests = [quests.copy()]
    stepQuest = 0

def newCondTest():
    """Menu function for setting filtering conditions 
    tests in the testing menu"""
    global openQuests
    global stepQuest
    openQuests = openQuests[:stepQuest + 1]
    cond = input("Введите условие:\n---> ")
    openQuests.append(list(filter(lambda x: eval(cond), openQuests[stepQuest])))
    stepQuest += 1


def backTest():
    """A menu function that takes you back to 
    previous step in the testing menu"""
    global stepQuest
    stepQuest = max(0, stepQuest - 1)


def forwardTest():
    """A menu function that takes you back to 
    the next step of the testing menu"""
    global stepQuest
    stepQuest= min(stepQuest + 1, len(openQuests) - 1)


def showHideTest():
    """Menu function that hides or shows 
    all tests in the testing menu"""
    global showOpenQuestsFlag
    showOpenQuestsFlag = not showOpenQuestsFlag


def deleteTest():
    """A function of the testing menu that deletes all the tests found in it"""
    global quests
    global openQuests
    for to in openQuests[stepQuest]:
        del quests[quests.index(to)]
    openQuests = [quests.copy()]
    step = 0


# Фиксируем команды и функции, их реализующие
testMenu = {"Вернуться": exitTestMenu,
            "Добавить условие": newCondTest,
            "Показать/Скрыть тесты": showHideTest,
            "Назад": backTest,
            "Вперед": forwardTest,
            "Удалить найденные тесты": deleteTest,
            "Сброс": exitTestMenu}


def displayTestMenu():
    """Auxiliary function showing all tests in the testing menu"""
    if showOpenQuestsFlag:
        if openQuests[stepQuest]:
            print(*openQuests[stepQuest], sep = '\n')
        else:
            print("Не подходит ни одна карта")


# Сохраняем меню
testMenu = Menu.Menu(testMenu, displayTestMenu)


def exitMainMenu():
    """Shutdown function"""
    with open("config.txt", "w", encoding='utf-8') as fp:
        fp.write(str(len(cards)) + '\n')
        for to in cards:
            fp.write(to.fout())
        fp.write(str(len(quests)) + '\n')
        for to in quests:
            fp.write(to.name + '\n')
            fp.write(to.fout())


def addition():
    """Функция добавления карточки с вопросом"""
    global cards
    card = Card("", "")
    card.input()
    cards.append(card)


def shiftEdit():
    """The function of switching to the editing menu"""
    global openCards
    global stepCard
    openCards = [cards.copy()]
    stepCard = 0
    editMenu.play()


def shiftTest():
    """The function of switching to the testing menu"""
    global openQuests
    global stepQuest
    openQuests = [quests.copy()]
    stepQuest = 0
    testMenu.play()


def tests():
    """The function of selecting a test to pass it"""
    os.system("cls")
    if quests:
        for i, quest in enumerate(quests):
            print(f"{i + 1}. {quest}")
        try:
            choice = input("Введите номер теста:\n---> ")
            if choice.isdigit() and 0 < int(choice) <= len(quests):
                quests[int(choice) - 1].playTest()
            else:
                raise Menu.ErrorMenu(choice)
        except Menu.ErrorMenu as e:
            e.reaction()
    else:
        print("Нет ни одного теста, создайте их в меню редактирования")
    os.system("pause")


def api():
    os.system("cls")
    help(tests)
    help(shiftEdit)
    help(addition)
    help(exitMainMenu)
    help(displayTestMenu)
    help(deleteTest)
    help(delete)
    help(showHide)
    help(showHideTest)
    help(makeTest)
    help(edit)
    help(forward)
    help(forwardTest)
    help(back)
    help(backTest)
    help(newCond)
    help(newCondTest)
    help(Menu.Menu)
    help(Menu.ErrorMenu)
    help(Browser)
    help(Card)
    help(Quest)
    os.system("pause")


# Фиксируем команды и их реализующие функции
mainMenu = {"Завершение работы": exitMainMenu,
            "Добавить карточку": addition,
            "Меню редактирования": shiftEdit,
            "Меню тестов": shiftTest,
            "Документация": api,
            "Пройти тест": tests}


# Создаем меню с заданным функционалом
mainMenu = Menu.Menu(mainMenu)
# Запускаем меню
mainMenu.play()
