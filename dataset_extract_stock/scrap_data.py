from lxml import html
import requests

# data property to scrap and their Xpaths
data_prop = {
    "title": "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span/text()",
    "release_year": "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a/text()",
    "imdb_rating": "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[1]/span[1]/text()"
}

# fake user agent to allow scraping
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

# common string for url films
url_common = "http://www.imdb.com/title/"

def getData(imdb_id, xpath) -> str:
    """
    Scrap data from imdb website.
    

    Args:
        imdb_id (str): represents the film id.
        xpath (str): It is the Xpath where to get data we want.

    Returns:
        str: return data
    """
    # url where to scrap
    url = url_common + imdb_id


    # HTML request
    page = requests.get(url, headers=HEADERS)

    # Parsing
    tree = html.fromstring(page.content)

    # get data in string
    data = tree.xpath(xpath)
    data = str(data)
    
    # delete brackets and quotes
    data = data[2:-2]

    return data