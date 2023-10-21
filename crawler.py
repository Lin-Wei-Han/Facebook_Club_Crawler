from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv,find_dotenv
import time
import json
import urllib.parse
import os
import re

load_dotenv(find_dotenv())

class FacebookCrawler:
    def __init__(self):
        self.facebook_mail = os.environ.get("FACEBOOK_MAIL")
        self.facebook_password = os.environ.get("FACEBOOK_PASSWORD")
        self.login_url = 'https://www.facebook.com/login/device-based/regular/login/?login_attempt=1&next=https%3A%2F%2Fwww.facebook.com%2Fgroups%2F1786425331505061%2Fposts%2F1831438957003698%2F'

    def login_facebook(self, driver):
        try:
            email_element = driver.find_element(By.CSS_SELECTOR,'#email_container input')
            password_element = driver.find_element(By.CSS_SELECTOR,'._55r1._1kbt input')
            login_button = driver.find_element(By.CSS_SELECTOR, '#loginbutton')

            email_element.send_keys(self.facebook_mail)
            password_element.send_keys(self.facebook_password)
            login_button.click()
        except Exception as e:
            print(e)

    def openFullArticle(self, driver):
        try:
            target_1_class = '.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.x126k92a div .x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f'
            target_2_class = '.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.xtlvy1s.x126k92a div .x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f'
            target_1 = driver.find_elements(By.CSS_SELECTOR, target_1_class)
            target_2 = driver.find_elements(By.CSS_SELECTOR, target_2_class)

            for target in target_2:
                try:
                    driver.execute_script("arguments[0].click();",target)
                except:
                    continue
            for target in target_1:
                try:
                    driver.execute_script("arguments[0].click();",target)
                except:
                    continue
        except:
            print('展開錯誤')

    def getCommentShare(self, comment_and_share):
        comment = 0
        share = 0
        check = []
        for feature in comment_and_share:
            feature_text = feature.text
            check.append(feature_text)
            match = re.search(r'\d+', feature_text)

            if feature_text[-2:] == '留言':
                comment = int(match.group())
            elif feature_text[-2:] == '分享':
                share = int(match.group())
            else:
                continue
        
        if len(check) == 2 and comment == 0 and share == 0:
            comment = check[0]
            share = check[1]

        return comment, share
    
    def getPostId(self, twitter_send_btn):
        href = twitter_send_btn.get_attribute('href')

        parsed_url = urllib.parse.urlparse(href)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        if 'u' in query_params:
            post_url = query_params['u'][0]
            parsed_url = urllib.parse.urlparse(post_url)
            query_params = urllib.parse.parse_qs(parsed_url.query)

            match = re.search(r'/posts/(\d+)/', query_params['url'][0])
            post_id = match.group(1)
        return post_id

    
