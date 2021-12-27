import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

youtube_trending_url = 'https://www.youtube.com/feed/trending'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options=chrome_options)
  return(driver)

def get_videos(driver):
  video_div_tag = 'ytd-video-renderer'
  driver.get(youtube_trending_url)
  videos = driver.find_elements(By.TAG_NAME, video_div_tag)
  return(videos)

if __name__ == "__main__":
  
  driver = get_driver()
  videos = get_videos(driver)
  
  print(f"Hay {len(videos)} videos")

  video = videos[0]
  title_tag = video.find_element(By.ID, 'video-title')
  video_title = title_tag.text
  video_URL = title_tag.get_attribute('href')
  channel_tag = video.find_element(By.CLASS_NAME,'style-scope ytd-channel-name')
  channel_name = channel_tag.text
  channel_URL = channel_tag.get_attribute('href')
  

  url2 = channel_tag.find_element(By.TAG_NAME,'style-scope ytd-channel-name complex-string').get_attribute('href')


  print(f"Titulo: {video_title}")
  print(f"Video Link: {video_URL}")
  print(f"Channel name: {channel_name}")
  print(f"Channel link: {channel_URL}")
  #print(f"Channel link: {youtube_trending_url}")


