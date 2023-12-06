import logging
import warnings


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import scrapy
from scrapy.crawler import CrawlerProcess
from webdriver_manager.chrome import ChromeDriverManager

original_url = 'https://www.w3schools.com/python/python_operators.asp'


def get_driver_instance():
    """
    Create a Chromeoptions and pass arguments for using headless mode.
    Create Chrome browser instance and maximize the window
    :return: browser instance
    """
    options = webdriver.ChromeOptions()
    options.binary_location = "/chrome-linux64/chrome"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service('/chromedriver'), options=options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    return driver


def get_all_links():
    browser = get_driver_instance()
    browser.get(original_url)
    tags = browser.find_elements(By.CSS_SELECTOR, "a.w3-btn.btnsmall.btnsmall")
    links = [i.get_attribute('href') for i in tags]
    return links



class FetchDataSpider(scrapy.Spider):
    """
    Get all directories from original URL.
    Get the latest and second-latest directory and their subdirectory.
    Get the dictionary containing data to be downloaded.
    Pass the URLS to Scrapy parse function and upload files by converting them from .nc to .parquet to S3.
    """
    name = 'fetch_data'

    custom_settings = {'LOG_LEVEL': 'ERROR'}

    start_urls = get_all_links()

    def parse(self, response):
        text_data_element = response.xpath("//div[@id='iframeResult']/div/text()")
        text_data = text_data_element.get().strip().replace('\n', '')
        print(f"URL : {response.url}, Output : {text_data}")


def handler():
    """
    Disable scrapy logs and set log levels of urllib3, boto, botocore to critical
    Initiate the Spider with a user agent and crawl it.
    """
    logging.getLogger('scrapy').propagate = False
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    logging.getLogger('boto').setLevel(logging.CRITICAL)
    logging.getLogger('botocore').setLevel(logging.CRITICAL)

    warnings.filterwarnings("ignore", category=scrapy.exceptions.ScrapyDeprecationWarning)
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(FetchDataSpider)
    process.start()


handler()
