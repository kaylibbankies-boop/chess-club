# API Documentation

## Overview

The Chess Club Flask API provides comprehensive endpoints for managing chess club members, rankings, and match results.

**Base URL:** `http://localhost:5000/api/chess`

**Response Format:** All responses are JSON with the following structure:

```json
{
  "success": true/false,
  "data": {},
  "error": "error message (if success is false)",
  "message": "success message (optional)"
}
```

---

## Members Endpoints

### Get All Members

```
GET /members
```

**Query Parameters:**
- `page` (optional): Page number for pagination (default: 1)
- `per_page` (optional): Items per page (default: 20)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Alice",
      "surname": "Johnson",
      "full_name": "Alice Johnson",
      "email": "alice@chess.local",
      "birthday": "1990-05-15",
      "age": 35,
      "current_rank": 1,
      "games_played": 15,
      "profile_picture": null,
      "bio": "Chess Master",
      "created_at": "2024-01-01T10:00:00",
      "updated_at": "2024-01-15T14:30:00"
    }
  ],
  "total": 50,
  "pages": 3,
  "current_page": 1
}
```

---

### Get Single Member

```
GET /members/<id>
```

**Response:** Returns a single member object with all details

---

### Create Member

```
POST /members
```

**Request Body:**
```json
{
  "name": "John",
  "surname": "Doe",
  "email": "john@example.com",
  "birthday": "1990-01-15",
  "bio": "Chess enthusiast",
  "profile_picture": "url/to/image.jpg"
}
```

**Required Fields:**
- `name`
- `surname`
- `email` (must be unique)
- `birthday` (format: YYYY-MM-DD)

**Response:** Returns the created member object with ID and rank

---

### Update Member

```
PATCH /members/<id>
PUT /members/<id>
```

**Request Body:** (all fields optional)
```json
{
  "name": "New Name",
  "surname": "New Surname",
  "bio": "Updated bio",
  "profile_picture": "new/image/url"
}
```

**Note:** Cannot change email or birthday

**Response:** Returns updated member object

---

### Delete Member

```
DELETE /members/<id>
```

**Response:**
```json
{
  "success": true,
  "message": "Member deleted successfully"
}
```

---

### Get Leaderboard

```
GET /members/leaderboard
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "full_name": "Alice Johnson",
      "current_rank": 1,
      "games_played": 15,
      "profile_picture": null
    },
    {
      "id": 2,
      "full_name": "Bob Smith",
      "current_rank": 2,
      "games_played": 12,
      "profile_picture": null
    }
  ]
}
```

---

### Get Public Profile

```
GET /members/<id>/public-profile
```

**Response:** Limited member information (no email)

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Alice",
    "surname": "Johnson",
    "full_name": "Alice Johnson",
    "age": 35,
    "current_rank": 1,
    "games_played": 15,
    "profile_picture": null,
    "bio": "Chess Master"
  }
}
```

---

### Search Members

```
GET /members/search?q=query
```

**Query Parameters:**
- `q` (required): Search term (searches name, surname, email)

**Response:** Array of matching members

---

## Matches Endpoints

### Get All Matches

```
GET /matches
```

**Query Parameters:**
- `page` (optional): Page number
- `per_page` (optional): Items per page

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "player1": { member object },
      "player2": { member object },
      "player1_name": "Alice Johnson",
      "player2_name": "Bob Smith",
      "result": "player1_win",
      "match_date": "2024-01-15T14:30:00",
      "notes": "Great endgame",
      "player1_old_rank": 1,
      "player2_old_rank": 2,
      "player1_new_rank": 1,
      "player2_new_rank": 2,
      "rank_changes": {
        "player1": {
          "old_rank": 1,
          "new_rank": 1,
          "change": 0
        },
        "player2": {
          "old_rank": 2,
          "new_rank": 2,
          "change": 0
        }
      }
    }
  ],
  "total": 100,
  "pages": 5,
  "current_page": 1
}
```

---

### Get Recent Matches

```
GET /matches/recent
```

**Response:** Last 10 matches (no pagination)

---

### Record Match

```
POST /matches/record
```

**Request Body:**
```json
{
  "player1_id": 1,
  "player2_id": 2,
  "result": "player1_win",
  "notes": "Optional match notes"
}
```

**Required Fields:**
- `player1_id`
- `player2_id`
- `result` (must be: `player1_win`, `player2_win`, or `draw`)

**Optional Fields:**
- `notes`

**Response:** Returns the created match with updated rankings

---

### Get Single Match

```
GET /matches/<id>
```

**Response:** Returns a single match object

---

## Error Responses

### 400 Bad Request

```json
{
  "success": false,
  "error": "Missing required fields: name, email"
}
```

### 404 Not Found

```json
{
  "success": false,
  "error": "Not found"
}
```

### 500 Internal Server Error

```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## Ranking Algorithm Details

### Rules

1. **Higher-ranked player wins**: No rank change
2. **Draw between non-adjacent ranks**: Lower-ranked player moves up 1 position
3. **Draw between adjacent ranks**: No change
4. **Lower-ranked player wins**:
   - Higher-ranked player moves down 1 position
   - Lower-ranked player moves up by `floor(rank_difference / 2)` positions

### Example Scenarios

**Scenario 1: Higher-ranked wins**
- Player 1 (Rank 1) vs Player 2 (Rank 5)
- Result: Player 1 wins
- Outcome: Ranks unchanged

**Scenario 2: Draw (non-adjacent)**
- Player 1 (Rank 1) vs Player 2 (Rank 5)
- Result: Draw
- Outcome: Player 2 moves to Rank 4, Player 1 stays Rank 1

**Scenario 3: Upper draws lower (adjacent)**
- Player 1 (Rank 2) vs Player 2 (Rank 3)
- Result: Draw
- Outcome: No change

**Scenario 4: Lower-ranked wins**
- Player 1 (Rank 1) vs Player 2 (Rank 5)
- Result: Player 2 wins
- Outcome: Player 1 moves to Rank 2, Player 2 moves up 2 positions to Rank 3

---

## Pagination

Endpoints that return lists support pagination:

```
GET /members?page=2&per_page=10
```

Response includes:
- `total`: Total number of items
- `pages`: Total number of pages
- `current_page`: Current page number

---

## Curl Examples

### Add a member
```bash
curl -X POST http://localhost:5000/api/chess/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John",
    "surname": "Doe",
    "email": "john@example.com",
    "birthday": "1990-01-15",
    "bio": "Chess enthusiast"
  }'
```

### Record a match
```bash
curl -X POST http://localhost:5000/api/chess/matches/record \
  -H "Content-Type: application/json" \
  -d '{
    "player1_id": 1,
    "player2_id": 2,
    "result": "player1_win",
    "notes": "Great game!"
  }'
```

### Get leaderboard
```bash
curl http://localhost:5000/api/chess/members/leaderboard
```

### Search members
```bash
curl http://localhost:5000/api/chess/members/search?q=alice
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider adding rate limiting middleware.

---

## CORS

The API has CORS enabled for all origins. Modify in `config.py` for production:

```python
CORS(app, resources={
    r"/api/*": {"origins": ["https://yourdomain.com"]}
})
```

---

## Authentication

Currently, no authentication is required. For production, implement JWT authentication in the views.

---

**Last Updated:** March 2026  
**API Version:** 1.0.0
