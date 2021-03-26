# API Documentaion

Base URL: https://good-team.herokuapp.com/

[/auth](#auth)
* [Register voter](#register-voter) (`POST /register`)
* [Login](#login): (`POST /login`)

[/ballots](#ballots)
* [Record a ballot](#record-a-ballot): (`POST /ballots`) `🔒 voting machines`

[/voters](#voters)
* [Add election to voter](#add-election-to-voter): (`POST /voters/elections`)
* [Eligible elections for you](#eligible-elections-for-you): (`GET /voters/elections`)
* [Elegible elections for any voter](#elegible-elections-for-any-voter): (`GET /voters/<voter_id>/elections`) `🔒 voting machines`

[/elections](#elections)
* [Election details](#election-details): `GET /elections/<election_id>`
* [Create election](#create-election): `POST /elections`
* [Elections you created](#elections-you-created): `GET /elections/created`


**Auth**
----

### Register voter

Creates a new voter and returns their voter_id

* **URL**: `POST /register`
* **Sample Request:**  <br />
```json
{ 
    "name" : "john",
    "email" : "email@example.com",
    "password" : "12345" 
}
```
* **Sample Response:**  <br />
```json
{
    "_id" : "605d135f7d13e0855a7935e5",
    "success" : "true",
    "error" : "" 
}
```

### Login

Returns a temporary token for accessing other API routes

* **URL**: `POST /login`
* **Sample Request:**  <br />
```json
{ 
    "email" : "email@example.com",
    "password" : "12345"
}
```
* **Sample Response:**  <br />
```json
{ 
    "_id" : "605d135f7d13e0855a7935e5",
    "success" : "true",
    "error": "",
    "token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." 
}
```
  
**Ballots**
----

### Record a ballot

Creates a new ballot for a voter in an election

* **URL**: `POST /ballots`
* **Headers**: `voter-token: YOUR-TOKEN`
* **Sample Request:**  <br />
```json
{ 
    "voter_id" : "605d135f7d13e0855a7935e5",
    "election_id" : "605d135f7r43e0855a7935e2" 
}
  ```
* **Sample Response:**  <br />
```json
{
    "success" : "true",
    "error": "" 
}
```

**Voters**
----

### Add election to voter

Adds an election to the list of eligible elections for a voter

* **URL**: `POST /voters/elections`
* **Headers**: `voter-token: YOUR-TOKEN`
* **Sample Request:**  <br />
```json
{ 
    "email" : "example@email.com",
    "election_id" : "605d135f7r43e0855a7935e2"
}
  ```
* **Sample Response:**  <br />
```json
{ 
    "success" : "true",
    "error": "" 
}
  ```
  
### Eligible elections for you

Returns elections you are elegible for using voter_id from the voter-token

* **URL**: `GET /voters/elections`
* **Headers**: `voter-token: YOUR-TOKEN`
* **Sample Response:**  <br />
```json
{ 
    "votable": ["605d135f7r43e0855a7935e2"],
    "non_votable": ["605d13487d13e0855a7935e4"],
    "success": true,
    "error": "" 
}
```
### Elegible elections for any voter

Returns elections you are elegible for using voter_id from the URL

* **URL**: `GET /voters/<voter_id>/elections`
* **Headers**: `voter-token: YOUR-TOKEN`
* **Sample Response:**  <br />
```json
{ 
    "votable": ["605d135f7r43e0855a7935e2"],
    "non_votable": ["605d13487d13e0855a7935e4"],
    "success": true,
    "error": "" 
}
```
  
**Elections**
----

### Election details

Returns an object with election details

* **URL**: `POST /elections/<election_id>`
* **Headers**: `voter-token: YOUR-TOKEN`
* **Sample Response:**  <br />
```json
{ 
    "election": 
    {
        "_id": "605d135f7d13e0855a7935e5",
        "choices": [ { "count": 0, "option": "a" }, { "count": 0, "option": "b" } ],
        "creator": "605d11cf08f1fe475d9de2a0",
        "details": "(Live) Election 1",
        "end": 1648246994.0,
        "start": 1616711000.0 
    },
    "error": "",
    "success": true 
}
```

### Create election

Creates a new election with specified parameters

* **URL**: `POST /elections`
* **Headers**: `voter-token: YOUR-TOKEN`
* **Sample Request:**  <br />
```json
{
    "details":"(Live) Election 1", 
    "choices":["a", "b"], 
    "start": 1616711000.0, 
    "end": 1648246994.0
}
  ```
* **Sample Response:**  <br />
```json
{ 
    "success" : "true",
    "error": "" 
}
  ```
  
### Elections you created

Returns elections you created as two lists: currently ongoing (live) and past (expired)

* **URL**: `GET /elections/created`
* **Headers**: `voter-token: YOUR-TOKEN`
* **Sample Response:**  <br />
```json
{
    "expired": [ "605d0e2b2ed58befa97f7036" ],
    "live": [ "605d0dfec14ef63b60411f92" ],
    "success": true,
    "error": ""
}
```
