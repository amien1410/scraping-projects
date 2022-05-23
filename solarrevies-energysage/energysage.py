# load libraries
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from google.colab import files

# get every urls of suppliers from energysage
supplier_list = list()
for x in range(1, 170):

  # page number url
  url = 'https://www.energysage.com/supplier/search?selected_facets=technology_types:Solar%20PV&page=' + str(x)
  
  # request data from url
  res = requests.get(url)
  data = BeautifulSoup(res.text)

  links = data.find_all('a', class_="supplier-name")
  links = [l.get('href') for l in links]
  # links = [l for l in links if (l and '/supplier/' in l)]

  # remove duplicate link
  for item in links:
      if item not in supplier_list:
          supplier_list.append(item)

# print the number of urls we got
len(supplier_list)

result = {}
for x in range(len(supplier_list)):
  # request data from url
  res = requests.get('https://www.energysage.com' + supplier_list[x])

  # modify data response with bs4
  data = BeautifulSoup(res.text)

  # get all information
  company_name = data.select('span[itemprop=name]')[0].get_text()

  company_logo = data.select('img[itemprop=image]')
  if len(company_logo) != 0:
    company_logo = company_logo[0].get('src')
  else:
    company_logo = 'No data'

  expert_rating =data.select('img.block-energysage-approved')
  if len(expert_rating) != 0:
    expert_rating = expert_rating[0].get('alt')
  else:
    expert_rating = 'No expert rating'

  # append to result dict
  result[x] = {
      "url": 'https://www.energysage.com' + supplier_list[x],
      "company_name": company_name,
      "company_logo": company_logo,
      "expert_rating": expert_rating
  }
  print('No: ' + str(x+1) + '- Url: ' + supplier_list[x])

with open("result.json", "w") as outfile:
    json.dump(result, outfile)
files.download('result.json')

headers = [ "url", "company_name", "company_logo", "expert_rating"]
df = pd.DataFrame.from_dict(result, orient='index')
df.to_excel("result.xlsx")
files.download('result.xlsx')
