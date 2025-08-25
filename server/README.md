# Weighly Backend API Documentation

## API Version: 0.1

### GET /{event}/summary

#### Description
This endpoint retrieves a list of weight entries.

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