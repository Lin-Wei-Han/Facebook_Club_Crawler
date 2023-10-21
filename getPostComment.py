from bs4 import BeautifulSoup
from crawler import FacebookCrawler
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import json

def getPage(driver):
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    return soup.select('.xv55zj0.x1vvkbs.x1rg5ohu.xxymvpz')

def openFulComment(driver):
    target_class = '.x1i10hfl.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x3nfvp2.x1q0g3np.x87ps6o.x1a2a7pz.x6s0dn4.xi81zsa.x1iyjqo2.xs83m0k.xsyo7zv.xt0b8zv'
    target = driver.find_elements(By.CSS_SELECTOR, target_class)

    while len(target) > 0:
        for more_comment_btn in target:
            driver.execute_script("arguments[0].click();",more_comment_btn)

        try:
            wait = WebDriverWait(driver, 2)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target_class)))
            target = driver.find_elements(By.CSS_SELECTOR, target_class)
        except:
            print('留言全數展開')
            break

def getComment(elements):
    row_list = []
    for element in elements:
        user_name = element.select('.x3nfvp2 span')
        content = element.select('.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs div')

        user_name = user_name[0].text if user_name else ''
        content = content[0].text if content else ''

        data = {}
        data['user_name'] = user_name
        data['content'] = content
        row_list.append(data)
    return row_list

if __name__ == '__main__':
    post_id = '1831438957003698'
    url = f'https://www.facebook.com/groups/1786425331505061/posts/{post_id}/'

    crawler = FacebookCrawler()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
    driver = webdriver.Chrome(options = chrome_options)

    driver.set_window_size(800,800)
    driver.get(crawler.login_url)

    crawler.login_facebook(driver)

    driver.get(url)
    openFulComment(driver)
    row_list = getComment(getPage(driver))

    with open('post_comment.json', 'w', encoding='utf-8') as json_file:
        json.dump(row_list, json_file, ensure_ascii=False, indent=4)