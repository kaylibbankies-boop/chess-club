# Quick Start Guide - Flask Chess Club App

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git (optional)

---

## 🚀 Setup (5 minutes)

### Step 1: Navigate to project directory

```bash
cd "e:\NetStock\Chess app"
```

### Step 2: Run setup script

**Windows:**
```bash
run.bat
```

**macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

That's it! The server will start automatically.

---

## ✅ Manual Setup (if scripts don't work)

### 1. Create virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
python app.py
```

---

## 🧪 Test the API

### Health Check
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Chess Club API"
}
```

### Get Leaderboard
```bash
curl http://localhost:5000/api/chess/members/leaderboard
```

### Add a Member
```bash
curl -X POST http://localhost:5000/api/chess/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John",
    "surname": "Doe",
    "email": "john@example.com",
    "birthday": "1990-01-15"
  }'
```

---

## 📊 Load Sample Data

After the server is running (in a new terminal):

```bash
python sample_data.py
```

This creates 5 sample members and 5 sample matches.

---

## 🌐 Access Points

- **API Root**: http://localhost:5000/
- **Health Check**: http://localhost:5000/health
- **Leaderboard**: http://localhost:5000/api/chess/members/leaderboard
- **All Members**: http://localhost:5000/api/chess/members

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `config.py` | Configuration settings |
| `chess_club/models.py` | Database models |
| `chess_club/views.py` | API routes |
| `requirements.txt` | Python dependencies |
| `sample_data.py` | Sample data loader |
| `API_DOCS.md` | Complete API documentation |

---

## 🔧 Configuration

Edit `.env` to customize:

```bash
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///chess_club.db
SECRET_KEY=your-secret-key
```

---

## 🐛 Troubleshooting

### Port 5000 already in use

**Option 1:** Change port in `app.py` line 70:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

**Option 2:** Kill the process using the port
```bash
# Windows
netstat -ano | findstr :5000

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### "ModuleNotFoundError: No module named 'flask'"

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database locked

```bash
# Delete and recreate the database
rm chess_club.db
python app.py  # Recreates it
```

---

## 📈 Next Steps

1. **Load Sample Data**: `python sample_data.py`
2. **Read API Docs**: See `API_DOCS.md`
3. **Code Your Integration**: Use the endpoints in `API_DOCS.md`
4. **Add Authentication**: Consider adding JWT in `chess_club/views.py`
5. **Deploy**: Deploy to production server

---

## 📚 Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **API Docs**: See `API_DOCS.md` in project root

---

## 💡 Tips

- Use Postman or Insomnia for easier API testing
- Check `chess_club.db` in SQLite browser to inspect data
- Enable CORS for frontend integration (already enabled in `app.py`)
- Use `FLASK_ENV=production` for production deployments

---

## 🎯 Common Tasks

### Add 10 members and record matches

```python
python sample_data.py
```

### Check database contents

```python
from app import create_app
from chess_club.models import ChessMember

app = create_app()
with app.app_context():
    members = ChessMember.query.all()
    for m in members:
        print(f"{m.full_name} - Rank {m.current_rank}")
```

### Reset database

```python
from app import create_app, db

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database reset")
```

---

**Ready to go!** 🚀

Need help? Check `API_DOCS.md` or `README.md`
