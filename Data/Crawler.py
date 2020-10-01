# Library Imports
import os
import pickle
import requests
from bs4 import BeautifulSoup

# Specifying the URL that is to be crawled on. This file is specific to this URL only.
URL_base = 'https://americanliterature.com'
URL = URL_base+'/authors'
page = requests.get(URL)

# Creating dictionaries to store fetched results
authors = dict()
author_works = dict()

# Try to load the pickle containing list of authors and their work titles with URLS. If it doesn't exist, the list is fetched and pickled for later.
try:
    authors = pickle.load(open("authors.pkl", "rb"))
    author_works = pickle.load(open("author_works.pkl", "rb"))
    print("Pickles found loaded")
except (OSError, IOError) as e:  
    print("Pickles missing.")

    # Computing pickles
    
    # Fetch the list of authors page
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Authors are stored within divs. Class is specified.
    divs = soup.find_all('div', class_='col-xs-6 col-sm-4')
    
    # For each author div, we fetch the link to their list of works and store it
    for div in divs:
        author = div.find('p')
        worklist = author.find('a')['href']    
        author_URL = URL_base+worklist
        
        # Store each author with a URL which contains their list of works
        authors[author.text] = author_URL

    pickle.dump(authors, open("authors.pkl", "wb"))

    # For each author just stored, save URLs of all their individual works
    for author in authors:
        
        # Fetch list of works page
        author_page = requests.get(authors[author])
        author_soup = BeautifulSoup(author_page.content, 'html.parser')
        
        # Their list of works are stored in a div element as well. Class is specified.
        author_divs = author_soup.find_all('div', class_='col-xs-6 col-md-4')
        
        # Initialize author_works dictionary 
        author_works[author] = [] 
        
        for author_div in author_divs:
            # Find section element within div
            sections = author_div.find_all('section')
            
            # Fetch all links within a section and store it for the corresponding author
            for section in sections:
                links = section.findAll('a')
                for link in links:
                    author_works[author].append(URL_base+link['href'])
    
    # Pickle the work list
    pickle.dump(author_works, open("author_works.pkl", "wb"))

# Printing what we fetched so far
for auth in author_works:
    print(auth, author_works[auth])

# Folder name of the corpus to be created
base = 'Author Corpus 2'

# To fetch data from <pre> elements in a webpage
def search_pre(soup):
    corpus=""
    pres = soup.find('pre', text=True)
    if pres:
        for pre in pres:
            corpus+=str(pre)+'\n'
    return corpus

# To check whether sub_link has base_link as prefix or not. The prefix property holds for the website in question.
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

# To find <p> tags in the page, retrieve their contents and go to subsequent specified depth for links in said tags.
def search_paragraphs(soup, base_url, depth):
    corpus=""
    
    # fetch all paragraph tags
    paragraphs = soup.find_all('p')
#    blockquotes = soup.find_all('blockquote')
#    block_itr=0

    for paragraph in paragraphs:
    
        # Add the text of the paragraph to the work
        corpus+=paragraph.text+'\n'
        
        # Find all links in a paragraph.
        links = paragraph.find_all('a', href=True)
        
        # If links exist and maximum exploring depth has not been exhausted
        if links and depth:
            # Then for each link
            for link in links:
            
                # If the link that we have fetched is not a 'backlink', i.e. must be a link that moves forward with prefix check. And not a link that leads back to the author page or some other page.
                if link_prefix_check(base_url, URL_base+link['href']):
                
                    # Fetch the page of the link
                    link_page = requests.get(URL_base+link['href'])
                    link_soup = BeautifulSoup(link_page.content, 'html.parser')

                    # Search for pre and para in the subsequent page with respective functions. Depth is decreased by 1.
                    pre_text =  search_pre(link_soup)
                    if not pre_text:
                        para_text = search_paragraphs(link_soup, base_url,depth-1)
                        # Add paragraph content to the work
                        corpus+=para_text
                    else:
                        # Add pre content to the work
                        corpus+=pre_text
    return corpus
        
try: 
    # If the base folder doesn't exist then make it
    if not os.path.exists(base):
        os.mkdir(base) 
        
    for author in author_works:
        author_dir = base+'\\'+author
        
        # If the folder of the author doesn't exist then make it
        if not os.path.exists(author_dir):
            os.mkdir(author_dir)

        # For each author work
        for work_URL in author_works[author]:
        
            # Fetch the title of the work from the URL (as leading links can be misleading)
            title = work_URL.split('/')[-1]
            title = title.replace('-', ' ')

            # Special case when an author work contains sublinks
            postfix = "summary"
            if title==postfix:
                title=work_URL.split('/')[-2]
                title = title.replace('-', ' ')
                
            # If the file of this work doesn't exisst then fetch it and make it. This means already created files will be avoided and won't be processed even if they were changed outside of the program.
            if not os.path.isfile(author_dir+'\\'+title):
                
                # Fetch the work page
                work_page = requests.get(work_URL)
                work_soup = BeautifulSoup(work_page.content, 'html.parser')
                work_corpus = ""
                
                # Search for pre element text
                pre_text =  search_pre(work_soup)
                
                # Search for paragraph texts
                para_text = search_paragraphs(work_soup, work_URL, depth=1)+'\n'
                
                # Append both to the work content
                work_corpus+=pre_text+'\n'+para_text

                # Write fetched content to file
                f = open(author_dir+"\\"+title, "x", encoding='utf-8')
                f.write(work_corpus)
                f.close()        
                print(title, len(work_corpus))

    print('Author Works Corpus Created')
except OSError as error: 
    print(error)   