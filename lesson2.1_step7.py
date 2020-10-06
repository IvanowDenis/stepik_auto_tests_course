from selenium import webdriver
import time
import math

def calc(x):
  return str(math.log(abs(12*math.sin(int(x)))))


try: 
    link = "http://suninjuly.github.io/get_attribute.html"
    browser = webdriver.Chrome()
    browser.get(link)

    # Ваш код, который заполняет обязательные поля
    x_el = browser.find_element_by_id('treasure')
    x_value = int(x_el.get_attribute("valuex"))

    answer = calc(x_value)

    input_field = browser.find_element_by_id('answer')
    input_field.send_keys(answer)

    checkbox_el = browser.find_element_by_id('robotCheckbox')
    checkbox_el.click()

    # Отправляем заполненную форму
    radio_button = browser.find_element_by_id("robotsRule")
    radio_button.click()

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
    time.sleep(10)
    # закрываем браузер после всех манипуляций
    browser.quit()
