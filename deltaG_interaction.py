from selenium import webdriver
from selenium.webdriver.common.by import By

# create webdriver object
driver = webdriver.Firefox()

seq = "ATEYIGYAWAMVVVIIGATIGIKLFKK"
link = "https://dgpred.cbr.su.se/analyze.php?with_length=on&seq=" + seq

driver.get(link)

# get element
#element = driver.find_element(By.CSS_SELECTOR,".analyze > tbody:nth-child(1) > tr:nth-child(51) > td:nth-child(1) > big:nth-child(1) > b:nth-child(7) > span:nth-child(1)")
element = driver.find_element(By.CSS_SELECTOR,"b.color: green")

print(element)