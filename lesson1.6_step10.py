from selenium import webdriver
import time

try: 
    link = "http://suninjuly.github.io/registration1.html"
    browser = webdriver.Chrome()
    browser.get(link)

    # Ваш код, который заполняет обязательные поля
    input_first_name = browser.find_element_by_css_selector(".first_block .first")
    input_first_name.send_keys("Denis")

    input_last_name = browser.find_element_by_css_selector(".first_block .second")
    input_last_name.send_keys("Ivanov")

    input_email = browser.find_element_by_css_selector(".first_block .third")
    input_email.send_keys("snoop@music.ua")

    # Ваш код, который заполняет не обязательные поля
    # input_phone = browser.find_element_by_class_name("city")
    # input_phone.send_keys("+38044 255 7333")

    # input_address = browser.find_element_by_id("country")
    # input_address.send_keys("вулиця Банкова, 11, Київ, 01220")

    # Отправляем заполненную форму
    button = browser.find_element_by_css_selector("button.btn")
    button.click()

    # Проверяем, что смогли зарегистрироваться
    # ждем загрузки страницы
    time.sleep(1)

    # находим элемент, содержащий текст
    welcome_text_elt = browser.find_element_by_tag_name("h1")
    # записываем в переменную welcome_text текст из элемента welcome_text_elt
    welcome_text = welcome_text_elt.text

    # с помощью assert проверяем, что ожидаемый текст совпадает с текстом на странице сайта
    assert "Congratulations! You have successfully registered!" == welcome_text

finally:
    # ожидание чтобы визуально оценить результаты прохождения скрипта
    time.sleep(10)
    # закрываем браузер после всех манипуляций
    browser.quit()






# не забываем оставить пустую строку в конце файла
# $x('//input').forEach( function(x) {x.value = "asdf"} )

# $x('//button[@type="submit"]')[0].click()


