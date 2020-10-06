from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time


try: 
    link = "http://suninjuly.github.io/selects2.html"
    browser = webdriver.Chrome()
    browser.get(link)

    # Ваш код, который заполняет обязательные поля
    number_elmnts = browser.find_elements_by_css_selector('[id^="num"]')
    sum_number_elmnts = sum(map(lambda x: int(x.text), number_elmnts))

    select = Select(browser.find_element_by_css_selector("select#dropdown"))
    select.select_by_value(str(sum_number_elmnts)) # ищем элемент с текстом sum_number_elmnts
    # Проверяем, что смогли зарегистрироваться
    # ждем загрузки страницы
    time.sleep(1)

    # находим элемент, содержащий текст
    submit = browser.find_element_by_css_selector('button[type="submit"]')
    submit.click()

    # с помощью assert проверяем, что ожидаемый текст совпадает с текстом на странице сайта
    # assert "Congratulations! You have successfully registered!" == welcome_text

finally:
    # ожидание чтобы визуально оценить результаты прохождения скрипта
    time.sleep(5)
    # закрываем браузер после всех манипуляций
    browser.quit()
