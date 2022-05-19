import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from time import sleep


url = "https://www.bokjiro.go.kr/ssis-teu/twataa/wlfareInfo/moveTWAT52005M.do"

driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url=url)

driver.implicitly_wait(time_to_wait=5)


filter_buttons = driver.find_elements(by=By.CLASS_NAME,value='cl-text-wrapper')

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


# 카드 타이틀 가져오기

# cards = driver.find_elements(by=By.CLASS_NAME,value='card-tit')

# for card in cards:
#   if card.accessible_name != '':
#     card_elements = card.find_elements(by=By.)
  # print(card)


# test = driver.find_elements(by=By.CLASS_NAME, value='badge')

cards = []

cards_elements = driver.find_elements(by=By.CSS_SELECTOR, value='.cl-layout-content > .card')
for card_element in cards_elements:
  card = {}
  # print(card_element.text)
  badges = []
  badges_elements = card_element.find_elements(by=By.CSS_SELECTOR, value='.badge')
  for badge_element in badges_elements:
    # print('----------------------------')
    # print(badge_element.text)
    badges.append(badge_element.text)
  # print('----------------------------')
  card['badges'] = badges
  
  title_element = card_element.find_element(by=By.CSS_SELECTOR, value='.card-tit')
  card['title'] = title_element.text

  sub_title_element = card_element.find_element(by=By.CSS_SELECTOR, value='.card-subtit')
  card['sub_title'] = sub_title_element.text

  sub_content_elements = card_element.find_elements(by=By.CSS_SELECTOR, value='.blt-tit ~ .cl-control')
  card['contact'] = sub_content_elements[0].text
  card['period'] = sub_content_elements[1].text
  card['type'] = sub_content_elements[2].text
  card['department'] = sub_content_elements[3].text

  button_element = card_element.find_element(by=By.CSS_SELECTOR, value='.btn-secondary')
  button_element.click()

  sleep(3) # 3초 대기

  driver.execute_script("window.history.go(-1)")


  cards.append(card)

print(cards)


# search_box = driver.find_element(by=By.XPATH,value='//*[@id="uuid-b0d22cdd-7ab6-e78e-d187-5f9ea74c5d94"]/div[1]/input')
# search_box = driver.find_element(by=By.CLASS_NAME,value='cl-text')
# print(search_box)
