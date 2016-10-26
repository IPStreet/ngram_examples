library(httr)


get_ngrams_from_grant_number <- function(grant_number, api_key){
  
  r = POST(url = "https://api.ipstreet.com/v2/claim_parser/ngram",
           add_headers(`x-api-key`=api_key),
           body = list(q=list(grant_number=grant_number)),
           encode ="json")
  
  return(content(r))
  
}

download_csv_from_response <- function(response, download_target_location){
  csv_location = response$csv
  download.file(url=csv_location, destfile=download_target_location, method='curl')
}

#configuartion parameters
api_key = "YOUR_API_KEY_GOES_HERE"
download_target_location = "YOUR_DOWNLOAD_TARGET_LOCATION_GOES_HERE"


response = get_ngrams_from_grant_number('7546750', api_key)
download_csv_from_response()