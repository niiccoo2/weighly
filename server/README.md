# Weighly Backend API Documentation

## API Version: 0.1

### GET /weights/{group}

#### Description
This endpoint retrieves a list of weight entries.

#### Request
- **Method**: GET
- **Endpoint**: `/weights/{group}`
- **Example**: `/weights/troop30`

#### Response
- **Status Code**: 200 OK
- **Body**:
  ```json
  [
    {
      "id": 1,
      "name": "Nico",
      "weight": 67
    },
    {
      "id": 2,
      "name": "Alex",
      "weight": 75
    }
  ]
  ```

#### Error Responses
- **404 Not Found**: If there are no weight entries.
- **500 Internal Server Error**: If there is a server issue.