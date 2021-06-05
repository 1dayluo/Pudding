import time
import undetected_chromedriver.v2 as uc

# options = uc.ChromeOptions()

def search_virusTotal(search_content):

    driver = uc.Chrome()
    # driver = uc.Chrome()
    with driver:
        url = 'https://cn.bing.com/search?q={}&ensearch=1&FORM=BESBTB'.format(search_content)


        driver.get(url)
        for li in  driver.find_elements_by_tag_name('li'):
            print(li.get_attribute('class'))
        # input_search = driver.find_element_by_xpath('//*[@id="input"]')
        # input_search.send_keys('abcdefg')


    driver.close()


search_virusTotal('6cd3556deb0da54bca060b4c39479839')
