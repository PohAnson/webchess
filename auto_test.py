import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def main():

#   import 

  os.system('python web.py &')
#   os.popen('python web.py')

  time.sleep(1)
  print('\n\npaste the link near the place with open new tab')
  print('e.g. https://webchess-1.pohanson.repl.co')
  url = input('Url of web: ')

  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  driver = webdriver.Chrome(options=chrome_options)
  driver.implicitly_wait(15)
  driver.get(url)
  
  print(driver.title)
  driver.find_element_by_xpath("//form//input[@type='submit']").click()

  def move(moves:list):
      """
      give the list moves as a string like how you would input it
      
      e.g. ['51 52', '46 45', '11 12']
      """
      for move in moves:
          move_box = driver.find_element_by_name('move')
          print(move)
          move_box.send_keys(move)
          move_box.submit()
          time.sleep(1.5)

  def fool_mate():
    move(['51 52', '46 45', '61 63', '37 73'])
    # move(['51 52', '46 45', '11 12', '37 73', '12 13', '73 40'])

  # replace the 'Winner' with whatever text on the screen
    if 'Winner' in driver.page_source:
        print("\n===SUCCESS!!===")
    else:
        print('\n===FAIL!!===')

  fool_mate()

main()
time.sleep(120)