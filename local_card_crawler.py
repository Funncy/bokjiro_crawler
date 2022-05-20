from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

class LocalCardCrawler:
  def __init__(self, driver, element: WebElement):
    self.element = element
    self.driver = driver
    self.result = {}

  def runCrawling(self):
    card_info = self.getCardInfo()
    self.goToDetail()
    sleep(1) # 1초 대기
    card_detail = self.getDetailInfo()

    card_info['url'] = self.driver.current_url
    self.driver.execute_script("window.history.go(-1)")


    card_info.update(card_detail)
    return card_info

  def goToDetail(self):
    element = self.element.find_element(by=By.CSS_SELECTOR, value='.btn-secondary')
    self.driver.execute_script("arguments[0].click();", element)

  def getCardInfo(self):
    result = {}
    result['badges'] = self.getBadge()
    result['title'] = self.getTitle()
    result['sub_title'] = self.getSubTitle()
    sub_contents = self.getSubContents()
    result['location'] = sub_contents['location']
    result['type'] = sub_contents['type']
    result['apply_method'] = sub_contents['apply_method']
    result['period'] = sub_contents['period']
    return result

  def getBadge(self):
    result = []
    elements = self.element.find_elements(by=By.CSS_SELECTOR, value='.badge')
    for element in elements:
      result.append(element.text)
    return result

  def getTitle(self):
    element = self.element.find_element(by=By.CSS_SELECTOR, value='.card-tit')
    return element.text
    
  def getSubTitle(self):
    element = self.element.find_element(by=By.CSS_SELECTOR, value='.card-subtit')
    return element.text

  def getTitle(self):
    element = self.element.find_element(by=By.CSS_SELECTOR, value='.card-tit')
    return element.text

  def getSubContents(self):
    sub_content_elements = self.element.find_elements(by=By.CSS_SELECTOR, value='.blt-tit ~ .cl-control')
    return {
      'period' : sub_content_elements[0].text,
      'type' : sub_content_elements[2].text,
      'apply_method' : sub_content_elements[4].text,
      'location' : sub_content_elements[6].text,
    };

  def getDetailInfo(self):
    detail = {}
    #내부 페이지에서 tag별 정리
    card_elements = self.driver.find_elements(by=By.CLASS_NAME, value='card')
    if len(card_elements) == 0 :
      return {}
    sub_contents_elements = card_elements[1].find_elements(by=By.CLASS_NAME, value='cl-htmlsnippet')
    # law_element = card_elements[1].find_element(by=By.CLASS_NAME, value='blt-tit-m')
    return {
      'support_target': sub_contents_elements[0].text,
      'service_contents': sub_contents_elements[1].text,
      'apply_method_detail': sub_contents_elements[2].text,
      # 'law' : law_element.text
    }