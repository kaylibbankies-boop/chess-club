# Installation & Verification Checklist

## ✅ Pre-Installation

- [ ] Python 3.8+ installed (`python --version`)
- [ ] pip available (`pip --version`)
- [ ] Project folder: `e:\NetStock\Chess app`
- [ ] Internet connection (for pip install)

---

## 🚀 Installation

### Method 1: Automatic (Recommended)

- [ ] Open `run.bat` (Windows) or `run.sh` (macOS/Linux)
- [ ] Double-click `run.bat` or `bash run.sh`
- [ ] Wait for "Server starting" message

### Method 2: Manual

```bash
cd "e:\NetStock\Chess app"
python -m venv venv
```

- [ ] Venv created

```bash
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

- [ ] Venv activated (should see `(venv)` in terminal)

```bash
pip install -r requirements.txt
```

- [ ] Dependencies installed (no errors)

```bash
python app.py
```

- [ ] Server started (should see "Running on http://localhost:5000")

---

## ✨ Post-Installation Tests

### 1. Health Check

```bash
curl http://localhost:5000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "service": "Chess Club API"
}
```

- [ ] Response received
- [ ] Status is "healthy"

### 2. Root Endpoint

```bash
curl http://localhost:5000/
```

**Expected:**
```json
{
  "service": "Chess Club Administration API",
  "version": "1.0.0",
  ...
}
```

- [ ] Response received
- [ ] Service name correct

### 3. Empty Members List

```bash
curl http://localhost:5000/api/chess/members
```

**Expected:**
```json
{
  "success": true,
  "data": [],
  "total": 0,
  ...
}
```

- [ ] Response received
- [ ] Data array is empty (or populated if sample data loaded)

### 4. Empty Leaderboard

```bash
curl http://localhost:5000/api/chess/members/leaderboard
```

**Expected:**
```json
{
  "success": true,
  "data": []
}
```

- [ ] Response received

---

## 📊 Load Sample Data

```bash
# In a new terminal (keep server running)
python sample_data.py
```

**Expected output:**
```
Database reset and recreated
✓ Created 5 members
✓ Created 5 matches

✓ Sample data created successfully!

Members:
  1. Alice Johnson (Rank: 1, Games: 2)
  2. Bob Smith (Rank: 2, Games: 2)
  ...
```

- [ ] Command runs without errors
- [ ] 5 members created
- [ ] 5 matches created

### Test with Sample Data

```bash
curl http://localhost:5000/api/chess/members/leaderboard
```

**Expected:** Array of 5 members

- [ ] 5 members in response
- [ ] Ranked 1-5

---

## 📁 File Structure Verification

From project root, verify these files exist:

- [ ] `app.py` - Main Flask app
- [ ] `config.py` - Configuration
- [ ] `requirements.txt` - Dependencies
- [ ] `.env.example` - Env template
- [ ] `sample_data.py` - Sample data loader
- [ ] `chess_club/models.py` - Database models
- [ ] `chess_club/views.py` - API routes
- [ ] `chess_club/__init__.py` - Module init
- [ ] `chess_club/migrations/` - Migrations folder

---

## 🧪 API Tests

### Create a Member

```bash
curl -X POST http://localhost:5000/api/chess/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "surname": "User",
    "email": "test@example.com",
    "birthday": "2000-01-01"
  }'
```

- [ ] Response status: 201
- [ ] Contains new member ID
- [ ] Rank assigned

### Get Specific Member

```bash
# Replace 1 with actual ID from above
curl http://localhost:5000/api/chess/members/1
```

- [ ] Response status: 200
- [ ] Contains member details

### Search Members

```bash
curl http://localhost:5000/api/chess/members/search?q=alice
```

- [ ] Response status: 200
- [ ] Returns matching members

### Record a Match

```bash
# After creating at least 2 members
curl -X POST http://localhost:5000/api/chess/matches/record \
  -H "Content-Type: application/json" \
  -d '{
    "player1_id": 1,
    "player2_id": 2,
    "result": "player1_win",
    "notes": "Test match"
  }'
```

- [ ] Response status: 201
- [ ] Contains match details
- [ ] Rank changes calculated

---

## 📝 Configuration Verification

Check `.env.example`:

- [ ] Contains FLASK_ENV
- [ ] Contains FLASK_APP
- [ ] Contains DATABASE_URL
- [ ] Contains SECRET_KEY

If needed, create `.env`:

```bash
cp .env.example .env
```

- [ ] `.env` file created
- [ ] `.env` not committed to git (if using git)

---

## 🔧 Advanced Tests

### Database File

Check that `chess_club.db` exists:

```bash
# Should exist after first run
ls chess_club.db  # or dir chess_club.db on Windows
```

- [ ] `chess_club.db` exists in root

### Database Contents

```python
# In Python REPL
from app import create_app, db
from chess_club.models import ChessMember

app = create_app()
with app.app_context():
    members = ChessMember.query.all()
    print(f"Total members: {len(members)}")
```

- [ ] Query executes without errors
- [ ] Shows member count

---

## 🐛 Troubleshooting Checklist

### Port 5000 in Use

If you see "Address already in use":

```bash
# Option 1: Kill existing process
# Windows: netstat -ano | findstr :5000
# macOS/Linux: lsof -i :5000

# Option 2: Use different port
# Edit line 74 in app.py to port 5001
```

- [ ] Port issue resolved

### Dependencies Not Installing

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

- [ ] Dependencies installed successfully

### Database Locked

```bash
rm chess_club.db  # Deletes database
python app.py     # Recreates it
```

- [ ] Database error resolved

---

## ✅ Final Verification

### Complete Workflow

1. Start server:
```bash
python app.py
```
- [ ] Server starts at port 5000

2. Load sample data:
```bash
python sample_data.py
```
- [ ] 5 members created
- [ ] 5 matches created

3. Test leaderboard:
```bash
curl http://localhost:5000/api/chess/members/leaderboard
```
- [ ] Returns 5 members
- [ ] Ranked correctly

4. Record new match:
```bash
curl -X POST http://localhost:5000/api/chess/matches/record \
  -H "Content-Type: application/json" \
  -d '{
    "player1_id": 1,
    "player2_id": 3,
    "result": "player2_win"
  }'
```
- [ ] Match recorded
- [ ] Ranks updated

---

## 📚 Documentation

Verify all docs exist:

- [ ] `README.md` - Main documentation
- [ ] `API_DOCS.md` - API reference
- [ ] `QUICKSTART.md` - Quick start guide
- [ ] `CONVERSION_SUMMARY.md` - What changed

---

## 🎉 You're Ready!

If all checkboxes above are checked:

✅ **Installation complete**
✅ **Server running**
✅ **API working**
✅ **Sample data loaded**
✅ **Ready to develop**

---

## 🚀 Next Steps

1. **Read the docs**: Start with `QUICKSTART.md`
2. **Explore API**: See `API_DOCS.md` for all endpoints
3. **Build frontend**: Use React, Vue, or any JS framework
4. **Add features**: Edit `chess_club/views.py` for new endpoints
5. **Deploy**: Use Gunicorn + Nginx for production

---

## 📞 Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` |
| `Address already in use` | Kill process on port 5000 or use `--port 5001` |
| `Database locked` | Delete `chess_club.db` and restart |
| `CORS errors in browser` | Already enabled, check CORS plugin disabled |
| `No database file created` | Normal - created on first run |

---

**Everything working?** You're all set! 🚀♟️

