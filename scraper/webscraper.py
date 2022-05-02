import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import random

parentList = []

urls = ["actresses", "actors", "baseball-players", "basketball-players", 
        "businesswomen", "businessmen", "ceos", "comedians", "entrepreneurs", 
        "directors", "hockey-players", "models", "musicians", "nfl-players", 
        "producers", "rappers", "singers", "soccer-players", "tv-personalities"]

# Lawyers, Doctors, Scientist, Writer, Engineers, Politicians, cricketers, Youtubers 

for category in urls : 
    for i in range(4) : 
        
        url = "https://www.therichest.com/top-lists/top-100-richest-"+category+"/page/"+str(i+1)+"/"
        # print(url)
        headers = requests.utils.default_headers()

        headers.update(
            {
                'User-Agent': 'My User Agent 1.0',
            }
        )

        page = requests.get(url, headers=headers)

        htmlContent = page.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        tbody = soup.find('tbody')
        try : 
            tableRow = tbody.find_all('tr')
            for row in tableRow : 
                childList = []
                name = row.find('td', {'class' : 'name'})
                networth = row.find('td', {'class' : 'networth'})
                age = row.find('td', {'class' : 'age'})
                country = row.find('td', {'class' : 'country'})

                childList.append(name.text.strip())
                childList.append(age.text.strip())
                childList.append(country.text.strip())
                childList.append(category)

                link = row.find('a')
                pageLink = "https://www.therichest.com/" + link.get('href')
                celebPage = requests.get(pageLink, headers=headers)
                celebPage_HTMLContent = celebPage.content
                celebPage_Soup = BeautifulSoup(celebPage_HTMLContent, 'html.parser')

                picture = celebPage_Soup.find('picture')
                source = picture.find('source')
                image_link = source.get('srcset')[:-4]
                childList.append(image_link)

                celebPage_Table = celebPage_Soup.find('ul', {'class' : "net-profile_stats_list"})
                celebPage_ListItems = celebPage_Table.find_all('li')
                featureDict = {}
                for items in celebPage_ListItems : 
                    h3_text = items.find('h3')
                    if h3_text.text.strip() == 'Marital Status:' : 
                        value_text = items.find('span')
                        featureDict['marital_status'] = value_text.text
                    if h3_text.text.strip() == 'Education:' : 
                        value_text = items.find('span')
                        featureDict['education'] = value_text.text

                try : 
                    childList.append(featureDict['marital_status'])
                except : 
                    childList.append(np.nan)

                try: 
                    childList.append(featureDict['education'])
                except : 
                    childList.append(np.nan)


                childList.append(networth.text)
                parentList.append(childList)
            
        except: 
            print(category, i+1)

df = pd.DataFrame(parentList, columns=['Name', 'age', 'country', 'category', 
                                       'image', 'marital_status', 'Education', 'net_worth'])

degree = []
for i in range(len(df)) :
    try : 
        if 'College' in  df['Education'][i] : 
            degree.append('Graduate')
        elif 'University' in df['Education'][i] : 
            degree.append('Graduate')
        elif 'High School' in df['Education'][i] : 
            degree.append('high school')
        elif df['Education'][i] != np.nan : 
            degree.append('Graduate')
        else :
            degree.append(np.nan)
    except :
        degree.append(np.nan) 

df['Degree'] = degree

df