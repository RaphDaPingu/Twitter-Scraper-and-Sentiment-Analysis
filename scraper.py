# Import Dependencies
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from langdetect import detect
from keys import *

driver = webdriver.Chrome()
driver.get("https://twitter.com/login")

#subject = "@danielblupi1"

# Setup the log in
sleep(2)
username = driver.find_element(By.XPATH,"//input[@name='text']")
username.send_keys(USERNAME)
next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
next_button.click()

sleep(2)
password = driver.find_element(By.XPATH,"//input[@name='password']")
password.send_keys(PASSWORD)
log_in = driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
log_in.click()

# Go to section where the search bar exists
#sleep(2)
#driver.get("https://twitter.com/explore")

# Search item and fetch it
#sleep(2)
#search_box = driver.find_element(By.XPATH,"//input[@data-testid='SearchBox_Search_Input']")
#search_box.send_keys(subject)
#search_box.send_keys(Keys.ENTER)

#sleep(2)
#people = driver.find_element(By.XPATH,"//span[contains(text(),'People')]")
#people = driver.find_element(By.XPATH,"//span[contains(text(),'Top')]")
#people.click()

#sleep(2)
#profile = driver.find_element(By.XPATH,"//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/div/div/div[2]/div")
#profile.click()

#//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div[1]/div/div/div/div/div[2]/div

# UserTag = driver.find_element(By.XPATH,"//div[@data-testid='User-Names']").text
# TimeStamp = driver.find_element(By.XPATH,"//time").get_attribute('datetime')
# Tweet = driver.find_element(By.XPATH,"//div[@data-testid='tweetText']").text
# Reply = driver.find_element(By.XPATH,"//div[@data-testid='reply']").text
# reTweet = driver.find_element(By.XPATH,"//div[@data-testid='retweet']").text
# Like = driver.find_element(By.XPATH,"//div[@data-testid='like']").text

Tweets = []

start = 0
end = 1000

filter_list = ["twitter.com", "free", "giveaway", "http", "https", "ai"]

sleep(5)

articles = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")

while True:
    for article in articles:
        try:
            Tweet = driver.find_element(By.XPATH,".//div[@data-testid='tweetText']").text.lower()

            if (detect(Tweet) == "en" and any(keyword in Tweet for keyword in filter_list) == False):
                Tweets.append(Tweet)
        except:
            pass
      
    driver.execute_script('window.scrollTo({s}, {e});'.format(s=start, e=end))
    
    sleep(2)
    articles = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")
    
    Tweets2 = list(set(Tweets))
    print("Tweets2:", str(Tweets2))
    if len(Tweets2) == 50:
        break
    
    start = end
    end += 1000

print("All the tweets:", str(Tweets2))
print("I managed to scrape this many tweets:", len(Tweets2))

import pandas as pd

df = pd.DataFrame(zip(Tweets2), columns=['Tweets'])

df.head()
df.to_excel(r"C:\\Users\\Administrator\\Desktop\\school work\\Sentiment Analysis\\tweets_test.xlsx",index=False)

import os

os.system('start "excel" "C:\\Users\\Administrator\\Desktop\\school work\\Sentiment Analysis\\tweets_test.xlsx"')
