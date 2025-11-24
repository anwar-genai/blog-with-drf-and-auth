# 🚀 How to Run

## Run Both Servers:

**Terminal 1 - Django:**
```bash
uv run daphne -b 127.0.0.1 -p 8000 config.asgi:application
```

**Terminal 2 - Next.js:**
```bash
cd frontend
npm run dev
```

Visit: **http://localhost:3000**

---

## Features:
- ✅ **Register** - http://localhost:3000/register
- ✅ **Login** - http://localhost:3000/login
- ✅ **Create Posts** - Compose box on home
- ✅ **Like Posts** - Click heart icon
- ✅ **Comment** - Click post to view details & comment
- ✅ **Logout** - Sidebar button
 now working on authentications
---

## Quick Test:
1. Visit http://localhost:3000/register
2. Create account (username, password)
3. Auto-logged in after registration
4. Create a post using compose box
5. Like posts by clicking ❤️
6. Click post to view & add comments

Done!