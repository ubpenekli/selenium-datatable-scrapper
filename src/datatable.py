from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
import time

class DatatableScrapper:
    def __init__(self, url, dtId, delay, perPage):

        chromeOptions = Options()
        chromeOptions.add_argument('--kiosk')
        self.driver = webdriver.Chrome(chrome_options = chromeOptions)
        self.url = url
        self.dtId = dtId
        self.delay = delay
        self.perPage = perPage
        self.data = []

        self.setSource(self.url)

    def __del__(self):
        self.driver.close()

    def setSource(self, url):
        self.driver.get(url)
        self.data = []
        self.url = url
        self.waitForPageLoad()

    def waitForPageLoad(self):
        try:
            print('Loading...')
            self.pageLoadRecursive()
            print('Page loaded: ' + self.title + '...')
            self.is_usable = True
        except TimeoutException:
            print("Error on getting... " + self.url)
            self.is_usable = False
    
    def pageLoadRecursive(self):
        waitingTable = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#' + self.dtId + ' tbody')))
        waitingButtons = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#' + self.dtId + '_paginate ul li.paginate_button.active a')))
        waitingInfo = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#' + self.dtId + '_info')))
        try:
            self.title = self.driver.find_element(By.CSS_SELECTOR, 'html head title').get_attribute('innerHTML')
            self.table = self.driver.find_element(By.CSS_SELECTOR, '#' + self.dtId + ' tbody')
            self.pagination = self.driver.find_element(By.CSS_SELECTOR, '#' + self.dtId + '_paginate')
            self.info = self.driver.find_element(By.CSS_SELECTOR, '#' + self.dtId + '_info')
        except:
            self.pageLoadRecursive()
    
    def fetchPages(self, pagesCount = False, rowsCount = False):
        if self.is_usable == False:
            print('Table elements not reachable... ' + self.url)
            return []
        while(1):
            currentPage, currentPageNumber, currentIndex, nextIndex, nextPage = self.tryGetPage()
            if currentPage != False:
                if pagesCount is not False and rowsCount is not False:
                    self.fetchRows(currentPageNumber, rowsCount)
                    if int(currentPageNumber) >= pagesCount:
                        print('End with pages count finishing...')
                        print('-' * 100)
                        break
                else:
                    self.fetchRows(currentPageNumber)
                    if nextPage.find_element(By.XPATH, '..').get_attribute('id') == self.dtId + '_next':
                        print('End with next page could not find...')
                        print('-' * 100)
                        break

                self.step(nextPage, nextIndex)

    def tryGetPage(self, counter = 1):
        if counter >= 5:
            waitingRows = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#' + self.dtId + ' tbody tr')))
            rows = self.table.find_elements(By.CSS_SELECTOR, 'tr')
            if len(rows) == 1:
                cols = rows[0].find_elements(By.CSS_SELECTOR, 'td')
                if len(cols) == 1 and cols[0].get_attribute('innerHTML') == 'Tabloda herhangi bir veri mevcut değil':
                    return [
                        False,
                        False,
                        False,
                        False,
                        False
                    ]
        try:
            currentPage = self.pagination.find_element(By.CSS_SELECTOR, 'ul li.paginate_button.active a')
            currentPageNumber = currentPage.get_attribute('innerHTML')
            currentIndex = currentPage.get_attribute('data-dt-idx')
            nextIndex = int(currentIndex) + 1
            nextPage = self.pagination.find_element(By.CSS_SELECTOR, 'ul li.paginate_button a[data-dt-idx="' + str(nextIndex) + '"]')
            return [
                currentPage,
                currentPageNumber,
                currentIndex,
                nextIndex,
                nextPage
            ]
        except:
            self.tryGetPage(counter + 1)

    def step(self, nextPage, nextIndex):
        time.sleep(self.delay)
        try:
            nextPage.click()
            expected = str((nextIndex - 1) * self.perPage + 1)
            detected = self.info.get_attribute('innerHTML').split()[3].replace('.','')
            if expected != detected:
                self.step(nextPage, nextIndex)
        except:
            pass

    def fetchRows(self, page, rowsCount = False):
        waitingRows = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#' + self.dtId + ' tbody tr')))
        rows = self.table.find_elements(By.CSS_SELECTOR, 'tr')
        for index, row in enumerate(rows):
            cols = row.find_elements(By.CSS_SELECTOR, 'td')
            self.prefetch(page, index, cols)
            if rowsCount is not False:
                if index >= rowsCount:
                    break

    def prefetch(self, page, index, cols):
        key = (int(page) - 1) * self.perPage + index
        data = []
        for col in cols:
            data.append(col.get_attribute('innerHTML'))
        self.data.append(data)
        print(str(key) + ". row prefetched...")

    def format(self, extra_fields = False):
        return self.data