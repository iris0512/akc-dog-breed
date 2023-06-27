import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from akc_utils import *

path = "YOUR PATH HERE"

search_query = 'https://www.akc.org/dog-breeds/'
page = requests.get(search_query)
soup = BeautifulSoup(page.content, "html.parser")

divs = soup.find("div","breed-explorer")
breed_div = divs.find("div","custom-select")

breedList = []
for o in breed_div.find_all("option"):
    url,name = '',''
    if o.attrs['value']:
        url = o.attrs['value']
        name = o.text
        breedList.append([url,name])
df_breed = pd.DataFrame(breedList,columns=['URL','Breed'])

DRIVER_PATH = 'C:\\Users\\Siri Vishal Kumar\\Downloads\\chromedriver_win32\\'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

data,missing = [],[]
for i in range(len(df_breed)):
    name = df_breed.iloc[i][1]
    url = df_breed.iloc[i][0]
    print("Now extracting info for",name)
    try:
        driver.get(url)
        driver.implicitly_wait(10)
        ##group__column div
        group = driver.find_elements(By.XPATH, '//*[@id="breed-page__traits__all"]/div/div') 
        ##counting divs/attributes in the page
        count_of_divs = len(driver.find_elements(By.XPATH,'//*[@id="breed-page__traits__all"]/div/div/div')) 
        #getting temperament and group
        temp = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[2]/div/div[1]/div[1]/p'))).text
        group = driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/div/div[1]/div[1]/div[2]/a').text
        #get average sizes and life expectancy
        char = physicalCharacteristics(driver)
        #get traits and characteristics
        values = getScores(count_of_divs,driver)
        values.extend(char)
        values.extend([temp,group,name,url])
        #appending it to list
        data.append(values)
    except Exception as e:
        print("Error")
        missing.append([name,url])

colnames = ['Affectionate With Family','Good With Young Children','Good With Other Dogs','Shedding Level',
            'Coat Grooming Frequency','Drooling Level','Coat Type','Coat Length','Openness To Strangers',
            'Playfulness Level','Watchdog/Protective Nature','Adaptability Level','Trainability Level',
            'Energy Level','Barking Level','Mental Stimulation Needs','Height_Male','Height_Female',
            'Weight_Male','Weight_Female','Life_Expectancy','Temperament','Group','Breed','URL']

df_akc = pd.DataFrame(data,columns=colnames)
df_akc.to_csv(path+'american-kennel-club-dataset.csv',index=False)