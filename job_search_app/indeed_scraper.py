import requests
from bs4 import BeautifulSoup

def verify(results):
    loc_error = results.find('div', class_='invalid_location')
    query_error = results.find('div', class_='bad_query')
    if loc_error == None and query_error == None:
        filter(results)
    else:
        search_ops = results.find(id='search_suggestions')
        list_ops = search_ops.find_all('li')
        if loc_error == None:
            print('\nError: No job matches found.\n')
        else:
            print('\nError: Location not found.\n')
        for op in list_ops:
            print('-' + op.text.strip())



def filter(results):
    job_cards = results.find_all('div', class_='jobsearch-SerpJobCard')
    i = 0
    while True:
        for card in job_cards:
            card_info = []
            title = card.find(class_='title')
            card_info.append(title)
            comp = card.find(class_='company')
            card_info.append(comp)
            loc = card.find(class_='location')
            card_info.append(loc)
            salary = card.find(class_='salaryText')
            card_info.append(salary)

            i += 1
            print('\n')
            for elem in card_info:
                if elem == None:
                    continue
                elif elem == card_info[0]:
                    print(str(i) + '.' + ' ' + elem.text.strip())
                    continue
                else:
                    print(elem.text.strip())
                    continue
        break

def main():
    info = """
    This program will ask questions to provide quick info of a
    job search from indeed.com.
    """
    print(info)
    job_desc = input("Enter Job Title > ")
    city = input("Desired City > ")
    state = input("State > ")

    url = "https://www.indeed.com/jobs?q=" + job_desc + "&l=" + city + "%2C" + state
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    verify(soup)

if __name__ == '__main__':
    main()
