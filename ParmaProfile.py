{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from bs4 import BeautifulSoup\n",
    "import requests\n",
    "from selenium import webdriver\n",
    "import time\n",
    "import pandas as pd\n",
    "from tqdm.notebook import tqdm\n",
    "import datetime\n",
    "import pickle\n",
    "import numpy as np\n",
    "from selenium.webdriver.chrome.options import Options\n",
    "import re\n",
    "from selenium.webdriver.common.keys import Keys\n",
    "from selenium.webdriver.common.by import By\n",
    "from selenium.webdriver.support.ui import WebDriverWait\n",
    "from selenium.webdriver.support import expected_conditions as EC\n",
    "from tqdm import tqdm_notebook\n",
    "import pymongo\n",
    "from pymongo import MongoClient"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def read_mongoDB(localhost, database, collection):\n",
    "    client = MongoClient(\n",
    "        \"mongodb+srv://davaer:<password>@foodmarket.rrtsu.gcp.mongodb.net/test\"\n",
    "    )\n",
    "    db = client[database]\n",
    "    col = db[collection]\n",
    "    data = pd.DataFrame(list(col.find()))\n",
    "    result = data.drop(\"_id\", axis=1)\n",
    "    return result"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def insert_mongoDB(df, localhost, database, collection):\n",
    "    client = MongoClient(\n",
    "        \"mongodb+srv://davaer:<password>@foodmarket.rrtsu.gcp.mongodb.net/test\"\n",
    "    )\n",
    "    db = client[database]\n",
    "    col = db[collection]\n",
    "    col.insert_many(df.to_dict('records'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "flatten = lambda l: [item for sublist in l for item in sublist]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "date = datetime.datetime.now().timestamp()\n",
    "cleanDate = datetime.datetime.fromtimestamp(date)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "options = Options()\n",
    "options.add_argument(\"--headless\")\n",
    "browser = webdriver.Chrome(options=options)\n",
    "base_url = 'https://parma.am/en/'\n",
    "motherUrl = 'https://parma.am'\n",
    "browser.get(base_url)\n",
    "time.sleep(4)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "source = browser.page_source\n",
    "soup = BeautifulSoup(source, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# All category links\n",
    "generalContainer = soup.find('ul', {'class': 'main_list'})\n",
    "btfGeneral = BeautifulSoup(str(generalContainer), 'html.parser')\n",
    "rawGeneral = btfGeneral.find_all('li', {'class': None})\n",
    "btfRawGeneral = BeautifulSoup(str(rawGeneral), 'html.parser')\n",
    "noDropextensions = btfRawGeneral.find_all('a', {'href': True})\n",
    "link_extensions_noDrop = [i['href'] for i in noDropextensions]\n",
    "fullNoDrop = [motherUrl + link for link in link_extensions_noDrop]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "3118bbcb5fcb49b8a1346605eee462e9",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "HBox(children=(FloatProgress(value=0.0, max=134.0), HTML(value='')))"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n"
     ]
    }
   ],
   "source": [
    "# Product Links\n",
    "allLinks = []\n",
    "for link in tqdm(fullNoDrop):\n",
    "    browser = webdriver.Chrome(options=options)\n",
    "    browser.get(link)\n",
    "    time.sleep(4)\n",
    "\n",
    "    wait = WebDriverWait(browser, 40)\n",
    "    confirmAge = browser.find_elements_by_xpath(\n",
    "        \"//button[@type='button' and @class='swal2-confirm swal2-styled']\")\n",
    "    if confirmAge:\n",
    "        wait.until(\n",
    "            EC.element_to_be_clickable((\n",
    "                By.XPATH,\n",
    "                \"//button[@type='button' and @class='swal2-confirm swal2-styled']\"\n",
    "            )))\n",
    "        confirmAge[0].click()\n",
    "\n",
    "    source = browser.page_source\n",
    "    soup = BeautifulSoup(source, 'html.parser')\n",
    "\n",
    "    productBins = soup.find_all('div', class_='item_description')\n",
    "    btfProductBins = BeautifulSoup(str(productBins), 'html.parser')\n",
    "    linkContainer = btfProductBins.find_all(\"a\", {\n",
    "        'class': 'item_name',\n",
    "        \"href\": True\n",
    "    })\n",
    "    pureLinks = [i['href'] for i in linkContainer]\n",
    "    fullLinks = [motherUrl + link for link in pureLinks]\n",
    "    allLinks.append(fullLinks)\n",
    "    allLinks = flatten(allLinks)\n",
    "    pureLinks = list(dict.fromkeys(allLinks))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 161,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "7a816ba53a6649d99f5a7229a93d4c72",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "HBox(children=(FloatProgress(value=0.0, max=5751.0), HTML(value='')))"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n"
     ]
    }
   ],
   "source": [
    "# Content Scraper\n",
    "ans = []\n",
    "for link in tqdm(pureLinks):\n",
    "    ansDict = {}\n",
    "    browser = requests.get(link)\n",
    "    soup = BeautifulSoup(browser.content, 'html.parser')\n",
    "\n",
    "    detailContainer = soup.find('div',\n",
    "                                class_='col-md-6 descr basket_content_product')\n",
    "    btfDetailContainer = BeautifulSoup(str(detailContainer), 'html.parser')\n",
    "    # Scrape name\n",
    "    name = btfDetailContainer.find('h4').text.strip()\n",
    "    # Scrape description\n",
    "    description = btfDetailContainer.find('div',\n",
    "                                          class_='ingredients show-read-more')\n",
    "    if description:\n",
    "        desc = btfDetailContainer.find(\n",
    "            'div', class_='ingredients show-read-more').text.replace(\n",
    "                '\\n', ' ').replace(\n",
    "                    '                                                     ',\n",
    "                    '')\n",
    "        ansDict['Description'] = desc\n",
    "    if not description:\n",
    "        ansDict[\"Description\"] = None\n",
    "    # Scrape brand name\n",
    "    brand = btfDetailContainer.find('p', {'class': 'brand_'})\n",
    "    if brand:\n",
    "        brd = btfDetailContainer.find('p', {\n",
    "            'class': 'brand_'\n",
    "        }).text.strip().replace('\\n', '')\n",
    "        ansDict[\"Brand\"] = brd\n",
    "    if not brand:\n",
    "        ansDict['Brand'] = None\n",
    "    # Insert into dictionary, then list\n",
    "    ansDict['ProductLink'] = link\n",
    "    ansDict['ProductName'] = name\n",
    "    ansDict['ScrapeDate'] = cleanDate\n",
    "    ansDict['Source'] = motherUrl\n",
    "    ans.append(ansDict)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 162,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.DataFrame(ans)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Store full info in database\n",
    "insert_mongoDB(df, '27017', 'ProfileScraper', 'Parma')"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  },
  "toc": {
   "base_numbering": 1,
   "nav_menu": {},
   "number_sections": true,
   "sideBar": true,
   "skip_h1_title": false,
   "title_cell": "Table of Contents",
   "title_sidebar": "Contents",
   "toc_cell": false,
   "toc_position": {},
   "toc_section_display": true,
   "toc_window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
