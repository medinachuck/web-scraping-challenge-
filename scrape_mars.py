
#dependencies and set up
def scrape():
    import pandas as pd 
    from bs4 import BeautifulSoup as bs
    import requests 
    from splinter import Browser
    import time
    from urllib.parse import urljoin
    #set up Chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(3) 
    #create the soup
    html = browser.html
    nasa_soup = bs(html, 'html.parser')
    

    latest_article = nasa_soup.find('li', class_='slide')
    latest_title = latest_article.find('div', class_='content_title').text
    news_p = latest_article.a.text

    browser.quit()

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    jpl_url = 'https://mars.nasa.gov/multimedia/images/?page=0&per_page=25&order=pub_date+desc&search=&condition_1=1%3Ais_in_resource_list&category=51'
    browser.visit(jpl_url)
    #create soup for jpl site 
    time.sleep(1)
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    #navigate to the featured image's page 
    item = jpl_soup.find('ul', class_='item_list')
    latest_item = item.li
    pic_href = latest_item.a['href']
    browser.click_link_by_href(pic_href)
    #create soup for the new page and store image url in new variable
    jpl_image_page = browser.html
    jpl_image_page_soup = bs(jpl_image_page, 'html.parser') 
    image_anchor = jpl_image_page_soup.find('a', class_='fancybox')
    image_link = image_anchor.find('img')['src']

    #use urljoin to get full image url
    base = 'https://mars.nasa.gov'
    featured_image_url = urljoin(base, image_link)

    #load page for mars facts 
    mars_facts = 'https://space-facts.com/mars/'
    browser.visit(mars_facts)
    facts_html = browser.html

    # scrape mars facts using pandas
    facts = pd.read_html(facts_html)
    table = facts[0]
    #write table to html 
    table_html = table.to_html()

    #visit usgs site 
    usgs = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs)
    usgs_html = browser.html 
    usgs_soup = bs(usgs_html, 'html.parser')
    
    #make list of links to visit 
    links = usgs_soup.find_all('div', class_='item')
    links_list = []
    for link in links:
        links_list.append(link.h3.text)

    hemisphere_urls = []
    for link in links_list:
        browser.click_link_by_partial_text(link)
        browser.click_link_by_partial_text('Sample')
        image_link = browser.url
        info_dict = dict({"title":link, "img_url":image_link})
    #     print(info_dict)
        hemisphere_urls.append(info_dict)
        browser.visit(usgs)
    browser.quit()
    output = dict(news_title = latest_title, description = news_p,
     picture_url = featured_image_url, facts_table = table_html,
     hemisphere_data = hemisphere_urls)
    print(output)
scrape()
