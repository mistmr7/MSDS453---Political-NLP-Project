import requests
from bs4 import BeautifulSoup
import time


url = "https://www.reddit.com/r/Conservative/top/?t=year"
html = requests.get(url)

soup = BeautifulSoup(html.text, "html.parser")
time.sleep(4)
links = soup.find_all("a", {"class": "inset-0"})
for i in links:
    print(i["href"])


# session = HTMLSession()
# r = session.get(url)
# r.html.render()
# print(r.html.html)
