# Vote API

Base URL: https://good-team.herokuapp.com/

[TOC]



**/voters**
----

https://good-team.herokuapp.com/voters

### Show all voters

Returns a JSON data array of all existing voter

* **URL**

  /voters

* **Method:** `GET` 

* **Sample Response:**

  * **Code:** 200 <br />
    **Sample Content:**

    ```json
     [
       { 
       		"_id" : "012345678901234567890123",
      		"name" : "sample",
      		"email" : "sample@gmail.com",
      		"elections": ["123456712345671234567111", "111122223333444455551111"]
       },
       { 
       		"_id" : "011.....",
      		"name" : "...",
      		"email" : "..",
      		"elections": []
       },
       .....
     ]
    ```



### Show voter

Returns JSON data about a single voter

* **URL**

   /voters/<voter_id>

* **Method:** `GET` 

  `GET` | `POST` | `DELETE` | `PUT`

* **URL Params**

  **Required:**

  `voter_id=[string]`

* **Sample Response:**

  * **Code:** 200 <br />
    **Content:**

    ```json
     { "_id" : "012345678901234567890123",
      "name" : "sample",
      "email" : "sample@gmail.com",
      "elections": ["123456712345671234567111", "111122223333444455551111"]}
    ```



### Create/update voter's info

Updates a voter's info  based on a given name and email. If there's no existing voter with the same name and email, a new voter is created.

Returns JSON data of the newly updated/created voter.

* **URL**

  /voters/<name>/ <email>

* **Method:** `POST` 

* **URL Params**

  **Required:**

  `name=[string]`

  `email=[string]`

  

* **Sample Response:**

  * **Code:** 200 <br />
    **Content:**

    ```json
     { "_id" : "012345678901234567890123",
      "name" : "sample",
      "email" : "sample@gmail.com",
      "elections": ["123456712345671234567111", "111122223333444455551111"]}
    ```



### Delete voter

Deletes a specified voter and returns JSON success data if deleted successfully

* **URL**

   /voters/<voter_id>

* **Method:** `DELETE` 

* **URL Params**

  **Required:**

  `voter_id=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**

    ```json
     { "success" : true}
    ```

### 

**/elections**
----

https://good-team.herokuapp.com/elections

### Show all elections

Returns a JSON data array of all existing elections

* **URL**

  /elections

* **Method:** `GET` 

* **Sample Response:**

  * **Code:** 200 <br />
    **Sample Content:**

    ```json
     [
       { 
       		"_id" : "012345678901234567890123",
      		"details" : "sample",
      		"choices" : {
            "a" : 1,
            "b" : 2,
            "c" : 0
          }
       },
       { 
       		"_id" : "0123456789321asdfasdfasd",
      		"details" : "snacks",
      		"choices" : {
            "pizza" : 0,
            "apples" : 3,
          }
       },
       .....
     ]
    ```



### Show election

Returns JSON data about a single election

* **URL**

   /elections/<election_id>

* **Method:** `GET` 

* **URL Params**

  **Required:**

  `election_id=[string]`

* **Sample Response:**

  * **Code:** 200 <br />
    **Content:**

    ```json
      { 
       		"_id" : "012345678901234567890123",
      		"details" : "sample",
      		"choices" : {
            "a" : 1,
            "b" : 2,
            "c" : 0
          }
       }
    ```



### Create new election

Creates a new election based on given details and choices. 

Returns JSON data of the newly created election.

* **URL**

  /election/<election_id>/<name>/ <email>

* **Method:** `POST` 

* **URL Params**

  **Required:**

  `details=[string]`

  `choices=[JSON array]`

  For example, choices can be:

  `{"a":0, "b":0, "c":0, "d":0}`

* **Sample Response:**

  * **Code:** 200 <br />
    **Content:**

    ```json
     { 
       		"_id" : "012345678901234567890123",
      		"details" : "newelection",
      		"choices" : {
            "a" : 0,
            "b" : 0,
            "c" : 0,
            "d" : 0
          }
       }
    ```



### Update existing election

Updates an election's details and choices based on a given election id.

Returns JSON data of the newly updated election.

* **URL**

  /election/<election_id>/<name>/ <email>

* **Method:** `POST` 

* **URL Params**

  **Required:**

  `election_id=[string]`

  `details=[string]`

  `choices=[JSON array]`

  For example, choices can be:

  `{"a":0, "b":0, "c":0, "d":0}`

* **Sample Response:**

  * **Code:** 200 <br />
    **Content:**

    ```json
     { 
       		"_id" : "012345678901234567890123",
      		"details" : "updated_election",
      		"choices" : {
            "a" : 0,
            "b" : 0,
            "c" : 0,
            "d" : 0
          }
       }
    ```



### Delete election

Deletes a specified electionand returns JSON success data if deleted successfully

* **URL**

   /election/<election_id>

* **Method:** `DELETE` 

* **URL Params**

  **Required:**

  `election_id=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**

    ```json
     { "success" : true}
    ```

### 

**/eligible**
----

https://good-team.herokuapp.com/eligible

### Show all elections a voter is eligible for

Returns a data array of all elections a voter is eligible for

* **URL**

  /eligible/<voter_id>

* **Method:** `GET` 

* **URL Params**

  **Required:**

  `voter_id=[string]`

* **Sample Response:**

  * **Code:** 200 <br />
    **Sample Content:**

    ```json
    [
        "60234cc32a45ae3eec0a720b",
        "60234cc32a45ae3eec0a720a"
    ]
    ```



### Check voter eligibility

Returns JSON success about voter's eligibility based on given voter id and election id

* **URL**

   /eligible/<voter_id>/<election_id>

* **Method:** `GET` 

* **URL Params**

  **Required:**

  `voter_id=[string]`

  `election_id=[string]`

* **Sample Response:**

  * **Code:** 200 <br />
    **Content:**

    ```json
     { "eligible" : true}
    ```



### Add voter to an election

Updates the voter's elections array with the given election id.

Returns JSON success data if updated successfully.

* **URL**

   /eligible/<voter_id>/<election_id>

* **Method:** `POST` 

* **URL Params**

  **Required:**

  `voter_id=[string]`

  `election_id=[string]`

  

* **Sample Response:**

  * **Code:** 200 <br />
    **Content:**

    ```json
     { "success" : true}
    ```

### 

**/vote**
----

https://good-team.herokuapp.com/vote

### Record a voter's vote in a given election

Records a specified voter's vote in a given election.

Returns JSON success data if voted successfully.

* **URL**

  /vote/:voter_id/:election_id/:choice

* **Method:** `POST`

* **URL Params**

  **Required:**

  `voter_id=[string]`

  `election_id=[string]`

  `choice=[string]`

* **Sample Response:**

  * **Code:** 200 <br />
    **Sample Content:**

    ```json
     { "success" : true}
    ```





**/results**
----

https://good-team.herokuapp.com/results

### Show an election's results

Returns a given election's results

* **URL**

  /results/<election_id>

* **Method:** `GET`

* **URL Params**

  **Required:**

  `voter_id=[string]`

  `election_id=[string]`

  `choice=[string]`

* **Sample Response:**

  * **Code:** 200 <br />
    **Sample Content:**

    ```json
    {
        "a": 2,
        "b": 0,
        "c": 0
    }
    ```

    

**/ballots**
----

https://good-team.herokuapp.com/ballots

* * ?????

