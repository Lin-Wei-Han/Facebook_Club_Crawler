from selenium import webdriver
from crawler import FacebookCrawler
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json

def getPage():
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    return soup.select('.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z')

def openTwitterShareBtn(driver):
    share_btn = driver.find_elements(By.CSS_SELECTOR, '.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z div.xq8finb.x16n37ib > div > div:nth-child(3) > div')
    for btn in share_btn:
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)

    twitter_send_btn = driver.find_elements(By.CSS_SELECTOR, '.xsag5q8.xz9dl7a > div > div:nth-child(5) > a')
    print('twitter_send_btn：', len(twitter_send_btn))
    if twitter_send_btn: link_list = [crawler.getPostId(element) for element in twitter_send_btn]
    print('link_list：', len(link_list))
    return link_list

def getElement(elements, link_list):
    row_list = []
    for index, element in enumerate(elements):
        like = 0
        
        name = element.select('.x1heor9g.x1qlqyl8.x1pd3egz.x1a2a7pz.x1gslohp.x1yc453h strong:first-child span')[0].text
        createAt = element.select('.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm span')[0].text
        like = element.select('.xt0b8zv.x2bj2ny.xrbpyxo.xl423tq span.x1e558r4')[0].text
        comment_and_share = element.select('.x9f619.x1n2onr6.x1ja2u2z.x78zum5.x2lah0s.x1qughib.x1qjc9v5.xozqiw3.x1q0g3np.xykv574.xbmpl8g.x4cne27.xifccgj span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xi81zsa')
        comment, share = crawler.getCommentShare(comment_and_share)
        
        content_1 = element.select('.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.x126k92a')
        content_2 = element.select('.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.xtlvy1s.x126k92a')
        text_string_1 = ','.join(list(content_1[0].stripped_strings)) if content_1 else ""
        text_string_2 = ','.join(list(content_2[0].stripped_strings)) if content_2 else ""
        full_text = text_string_1 + (',' if text_string_1 and text_string_2 else '') + text_string_2

        data = {}
        data['name'] = name
        data['createAt'] = createAt
        data['like'] = like
        data['comment'] = comment
        data['share'] = share
        data['article'] = full_text
        data['post_id'] = link_list[index]
        row_list.append(data)
    return row_list

if __name__ == '__main__':
    search_word = '生魚片'
    url = f'https://www.facebook.com/groups/1786425331505061/search/?q={search_word}'

    crawler = FacebookCrawler()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
    driver = webdriver.Chrome(options = chrome_options)

    driver.set_window_size(800,800)
    driver.get(crawler.login_url)
    crawler.login_facebook(driver)

    time.sleep(1)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    stop_flag = False
    elements = driver.find_elements(By.CSS_SELECTOR, '.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z .xt0b8zv.x2bj2ny.xrbpyxo.xl423tq span.x1e558r4')
    while len(elements) < 100 and not stop_flag:
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z')))
        driver.execute_script(
            '''
                let elements = document.querySelectorAll(".x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z .xt0b8zv.x2bj2ny.xrbpyxo.xl423tq span.x1e558r4");
                for (var i = 0; i < elements.length; i++) {
                    let element = elements[i];
                    let value = (element.textContent === '') ? 0 : parseInt(element.textContent, 10);

                    if (!isNaN(value)) {
                        let parentElement = element.closest(".x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z");
                        if (parentElement && value < 100) {
                            parentElement.parentNode.removeChild(parentElement);
                        }
                    }
                }
            '''
        )
        
        stop_class = '.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xi81zsa.x2b8uid'
        stop_block = driver.find_elements(By.CSS_SELECTOR, stop_class)
        if stop_block: stop_flag = True
        elements = getPage()

    
    time.sleep(1)
    crawler.openFullArticle(driver)
    elements = getPage()

    link_list = openTwitterShareBtn(driver)

    row_list = getElement(elements, link_list)

    with open('data/sashimi_100_posts.json', 'w', encoding='utf-8') as json_file:
        json.dump(row_list, json_file, ensure_ascii=False, indent=4)

    driver.quit()