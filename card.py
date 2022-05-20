from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

class BokjiroCrawler:
  def __init__(self):
    self.cards = []
    self.driver = webdriver.Chrome(executable_path='./chromedriver')

  def driverInit(self):
    url = "https://www.bokjiro.go.kr/ssis-teu/twataa/wlfareInfo/moveTWAT52005M.do"
    self.driver.get(url)
    self.driver.implicitly_wait(time_to_wait=5)

  def getData(self):
    self.setFilter()
    cards_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='.cl-layout-content > .card')
    for element in cards_elements:
      cardCrawler = CentralCardCrawler(self.driver, element)
      result = cardCrawler.runCrawling()
      print(result)

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


class CentralCardCrawler:
  def __init__(self, driver, element: WebElement):
    self.element = element
    self.driver = driver
    self.result = {}

  def runCrawling(self):
    card_info = self.getCardInfo()
    self.goToDetail()
    sleep(1) # 3초 대기
    card_detail = self.getDetailInfo()

    card_info.update(card_detail)
    return card_info

    

  def goToDetail(self):
    element = self.element.find_element(by=By.CSS_SELECTOR, value='.btn-secondary')
    element.click()

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
    detail['selection_criteria'] = support_target_element[1].text

    tab_button_elements = self.driver.find_elements(by=By.CLASS_NAME, value='cl-tabfolder-item')

    # 서비스 내용
    tab_button_elements[1].click()
    service_contents_elements = self.driver.find_elements(by=By.CLASS_NAME,value='bokjiBlit01')
    detail['service_contents'] = service_contents_elements[2].text

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

