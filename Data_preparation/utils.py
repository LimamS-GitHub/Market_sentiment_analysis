import random
import re
from datetime import timedelta
from bs4 import BeautifulSoup
from langdetect import detect
import requests
import pandas as pd

#------------------------------------------------------------------------------------------------------------------

def is_english_text(text):
    try:
        language = detect(text)
        return language == 'en'
    except:
        return False

#------------------------------------------------------------------------------------------------------------------

def clean_tweet(tweet):
    """Cleans a tweet by removing mentions, links, special characters, and numbers."""
    tweet = re.sub(r'@', '', tweet)
    tweet = re.sub(r'http\S+|www\S+', '', tweet)
    tweet = re.sub(r'[^\w\s]', '', tweet)
    tweet = re.sub(r'\d+', '', tweet)
    tweet = re.sub(r'\n', '', tweet)
    tweet = tweet.strip()
    
    return tweet

#------------------------------------------------------------------------------------------------------------------

def generate_date_list(start_date, end_date):
    """Generates a list of dates between start_date and end_date."""
    return [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]

#------------------------------------------------------------------------------------------------------------------
def list_proxies():
    """List of proxies to use for scraping"""
    url = "https://www.sslproxies.org/"
    response = requests.get(url)
    print (response.status_code)
    if response.status_code != 200:
        print("❌ Erreur de chargement de la page de proxy.")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"class": "table table-striped table-bordered"})

    ip_list = []
    rows = table.tbody.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        ip = columns[0].text.strip()
        port = columns[1].text.strip()
        ip_port = f"{ip}:{port}"
        ip_list.append(ip_port)

    print(f"🔍 {len(ip_list)} proxies récupérés")
    return ip_list

#------------------------------------------------------------------------------------------------------------------

def valid_proxy (ip_list):
    """Teste la liste de proxies pour trouver un proxy HTTPS valide"""
    while ip_list:
        proxy = random.choice(ip_list)
        if test_https_proxy(proxy):
            print(f"✅ Proxy valide : {proxy}")
            return proxy,ip_list
        else:
            print(f"❌ Proxy refusé : {proxy}")
            ip_list.remove(proxy)

    print("❌ Aucun proxy HTTPS valide trouvé.")
    return None,ip_list

#------------------------------------------------------------------------------------------------------------------

def test_https_proxy(proxy):
    """Teste si un proxy supporte correctement HTTPS"""
    try:
        response = requests.get(
            "https://nitter.net",
            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            timeout=5
        )
        if response.status_code == 200:
            print(f"✅ Proxy HTTPS OK : {proxy}")
            return True
    except Exception as e:
        print(f"❌ Proxy HS : {proxy} | Erreur : {e}")
    return False

#------------------------------------------------------------------------------------------------------------------

def save_monthly_data(monthly_buffer, current_month):
    """Save tweets collected for a given month."""
    if monthly_buffer:
        monthly_df = pd.concat(monthly_buffer, ignore_index=True)
        filename = f"C:\\Users\\selim\\Desktop\\Market_sentiment_analysis\\Data_preperation\\{current_month}.csv"
        monthly_df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"💾 Month {current_month} saved with {len(monthly_df)} tweets.")