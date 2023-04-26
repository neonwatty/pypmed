from .parsers import elem_to_dict, build_query_string
from .filters import author_metadata_filter
import requests
import time
from requests.exceptions import RequestException
from typing import Dict, List
from xml.etree import ElementTree as ET
from datetime import datetime
current_year = datetime.now().year


# retry function requests
def retry_post_request(url: str,
                       params: Dict,
                       max_retries: int = 5,
                       retry_delay: int = 10,
                       timeout: int = 45) -> List[Dict]:
    # make request with retries
    for retry_count in range(max_retries):
        try:
            # make request
            response = requests.post(url, params=params, timeout=timeout)
            # check status code - else return data
            if response.status_code >= 400 and response.status_code < 500:
                print(f"Bad request: {response.text}")
                if retry_count < max_retries - 1:
                    print(f"Retrying after {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise Exception(f"Failed to complete POST request after {max_retries} attempts")
            else:
                return response
        except RequestException as e:
            print(f"POST request failed: {e}")
            if retry_count < max_retries - 1:
                print(f"Retrying after {retry_delay} seconds...")
                time.sleep(retry_delay)
    raise Exception(f"Failed to complete POST request after {max_retries} attempts")


def query_pubmed_api(search_criteria: dict) -> list:
    # unpack institution if present - not a search criteria for official pubmed api
    institution = None
    if 'institution' in search_criteria.keys():
        institution = search_criteria['institution']
    # build query string from input search_criteria
    query_str = build_query_string(search_criteria)
    # setup api endpoint to retrieve pubmed ids based on input query
    endpoint_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    params = {
        'db': 'pubmed',
        'term': f'{query_str}',
        'retmode': 'json'
    }

    # Make API request and retrieve json response with ids
    response = retry_post_request(endpoint_url, params=params)

    # if response is ok, retrieve the ids and use them to retrieve the desired fields for each article
    if response.ok:
        data = response.json()
        id_list = data["esearchresult"]["idlist"]
        # Use the IDs to retrieve the desired fields for each article
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "xml"
        }
        # make request
        response = retry_post_request(url, params=params)
        # if response is ok, parse the xml and convert to a dictionary
        if response.ok:
            # Parse the XML file
            root = ET.fromstring(response.text)

            # Convert the root element to a dictionary
            article_list = []
            try:
                article_list = elem_to_dict(root)['PubmedArticle']
                if not isinstance(article_list, list):
                    article_list = [article_list]
            except Exception as e:
                print(e)
                print(f"No articles found for search criteria: {search_criteria}")
                return None

            # filter articles by checking that desired author / institution is present
            final_articles = []
            for article in article_list:
                # generate example
                pmid = article['MedlineCitation']['PMID']
                journal_issn = article['MedlineCitation']['Article']['Journal']['ISSN']
                journal_title = article['MedlineCitation']['Article']['Journal']['Title']
                article_title = article['MedlineCitation']['Article']['ArticleTitle']
                publication_year = article['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Year']
                author_list = article['MedlineCitation']['Article']['AuthorList']['Author']

                # start article package
                article_dict = {}
                article_dict['pmid'] = pmid
                article_dict['journal_issn'] = journal_issn
                article_dict['journal_title'] = journal_title
                article_dict['article_title'] = article_title
                article_dict['publication_year'] = publication_year

                # if author search - perform filtering (double check that correct author is pulled)
                if search_criteria['author_first_name'] is not None and search_criteria['author_last_name'] is not None:
                    # package author info for filter
                    author_metadata = {}
                    author_metadata['author_first_name'] = search_criteria['author_first_name']
                    author_metadata['author_last_name'] = search_criteria['author_last_name']
                    author_metadata['institution'] = institution
                    # apply filter
                    filtered_article = author_metadata_filter(author_metadata, article_dict, author_list)
                    # store
                    if filtered_article is not None:
                        final_articles.append(filtered_article)
                else:
                    article_dict['author_list'] = author_list
                    final_articles.append(article_dict)
                return final_articles
            return None
