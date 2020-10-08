from selenium import webdriver
import time
import os
import re
import math
from parsel import Selector
import requests
import urllib.parse as url_parse
import argparse



COOKIES_FILE = "stepic_cookies.txt"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
xpaths = {'quiz_url': '//li[contains(., "страницу")][contains(., "ткрыть")]//a/@href', 
'quiz_form': '//form/@onsubmit', }



def get_hashcode(problem_number):
    answer = math.log(round(int(time.time())) * int(problem_number))
    return answer

solve_methods = {'showResult': get_hashcode, }


def parse_quiz_page(page):
    sel = Selector(page)
    form_el = sel.xpath(xpaths['quiz_form']).get()
    paths = re.findall("([^(]+)\((\d+)", form_el)
    if paths:
        method, problem_number = paths[0]
    return (method, problem_number)


def get_quiz_url(page):
    sel = Selector(page)
    answer = sel.xpath(xpaths['quiz_url']).get()
    return answer


def open_cookies(cookies_file=COOKIES_FILE):
    path_cookies_file = get_file_path(cookies_file)
    with open(path_cookies_file) as f:
        cookies = f.read().strip()
    cookies = cookies.split('; ')
    cookies = dict(i.split('=') for i in cookies)
    # print(cookies)
    return cookies


def get_file_path(file_name=""):
    current_dir = os.path.abspath(os.path.dirname(__file__))
    print("Current_dir", current_dir)
    file_path = os.path.join(current_dir, file_name)
    print(file_path)
    return file_path


def save_page(page):
    with open("test_page.html", "w", encoding="utf-8") as f:
        f.write(page)
    return


def get_stepic_api_url(lesson_id):
    stepic_api__url = f"https://stepik.org/api/lessons/{lesson_id}"
    return stepic_api__url


def get_steps_url(stepik_ids):
    url_query = url_parse.urlencode({'ids[]': stepik_ids}, doseq=True)
    url = url_parse.urlunsplit(("https", "stepik.org", "api/steps", url_query, ""))
    return url


def parse_lesson_link(url):
    lesson_id = re.findall("lesson.(\d+)", url)
    if lesson_id:
        lesson_id = lesson_id[0]
    else:
        return False
    step_number = re.findall("step.(\d+)", url)
    if step_number:
        step_number = int(step_number[0])
    else:
        return False
    return {"lesson_id": lesson_id, "step_number": step_number}


def get_profile_id(session, url):
    response = session.get(url)
    sel = Selector(response.text)
    user_href_el = sel.css('.navbar__profile').xpath('.//a[contains(@href, "user")]/@href')
    user_href = user_href_el.re_first(r".+?(\d+)")
    return user_href


def get_attempts(session, step, user):
    query = url_parse.urlencode({'step': [step], 'user': [user]}, doseq=True)
    url = url_parse.urlunsplit(('https', 'stepik.org', '/api/attempts', query, ''))
    response = session.get(url)
    if response:
        data = response.json()
        attempts = data['attempts']
        for attempt in attempts:
            if attempt['status'] == "active":
                return attempt['id']


def send_submission(session, submission, attempt, cookies, referer, step, user):
    cookies = session.cookies
    print('Cookies', cookies)
    csrftoken = ""
    for name, value in cookies.items():
        if name == 'csrftoken':
            csrftoken = value
            print("Csrftoken", csrftoken)
            break
    post_url = "https://stepik.org/api/submissions"
    headers = {'x-csrftoken': csrftoken,
                'referer': referer,
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'uk,en;q=0.9,en-US;q=0.8,ru;q=0.7,la;q=0.6',
                'content-type': 'application/json; charset=UTF-8',
                'origin': 'https://stepik.org',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest' }

    data = {'submission': 
                        {'eta': None, 'has_session': False, 'hint': None, 'reply': 
                            {'text': f"{submission:.15f}", 'files': []}, 
                            'reply_url': None, 'score': None, 'session_id': None, 
                            'status': None, 'time': None, 'attempt': f"{attempt}", 'session': None}}
    response = session.post(post_url, json=data, headers=headers)
    print("Send submission\nstatus:", response.status_code)
    if response.status_code:
        query = url_parse.urlencode({'limit': [1], 'order': ['desc'], 'step': [step], 'user': [user]}, doseq=True)
        url = url_parse.urlunsplit(('https', 'stepik.org', '/api/submissions', query, ''))
        response = session.get(url)
        print("Submission get:\nStatus", response.status_code)
        print("Data:", response.json())
        status_answer = response.json()['submissions'][0]['status']
        print("Status answer:", status_answer)
        return status_answer



def main(url):
    file_name = "file_for_stepic.txt"
    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_dir, file_name)

    cookies = open_cookies()
    headers = {'User-Agent': UA, 'user-agent': UA}
    try:
        session = requests.session()
        session.headers.update(headers)
        session.cookies.update( cookies)
        session.headers.pop('User-Agent')

        profile_id = get_profile_id(session, url)

        parsed_lesson_url = parse_lesson_link(url)
        stepic_api_url = get_stepic_api_url(parsed_lesson_url['lesson_id'])
        print("Stepic Api Url", stepic_api_url)

        response = session.get(stepic_api_url)
        print("Response for", stepic_api_url, response)
        steps = response.json()['lessons'][0]['steps']
        step = steps[parsed_lesson_url['step_number'] -1]
        steps_url = get_steps_url([step])


        response = session.get(steps_url)
        print("Response for", steps_url, response)
        step_description = response.json()["steps"][0]["block"]["text"]
        quiz_url = get_quiz_url(step_description)
        print("Quiz Url:", quiz_url)


        response = session.get(quiz_url)
        method, problem_number = parse_quiz_page(response.text)
        print('method', method, '\nproblem_number', problem_number)
        answer = solve_methods[method](problem_number)
        print("Answer", answer)

        attempt = get_attempts(session, step, profile_id)

        status_answer = send_submission(session, answer, attempt, cookies, url, step, profile_id)
    finally:
        session.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stepik tasks solver.')
    parser.add_argument('url', metavar="https://stepik.org/lesson/228249/step/8?unit=200781", 
                        type=str, help='Url for the task')
    args = parser.parse_args()
    main(args.url)

