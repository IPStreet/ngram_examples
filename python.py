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


def download_csv_from_response(response,download_target_location):
    """

    :param response: a json response from the /claim_parser/ endpoint
    :param download_target_location: where you want the csv file to be downloaded to
    :return: void
    """
    csv_location = response['csv']
    patent_unique_id = response['application_number']
    target_file_name = download_target_location + patent_unique_id + '.csv'

    response = requests.get(csv_location, stream=True)


    with open(target_file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response



if __name__ == "__main__":

    api_key = "YOUR-API-KEY"

    ngram_response = get_ngrams_from_grant_number('7546750', api_key)
    print(ngram_response)
    keyphrase_response = get_keyphrases_from_grant_number('7546750', api_key)
    print(keyphrase_response)

    ngram_download_target_location = 'C:/Users/reedj_000/Desktop/Schwegment/output/ngram-'
    keyphrase_download_target_location = 'C:/Users/reedj_000/Desktop/Schwegment/output/keyphrase-'

    download_csv_from_response(ngram_response,ngram_download_target_location)
    download_csv_from_response(keyphrase_response, keyphrase_download_target_location)