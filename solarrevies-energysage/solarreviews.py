# install missing module
!pip install lxml

# load libraries
import requests
import json
from bs4 import BeautifulSoup
from google.colab import files

# request data from url
response = requests.get('https://www.solarreviews.com/sitemap.xml')

# modify data response with bs4
soup = BeautifulSoup(response.text, 'xml')

# get all links
links = soup.find_all('loc')

# filter specific links
links = [l.get_text() for l in links]
links = [l for l in links if (l and '/installers/' in l) and ('#' not in l)]

result = {}
for x in range(len(links)):
  # request data from url
  res = requests.get(links[x])
  print('No: ' + str(x+1) + ' - Url: ' + links[x])

  # modify data response with bs4
  data = BeautifulSoup(res.text)

  error = data.select('h1.md:text-d3')
  if error:
        continue

  # get all information
  company_name = data.find('h1').get_text()
  company_logo = data.find('img', class_="p-3").get('src')
  expert_rating = data.select('.flex.solarreviews-ranking')[0].get('data-ranking')
  expert_rating_class = data.select('.flex.solarreviews-ranking')[0].find('p').get_text()

  # append to result dict
  result[x] = {
      "url": links[x],
      "company_name": company_name,
      "company_logo": company_logo,
      "expert_rating": expert_rating,
      "expert_rating_class": expert_rating_class
  }

# convert the result to excel format
headers = ["url","company_name","company_logo","expert_rating","expert_rating_class"]
df = pd.DataFrame.from_dict(result, orient='index')
df.to_excel("result.xlsx")
files.download('result.xlsx')
