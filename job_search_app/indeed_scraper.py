import requests
from bs4 import BeautifulSoup


def verify(title, city, state):
    """Verify valid search results or alert invalid results.

    Args:
        title (str): Job Title to be searched.
        city (str): City to be searched.
        state (str): State to be searched.
        desc (str):
    Returns:
        Invalid input messages or
        Sends valid input to a filter function
    """
    # Create HTTP request and pull HTML with BeautifulSoup
    url = "https://www.indeed.com/jobs?q=" + title + "&l=" + city + "%2C" + state

    response = requests.get(url)
    results = BeautifulSoup(response.content, 'html.parser')

    # Parse HTML and look for invalid query alerts
    loc_error = results.find('div', class_='invalid_location')
    query_error = results.find('div', class_='bad_query')

    # If the coast is clear, filter HTML
    if loc_error is None and query_error is None:
        return results, url
    # Return invalid search suggestions
    else:
        search_ops = results.find(id='search_suggestions')
        list_ops = search_ops.find_all('li')
        list_ops = [op.text.strip() for op in list_ops]
        # Present job match error if no location error is found and vice-versa
        if loc_error is None:
            return ['ERROR: No job matches found', list_ops]
        else:
            return ['ERROR: Location not found', list_ops]


def filter(results, url):
    """Filter HTML to extract Job Card information.

    Args:
        results (bs4 object): HTML from scraped page
        url (str): URL for page control
    Returns:
        jobs (list): list of lists contiaing information abour each job result
    """
    i = 0
    # Reconstruct url in order to control page count
    url += "&radius=15" + "&start=" + str(i)
    # Navigate to JobCard element in HTML
    job_cards = results.find_all('div', class_='jobsearch-SerpJobCard')

    # Iterate through JobCard to extract necessary info
    while True:
        jobs = []
        for card in job_cards:
            card_info = {}

            # Extract all information
            title = card.find(class_='title')
            comp = card.find(class_='company')
            loc = card.find(class_='location')
            salary = card.find(class_='salaryText')
            # Extract description for NLP model
            desc = card.find(class_='summary')

            # Organize all information
            card_info["title"] = title
            card_info["comp"] = comp
            card_info["loc"] = loc
            card_info["salary"] = salary
            card_info["desc"] = desc

            i += 1

            # Extract element text and save over original dictionary
            for key in card_info:
                elem = card_info[key]
                # Save valid elements to dictionary
                if elem:
                    card_info[key] = elem.text.strip().replace("\n", " ")
                    continue
                # Continue to next element if current element is empty
                else:
                    continue

            jobs.append(card_info)

        break

    return jobs
