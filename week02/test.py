from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json
import time
from lxml import etree
from pathlib import Path


def get_driver():
    try:
        return webdriver.Chrome()
    except Exception:
        return webdriver.Firefox()

# login into the zhihu


def login():
    driver = get_driver()
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)
    LOGIN_URL = 'https://www.zhihu.com/'
    driver.get(LOGIN_URL)
    input("Press Enter after login at the popup chrome browser")
    time.sleep(5)

    return driver


def get_answers(question_url, driver):
    # visit target url
    driver.get(question_url)

    # Some topic go folded, some are not
    try:
        number_text = driver.find_element_by_partial_link_text('查看全部').text
        number = int(re.search('[0-9]+', number_text).group())
        driver.find_element_by_partial_link_text('查看全部').click()
    except:
        tree = etree.HTML(driver.page_source)
        number = int(tree.xpath(
            '//div/h4[@class="List-headerText"]/span/text()')[0].split(" ")[0])

    # Scroll to get some dynamic page
    print(number)
    number_question = 50 if number >= 15 else number
    print(number_question)
    for k in range(number_question):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        ActionChains(driver).key_down(Keys.DOWN).perform()
        time.sleep(5)
        # Get Answers source html
        if k == number_question - 1:
            tree = etree.HTML(driver.page_source)

    content = tree.xpath('''//div[@class="RichContent-inner"]/span''')

    # Filter out the Top 15 answers and save to a file
    upperBound = 15 if len(content) >= 15 else len(content)
    print(len(content), upperBound)

    Path(f"./savefile/").mkdir(parents=True, exist_ok=True)

    with open("savefile/answers.txt", "w+") as f:
        for i in range(upperBound):
            outputString = f"Answer of Question {i} is \n" + \
                content[i].xpath('string(.)') + "\n--------\n"
            f.write(outputString)


if __name__ == "__main__":
    question_url = 'https://www.zhihu.com/question/432808267'
    driver = login()

    get_answers(question_url, driver)
