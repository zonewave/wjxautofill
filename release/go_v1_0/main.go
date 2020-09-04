package main

import (
	"flag"
	"fmt"
	gq "github.com/PuerkitoBio/goquery"
	log "github.com/astaxie/beego/logs"
	"github.com/tebeka/selenium/chrome"
	"strings"
	"time"
	"wjxautofill/src/go/conf"
)

import (
	"github.com/tebeka/selenium"
)

const (
	baseUrl   = "https://www.wjx.cn"
	loginUrl  = baseUrl + "/Login.aspx"
	mutualUrl = "https://www.wjx.cn/wjx/promote/joinbacklist.aspx?activityid="
)

func GetChrom() selenium.WebDriver {

	var opts []selenium.ServiceOption
	caps := selenium.Capabilities{
		"browserName": "chrome",
	}

	chromeCaps := chrome.Capabilities{
		//Prefs: imagCaps,
		Path: "",
		Args: []string{
			//"--headless", // 设置Chrome无头模式
			//	"--no-sandbox",
			"--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7", // 模拟user-agent，防反爬
		},
	}
	caps.AddChrome(chromeCaps)
	// 启动chromedriver
	_, err := selenium.NewChromeDriverService("d://myconfig//chromedriver.exe", 9515, opts...)

	if err != nil {
		log.Info("Error starting the ChromeDriver server: %v", err)
	}
	// 调起chrome浏览器
	webDriver, err := selenium.NewRemote(caps, fmt.Sprintf("http://localhost:%d/wd/hub", 9515))
	if err != nil {
		panic(err)
	}
	webDriver.AddCookie(&selenium.Cookie{
		Name:  "defaultJumpDomain",
		Value: "www",
	})

	return webDriver

}

func main() {
	var err error
	flag.Parse()
	if err = conf.Init(); err != nil {
		panic(err)
	}
	conf.BeeConfInit()
	crawler()

}
func crawler() {
	wd := GetChrom()
	var err error
	err = Login(wd)
	if err != nil {
		log.Error(err.Error())
		return
	}
	err = GetQuestionnaireListInPage(wd)
	if err != nil {
		log.Error(err.Error())
		return
	}

}
func Login(wd selenium.WebDriver) (err error) {

	err = wd.Get(loginUrl)
	if err != nil {

		return
	}
	var el selenium.WebElement
	el, _ = wd.FindElement(selenium.ByID, "UserName")
	el.SendKeys(conf.Conf.UserName)
	el, _ = wd.FindElement(selenium.ByID, "Password")
	el.SendKeys(conf.Conf.PassWord)
	el, _ = wd.FindElement(selenium.ByID, "LoginButton")
	err = el.Click()
	if err != nil {

		return
	}
	return
}

func GetQuestionnaireListInPage(wd selenium.WebDriver) (err error) {

	err = wd.Get(mutualUrl + conf.Conf.MutualId)
	if err != nil {

		return
	}
	html, _ := wd.PageSource()
	docs, _ := gq.NewDocumentFromReader(strings.NewReader(html))
	lists := docs.Find("#ctl02_ContentPlaceHolder1_divJoinData")
	urls := []string{}
	lists.Children().Each(func(i int, wjNode *gq.Selection) {
		if i < 1 {
			return
		}
		href, _ := wjNode.Find("a").Attr("href")
		urls = append(urls, href)

	})
	for i := range urls {

		err = wd.Get(baseUrl + urls[i])
		if err != nil {
			continue
		}
		if ok := IsHasFill(wd); ok {
			continue
		}
		//*[@id="divquestion1"]/ul/li[1]/a
		singHtml, _ := wd.PageSource()
		singDocs, _ := gq.NewDocumentFromReader(strings.NewReader(singHtml))

		sq := singDocs.Find("div[class=div_question]")
		isContinue := false
		qI := 0
		for {
			qI += 1
			if isContinue {
				break
			}
			fmt.Println(sq.Html())

			time.Sleep(time.Duration(conf.Conf.InternalSeconds) * time.Second)
			var inputs selenium.WebElement
			if tmp := sq.Find(".jqCheckbox"); tmp.Nodes != nil {
				ids := fmt.Sprintf("q%d_1", qI)
				inputs, err = wd.FindElement(selenium.ByXPATH, `//*[@id="`+ids+`"]/../a`)
				if err != nil {
					isContinue = true
					continue
				}
				inputs.Click()
			} else if tmp := sq.Find(".jqRadio"); tmp.Nodes != nil {
				ids := fmt.Sprintf("q%d_1", qI)
				inputs, err = wd.FindElement(selenium.ByXPATH, `//*[@id="`+ids+`"]/../a`)
				if err != nil {
					isContinue = true
					continue
				}
				//}#divquestion1 > ul > li:nth-child(1) > a
				inputs.Click()

			} else if tmp := sq.Find(".inputtext"); tmp.Nodes != nil {
				ids := fmt.Sprintf("q%d", qI)
				inputs, err = wd.FindElement(selenium.ByID, ids)
				if err != nil {
					isContinue = true
					continue
				}
				inputs.SendKeys("i don't know anything")
			} else {
				isContinue = true
				continue
			}
			sq = sq.Next()
			if sq.Nodes == nil {
				break
			}
		}

		if isContinue {
			continue
		}
		var submit selenium.WebElement
		submit, err = wd.FindElement(selenium.ByID, `submit_button`)
		if err != nil {
			continue
		}
		submit.Click()
		time.Sleep(2 * time.Second)
		IsFailFill(wd)
	}

	return
}

//###判断是否填写过
func IsHasFill(wd selenium.WebDriver) bool {
	PopCondition := func(wd selenium.WebDriver) (bool, error) {
		input, err := wd.FindElement(selenium.ByXPATH, `// *[ @ id = "divNotRun"] / div / div / input`)
		if err != nil {
			return false, err
		}
		input.Click()
		return true, nil
	}
	err := wd.WaitWithTimeout(PopCondition, time.Second*3)
	if err != nil { //没有填写过
		return false
	} else {
		return true
	}

}

//###判断是否填写失败
func IsFailFill(wd selenium.WebDriver) (err error) {
	wd.AcceptAlert()
	return
}
