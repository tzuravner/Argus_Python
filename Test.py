from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from itertools import repeat
import os
import time


def openRepo():
    driver.get("https://github.com/")
    # get the search textbox
    search_field = driver.find_element_by_css_selector("[placeholder='Search GitHub']")
    search_field.clear()
    # enter search keyword and submit
    search_field.send_keys("Selenium")
    start = time.time()
    search_field.send_keys(Keys.ENTER)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".repo-list-item")))
    end = time.time()
    executingtime = end - start
    writeresulttime("Searching selenium at github",executingtime)



def exportRepo():
    lists = driver.find_elements_by_css_selector(".repo-list-item")
    for listitem in lists:
        Title = listitem.find_element_by_css_selector(".v-align-middle").text
        URL = listitem.find_element_by_css_selector(".v-align-middle").get_attribute("href")
        try:
         Description = listitem.find_element_by_css_selector(".pr-4").text
        except:
           print("no description")
        Tags = listitem.find_elements_by_css_selector(".topic-tag")
        Tagresult = ""
        if (Tags.count == 0):
            Tagresult = "none"
        else:
            for Tag in Tags:
                Tagresult = Tagresult + " | " + Tag.text
        Time = listitem.find_element_by_css_selector("relative-time").text
        Lang = listitem.find_element_by_css_selector(".d-table-cell").text
        Star = listitem.find_element_by_css_selector(".muted-link:not(.mt-2)").text
        print("finished to analyze a repo")
        try:
            writeresult(Title, Description, Tagresult, Time, Lang, Star)
        except:
            print("failed to print the result")

def writeresult(Title, Description ,Tagresult , Time, Lang, Star):

    Title = re.sub(',', ' ', Title)
    Description=re.sub(',', ' ', Description)
    Tagresult = re.sub(',', ' ', Tagresult)
    Time = re.sub(',', ' ', Time)
    text = "%s,%s,%s,%s,%s,%s \n" % (Title, Description ,Tagresult , Time, Lang, Star)
    file.writelines(text)


def writeresulttime(Title, data):
   text = "%s: %s*(Seconds) \n" % (Title, data)
   file1.writelines(text)


def clickOnNextPage():
    start = time.time()
    driver.find_element_by_css_selector(":not(.next_page)[rel='next']").click()
    end = time.time()
    executingtime = end-start
    print("moved to next page")
    print(end-start)
    writeresulttime("Clicking on the next page took" , executingtime)


if os.path.exists("RepoDetail.csv"):
    os.remove("RepoDetail.csv")
if os.path.exists("TimingResult.txt"):
    os.remove("TimingResult.txt")
file = open("RepoDetail.csv","a")
file1 = open("TimingResult.txt","a")
file.writelines("Title,Description,Tags,Time,Lang,Star \n")
driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.maximize_window()
openRepo()
exportRepo()
for i in repeat(None, 4):
    clickOnNextPage()
    driver.refresh()
    exportRepo()

# close the browser window
file.close()
driver.quit()
