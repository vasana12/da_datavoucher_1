import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymysql
import os
import random
import colorsys
import time
import re
import math
import operator
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

class SeleniumDriver :

    def __init__(self):
        '''
        Almaden SeleniumCrawler 1.0
        date 2020-02-18
        by Bae Jin
        '''
        #option
        self.option = Options()
        self.option.add_argument("--disable-infobars")
        self.option.add_argument("start-maximized")
        self.option.add_argument("--disable-extensions")
        # Pass the argument 1 to allow and 2 to block
        self.option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        path = os.path.dirname(os.path.realpath(__file__))
        self.driver = webdriver.Chrome(options=self.option, executable_path=path + "\chromedriver.exe")
        self.wait = None

    def get(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.close()

    def find_elements_by_xpath(self,xpath):
        return self.driver.find_elements_by_xpath(xpath)
    def find_element_by_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath)

    def scrollDown(self, scnum=1, wait=0.1):
        scrollnum = 0
        while scrollnum <= scnum:
            last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            #print("\n\n\nScroll_Down**************\n\n\n")
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
            time.sleep(wait)
            self.driver.implicitly_wait(3)
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            scrollnum += 1

    def waitUntil_className(self, className, sec=1000):
        WebDriverWait(self.driver, sec).until(EC.element_to_be_clickable((By.CLASS_NAME, className)))
        # try:
        #     element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "change-theme")))
        #     driver.implicitly_wait(3)
        #     # c_elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]")
        #     # c_elem.click()
        #     time.sleep(5)
        # finally:
        #     print("phase 2")

class Sql :
    def __init__(self, dbName, tableName = "*",
                 hostIP='106.246.169.202', userID='root', password='robot369', charset='utf8mb4'):
        self.dbName = dbName
        self.tableName = tableName
        self.hostIP = hostIP
        self.userID = userID
        self.password = password
        self.charset = charset
        self.conn = None
        self.curs = None
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.hostIP, user=self.userID, password=self.password,
                               db=self.dbName, charset=self.charset)
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)

    def select(self, tableName=None, colNames=['*'], where_query=None):
        query = "select %s from %s" %(",".join(colNames), self.tableName if not tableName else tableName)
        if where_query :
            query += "where "+where_query
        self.curs.execute(query)
        result_dict = self.curs.fetchall()
        return result_dict

    def insert(self, tablename, **params):
        sql = "insert into %s("%(tablename)
        for k in params.keys() :
            sql = sql+str(k)+","
        sql = sql[:-1]+") values("
        for k in params.keys() :
            sql = sql+"%s"+","
        sql = sql[:-1]+")"
        v = tuple(params.values())
        self.curs.execute(sql, v)
        row_id = self.curs.lastrowid
        self.conn.commit()
        return row_id

    def close(self):
        self.conn.close()

    def get_now_datetime(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

