import requests
from bs4 import BeautifulSoup
import pprint

def write_to_file(data):
    with open('output.txt', mode='w') as output_file:
      for elem in data:
        output_file.write(str(elem) + '\n\n')

def sort_stories_by_votes(hnlist):
  return sorted(hnlist, key=lambda k:k['votes'], reverse=True) 

def create_custom_hacker_news(links, subtext):
  hn = []
  for idx, item in enumerate(links):
    title = item.getText()
    href = item.get('href', None)
    vote = subtext[idx].select('.score')
    if len(vote):
      points = int(vote[0].getText().replace(' points', ''))
      if(points > 99):
        hn.append({'title': title, 'link': href, 'votes': points})
  return sort_stories_by_votes(hn)

url = 'https://news.ycombinator.com/news'

hn_first_and_second = []

for page in range(1, 4):
  res = requests.get(url + '?p=' + str(page))
  soup = BeautifulSoup(res.text, 'html.parser')

  links = soup.select('.titlelink')
  subtext = soup.select('.subtext')

  hn_first_and_second.append(create_custom_hacker_news(links, subtext))

flat_list_hn = [item for sublist in hn_first_and_second for item in sublist]

write_to_file(sort_stories_by_votes(flat_list_hn))
