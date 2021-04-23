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


    #authors = {
    #        'Alger, Horatio':'https://americanliterature.com/author/horatio-alger',
    #           'Poe, Edgar Allan':'https://americanliterature.com/author/edgar-allan-poe',
    #           'Shakespeare, William':'https://americanliterature.com/author/william-shakespeare',
    #           'Tzu, Sun':'https://americanliterature.com/author/sun-tzu',
    #           'Abbott, Eleanor Hallowell':'https://americanliterature.com/author/eleanor-hallowell-abbott',
    #            'Tennyson, Alfred':'https://americanliterature.com/author/alfred-lord-tennyson'
    #            }

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

# In[ ]:

base = 'Author Corpus 2'

def search_pre(soup):
    corpus=""
    pres = soup.find('pre', text=True)
    if pres:
        for pre in pres:
            corpus+=str(pre)+'\n'
    return corpus

def link_prefix_check(base_link, sub_link):
    if len(sub_link)<len(base_link):
        return False
    postfix = "summary"
    if base_link[-len(postfix):]:
        base_link=base_link[:-len(postfix)]
    if base_link == sub_link[:len(base_link)]:
        return True
    else:
        return False

def search_paragraphs(soup, base_url, depth):
    corpus=""
    blockquotes = soup.find_all('blockquote')
    for blockquote in blockquotes:
        corpus+=blockquote.text+'\n'
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        corpus+=paragraph.text+'\n'
        links = paragraph.find_all('a', href=True)
        if links and depth:
            for link in links:
                if link_prefix_check(base_url, URL_base+link['href']):
                    link_page = requests.get(URL_base+link['href'])
                    link_soup = BeautifulSoup(link_page.content, 'html.parser')
                    
                    pre_text =  search_pre(link_soup)
                    para_text = search_paragraphs(link_soup, base_url, depth-1)+'\n'
                    corpus+=pre_text+'\n'+para_text
    return corpus
        
try: 
    if not os.path.exists(base):
        os.mkdir(base) 
    for author in author_works:
        author_dir = base+'\\'+author
        if not os.path.exists(author_dir):
            os.mkdir(author_dir)
        for work_URL in author_works[author]:
            title = work_URL.split('/')[-1]
            title = title.replace('-', ' ')
            postfix = "summary"
            if title==postfix:
                title=work_URL.split('/')[-2]
                title = title.replace('-', ' ')
            if not os.path.isfile(author_dir+'\\'+title):
                work_page = requests.get(work_URL)
                work_soup = BeautifulSoup(work_page.content, 'html.parser')
                work_corpus = ""
                
                pre_text =  search_pre(work_soup)
                para_text = search_paragraphs(work_soup, work_URL, depth=1)+'\n'
                work_corpus+=pre_text+'\n'+para_text

                f = open(author_dir+"\\"+title, "x", encoding='utf-8')
                f.write(work_corpus)
                f.close()        
                print(title, len(work_corpus))

    print('Author Works Corpus Created')
except OSError as error: 
    print(error)   