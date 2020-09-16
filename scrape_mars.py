from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt


def scrape_all():

    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data



    def mars_news(browser):
        url = "https://mars.nasa.gov/news/"
        browser.visit(url)

        browser.is_element_present_by_css("ul.item_list li.slide")

        html = browser.html
        soup = bs(html, "html.parser")

        try:
            element = soup.select_one("ul.item_list li.slide")
            news_title = element.find("div", class_="content_title").get_text()
            news_para = element.find("div", class_="article_teaser_body").get_text()

        except AttributeError:
            return None, None

        return news_title, news_p


    def featured_image(browser):
        url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(url)

        #Need to click on full image for the large size jpg image
        browser.find_by_id('full_image').click()

        #Then click on more info button
        browser.is_element_present_by_text('more info', wait_time=1)
        browser.find_link_by_partial_text('more info').click()

        #Create BeautifulSoup object; parse with 'html.parser'
        html = browser.html
        i_soup = bs(html, "html.parser")

        #Pull the .jpg url and create a full url
        partial_image_url = i_soup.select_one('figure.lede a').get('href')

        image_url = f"https://www.jpl.nasa.gov{partial_image_url}"

        return image_url

    def twitter_weather(browser):
        url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(url)

        html = browser.html
        w_soup = bs(html, "html.parser")

        # First, find a tweet with the data-name `Mars Weather`
        tweet_attrs = {"class": "tweet", "data-name": "Mars Weather"}
        mars_weather_tweet = weather_soup.find("div", attrs=tweet_attrs)

        # Next, search within the tweet for the p tag containing the tweet text
        mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()

        return mars_weather
    def mars_facts():
        #Place mars facts into dataframe
        facts_df = pd.read_html('https://space-facts.com/mars/')[0]
        facts_df.columns=['Description', 'Value']
        facts_df.set_index('Description', inplace=True)


        return df.to_html(classes="table")

    def hemispheres(browser):
        url = ("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
        browser.visit(url)

        hem_image_urls = []

        # List of all of the hemispheres
        hem_links = browser.find_by_css("a.product-item h3")

        # Loop through to return the image up for each
        for r in range(4):

            browser.find_by_css("a.product-item h3")[r].click()

            sample = browser.find_link_by_text('Sample').first
            url= sample['href']

            title= browser.find_by_css("h2.title").text

            #place info into dictionary
            hem_image_url.append({'Image URL': url, 'Title':title})

            #Now we need to go back to the main page
            browser.back()

        return hem_image_urls


    def scrape_hemisphere(html_text):
        hemi_soup = BeautifulSoup(html_text, "html.parser")

        try:
            title_elem = hemi_soup.find("h2", class_="title").get_text()
            sample_elem = hemi_soup.find("a", text="Sample").get("href")

        except AttributeError:

            title_elem = None
            sample_elem = None

        hemisphere = {
            "title": title_elem,
            "img_url": sample_elem
        }

        return hemisphere

    if __name__ == "__main__":

        # Print data
        print(scrape_all())
