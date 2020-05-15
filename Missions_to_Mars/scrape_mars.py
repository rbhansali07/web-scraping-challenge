#import dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import re
import time

def scrape_info():

   #Scrape the Nasa News
    #execute browser for navigation
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Save News title and paragraph
    url_nasa_news = "https://mars.nasa.gov/news/"
    browser.visit(url_nasa_news)
    time.sleep(10)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find_all("div", class_= "content_title")[1].text
    news_p = soup.find("div", class_= "article_teaser_body").text
    print(news_title)
    print(news_p)
    

    #JPL Mars Space Images - Featured Image
    url_mars_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_mars_image)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_page = soup.find("figure", class_="lede")
    image_url = image_page.find("a")["href"]
    featured_image_url =f"https://www.jpl.nasa.gov{image_url}"
    print(featured_image_url)

    # Mars Weather
    # Mars Weather
    url_mars_weather = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url_mars_weather)
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)
    pattern = re.compile(r'InSight sol')
    mars_weather = soup.find('p', text=pattern).text
    print(mars_weather)


    # Mars Facts
    url_mars_facts = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(url_mars_facts)
    mars_facts_df = pd.DataFrame(mars_facts[0])
    mars_facts_df = mars_facts_df.rename(columns={0:"Description", 1:"Value"})
    mars_facts_df.set_index('Description', inplace=True)

    #store html table
    html_table = mars_facts_df.to_html()
    html_table.replace("\n", "")
    print(html_table)


    #save df as html file
    mars_facts_df.to_html("mars_facts.html")

    # Mars Hemispheres
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemispheres_response = requests.get(mars_hemispheres_url)
    soup = BeautifulSoup(hemispheres_response.text, 'html.parser')

    #image data
    image_data = soup.find_all("div", class_="item")

    #hemisphere dictionary
    hemisphere_image_urls = []
    for image in image_data:
        image_title = image.find("h3").text
        image_url = image.find("a", class_="itemLink product-item")['href']
        full_image_url = f'https://astrogeology.usgs.gov{image_url}'
        
        # find image src
        image_response = requests.get(full_image_url)
        image_soup = BeautifulSoup(image_response.text, 'html.parser')
        image_src = image_soup.find('img', class_="wide-image")["src"]
        img_src_url = f'https://astrogeology.usgs.gov{image_src}'
        
        #add image title and source url to hemisphere dictionary
        hemisphere_image_urls.append({"title":image_title, "img_url": img_src_url })
      
    print(hemisphere_image_urls)

    #store all scraped information in a new dictionary

    mars_scraped_data = {
        "news_title": news_title,
        "news_p" : news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts" : html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

     # Return results
    return mars_scraped_data


