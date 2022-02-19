from selenium import webdriver
import time
import os


def hmmtop_search(seq_dict):
    driver = webdriver.Chrome()
    print(driver)
    driver.maximize_window()
    time.sleep(10)
    url = "http://www.enzim.hu/hmmtop/html/submit.html"
    driver.get(url)
    id = "//*[@id=\"m3\"]/font/textarea"
    button_id = "//*[@id=\"m3\"]/input"
    text_area = driver.find_element(id)
    button_area = driver.find_element(button_id)
    for current_id in seq_dict.keys():
        text_area.send_keys(seq_dict[current_id]['seq'])
        time.sleep(1)
        button_area.click()
        time.sleep(1)
        print(driver.current_url)
        break


if __name__ == "__main__":
    seq_dict = {'seq': "MVQRWLYSTNAKDIAVLYFMLAIFSGMAGTAMSLIIRLELAAPGSQYLHGNSQLVQS"}
    hmmtop_search(seq_dict)
