from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import re
import math



# file_name = "file_for_stepic.txt"

# current_dir = os.path.abspath(os.path.dirname(__file__))

# file_path = os.path.join(current_dir, file_name)

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
    link = "http://suninjuly.github.io/redirect_accept.html"
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={get_user_data_folder_path()}")
    browser = webdriver.Chrome(options=chrome_options)
    # chrome_options.add_argument("user-data-dir=chrome-data") 
    browser.get(link)

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
    button = browser.find_element_by_tag_name("button")
    button.click()

    # подтверждаем alert
    windows = browser.window_handles
    if len(windows) == 2:
        browser.switch_to.window(windows[-1])

    # находим нужное значение x
    x_el = browser.find_element_by_id("input_value")
    x_val = int(x_el.text)

    answer = math.log(abs(12 * math.sin(x_val)))

    answer_form = browser.find_element_by_id("answer")
    answer_form.send_keys(str(answer))

    button = browser.find_element_by_tag_name("button")
    button.click()

    # Забираем ответ из всплывающего окна и копируем его в буфер, чтобы потом вставить комбинацией ctrl + v
    get_text_from_alert()

finally:
    # ожидание чтобы визуально оценить результаты прохождения скрипта
    time.sleep(5)
    # закрываем браузер после всех манипуляций
    browser.quit()
