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

def download_csv_from_response(response,download_target_location):
    """

    :param response: a json response from the /claim_parser/ngram endpoint
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

    api_key = "YOUR_API_KEY_GOES_HERE"

    response = get_ngrams_from_grant_number('7546750', api_key)
    print(response)

    download_target_location = 'YOUR_DOWNLOAD_TARGET_LOCATION_GOES_HERE'

    download_csv_from_response(response,download_target_location)