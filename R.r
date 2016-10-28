library(httr)


get_ngrams_from_grant_number <- function(grant_number, api_key){

  r = POST(url = "https://api.ipstreet.com/v2/claim_parser/ngram",
           add_headers(`x-api-key`=api_key),
           body = list(q=list(grant_number=grant_number)),
           encode ="json")

  return(content(r))

}

get_keyphrases_from_grant_number <- function(grant_number, api_key){

  r = POST(url = "https://api.ipstreet.com/v2/claim_parser/keyphrase",
           add_headers(`x-api-key`=api_key),
           body = list(q=list(grant_number=grant_number)),
           encode ="json")

  return(content(r))

}

download_csv_from_response <- function(response, download_target_folder){
  csv_location = response$csv_link
  
  if (response$grant_number != ''){
    unique_id = response$grant_number
  } else {
    unique_id = response$application_number
  }

  download_target_file = paste(download_target_folder,unique_id,".csv", sep = "")
  download.file(url=csv_location, destfile=download_target_file, method='auto',mode = "wb")
}

#configuartion parameters
api_key = "YOUR_API_KEY_GOES_HERE"
ngram_download_target_folder = 'WHERE_YOU_WANT_YOUR_NGRAM_RESULTS_TO_BE_STORED'
keyphrase_download_target_folder = 'WHERE_YOU_WANT_YOUR_KEYPHRASE_RESULTS_TO_BE_STORED'


#send a ngram request
ngram_response = get_ngrams_from_grant_number('7546750', api_key)
#send a keyphrase request
keyphrase_response = get_keyphrases_from_grant_number('7546750', api_key)

#save both requests to csv files
download_csv_from_response(ngram_response,ngram_download_target_folder)
download_csv_from_response(keyphrase_response,keyphrase_download_target_folder)
