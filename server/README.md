# Weighly Backend API Documentation

## API Version: 0.1

### GET /{event}/summary

#### Description
This endpoint retrieves both the event details, and [totals](#get-event-totals).

#### Request
- **Method**: GET
- **Endpoint**: `/{event}/summary`
- **Example**: `/1/summary`

#### Response
- **Status Code**: 200 OK
- **Body**:
  ```json
  { "event": 
    {
    "event_id": 1,
    "name":"Troop 30 Food Drive",
    "custom_url":null 
    },
    "totals": 
    [ 
      {
        "name":"Nico",
        "weight":8.0,
        "type":"scout"
      },
      {
        "name":"Ben",
        "weight":3.0,
        "type":"cub"
      },
      {
        "name":"Ben",
        "weight":3.0,
        "type":"scout"
      }
    ]
  }
  ```

#### Error Responses
- **404 Not Found**: If there are no weight entries.
- **500 Internal Server Error**: If there is a server issue.

### GET /{event}/totals

#### Description
This endpoint retrieves, adds and sorts a list of peoples total weights. Sorted by weight, largest first.

#### Request
- **Method**: GET
- **Endpoint**: `/{event}/totals`
- **Example**: `/1/totals`

#### Response
- **Status Code**: 200 OK
- **Body**:
  ```json
  [ 
    {
      "name":"Nico",
      "weight":8.0,
      "type":"scout"
    },
    {
      "name":"Ben",
      "weight":3.0,
      "type":"cub"
    },
    {
      "name":"Ben",
      "weight":3.0,
      "type":"scout"
    }
  ]
  ```

#### Error Responses
- **404 Not Found**: If there are no weight entries.
- **500 Internal Server Error**: If there is a server issue.

#### Error Responses
- **404 Not Found**: If there are no weight entries.
- **500 Internal Server Error**: If there is a server issue.

### GET /{event}/entries

#### Description
This endpoint retrieves a list of weight entries.

#### Request
- **Method**: GET
- **Endpoint**: `/{event}/entries`
- **Example**: `/1/entries`

#### Response
- **Status Code**: 200 OK
- **Body**:
```json
[
  {
    "id": 1,
    "name":"Nico",
    "weight":5.0,
    "type":"scout",
    "time":"2024-11-23 13:56:18.506589"
    },
    {
      "id":2,
      "name":"Nico",
      "weight":3.0,
      "type":"scout",
      "time":"2024-11-23 13:56:18.506589"
    },
    {
      "id":3,
      "name":"Ben",
      "weight":3.0,
      "type":"cub",
      "time":"2024-11-23 13:56:18.506589"
    },
    {
      "id":4,
      "name":"Ben",
      "weight":3.0,
      "type":"scout",
      "time":"2024-11-23 13:56:18.506589"
    }
  ]
```

#### Error Responses
- **404 Not Found**: If there are no weight entries.
- **500 Internal Server Error**: If there is a server issue.

### GET /{event}/total

#### Description
This endpoint returns the total of all weights for an event

#### Request
- **Method**: GET
- **Endpoint**: `/{event}/total`
- **Example**: `/1/total`

#### Response
- **Status Code**: 200 OK
- **Body**:
```json
14.0
```

#### Error Responses
- **500 Internal Server Error**: If there is a server issue.

### POST /{event}/add_weight

#### Description
This endpoint adds weights to the database.

#### Request
- **Method**: POST
- **Endpoint**: `/{event}/add_weight`
- **Example**: `/1/add_weight`

#### Request
- **Status Code**: 200 OK
- **Body**:
```json
{
  "id": "1",
  "name": "Nico",
  "weight": 16.5,
  "type": "scout",
  "time": "2024-11-23 13:56:18.506589"
}
```

#### Error Responses
- **404 Not Found**: If there are no weight entries.
- **500 Internal Server Error**: If there is a server issue.