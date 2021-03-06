import csv
import json
import shutil

import requests


def get_ngrams_from_grant_number(grant_number, api_key):
    """

    :param grant_number: a patent grant number
    :param api_key: client api key
    :return: ngrams json object
    """
    endpoint = 'https://api.ipstreet.com/v2/claim_parser/ngram'
    headers = {'x-api-key': api_key}
    payload = json.dumps({'q': {'grant_number': grant_number}})
    r = requests.post(endpoint, headers=headers, data=payload)

    response = r.json()

    return response

def get_keyphrases_from_grant_number(grant_number, api_key):
    """

    :param grant_number: a patent grant number
    :param api_key: client api key
    :return: keyphrases json object
    """
    endpoint = 'https://api.ipstreet.com/v2/claim_parser/keyphrase'
    headers = {'x-api-key': api_key}
    payload = json.dumps({'q': {'grant_number': grant_number}})
    r = requests.post(endpoint, headers=headers, data=payload)

    response = r.json()

    return response

def get_claim_elements_from_grant_number(grant_number, api_key):
    """

    :param grant_number: a patent grant number
    :param api_key: client api key
    :return: keyphrases json object
    """
    endpoint = 'https://api.ipstreet.com/v2/claim_parser/claim_element'
    headers = {'x-api-key': api_key}
    payload = json.dumps({'q': {'grant_number': grant_number}})
    r = requests.post(endpoint, headers=headers, data=payload)

    response = r.json()

    return response



def download_csv_from_response(response,download_target_location):
    """

    :param response: a json response from the /claim_parser/ endpoint
    :param download_target_location: where you want the csv file to be downloaded to
    :return: void
    """
    csv_location = response['csv_link']
    patent_unique_id = response['application_number']
    target_file_name = download_target_location + patent_unique_id + '.csv'

    response = requests.get(csv_location, stream=True)


    with open(target_file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def get_list_of_unique_ids_from_csv(csv_file):
    """

    :param csv_file: a csv file with patent unique ids in the first column
    :return: a list of patent unique id numbers
    """

    pat_nums = []
    with open(patent_list_location, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                pat_nums.append(row[0])
            except:
                pass

    return pat_nums


if __name__ == "__main__":

    api_key = "YOUR_API_KEY_GOES_HERE"

    ngram_download_target_location = 'WHERE_YOU_WANT_YOUR_NGRAM_RESULTS_TO_BE_STORED'
    keyphrase_download_target_location = 'WHERE_YOU_WANT_YOUR_KEYPHRASE_RESULTS_TO_BE_STORED'
    claim_elements_download_target_location = 'WHERE_YOU_WANT_YOUR_KEYPHRASE_RESULTS_TO_BE_STORED'

    patent_list_location = 'LOCATION_OF_A_CSV_FILE_WITH_GRANT_NUMBERS_IN_FIRST_COLUMN'

    target_patents = get_list_of_unique_ids_from_csv(patent_list_location)


    for num in target_patents:

        try:
            ngram_response = get_ngrams_from_grant_number(num, api_key)
            download_csv_from_response(ngram_response, ngram_download_target_location)
            print("Success: N-Grams found in asset " + num + " successfully downloaded")
        except:
            print("Error " + num)

        try:
            keyphrase_response = get_keyphrases_from_grant_number(num, api_key)
            download_csv_from_response(keyphrase_response, keyphrase_download_target_location)
            print("Success: Key Phrases found in assets " + num + " successfully downloaded")
        except:
            print("Error " + num)

        try:
            claim_elements = get_claim_elements_from_grant_number(num, api_key)
            download_csv_from_response(claim_elements, claim_elements_download_target_location)
            print("Success: Claim Elements found in asset " + num + " successfully downloaded")
        except:
            print("Error " + num)
