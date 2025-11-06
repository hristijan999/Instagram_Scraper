import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from IPython.display import HTML
import warnings
requests.packages.urllib3.disable_warnings()
warnings.filterwarnings('ignore')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}
session=requests.Session()
session.headers.update(headers)



snapshot_url='https://www.cnbc.com/markets/'

resp=session.get(snapshot_url,timeout=5)
soup=BeautifulSoup(resp.text,"html.parser")
print(soup.prettify())