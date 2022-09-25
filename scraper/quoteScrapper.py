import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.forbes.com/sites/robertberger/2014/04/30/top-100-money-quotes-of-all-time/?sh=fb557bc4998d'
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)

page = requests.get(url, headers=headers)
htmlContent = page.content
soup = BeautifulSoup(htmlContent, 'html.parser')

articleDiv = soup.find('div', {'class' : 'article-body fs-article fs-responsive-text current-article'}).find('ol').find_all('li')
parentList = []
for li in articleDiv : 
    childList = []
    quote, author = li.text.strip().split('--')
    childList.append(quote)
    childList.append(author)
    parentList.append(childList)

quoteDf = pd.DataFrame(parentList, columns = ['quotes', 'author'])
root = '../data/'
quoteDf.to_csv(root+'quoteDf.csv', encoding='utf-8', index= False)