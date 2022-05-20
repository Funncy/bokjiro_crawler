from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

class PrivateCardCrawler:
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
    self.driver.implicitly_wait(time_to_wait=1)
    self.driver.execute_script("arguments[0].click();", element)
    # element.send_keys(Keys.ENTER)

  def getCardInfo(self):
    result = {}
    result['badges'] = self.getBadge()
    result['title'] = self.getTitle()
    result['sub_title'] = self.getSubTitle()
    sub_contents = self.getSubContents()
    result['company_name'] = sub_contents['company_name']
    result['in_progress'] = sub_contents['in_progress']
    result['date'] = sub_contents['date']
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
      'company_name' : sub_content_elements[0].text,
      'in_progress' : sub_content_elements[2].text,
      'date' : sub_content_elements[4].text,
    };

  def getDetailInfo(self):
    detail = {}
    circle_tag_elements = self.driver.find_elements(by=By.CLASS_NAME,value='card-subtit')
    detail['phone'] = circle_tag_elements[0].text
    detail['person_in_charge'] = circle_tag_elements[1].text
    detail['email'] = circle_tag_elements[3].text


    card_elements = self.driver.find_elements(by=By.CLASS_NAME, value='card')
    sub_contents_elements = card_elements[1].find_elements(by=By.CSS_SELECTOR, value='.cl-last-row > .cl-output > div')

    detail['purpose'] = sub_contents_elements[0].text
    detail['support_target'] = sub_contents_elements[1].text
    detail['service_contents'] = sub_contents_elements[2].text
    detail['apply_method'] = sub_contents_elements[3].text
    detail['need_files'] = sub_contents_elements[4].text
    detail['etc'] = sub_contents_elements[5].text
    
    return detail