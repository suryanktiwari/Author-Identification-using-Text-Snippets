# In[1]:

import os
import pickle
import requests
from bs4 import BeautifulSoup

# In[2]:

URL = 'https://americanliterature.com/authors'
URL_base = 'https://americanliterature.com'
page = requests.get(URL)

# In[3]:

authors = dict()
author_works = dict()
author_works_corpus = dict()

# In[4]:

try:
    authors = pickle.load(open("authors.pkl", "rb"))
    author_works = pickle.load(open("author_works.pkl", "rb"))
    print("Pickles found loaded")
except (OSError, IOError) as e:  
    print("Pickles missing.")

# In[5]:

    soup = BeautifulSoup(page.content, 'html.parser')
    divs = soup.find_all('div', class_='col-xs-6 col-sm-4')
    for div in divs:
        author = div.find('p')
        worklist = author.find('a')['href']    
        author_URL = URL_base+worklist
        authors[author.text] = author_URL

    pickle.dump(authors, open("authors.pkl", "wb"))

#
#authors = {
##        'Alger, Horatio':'https://americanliterature.com/author/horatio-alger',
##           'Poe, Edgar Allan':'https://americanliterature.com/author/edgar-allan-poe',
#           'Shakespeare, William':'https://americanliterature.com/author/william-shakespeare',
#           'Tzu, Sun':'https://americanliterature.com/author/sun-tzu',
##           'Abbott, Eleanor Hallowell':'https://americanliterature.com/author/eleanor-hallowell-abbott',
##            'Tennyson, Alfred':'https://americanliterature.com/author/alfred-lord-tennyson'
#            }

# In[6]:

    for author in authors:
        author_page = requests.get(authors[author])
        author_soup = BeautifulSoup(author_page.content, 'html.parser')
        author_divs = author_soup.find_all('div', class_='col-xs-6 col-md-4')
        author_works[author] = [] 
        for author_div in author_divs:
            sections = author_div.find_all('section')
            for section in sections:
                links = section.findAll('a')
                for link in links:
                    author_works[author].append(URL_base+link['href'])
    pickle.dump(author_works, open("author_works.pkl", "wb"))


for auth in author_works:
    print(auth, author_works[auth])
