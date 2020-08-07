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
    "from tqdm import tqdm_notebook"
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
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Content scraper for updating profile scraper\n",
    "def content_scraper(link):\n",
    "    ans = []\n",
    "    for link in tqdm(pureLinks):\n",
    "        ansDict = {}\n",
    "        browser = requests.get(link)\n",
    "        soup = BeautifulSoup(browser.content, 'html.parser')\n",
    "\n",
    "        detailContainer = soup.find('div', class_ = 'col-md-6 descr basket_content_product')\n",
    "        btfDetailContainer = BeautifulSoup(str(detailContainer), 'html.parser')\n",
    "\n",
    "        name = btfDetailContainer.find('h4').text.strip()\n",
    "\n",
    "        description = btfDetailContainer.find('div', class_ = 'ingredients show-read-more')\n",
    "        if description:\n",
    "            desc = btfDetailContainer.find('div', class_ = 'ingredients show-read-more').text.replace('\\n', ' ').replace('                                                     ', '')\n",
    "            ansDict['Description'] = description\n",
    "        if not description:\n",
    "            ansDict[\"Description\"] = None\n",
    "\n",
    "        brand = btfDetailContainer.find('p', {'class': 'brand_'})\n",
    "        if brand:\n",
    "            brd = btfDetailContainer.find('p', {'class': 'brand_'}).text.strip().replace('\\n', '')\n",
    "        if not brand:\n",
    "            ansDict['Brand'] = None\n",
    "\n",
    "        ansDict['ProductLink'] = link\n",
    "        ansDict['ProductName'] = name\n",
    "        ansDict['ScrapeDate'] = cleanDate\n",
    "        ansDict['Source'] = motherUrl\n",
    "        ans.append(ansDict)\n",
    "    return ans"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 75,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_previous = pd.read_csv(\"parma.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "date = datetime.datetime.now().timestamp()\n",
    "cleanDate = datetime.datetime.fromtimestamp(date)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
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
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "source = browser.page_source\n",
    "soup = BeautifulSoup(source, 'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "generalContainer = soup.find('ul', {'class': 'main_list'})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
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
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "97fdcee148574836b07cecab36edc72a",
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
    "prices = []\n",
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
    "\n",
    "    it_descs = soup.body.findAll('div', attrs={'class': 'item_description'})\n",
    "    for it_desc in it_descs:\n",
    "        it_html = BeautifulSoup(str(it_desc), 'html.parser')\n",
    "        price = it_html.find('span', attrs={'class': 'product_price'})\n",
    "        if not price:\n",
    "            price = it_html.find('p', attrs={'class': 'item_price'})\n",
    "        if price:\n",
    "            price = max([int(i) for i in re.findall('\\d+', price.text)])\n",
    "            prices.append(price)\n",
    "        if not price:\n",
    "            prices.append('Out of Stock')\n",
    "allLinks = flatten(allLinks)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.DataFrame(prices, index=allLinks, columns=[cleanDate])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_combination = df_previous.merge(df, how = \"outer\", on = df.index).drop_duplicates().set_index(\"key_0\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_combination.to_csv('parma.csv', encoding='utf-8')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "metadata": {},
   "outputs": [],
   "source": [
    " new_links = list(df[~df.index.isin(df_previous.index)].index)\n",
    " repeating_links = list(df[df.index.isin(df_previous.index)].index)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "if len(new_links) > 0:\n",
    "    df_old = pd.read_csv(\"parmaData.csv\")\n",
    "    newLinks = content_scraper(new_links)\n",
    "    dfProfile = pd.DataFrame(newLinks)\n",
    "    df_updated = df_old.merge(dfProfile, how = \"outer\", on = 'ProductLink').drop_duplicates().set_index(\"key_0\")\n",
    "    df_updated.to_csv(\"parmaData.csv\", encoding='utf-8')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 62,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "9 new links have been found: ['https://parma.am/en/product/product?slug=bread-parma-baguette-mini-130g_83525', 'https://parma.am/en/product/product?slug=curd-%2B-sour-cream-ashtarak-kat-7-200g_12304', 'https://parma.am/en/product/product?slug=curd-ashtarak-kat-7-200g_12302', 'https://parma.am/en/product/product?slug=olive-artoliva-xl-pitted-400g_84333', 'https://parma.am/en/product/product?slug=chocolate-candies-pralibel-n27-330g_82371', 'https://parma.am/en/product/product?slug=body-cream-lovea-shea-coconut-150ml_82243', 'https://parma.am/en/product/product?slug=_26092', 'https://parma.am/en/product/product?slug=shampoo-l%60angelica-wheat-250ml_82115', 'https://parma.am/en/product/product?slug=pads-always-platinum-ultra-n2-8-pcs_75254'] and 5913 repeating links.\n"
     ]
    }
   ],
   "source": [
    "# Print for logger\n",
    "print(\n",
    "    str(len(new_links)) + ' new links have been found: ' + str(new_links) +\n",
    "    ' and ' + str(len(repeating_links)) + ' repeating links.')"
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
