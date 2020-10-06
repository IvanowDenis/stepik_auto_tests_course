from selenium import webdriver
# from selenium.webdriver.support.ui import Select
import time
import math


def calc(x):
    return math.log(abs(12 * math.sin(x)))


try: 
    link = "https://SunInJuly.github.io/execute_script.html"
    browser = webdriver.Chrome()
    browser.get(link)

    # Ваш код, который заполняет обязательные поля
    x_el = browser.find_element_by_id("input_value")
    x = int(x_el.text)

    answer = str(calc(x))

    answer_field = browser.find_element_by_id("answer")
    answer_field.send_keys(answer)

    robot_checkbox = browser.find_element_by_id("robotCheckbox")
    # if not robot_checkbox.is_displayed():
    browser.execute_script("return arguments[0].scrollIntoView(true);", robot_checkbox)
    time.sleep(1)
    robot_checkbox.click()

    robots_rule = browser.find_element_by_css_selector('[for="robotsRule"]')
    # if not robots_rule.is_displayed():
    browser.execute_script("return arguments[0].scrollIntoView(true);", robots_rule)
    time.sleep(1)
    robots_rule.click()


    # number_elmnts = browser.find_elements_by_css_selector('[id^="num"]')
    # sum_number_elmnts = sum(map(lambda x: int(x.text), number_elmnts))

    # select = Select(browser.find_element_by_css_selector("select#dropdown"))
    # select.select_by_value(str(sum_number_elmnts)) # ищем элемент с текстом sum_number_elmnts
    # Проверяем, что смогли зарегистрироваться
    # ждем загрузки страницы
    # time.sleep(1)

    # находим элемент, содержащий текст
    button = browser.find_element_by_tag_name("button")
    # if not button.is_displayed():
    browser.execute_script("return arguments[0].scrollIntoView(true);", button)
    button.click()
    # submit = browser.find_element_by_css_selector('button[type="submit"]')
    # submit.click()

    # с помощью assert проверяем, что ожидаемый текст совпадает с текстом на странице сайта
    # assert "Congratulations! You have successfully registered!" == welcome_text

finally:
    # ожидание чтобы визуально оценить результаты прохождения скрипта
    time.sleep(5)
    # закрываем браузер после всех манипуляций
    browser.quit()
