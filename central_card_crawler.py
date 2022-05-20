from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep


class CentralCardCrawler:
  def __init__(self, driver, element: WebElement):
    self.element = element
    self.driver = driver
    self.result = {}

  def runCrawling(self):
    card_info = self.getCardInfo()
    self.goToDetail()
    sleep(1) # 1초 대기
    card_detail = self.getDetailInfo()

    card_info.update(card_detail)
    card_info['url'] = self.driver.current_url
    self.driver.execute_script("window.history.go(-1)")


    return card_info
    

  def goToDetail(self):
    button = self.element.find_element(by=By.CSS_SELECTOR, value='.btn-secondary > a')
    button.send_keys(Keys.ENTER)
    sleep(0.1)

  def getCardInfo(self):
    result = {}
    result['badges'] = self.getBadge()
    result['title'] = self.getTitle()
    result['sub_title'] = self.getSubTitle()
    sub_contents = self.getSubContents()
    result['contact'] = sub_contents['contact']
    result['period'] = sub_contents['period']
    result['type'] = sub_contents['type']
    result['department'] = sub_contents['department']
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
      'contact' : sub_content_elements[0].text,
      'period' : sub_content_elements[2].text,
      'type' : sub_content_elements[4].text,
      'department' : sub_content_elements[6].text,
    };

  def getDetailInfo(self):
    detail = {}
    #내부 페이지에서 tag별 정리
    circle_tag_elements = self.driver.find_elements(by=By.CLASS_NAME,value='card-subtit')
    detail['department_sub'] = circle_tag_elements[1].text
    detail['base_year'] = circle_tag_elements[4].text

    support_target_element = self.driver.find_elements(by=By.CLASS_NAME,value='bokjiBlit01')
    detail['support_target'] = support_target_element[0].text
    if len(support_target_element) >= 2:
      detail['selection_criteria'] = support_target_element[1].text
    else:
      detail['selection_criteria'] = ''

    tab_button_elements = self.driver.find_elements(by=By.CLASS_NAME, value='cl-tabfolder-item')

    # 서비스 내용
    tab_button_elements[1].click()
    service_contents_elements = self.driver.find_elements(by=By.CSS_SELECTOR,value='.bokjiServiceView')
    detail['service_contents'] = service_contents_elements.pop().text

    # 신청방법
    tab_button_elements[2].click()
    apply_method_elements = self.driver.find_elements(by=By.CLASS_NAME, value='process-v-bar')
    detail['apply_method'] = apply_method_elements[0].text

    # 추가정보
    tab_button_elements[3].click()
    additional_info_elements = self.driver.find_elements(by=By.CLASS_NAME, value='process-v-bar')
    additional_info = ''
    for additional_info_element in additional_info_elements:
      additional_info += additional_info_element.text + '\n'
    detail['additional_info'] = additional_info
    return detail

