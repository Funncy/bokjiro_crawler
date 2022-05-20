from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

from central_card_crawler import CentralCardCrawler
from local_card_crawler import LocalCardCrawler
from private_card_crawler import PrivateCardCrawler

class BokjiroCrawler:
  def __init__(self):
    self.cards = []
    self.current_index = 0
    self.current_last_index = 0
    self.driver = webdriver.Chrome(executable_path='./chromedriver')

  def driverInit(self):
    url = "https://www.bokjiro.go.kr/ssis-teu/twataa/wlfareInfo/moveTWAT52005M.do"
    self.driver.get(url)
    self.driver.implicitly_wait(time_to_wait=3)
    self.setFilter()

  def getCentralData(self):
    return self.crawlingAllPage(CentralCardCrawler)

  def getLocalData(self):
    sleep(1)
    tab_buttons_elements = self.driver.find_elements(by=By.CLASS_NAME, value='tabfolder-item')
    self.driver.execute_script("arguments[0].click();", tab_buttons_elements[1])
    # tab_buttons_elements[1].click()
    sleep(1)
    return self.crawlingAllPage(LocalCardCrawler)
  
  def getPrivateData(self):
    sleep(1)
    tab_buttons_elements = self.driver.find_elements(by=By.CLASS_NAME, value='tabfolder-item')
    self.driver.execute_script("arguments[0].click();", tab_buttons_elements[2])
    # tab_buttons_elements[2].click()
    sleep(1)
    return self.crawlingAllPage(PrivateCardCrawler)

  def getData(self):
    self.setFilter()
    result = {}
    result['central'] = self.crawlingAllPage(CentralCardCrawler)

    tab_buttons_elements = self.driver.find_elements(by=By.CLASS_NAME, value='tabfolder-item')
    tab_buttons_elements[1].click()
    sleep(1)
    result['local'] = self.crawlingAllPage(LocalCardCrawler)
    
    
    tab_buttons_elements = self.driver.find_elements(by=By.CLASS_NAME, value='tabfolder-item')
    tab_buttons_elements[2].click()
    sleep(1)
    result['private'] = self.crawlingAllPage(PrivateCardCrawler)
    return result


  
  def crawlingAllPage(self, crawlerClass):
    # 현재 인덱스와 인덱스 최대값 저장
    
    changed_index = -1

    # 변경된 인덱스값과 현재 마지막 인덱스값이 일치하면 마지막 페이지
    result = []
    
    while changed_index != self.current_last_index:
      self.current_index  = self.getCurrentIndex()
      self.current_last_index = self.getCurrentLastIndex()
      data = self.crawlingCurrentPagination(crawlerClass)
      result.extend(data)
      # 다음 페이지네이션을 위해서 다음 버튼 클릭
      self.moveToNextPaginationIndex()
      sleep(0.5)
      # 이동된 페이지에서 마지막 인덱스 값 저장
      changed_index = self.getCurrentLastIndex()

    return result

  def crawlingCurrentPagination(self, crawlerClass):
    index_range  = int(self.current_last_index) - int(self.current_index) 
    result = []

    sleep(2)
    result.extend(self.getCrawlingData(crawlerClass))

    
    # 현재 페이지에서 나온 숫자 페이지네이션 이동하며 데이터 크롤링
    for i in range(index_range):
      self.moveToNextPage()
      self.current_index  = self.getCurrentIndex()
      sleep(2)
      result.extend(self.getCrawlingData(crawlerClass))
      sleep(2)
    return result


  
  def getCurrentIndex(self):
    index_elements =  self.driver.find_elements(by=By.CSS_SELECTOR, value='.cl-pageindexer-index.cl-selected')
    
    for element in index_elements:
      if element.text != '':
        return element.text
    
    return -1

  def getCurrentLastIndex(self):
    pagination_elements = self.driver.find_elements(by=By.CLASS_NAME, value='cl-pageindexer-index')
    return pagination_elements.pop().text

  def moveToNextPage(self):
    buttons = self.driver.find_elements(by=By.CLASS_NAME, value='cl-pageindexer-index')
    for button in buttons:
      if button.text == '':
        continue
      if int(button.text) > int(self.current_index):
        button.send_keys(Keys.ENTER)
        sleep(0.3)
        break


  def moveToNextPaginationIndex(self):
    buttons = self.driver.find_elements(by=By.CLASS_NAME, value='cl-pageindexer-next')
    buttons.pop().click()




  def getCentralCardInfos(self):
    elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='.cl-layout-content > .card')
    result = []
    for element in elements:
      cardCrawler = CentralCardCrawler(self.driver, element)
      card_info = cardCrawler.runCrawling()
      result.append(card_info)
    return result

  def getLocalInfos(self):
    elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='.cl-layout-content > .card')
    result = []
    for element in elements:
      if element.text != '':
        cardCrawler = LocalCardCrawler(self.driver, element)
        card_info = cardCrawler.runCrawling()
        result.append(card_info)
    return result
  
  def getCrawlingData(self, crawler):
    elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='.cl-layout-content > .card')
    sleep(0.1)
    result = []
    for element in elements:
      sleep(0.1)
      if element.text != '':
        cardCrawler = crawler(self.driver, element)
        card_info = cardCrawler.runCrawling()
        result.append(card_info)
    return result




  def setFilter(self):
    filter_buttons = self.driver.find_elements(by=By.CLASS_NAME,value='cl-text-wrapper')

    # 장애인 태그 클릭
    for button in filter_buttons:
      # print(button.accessible_name)
      if button.accessible_name == '장애인':
        button.click()
        break

    # 복지 관련 내용 검색
    is_find = False

    for button in filter_buttons:
      if button.aria_role == 'button':
        inner_elements = button.find_elements(by=By.CLASS_NAME, value='cl-text')
        for element in inner_elements:
          if element.text == '검색':
              element.click()
              is_find = True
              break
      if is_find == True:
        break


    sleep(3) # 3초 대기