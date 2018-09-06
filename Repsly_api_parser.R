library(httr)
library(xml2)
library(googlesheets)

query_params <- list(`contentType` =  "application/json")
get_result <- GET(url = "https://api.repsly.com/v3/export/photos/2", 
                  authenticate(user = "8F509842-1964-4474-9650-12DCBCF2E002", 
                                password = "1B39F561-7BAC-4AD4-9061-C7BA395D3011"),
                  query = query_params)
xml_t <- content(get_result, as = "text")
xml_r<- read_xml(xml_t)
#xml_structure(xml_r)

photo_id <- xml_text(
              xml_find_all(xml_r , "//Photos/Photo/PhotoID")
                )
client_code <- xml_text(
  xml_find_all(xml_r , "//Photos/Photo/ClientCode")
  )
client_name <- xml_text(
  xml_find_all(xml_r , "//Photos/Photo/ClientName")
)

note <- xml_text(
  xml_find_all(xml_r , "//Photos/Photo/Note")
)

date_time <- xml_text(
  xml_find_all(xml_r , "//Photos/Photo/DateAndTime")
)

photo_url <- xml_text(
  xml_find_all(xml_r , "//Photos/Photo/PhotoURL")
)
representative_code <- xml_text(
  xml_find_all(xml_r , "//Photos/Photo/RepresentativeCode")
)

representative_name <- xml_text(
  xml_find_all(xml_r , "//Photos/Photo/RepresentativeName")
)

visit_id <- xml_text(
  xml_find_all(xml_r , "//Photos/Photo/VisitID")
)

extracted_data <- data.frame(
  'PhotoId' = photo_id,
  'ClientCode' = client_code,
  'ClientName' = client_name,
  'Note' = note,
  'DateTime' = date_time,
  'PhotoURL' = photo_url,
  'RepresentativeCode' = representative_code,
  'RepresentativeName' = representative_name,
  'VisitId' = visit_id
)


#Работа с Google Sheet 
write.csv(extracted_data, "repsly_api_R_extraction.csv", row.names = FALSE)
repsly_api_R_extraction <- gs_upload("repsly_api_R_extraction.csv") #загрузка в Google Sheet
