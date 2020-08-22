def main():
  import os
  from selenium import webdriver
  from selenium.webdriver.common.keys import Keys
  from selenium.webdriver.chrome.options import Options
  import time

  os.system('python web.py &')

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

  def fool_mate():
      for move in ['51 52', '46 45', '11 12', '37 73', '12 13', '73 40']:
          move_box = driver.find_element_by_name('move')
          print(move)
          move_box.send_keys(move)
          move_box.submit()
          time.sleep(2)

  fool_mate()

  # replace the 'Winner' with whatever text on the screen
  if 'Winner' in driver.page_source:
      print("\n===SUCCESS!!===")
  else:
      print('\n===FAIL!!===')