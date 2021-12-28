import requests, pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

youtube_trending_url = 'https://www.youtube.com.ar/feed/trending'

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

def get_data(videos):
  video_data = []

  for index, video in enumerate(videos):
    # moves mouse to element and scrolls there
    webdriver.ActionChains(driver).move_to_element(video).perform()

    #get each element of data
    title_tag = video.find_element(By.ID, 'video-title')
    video_title = title_tag.text
    video_URL = title_tag.get_attribute('href')
    channel_tag = video.find_element(By.CLASS_NAME,'style-scope ytd-channel-name')
    channel_name = channel_tag.text.split('\n')[0]
    channel_URL = channel_tag.find_element(By.TAG_NAME,'a').get_attribute('href')
    video_desc = video.find_element(By.ID, "description-text").text
    thumbnail = video.find_element(By.ID, 'img').get_attribute('src')
    metadata = video.find_element(By.ID, 'metadata-line')
    views_timePosted = metadata.find_elements(By.TAG_NAME, "span")
    views = views_timePosted[0].text
    timePosted = views_timePosted[1].text

    # add data to list of dictionaries
    video_data.append({ 
      "Date extracted":pd.to_datetime('today').strftime("%d/%b/%Y"),
      "Rank":index+1,
      "Title":video_title, 
      "Channel":channel_name,
      "Time posted":timePosted,
      "Views":views,
      "Description":video_desc,
      "Video URL":video_URL,
      "Channel URL":channel_URL,
      "Thumbnail URL":thumbnail
      })

  #create and return dataframe
  data = pd.DataFrame(video_data)
  return(data)


if __name__ == "__main__":
  
  driver = get_driver()
  videos = get_videos(driver)
  data = get_data(videos)

  #add today's data to a csv but keep data in case you want to work on it further
  data.to_csv('video_data.csv', mode='a', header=False, index=False)

  print('Finished')