import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def getColnames(count_of_divs,driver):
    colnames = []
    for i in range(1,count_of_divs+1):
        header = driver.find_element(By.XPATH,'//*[@id="breed-page__traits__all"]/div/div/div['+str(i)+']/div/h4')
        colnames.append(header.get_attribute("innerHTML"))
    return colnames

def getScores(count_of_divs,driver):
    data = []
    for items in range(1,count_of_divs+1):
        score = driver.find_elements(By.XPATH,'//*[@id="breed-page__traits__all"]/div/div/div['+str(items)+']/div/div/div/div')
        value,count = "",0
        for i,s in enumerate(score,start=1):
            if "filled" in s.get_attribute("class"):
                count+=1
                value = str(count)
            if "selected" in s.get_attribute("class"):
                selected = driver.find_element(By.XPATH,'//*[@id="breed-page__traits__all"]/div/div/div['+str(items)+']/div/div/div/div['+str(i)+']/span')
                value+=""+selected.get_attribute("innerHTML")
        data.append(value)
    return data


def physicalCharacteristics(driver):
    len_h = len(driver.find_elements(By.XPATH,'/html/body/div[5]/div[2]/div/div[2]/div[2]/div[1]/div/p'))
    len_w = len(driver.find_elements(By.XPATH,'/html/body/div[5]/div[2]/div/div[2]/div[2]/div[2]/div/p'))
    height_male = driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/div/div[2]/div[2]/div[1]/div/p').text
    weight_male = driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/div/div[2]/div[2]/div[2]/div/p').text
    if len_h==1:
        height_female = 'N/A'
    else:
        height_female = driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/div/div[2]/div[2]/div[1]/div/p[2]').text
    if len_w==1:
        weight_female = 'N/A'
    else:
        weight_female = driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/div/div[2]/div[2]/div[2]/div/p[2]').text
    life = driver.find_element(By.XPATH,'/html/body/div[5]/div[2]/div/div[2]/div[2]/div[3]/div/p').text
    temp = [height_male,height_female,weight_male,weight_female,life]
    return temp

def convert(df,col):
    temp = df[col].apply(lambda x: re.findall("(\d+\.?\d*)",x)[:2])
    for x in temp:
        if not x:
            x.append('0')
    if 'Height' in col:
        constant = 2.54
    if 'Weight' in col:
        constant = 0.453592
    if 'Life' in col:
        constant = 1
    df[col] = df[col].fillna('0')
    min_value,max_value = [],[]
    for i in range(len(temp)):
        temp[i] = [float(x) for x in temp[i]]
        min_v = temp[i][0]*constant
        if len(temp[i])==1:
            min_value.append(min_v)
            max_value.append(min_v)
        elif len(temp[i])==2:
            min_value.append(min_v)
            max_v = temp[i][1]*constant
            if max_v>=min_v:
                max_value.append(max_v)
            else:
                max_value.append(min_v)
    return min_value,max_value