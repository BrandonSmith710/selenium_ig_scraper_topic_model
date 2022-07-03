import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import re
import pandas as pd
import csv, pickle

data_dict = {'date': [], 'likes': [], 'caption': []}

class InstaBot:
    """The class is set to require the username and password of an existing instagram
       account, as well as the number of photos to scrape. The bot currently only supports
       a number of photos that is less than or equal to the existing number of photos posted
       by the account associated with the username. The bot object logs in, navigates to the
       profile page of the account, then scrapes all of the captions and number of likes for
       the specified number of posted photos.
       
       Parameters:
           username: existing user account name for instagram
           
           pw: password for existing instagram account
           
           scrape: positive integer, the number of posted photos to scrape
           
       Returns:
           pandas dataframe containing the caption text and number of likes for each posted
           photo
       """
    
    
    def __init__(self, username, pw, scrape):
        self.username = username
        self.name = username
        self.count = 0
        self.scrape = scrape
        self.driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
        self.driver.get("https://www.instagram.com/")
        sleep(4)

        # for log in 
        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(username)
        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input").send_keys(pw)
        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]").click()
        sleep(3)
        # DONT SAVE PASS
        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/section/main/div/div/div/div/button").click()
        sleep(2)
        # click Not Now for the next spam question from IG
        self.driver.find_element(by=By.CLASS_NAME, value='aOOlW.HoLwm').click()

        sleep(3)
        # click then send keys
        self.driver.find_element(by=By.CLASS_NAME, value="TqC_a.xVrpc").click()
        sleep(2)
        self.driver.find_element(by= By.XPATH, value='/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input').send_keys(self.name)
        sleep(2)
        self.driver.find_element(by= By.XPATH, value='/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input').send_keys(Keys.ENTER)
        sleep(2)
        self.driver.find_element(by= By.XPATH, value='/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input').send_keys(Keys.ENTER)
        sleep(2)
        self.driver.find_element(by=By.CLASS_NAME, value='v1Nh3.kIKUG._bz0w').click()
        
        # scrape first 500 photos
        while self.count < self.scrape:
            
            try:
                likes = self.driver.find_element(by=By.CLASS_NAME, value='EDfFK.ygqzn').text
                data_dict['likes'] += [likes]
                date = self.driver.find_element(by=By.CLASS_NAME, value='NnvRN').text
                data_dict['date'] += [date]
                caption = self.driver.find_element(by=By.CLASS_NAME, value='MOdxS ').text
                data_dict['caption'] += [caption]

            except:
                print('No likes')
            
            if not len(data_dict['caption']) == len(data_dict['likes']) == len(data_dict['date']):
                a1 = [c+' '+str(len(data_dict[c])) for c in data_dict.keys()]

                minn = min(a1, key=lambda x: x.split()[-1])
                data_dict[minn.split()[0]] += ['None']
            self.count += 1
            sleep(4)

            # move to next photo
            self.driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.RIGHT)
            sleep(2)

        pd.DataFrame(data_dict).to_csv('brandon_ig_scrape3.csv', index=False)    
        
        sleep(8)
    
    def get_unfollowers(self):
        # CLICK PROFILE PIC
        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/span").click()
        self.driver.find_element(by=By.XPATH, value="/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]/div/div[2]/div/div/div/div").click()
        

InstaBot(username, password, 1000)
