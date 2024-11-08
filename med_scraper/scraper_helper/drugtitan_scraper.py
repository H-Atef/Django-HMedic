from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import threading

import med_scraper.scraper_helper.web_scraping_resources as wb
import med_scraper.scraper_helper.abstract_med_scraper as md





class DrugEyeTitanScraper(md.Scraper):
    def __init__(self):
        self.url = "http://www.drugeye.pharorg.com/drugeyeapp/android-search/drugeye-titan.aspx"
        self.scraper_name='drugeye_titan'
        
       
    def scrape_data(self, drug_name):
        try:
            drv_flag=[True]

            driver = wb.WebScarpingToolInit().initialize_driver("google")
            driver.get(self.url)
            #print(driver.current_url,drug_name)
            input_field = driver.find_element(By.NAME, "ttt")
            input_field.send_keys(drug_name)
            driver.find_element(By.ID, "BtnCounting").click()
            table = driver.find_element(By.CSS_SELECTOR, "#ctl00 > div.l-container > table:nth-child(3)")
            table.location_once_scrolled_into_view
            table_html = table.get_attribute('outerHTML')
            data = self._extract_data(table_html)
            return data
        except Exception as e:
            #print(f"An error occurred: {e}")
            return {}
        finally:
            if drv_flag[0]:
                driver.close()

    def scrape_multiple_data(self, drug_names):
        results = {}
        threads = []
        for drug_name in drug_names:
            thread = threading.Thread(target=lambda name=drug_name:
                                       results.update({name: self.scrape_data(name)}))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results

    def _extract_data(self, table_html):
        soup = BeautifulSoup(table_html, 'lxml')
        elements = [x.find_all("td") for x in soup.find_all("tr")][1:]

        data = {
            'drug_name': [],
            'repeat': [],
            'price': []
        }


        max_repeat=0

        for tr in elements:
            tds = [td.text for td in tr]
            data['drug_name'].append(tds[0])
            data['repeat'].append(tds[1])
            data['price'].append(tds[2])

        return data



