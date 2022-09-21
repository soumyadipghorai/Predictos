import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np 
import random
import time 

begin  = time.time()
url = 'https://www.therichest.com/celebnetworth-category/athletes/'
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)

page = requests.get(url, headers=headers)
htmlContent = page.content
soup = BeautifulSoup(htmlContent, 'html.parser')

side_bar_section = soup.find('section', {'class' : 'net-listing_nav'})
category_links = side_bar_section.find_all('li')

# extracting category name and category  link 
to_visit, category_name_list = [], []
for count, link in enumerate(category_links) : 
    if count != 0 : 
        to_visit.append('https://www.therichest.com' +  link.a.get('href'))
        category_name = link.text.strip()
        if len(category_name.split(' ')) > 1 : 
            category_name = category_name[8:]
            category_name_list.append(category_name)
        else : 
            category_name_list.append(category_name)

print(category_name_list)

female_category = ['Actresses', 'Adult Actresses', 'Businesswomen']
male_category = ['Actor', 'Adult Actor', 'Businessman']


# --> category link 
parentList, error, counter = [], 0, 0
for index, link in enumerate(to_visit) : 
    page = requests.get(link, headers = headers)
    htmlContent = page.content 
    soup = BeautifulSoup(htmlContent, 'html.parser')
    print(category_name_list[index])
    print("="*30)

    # extracting total pages in each category 
    try :
        page_num = soup.find('div', {'class' : 'pages'})
        last_page = page_num.find('span').text.strip()[2:]
    except : 
        last_page = 1
    
    # --> page num 
    for i in range(int(last_page)) : 
        page_num_link = link + 'page/' + str(i+1)+'/'
        page_num = requests.get(page_num_link, headers = headers)
        page_num_htmlContent = page_num.content 
        page_num_soup = BeautifulSoup(page_num_htmlContent, 'html.parser')
        popular_div = page_num_soup.find('div', {'class' : 'browse-net-worth'})
        articles = popular_div.find_all('article', {'class' : 'js-content'})
        print("page num : ",i+1)

        # --> person div 
        for richArticle in articles : 
            childList = []
            name = richArticle.find('h3', {'class' : 'bc-title'}).text.strip()[:-10]
            childList.append(name)

            networth = richArticle.find('div', {'class' : 'bc-networth'}).text.strip()
            childList.append(networth)

            category = category_name_list[index]
            if len(category.split(' ')) > 1 :
                category = category[8:]
            childList.append(category)

            if category in female_category : 
                childList.append('Female')
            elif category in male_category : 
                childList.append('Male')
            else : 
                childList.append(np.nan)

            # --> personal page
            personal_page_link = 'https://www.therichest.com' + richArticle.find('h3', {'class' : 'bc-title'}).a.get('href')

            personal_page = requests.get(personal_page_link, headers = headers)
            personal_page_htmlContent = personal_page.content 
            personal_page_soup = BeautifulSoup(personal_page_htmlContent, 'html.parser')
            
            try :
                profile_image_div = personal_page_soup.find('div', {'class' : 'responsive-img img-size-networth-profile'})
                profile_pic = profile_image_div.find('picture')
                profile_pic_source = profile_pic.find('source')
                profile_pic_link = profile_pic_source.get('srcset')[:-4]
                childList.append(profile_pic_link)
            except : 
                childList.append(np.nan)
                print('Image not found for {}'.format(name))

            # --> personal details 
            personal_details_table = personal_page_soup.find('section', {'class' : 'net-profile_stats'})
            try : 
                personal_deatails_li = personal_details_table.find_all('li')
                print(name)
                personal_details_dict = {}
                for list_item in personal_deatails_li : 
                    personal_details_dict[list_item.find('h3').text.strip()] = list_item.find('span').text.strip()

                try : 
                    childList.append(personal_details_dict['Age:'])
                except : 
                    childList.append(np.nan)
                    print('Age not found for {}'.format(name))

                try : 
                    childList.append(personal_details_dict['Date of Birth:'])
                except : 
                    childList.append(np.nan)
                    print('DOB not found for {}'.format(name))

                try : 
                    childList.append(personal_details_dict['Nationality:'])
                except : 
                    childList.append(np.nan)
                    print('Nationality not found for {}'.format(name))

                try : 
                    childList.append(personal_details_dict['Education:'])
                except : 
                    childList.append(np.nan)
                    print('Education not found for {}'.format(name))

                try : 
                    childList.append(personal_details_dict['Marital Status:'])
                except : 
                    childList.append(np.nan)
                    print('Marital Status not found for {}'.format(name))

                try : 
                    childList.append(personal_details_dict['Source of Wealth:'])
                except : 
                    childList.append(np.nan)
                    print('Source of Wealth not found for {}'.format(name))
                    
                try : 
                    childList.append(personal_details_dict['Birth Place:'])
                except : 
                    childList.append(np.nan)
                    print('Birth Place not found for {}'.format(name))

                try : 
                    personal_description = personal_page_soup.find('span', {'itemprop' : 'description'})
                    personal_description_para = personal_description.find_all('p')
                
                    whole_para_text = ''
                    for paranum, para in enumerate(personal_description_para) : 
                        if paranum == 0 : 
                            childList.append(para.text.strip())
                            whole_para_text += para.text.strip()
                        whole_para_text += para.text.strip()


                    if childList[3] is np.nan : 
                        whole_para_text = whole_para_text.lower()
                        personal_description_para_words = whole_para_text.split(' ')
                        description_male_count = personal_description_para_words.count('he') +  personal_description_para_words.count('his')
                        description_female_count = personal_description_para_words.count('she') +  personal_description_para_words.count('her')
                        print(description_male_count, description_female_count)
                        if (description_male_count == 0) and (description_female_count == 0) : 
                            childList[3] = np.nan
                        elif description_male_count > description_female_count : 
                            childList[3] = 'Male'
                        else : 
                            childList[3] = 'Female'
                except : 
                    childList.append(np.nan)
                    # raise Exception('Personal description not found for')
                    print('Personal description not found for {}'.format(name))

                childList.append(personal_page_link)
                print('person Data : ', childList)
                print('Check row length : ', end = ' ')
                print(len(childList) == 14)
                parentList.append(childList)
                counter += 1
                print(str(counter)+' persons inserted')
                print('\n\n')
                
            except : 
                error += 1
                print('ERROR PAGE NOT FOUND FOR {}'.format(name))
        print('\n\n')
    print("/"*30 + category + ' finished '+"/"*30)
    print('\n\n\n')
end  = time.time()
print('total time taken in sec : {}'.format(end - begin))      
print('#Pages gave error : {}'.format(error))

df = pd.DataFrame(
    parentList, columns = [
                            'Name', 'networth', 'category', 'gender', 'profile_pic', 'age', 
                            'DOB', 'nationality', 'education', 'marital_status',
                            'source_of_wealth', 'birth_place', 'personal_details', 'profile_link'
                            ]
                )

root = '../data/'
df.to_csv(root + 'raw_data.csv', encoding='utf-8', index= False)