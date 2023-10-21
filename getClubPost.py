from selenium import webdriver
from dotenv import load_dotenv,find_dotenv
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import re
import datetime
import time
import json
import pandas as pd

load_dotenv(find_dotenv())

def login_facebook(driver, FACEBOOK_MAIL, FACEBOOK_PASSWORD):
    try:
        login_btn = driver.find_element(By.CSS_SELECTOR, 'input.bk.bl.bm.bn.bo.bp')
        mail_input = driver.find_element(By.CSS_SELECTOR, '#m_login_email')
        password_input = driver.find_element(By.CSS_SELECTOR, 'input.bf.bg.bi.bj')

        mail_input.send_keys(FACEBOOK_MAIL)
        password_input.send_keys(FACEBOOK_PASSWORD)
        login_btn.click()
    except Exception as e:
        print(f"Login error: {str(e)}")

class ScrapeThread:
    def __init__(self):
        self.FACEBOOK_MAIL = os.environ.get("FACEBOOK_MAIL")
        self.FACEBOOK_PASSWORD = os.environ.get("FACEBOOK_PASSWORD")

    def getPage(self, driver):
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')
        return soup.select('#m_group_stories_container article')
    
    def get_post_id(self, href):
        post_id = ''
        pattern = r"/(\d+)/\?"
        match = re.search(pattern, href)
        if match:
            post_id = match.group(1)
        return post_id
    
    def getPostInfo(self, elements):
        row_list = []
        for element in elements:
            name = element.select('header h3 > span > strong:nth-child(1) > a')
            if len(name) == 0: name = element.select('header h3 > strong:nth-child(1) > a')
            name = name[0].text if name else ""
            
            content = element.select('div.dv div > span')
            if len(content) == 0: content = element.select('div.ds div > span')
            full_text = ''.join(list(content[0].stripped_strings)) if content else ''

            createAt = element.select('abbr')
            createAt = createAt[0].text if createAt else ""

            like = element.select('a.ee.ef')
            if len(like) == 0: like = element.select('a.eb.ec')
            like = like[0].text if like else ""

            comment = element.select('footer > div:nth-child(2) > a.ef')
            if len(comment) == 0: comment = element.select('a.ec')
            comment = comment[0].text if comment else ""

            href = element.select('footer > div:nth-child(2) > a:-soup-contains("完整動態")')
            post_id = self.get_post_id(href[0]['href']) if href else ""

            data = {}
            data['name'] = name
            data['createAt'] = createAt
            data['like'] = like
            data['comment'] = comment
            data['article'] = full_text
            data['post_id'] = post_id
            row_list.append(data)
        return(row_list)

    def run(self, driver, url):
        driver.get(url)

        login = driver.find_elements(By.CSS_SELECTOR, 'input.bk.bl.bm.bn.bo.bp')
        if login: login_facebook(driver, FACEBOOK_MAIL, FACEBOOK_PASSWORD)

        elements = self.getPage(driver)
        row_list = self.getPostInfo(elements)

        return row_list

if __name__ == '__main__':
    previous_time = datetime.datetime.now()
    print(previous_time)

    app = ScrapeThread()
    url = 'https://mbasic.facebook.com/groups/1786425331505061'
    amount = 3000

    FACEBOOK_MAIL = os.environ.get("FACEBOOK_MAIL")
    FACEBOOK_PASSWORD = os.environ.get("FACEBOOK_PASSWORD")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
    driver = webdriver.Chrome(options = chrome_options)
    
    result = []
    while len(result) < amount:
        data = app.run(driver, url)
        result.extend(data)

        view_more_button = driver.find_element(By.CSS_SELECTOR, "#m_group_stories_container > div > a")
        url = view_more_button.get_attribute("href")

    print(result)
    print(len(result[:amount]))
    with open('club_posts.json', 'w', encoding='utf-8') as json_file:
        json.dump(result[:amount], json_file, ensure_ascii=False, indent=4)

    time_difference = (datetime.datetime.now() - previous_time).total_seconds()
    print(time_difference)