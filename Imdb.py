"""Importing the required libraries"""
import bs4
import requests
import time
import random as ran
import sys
import pandas as pd
import numpy as np


"""Building the functions required to scrape the website"""

# ---------------------------------------------------------------------------

url = 'https://www.imdb.com/search/title/?title_type=feature&sort=num_votes,desc'

source = requests.get(url).text
soup = bs4.BeautifulSoup(source,'html.parser')

movie_blocks = soup.findAll('div',{'class':'lister-item-content'})


"""
mname = movie_blocks[0].find('a').get_text() # Name of the movie
print(mname)
m_reyear = int(movie_blocks[0].find('span',{'class': 'lister-item-year'}).contents[0][1:-1]) # Release year
print(m_reyear)
m_rating = float(movie_blocks[0].find('div',{'class':'inline-block ratings-imdb-rating'}).get('data-value')) #rating
print(m_rating)
m_votes = int(movie_blocks[0].find('span',{'name':'nv'}).get('data-value')) # votes
print(m_votes)
m_mscore = int(movie_blocks[0].find('span',{'class':'metascore favorable'}).contents[0].strip()) #meta score
print(m_mscore)
"""


def scrape_mblock(movie_block):
    movieb_data = {}

    try:
        movieb_data['name'] = movie_block.find('a').get_text()  # Name of the movie
    except:
        movieb_data['name'] = None

    try:
        movieb_data['year'] = str(
            movie_block.find('span', {'class': 'lister-item-year'}).contents[0][1:-1])  # Release year
    except:
        movieb_data['year'] = None

    try:
        movieb_data['rating'] = float(
            movie_block.find('div', {'class': 'inline-block ratings-imdb-rating'}).get('data-value'))  # rating
    except:
        movieb_data['rating'] = None

    try:
        movieb_data['m_score'] = float(
            movie_block.find('span', {'class': 'metascore favorable'}).contents[0].strip())  # meta score
    except:
        movieb_data['m_score'] = None

    try:
        movieb_data['votes'] = int(movie_block.find('span', {'name': 'nv'}).get('data-value'))  # votes
    except:
        movieb_data['votes'] = None

    return movieb_data

def scrape_m_page(movie_blocks):
    page_movie_data = []
    num_blocks = len(movie_blocks)

    for block in range(num_blocks):
        page_movie_data.append(scrape_mblock(movie_blocks[block]))

    return page_movie_data


def scrape_this(link, t_count):
    # from IPython.core.debugger import set_trace

    base_url = link
    target = t_count

    current_mcount_start = 0
    current_mcount_end = 0
    remaining_mcount = target - current_mcount_end

    new_page_number = 1

    movie_data = []

    while remaining_mcount > 0:
        url = base_url + str(new_page_number)

        # set_trace()

        source = requests.get(url).text
        soup = bs4.BeautifulSoup(source, 'html.parser')

        movie_blocks = soup.findAll('div', {'class': 'lister-item-content'})

        movie_data.extend(scrape_m_page(movie_blocks))

        current_mcount_start = int(
            soup.find("div", {"class": "nav"}).find("div", {"class": "desc"}).contents[1].get_text().split("-")[0])

        current_mcount_end = int(
            soup.find("div", {"class": "nav"}).find("div", {"class": "desc"}).contents[1].get_text().split("-")[
                1].split(" ")[0])

        remaining_mcount = target - current_mcount_end

        print('\r' + "currently scraping movies from: " + str(current_mcount_start) + " - " + str(current_mcount_end),
              "| remaining count: " + str(remaining_mcount), flush=True, end="")

        new_page_number = current_mcount_end + 1

        time.sleep(ran.randint(0, 10))

    return movie_data


base_scraping_link = "https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,2010-12-31&sort=num_votes,desc&start="

top_movies = 50 #input("How many movies do you want to scrape?")
films = []

films = scrape_this(base_scraping_link,int(top_movies))

print('\r'+"List of top " + str(top_movies) +" movies:" + "\n", end="\n")
df = pd.DataFrame(films)
df['m_score'].fillna(value='0', inplace=True)
#print(df)

#print(df['rating'][:10]>6.0)







    


