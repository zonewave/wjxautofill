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


def login():
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


def get_questionnaire_in_page():
    browser.get(Config.mutualurl)
    html = browser.page_source
    docs = pq(html)
    lists = docs('#ctl02_ContentPlaceHolder1_divJoinData')
    # ctl02_ContentPlaceHolder1_divJoinData > div:nth-child(1) > div > div:nth-child(2) > a
    flag=0
    for item in lists('a').items():
        # fieldset1
        if flag==0:
            flag=1
            continue
        browser.get(Config.baseurl + item.attr('href'))
        docs = pq(browser.page_source)
        savefile(item.attr('href'), browser.page_source)
        getquestionnairesnode(docs)


def savefile(filename, file):
    filename = removechar(filename, '/')
    filename = removechar(filename, '?')
    filename = removechar(filename, '.')
    filename = removechar(filename, '%')

    with open(filename + '.txt', 'w+', encoding='utf-8') as f:
        f.write(file)


def removechar(str, flag):
    strarr = str.split(flag)
    str = ''.join(strarr)
    return str


def getquestionnairesnode(docs):
    questionlists = docs('#fieldset1')
    for i, question in enumerate(questionlists('.div_question').items()):

        if len(question('.jqRadio')) > 0:
            ids='q' + str(i+1) + '_1'
            inputs=browser.find_element_by_id(ids)
           # // *[ @ id = "q1_2"]//*[@id="q1_2"]
            browser.find_element_by_xpath('''//*[@id="q1_2"]/../div[1]''')
            inputs.click()#divquestion1 > ul:nth-child(2) > li:nth-child(1) > a
        elif len(question('.jqCheckbox')) > 0:
            browser.find_element_by_id('q' + str(i+1)+ '_2').click()
        elif len(question('.inputtext')) > 0:
            browser.find_element_by_id('q' + str(i+1)).send_keys('I dont know anything')
        else:
            break
    return
    # elif len(question('.lisort')) > 0:
    #     sortlen=len(question('.lisort').items())
    #     for j in range(1,sortlen+1):
    #         browser.find_element_by_id('q' + i+'_'+j).click()
    # elif len(question('.rowth'))>0:
    #     rowlen=len(question('.rowth').items())
    #     for j in range(sortlen):
    #         browser.find_element_by_name('q' + i + '_' +j).click()
    # EC.element_to_be_clickable((By.CSS_SELECTOR. '//input[@value="cv1"]').click()  # click


# def isradio(docs):


browser = webdriver.Chrome()

wait = WebDriverWait(browser, 10)
if __name__ == '__main__':
    login()
    # questionid=getquestionid(browser,wait)
    get_questionnaire_in_page()
    # html = browser.page_source
    # doc = pq(html)
    # print(doc)
