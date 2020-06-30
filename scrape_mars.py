# Dependencies
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time 

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    ## Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    # Scrape page into soup 
    html = browser.html 
    soup = bs(html, 'html.parser')
    # Retrieve title and paragraph
    news_title = soup.find('div', class_="content_title").text.strip()
    news_p = soup.find('div', class_ = 'rollover_description_inner').text.strip()
    #print(f'Latest news: {news_title}')
    #print(f'News Paragraph: {news_p}')

    ## Featured Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    # Click the 'full image'
    browser.click_link_by_id('full_image')

    html = browser.html
    soup = bs(html, "html.parser")
    img_url = soup.find('img', class_ = 'fancybox-image')['src']

    base_url='https://www.jpl.nasa.gov/'
    featured_img_url = base_url+img_url
    #featured_img_url

    ## Mars Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    # Create beautifulSoup object 
    mars_weather_soup = bs(response.text, 'html.parser')
    # Find where the text is and access to retrieve text
    mars_weather_tweet = mars_weather_soup.find("div", class_="js-tweet-text-container")
    mars_weather_tweet = mars_weather_tweet.find('p').text
    # Remove unwanted elements
    mars_weather_tweet.replace('\n',' ').replace('twitter.com/JkNqAGB6WR',' ')

    ## Spcae Facts
    mars_facts_url = 'https://space-facts.com/mars/'
    # To read html by pandas
    tables = pd.read_html(mars_facts_url)
    # Retrieve the desired table 
    mars_df = tables[0]
    mars_df.columns=['Description','Value']
    mars_df.set_index('Description')
    # Convert the table to html 
    html_table = mars_df.to_html()
    html_table = html_table.replace('\n','')
    html_table
    mars_df.to_html('mars_table.html')

    ## Mars Hemispheres
    Mars_Hemispheres_url='https://www.planetary.org/blogs/guest-blogs/bill-dunford/20140203-the-faces-of-mars.html'
    response = requests.get(Mars_Hemispheres_url)
    soup=bs(response.text, 'html.parser')

    hemisphere_image_urls = []

    items = soup.find_all('img', class_='img840')
    for item in items:
        #title = item.h5.text
        title = item['alt']
        image_url = item['src']
        
        post = {
            'title':title,
            'image_url': image_url
        }
        
        hemisphere_image_urls.append(post)

    hemisphere_image_urls


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_img_url": featured_img_url,
        "mars_weather_tweet":mars_weather_tweet,
        "html_table":html_table,
        "hemisphere_image_urls":hemisphere_image_urls
    }
    
    # Close the browser after scraping 
    browser.quit()

    # Return results
    return mars_data