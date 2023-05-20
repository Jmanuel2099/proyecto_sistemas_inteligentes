# proyecto_sistemas_inteligentes
Machine learning microservices 

# Project setup
- Create virtual environment 
```sh
py -m venv venv
```
- Activate virtual environment
```sh
.\venv\Scripts\activate
```

- Download python libraries used in the project
```sh
pip install -r requirements.txt
```

# End points
## Load an excel (.xlsx) file
Method: POST http://127.0.0.1:8000/file/load
- Request: 
```json
{
    "file" : "<file_path>"
}
```
- Response: 
  - if do not send a non-.xlsx file
  ```json
  {
      "Error": "400 Bad Request", 
      "Message": "expect a file with .xlsx extension"
  }
  ```
  - If do not send any document
  ```json
  {
      "Error": "400 Bad Request", 
      "Message": "A file was expected to be received."
  }
  ```
  - Success
  ```json
  {
      "Message": "Success"
  }
  ```

## Identify column types or describe the file
Method: GET http://127.0.0.1:8000/file/describe
- Request: No body requets
- Response:
  - If no file has been uploaded to the system
  ```json
  {
      "Error": "424 Failed Dependency", 
      "Message": "No document has been uploaded yet."
  }
  ```
  - Success
  ```json
  {
      "data": 
          {
              "año": "float",
              "edad": "str",
              "sexo": "str",
              "id_comuna": "float",
              "comuna": "str",
              "valor": "float"
          }
  }
  ```
## Missing data processing
Method: GET http://127.0.0.1:8000/file/missingdata/method_id
- Request: The request has no body, to select a missing data processing method, send the ID of the method by parameters in the url.
  - Imputation: 1 (For categorical data, imputation is done by mode and for numerical data, imputation is done by mean).
  - Discard: 2
- Response:
  - if send an id that is neither 1 nor 2 
   ```json
  {
      "Error": "408 Time out", 
      "Message": "Method_id parameter must be 1 or 2."
  }
  ```
  - Success
  ```json
  {
      "Message": "Method applied successfully."
  }
  ``` 
## Graphical statistical analysis
Method: GET http://127.0.0.1:8000/file/graphicalanalysis
- Request: The request has no body
- Response:
  - If a missing data treatment has not been done, since it is recommended to do it before doing any analysis on the variables.
  ```json
  {
      "Error": "424 Failed Dependency", 
      "Message": "It is recommended to do the missing data treatment first."
  }
  ```
  - Success
  ```json
  {
    "histograms": ".\\proyecto_sistemas_inteligentes\\archivos\\histograms\\2023-05-19_19-45-00.png",
     "correlation_matrix": ".\\proyecto_sistemas_inteligentes\\archivos\\ correlation_matrix\\2023-05-19_19-45-01.png"
  }
  ``` 
  ## Critical response
  response if something unexpected happens on the server
  ```json
  {
      "Error": "500 Internal Server Error"
  }
  ```
