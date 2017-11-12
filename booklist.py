from lxml import html
import requests


def get_book_links(searchTerm):
    page = requests.get('https://catalog.guelphpl.ca/Mobile/Search/Results/?t=' + searchTerm + '&f=a&s=TI&l=(TOM%3dbks+or+TOM%3dser)+not+TOM%3debk&o=RELEVANCE&ls=1.10.0.')
    tree = html.fromstring(page.content)

    links = tree.xpath('//@href')
    book_links = []
    for link in links:
        if '/Mobile/Search/Title/' in str(link):
            detail_link = link.replace('Title', 'Details')
            if not detail_link in book_links:
                book_links.append(detail_link)
    get_book_availability(book_links)

def get_book_availability(book_links):
    print book_links
    page = requests.get('https://catalog.guelphpl.ca' + book_links[0])
    tree = html.fromstring(page.content)
    title = [span.xpath('string()') for span in
             tree.xpath('//div[@class="nsm-long-item nsm-e35"]/span')]
    print title

book = raw_input('Enter book name: ').strip().replace(' ', '+')
author = raw_input('Enter author name: ')
get_book_links(book)
