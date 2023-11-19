import requests
from bs4 import BeautifulSoup
def get_movie_reviews(base_link = "https://www.imdb.com/title/tt13433812/"):
    start_url = f'{base_link}reviews?ref_=tt_urv'
    link = f'{base_link}reviews/_ajax'

    params = {
        'ref_': 'undefined',
        'paginationKey': ''
    }

    with requests.Session() as s:
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        res = s.get(start_url)
        reviews = []
        while True:
            soup = BeautifulSoup(res.text,"lxml")
            for item in soup.select(".review-container"):
                reviewer_heading = item.select_one("div.lister-item-content > a.title").get_text(strip=True)
                reviewer_content = item.select_one("div.content > div").get_text(strip=True)
                reviews.append(reviewer_heading + " " + reviewer_content)
            try:
                pagination_key = soup.select_one(".load-more-data[data-key]").get("data-key")
            except AttributeError:
                break
            params['paginationKey'] = pagination_key
            res = s.get(link,params=params)
    return reviews
