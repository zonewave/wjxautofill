from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq


class Config(object):
    baseurl = 'https://www.wjx.cn'
    loginurl = 'https://www.wjx.cn/login.aspx'
    loginusername = '751761610@qq.com'
    loginpassoword = '318ZYB123'
    questionnairelisturl = 'https://www.wjx.cn/newwjx/manage/myquestionnaires.aspx'
    mutualurl = 'https://www.wjx.cn/wjx/promote/joinbacklist.aspx?activityid=9204675'


def login(browser, wait):
    browser.get(Config.loginurl)
    input = wait.until(
        EC.presence_of_element_located((By.ID, 'UserName'))
    )
    inputpwd = wait.until(
        EC.presence_of_element_located((By.ID, 'Password'))
    )
    submit = wait.until(
        EC.element_to_be_clickable((By.ID, 'LoginButton'))
    )

    input.clear()
    input.send_keys(Config.loginusername)
    inputpwd.clear()
    inputpwd.send_keys(Config.loginpassoword)
    submit.click()


def get_questionnaire_in_page(browser, wait):
    browser.get(Config.mutualurl)
    html = browser.page_source
    docs = pq(html)
    lists = docs('#ctl02_ContentPlaceHolder1_divJoinData')
    # ctl02_ContentPlaceHolder1_divJoinData > div:nth-child(1) > div > div:nth-child(2) > a
    for item in lists('a').items():
        getquestionnairesnode(Config.baseurl + item.attr('href'), browser, wait)


def getquestionnairesnode(url, browser, wait):
    browser.get(url)
    html = browser.page_source
    docs = pq(html)
    lists = docs('#ctl02_ContentPlaceHolder1_divJoinData')


if __name__ == '__main__':
    browser = webdriver.Chrome()

    wait = WebDriverWait(browser, 10)
    login(browser, wait)
    # questionid=getquestionid(browser,wait)
    get_questionnaire_in_page(browser, wait)
    # html = browser.page_source
    # doc = pq(html)
    # print(doc)
