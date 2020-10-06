from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import re
import math



# file_name = "file_for_stepic.txt"

# current_dir = os.path.abspath(os.path.dirname(__file__))

# file_path = os.path.join(current_dir, file_name)


LINK = "http://suninjuly.github.io/explicit_wait2.html"


def calc(x: int) -> int:
    return math.log(abs(12 * math.sin(x_val)))


def get_user_data_folder_path(folder_name="chrome-data"):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    folder_path = os.path.join(current_dir, folder_name)
    return folder_path


def get_text_from_alert():
    # Забираем ответ из всплывающего окна и копируем его в буфер, чтобы потом вставить комбинацией ctrl + v
    time.sleep(1)
    alert_el = browser.switch_to_alert()
    alert_text = alert_el.text
    key = re.findall("[\d.]+", alert_text)
    if key:
        key = key.pop()
        command = f'echo | set /p nul={key.strip()}| clip'
        print("Key for quiz =", key, "it's already copied to your clipboard")
        os.system(command)
    alert_el.accept()


try: 
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={get_user_data_folder_path()}")
    browser = webdriver.Chrome(options=chrome_options)
    # chrome_options.add_argument("user-data-dir=chrome-data") 
    browser.get(LINK)

    # Находим цену и ждем шалену знижку
    # WebDriverWait(browser, 12).until( EC.text_to_be_present_in_element((By.ID, "price"), "100"))
    WebDriverWait(browser, 12).until( EC.visibility_of_element_located((By.ID, "price")))
    price_el = browser.find_element_by_id("price")
    for i in range(200):
        price = re.search("\d+", price_el.text).group()
        print(price)
        if int(price) <= 100:
            break
        else:
            time.sleep(0.3)

    # # Ваш код, который заполняет поля
    # first_name_el = browser.find_element_by_css_selector('[name="firstname"]')
    # first_name_el.send_keys("Denis")

    # last_name_el = browser.find_element_by_css_selector('[name="lastname"]')
    # last_name_el.send_keys("Ivanov")

    # email_el = browser.find_element_by_css_selector('[name="email"]')
    # email_el.send_keys("snoop@music.ua")

    # # Загружаем файл
    # file_el = browser.find_element_by_id("file")
    # file_el.send_keys(file_path)

    # кликаем по кнопке "submit"
    button = browser.find_element_by_id("book")
    button.click()


    WebDriverWait(browser, 5).until( EC.visibility_of_element_located((By.ID, "input_value")))

    # подтверждаем alert
    # windows = browser.window_handles
    # if len(windows) == 2:
    #     browser.switch_to.window(windows[-1])

    # находим нужное значение x
    x_el = browser.find_element_by_id("input_value")
    x_val = int(x_el.text)

    answer = calc(x_val)

    answer_form = browser.find_element_by_id("answer")
    answer_form.send_keys(str(answer))

    button = browser.find_element_by_id("solve")
    button.click()

    # Забираем ответ из всплывающего окна и копируем его в буфер, чтобы потом вставить комбинацией ctrl + v
    get_text_from_alert()

finally:
    # ожидание чтобы визуально оценить результаты прохождения скрипта
    time.sleep(5)
    # закрываем браузер после всех манипуляций
    browser.close()
    browser.quit()
