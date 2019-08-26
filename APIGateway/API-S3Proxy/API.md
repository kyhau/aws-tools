# DataService

Data Service at [todo.example.com](https://todo.example.com).

Version: v1

Scheme: https

## Paths

### DELETE /item {#DELETE--item}

Delete a file from the datastore.

Query Params:
  
  - key [string]: File name with full destination path.

Responses:
    
  - 200: Successful operation.

    [Empty](#Empty)
    
  - 400: Invalid request.
    
  - 500: Internal server error.

### GET /item {#GET--item}

Retrieve a file from the datastore.

Query Params:
  
  - key [string]: File name with full destination path.

Responses:
    
  - 200: Successful operation.

    [Empty](#Empty)      
    
  - 400: Invalid request.
    
  - 500: Internal server error.


### HEAD /item {#HEAD--item}

Test if a file exists in the datastore.

Query Params:
  
  - key [string]: File name with full destination path.

Responses:
    
  - 200: Successful operation.

    [Empty](#Empty)

  - 400: Invalid request.
          
  - 500: Internal server error.


### PUT /item {#PUT--item}

Add a file to the datastore.

Query Params:
  
  - key [string]: File name with full destination path.
  

Responses:
    
  - 200: Successful operation.
      
    [Empty](#Empty)


  - 400: Invalid request.
          
  - 500: Internal server error.
      

## Definitions
  
### Empty{#Empty}
