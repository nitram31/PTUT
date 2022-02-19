from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import tm_hmm as tm
import re
import time

def hmmtop_reformat(results):
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
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(1)
    url = "http://www.enzim.hu/hmmtop/html/submit.html"
    driver.get(url)
    text_id = '/html/body/center/table/tbody/tr[2]/td/table/tbody/tr[2]/td/font/textarea'
    button_id = '/html/body/center/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/input'
    text_area = driver.find_element(By.XPATH, text_id)
    button_area = driver.find_element(By.XPATH, button_id)

    for current_id in seq_dict.keys():
        text_area.send_keys(seq_dict[current_id]['seq'])
        time.sleep(0.5)
        button_area.click()
        time.sleep(0.5)
        page = driver.page_source
        soup = BeautifulSoup(page, features="html.parser")
        other_res = re.compile(r'(pred )(\D*)')
        results = ''
        for line in soup:
            #print("line:", str(line))
            HMMTOP_result = re.search(other_res, str(line))
            if HMMTOP_result is not None:
                results += HMMTOP_result.group(2)
                annotation = hmmtop_reformat(results)
                pos_list = tm.str_to_pos(annotation)
                seq_dict[current_id]['HMMTOP_pred'] = pos_list

    return seq_dict


if __name__ == "__main__":
    seq_dict = {'sp|Q07914|TIM14_YEAST': {'seq': "MVQRWLYSTNAKDIAVLYFMLAIFSGMAGTAMSLIIRLELAAPGSQYLHGNSQLVQS"}}
    seq_dict = hmmtop_search(seq_dict)
    print(seq_dict)
