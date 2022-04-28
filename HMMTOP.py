from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import tm_hmm as tm
import re
import time


def hmmtop_reformat(results):
    """takes the results from the HMMTOP_search function, and reformat it to a same form as the pytmhmm.predict
    function."""

    annotation = ''
    for res in results:
        if res == 'i' or res == 'I':
            annotation += 'i'
        elif res == 'H' or res == 'h':
            annotation += 'M'
        elif res == 'o' or res == 'O':
            annotation += 'O'
    return annotation


def hmmtop_search(seq_dict):
    """takes the dictionary, and if the sequence has not been predicted with a TM segment, it tries to predict it with
    HMMTOP"""

    WINDOW_SIZE = "1920,1080"
    # initialization of Chrome web driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")   # allows the window to not be seen in console
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(1) #time of web page charging
    url = "http://www.enzim.hu/hmmtop/html/submit.html"
    text_id = '/html/body/center/table/tbody/tr[2]/td/table/tbody/tr[2]/td/font/textarea' #XPATH adress pointing to the zone of sequence input
    button_id = '/html/body/center/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/input' #XPATH adress pointing to the button we need to click to start the research
    cpt = 1

    max_length = len(seq_dict.keys())
    for current_id in seq_dict.keys():
        print(cpt, "/", max_length)
        cpt += 1
        #if seq_dict[current_id]['TMsegment_pred'].count('M') == 0:  # finds sequence without TM predicted
        print(current_id)  #shows the progress
        driver.get(url)  # refreshes the page to the menu
        text_area = driver.find_element(By.XPATH, text_id)  # find the text area to paste the sequence in
        button_area = driver.find_element(By.XPATH, button_id)
        text_to_send = seq_dict[current_id]['seq'] #paste the used part of the sequence in main dictionnary
        text_area.send_keys(text_to_send)
        time.sleep(0.25)
        button_area.click()
        time.sleep(0.75)
        text = driver.find_element(By.XPATH, '/html/body/pre').text
        other_res = re.compile(r'(pred )(\D*)')  # regular expression that finds the string of results
        results = ''
        for line in text.splitlines():
            hmmtop_result = re.search(other_res, str(line))
            if hmmtop_result is not None:
                results += hmmtop_result.group(2)
                annotation = hmmtop_reformat(results)
                """Reformat the results to be used by the str_to_pos function 
                that allows the string to be included in the dictionary as a list"""
                pos_list = tm.str_to_pos(annotation) #list initialization containing predicted TM positions and prediction score
                #pos_list = [annotation[0], 1]
                seq_dict[current_id]['HMMTOP_TM_pred'] = pos_list


    return seq_dict


if __name__ == "__main__":
    seq_dict = {'sp|Q07914|TIM14_YEAST': {'seq': "MVQRWLYSTNAKDIAVLYFMLAIFSGMAGTAMSLIIRLELAAPGSQYLHGNSQLVQS"}}
    seq_dict = hmmtop_search(seq_dict)
    print(seq_dict)
