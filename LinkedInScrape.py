from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time 

def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait to load page
        time.sleep(2)  # You can adjust the sleep time according to your needs
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


service = Service(executable_path="/Users/bubby/Documents/PythonProjects/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service = service)

driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3891327736&f_WT=2&keywords=data%20scientist&origin=JOBS_HOME_SEARCH_BUTTON&refresh=true')
scroll_to_bottom()
soup = BeautifulSoup(driver.page_source, 'lxml')

boxes = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
print(len(boxes))


df = pd.DataFrame({'Job Title' : [''], 'Company':[''], 'Location':[''], 'When Posted':[''], 'Link':['']})


for box in boxes:
    link = box.find('a').get('href')
    jobTitle = box.find('h3', class_='base-search-card__title').text
    Company = box.find('a', class_='hidden-nested-link').text
    Location = box.find('span', class_='job-search-card__location').text
    whenPosted = box.find('time').get('datetime')
    df = df._append({'Job Title' : jobTitle, 'Company':Company, 'Location':Location, 'When Posted':whenPosted, 'Link':link}, ignore_index = True)

print(df.shape[0])

df.to_csv('postings.csv', index=False)

driver.quit()