from selenium import webdriver
import time
import os
import re


file_name = "file_for_stepic.txt"

current_dir = os.path.abspath(os.path.dirname(__file__))

file_path = os.path.join(current_dir, file_name)


try: 
    link = "http://suninjuly.github.io/file_input.html"
    browser = webdriver.Chrome()
    browser.get(link)

    # Ваш код, который заполняет поля
    first_name_el = browser.find_element_by_css_selector('[name="firstname"]')
    first_name_el.send_keys("Denis")

    last_name_el = browser.find_element_by_css_selector('[name="lastname"]')
    last_name_el.send_keys("Ivanov")

    email_el = browser.find_element_by_css_selector('[name="email"]')
    email_el.send_keys("snoop@music.ua")

    # Загружаем файл
    file_el = browser.find_element_by_id("file")
    file_el.send_keys(file_path)

    # кликаем по кнопке "submit"
    button = browser.find_element_by_tag_name("button")
    button.click()

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

finally:
    # ожидание чтобы визуально оценить результаты прохождения скрипта
    time.sleep(5)
    # закрываем браузер после всех манипуляций
    browser.quit()
