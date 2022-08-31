



from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

import chromedriver_autoinstaller


# Set up Splinter

executable_path = {'executable_path': chromedriver_autoinstaller.install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit NASA Mars News Site




# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# my Notes----With the following line, browser.is_element_present_by_css('div.list_text', wait_time=1), we are accomplishing two things.

# One is that we're searching for elements with a specific combination of tag (div) and attribute (list_text). As an example, ul.item_list would be found in HTML as <ul class="item_list">.

# Secondly, we're also telling our browser to wait one second before searching for components. The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.



# setting up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Notes: The title is in that mix of HTML in our output—that's awesome! But we need to get just the text, and the extra HTML stuff isn't necessary.


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Image Scraping 

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup



# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel



# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# note;Instead of scraping each row, or the data in each <td />, we're going to scrape the entire table with Pandas' .read_html() function



df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# Toconvert our DataFrame back into HTML
df.to_html()


# ## D1: Scrape High Resolution Mar's Hemisphere Images and Titles

# ### Hemispheres



# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)



# 2. Create a list to hold the images and titles.
hemisphere_image_urls = [
    {"title": "Cerberus Hemisphere Enhanced", "img_url": "..."},
    {"title": "Schiaparelli Hemisphere Enhanced", "img_url": "..."},
    {"title": "Syrtis Major Hemisphere Enhanced", "img_url": "..."},
    {"title": "Valles Marineris Hemisphere Enhanced", "img_url": "..."},
]

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for i in range(4):
    #create empty dictionary
    hemispheres = {}
    #<img class="wide-image" src="images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg">
    #<img class="wide-image" src="images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg">
    browser.find_by_css('a.product-item h3')[i].click()
    element = browser.find_by_text('Sample').first
    img_url = element['href']
    title = browser.find_by_css("h2.title").text
    hemispheres["img_url"] = img_url
    hemispheres["title"] = title
    hemisphere_image_urls.append(hemispheres)
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls
# very very important ---- Without it, the automated browser won't know to shut down----------
browser.quit()

