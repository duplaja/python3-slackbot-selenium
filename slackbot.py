#!/usr/bin/python3
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#Slack variables
user_email = "login_email"
user_password = "login_password"
slackname = "subdomain-here" #the subdomain slackname.slack.com
channel_id = "channel or user ID number" #Grabbed by looking at the url in web browser, can be a channel or user

#Joke Variables
joke_fname = 'Smith'
joke_lname = 'Smithison'

#Handles getting the joke
joke_url = "http://api.icndb.com/jokes/random?firstName="+joke_fname+"&lastName="+joke_lname+"&escape=javascript&limitTo=[nerdy]"
raw_joke = requests.get(joke_url).content.decode('utf8')
joke = json.loads(raw_joke)
joke_text = joke['value']['joke']


#Runs with Headless enabled
chrome_options = Options()  
chrome_options.add_argument("--headless")  
driver = webdriver.Chrome(chrome_options=chrome_options)

#Uncomment line 34, and comment line 31 to run in windowed mode
#driver = webdriver.Chrome()

#Opens Login Page
driver.get("https://"+slackname+".slack.com/")

#Fills out login form and submits it
driver.find_element_by_id("email").send_keys(user_email)
driver.find_element_by_id ("password").send_keys(user_password)
driver.find_element_by_id("signin_btn").click()

#navigates to channel given in channel_id
driver.get("https://"+slackname+".slack.com/messages/"+channel_id+"/details/")

#Explicitly wait for the element to become present (max 30 seconds)
wait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "msg_input")))

time.sleep(4) #extra wait to be sure page has loaded

#Sends keystrokes to generic page: Used because Slack uses a div / p as an input
actions = webdriver.ActionChains(driver)
actions.send_keys('*Jokebot:* '+joke_text+'\n')
actions.perform()

time.sleep(1) #Pauses 1 second to be sure its finished
driver.quit() #Closes the window
