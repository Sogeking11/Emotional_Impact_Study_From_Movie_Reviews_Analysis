from lxml import html
import requests

def getTitle(url: str) -> str:
    # fake user agent to allow scraping
    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

    # xPATH FOR TITLE
    xpath = '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span/text()'

    # HTML request
    page = requests.get(url, headers=HEADERS)

    # Parsing
    tree = html.fromstring(page.content)

    # get title and print it
    title = tree.xpath(xpath)
    title = str(title)
    title = title[2:-2]

    return title

# The data set must be up from local place to use python script
file_url = "../aclImdb/test/urls_neg.txt"

# This is the Xpath to get title in the page from Imdb source
xpath = '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span/text()'


# operation
# Here we get all the lines from the file, for each line we add his title and append it in a list
filelines = []
with open(file_url, 'r') as f:
    for line in f.readlines():
        url_to_scrap = line[0:-13]
        title = getTitle(url_to_scrap)
        filelines.append(line.rstrip('\n') + "," + title + '\n')
        print(title)

# Here we just add in the precedent file each element from the list to a new line
with open(file_url, 'w') as f:
    for line in filelines:
        f.write(line)