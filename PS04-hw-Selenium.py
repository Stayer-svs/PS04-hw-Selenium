from selenium import webdriver # импорт webdriver
from selenium.webdriver.common.by import By    # Импорт модуля для поиска элементов на странице
from selenium.webdriver.common.keys import Keys  # Импорт модуля для работы с клавиатурой
import time  # Импорт модуля для управления паузами в выполнении скрипта

# Создание объекта WebDriver для браузера Firefox
driver = webdriver.Firefox()


def search_wikipedia(query):
    """
    Функция выполняет поиск статьи на Википедии по заданному запросу.
    Открывает страницу поиска, вводит запрос, отправляет его и переходит к первой найденной статье.
    """
    driver.get("https://ru.wikipedia.org/wiki/Служебная:Поиск")  # Открытие страницы поиска Википедии

    search_box = driver.find_element(By.NAME, "search")  # Поиск поля ввода запроса
    search_box.send_keys(query)  # Ввод текста запроса
    search_box.send_keys(Keys.RETURN)  # Нажатие клавиши "Enter" для отправки запроса

    time.sleep(2)  # Ожидание загрузки страницы результатов

    try:
        first_link = driver.find_element(By.CSS_SELECTOR, ".mw-search-result-heading a")  # Поиск первой ссылки
        first_link.click()  # Переход по первой ссылке
        time.sleep(2)  # Ожидание загрузки статьи
    except Exception as e:
        print("Статья не найдена.")  # Вывод сообщения об ошибке
        return None

    return driver.current_url  # Возвращает URL открытой статьи


def get_paragraphs():
    """
    Функция извлекает первые 5 параграфов статьи и выводит их на экран.
    """
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")  # Поиск всех параграфов в статье
    for i, paragraph in enumerate(paragraphs[:5]):  # Ограничение вывода первыми 5 параграфами
        print(f"{i + 1}. {paragraph.text[:200]}...")  # Вывод первых 200 символов каждого параграфа
    print("\n")


def list_links():
    """
    Функция находит все ссылки на связанные страницы Википедии и выводит их.
    """
    links = driver.find_elements(By.CSS_SELECTOR, "a")  # Поиск всех ссылок на странице
    filtered_links = [link.get_attribute("href") for link in links if
                      link.get_attribute("href") and "/wiki/" in link.get_attribute("href")]  # Фильтрация ссылок Википедии
    filtered_links = list(set(filtered_links))[:10]  # Ограничение списка до 10 ссылок

    for i, link in enumerate(filtered_links):
        print(f"{i + 1}. {link}")  # Вывод списка ссылок
    return filtered_links


def main():
    """
    Основная функция программы. Запрашивает ввод пользователя, выполняет поиск на Википедии и дает возможность
    просматривать содержимое статьи или переходить по связанным ссылкам.
    """
    query = input("Введите запрос для Википедии: ")  # Запрос ввода от пользователя
    url = search_wikipedia(query)  # Выполнение поиска

    if not url:  # Проверка на успешность поиска
        return

    while True:
        print("\nВыберите действие:")
        print("1. Листать параграфы статьи")
        print("2. Перейти на связанную страницу")
        print("3. Выйти")

        choice = input("Ваш выбор: ")  # Ввод выбора пользователя

        if choice == "1":
            get_paragraphs()  # Вывод параграфов статьи
        elif choice == "2":
            links = list_links()  # Вывод списка связанных страниц
            try:
                link_choice = int(input("Введите номер ссылки: ")) - 1  # Запрос номера ссылки
                if 0 <= link_choice < len(links):  # Проверка корректности номера
                    driver.get(links[link_choice])  # Переход по ссылке
                    time.sleep(2)  # Ожидание загрузки страницы
                else:
                    print("Неверный выбор.")
            except ValueError:
                print("Введите число!")  # Обработка ошибки некорректного ввода
        elif choice == "3":
            print("Выход из программы.")
            driver.quit()  # Закрытие браузера
            break
        else:
            print("Неверный ввод, попробуйте снова.")  # Обработка некорректного выбора


if __name__ == "__main__":
    main()
