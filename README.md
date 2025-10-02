## Django Blog Project

Minimal social blogging app with accounts, posts/articles, polls, follows, chat, and DRF API.

### Features
- Accounts: signup/login/logout, profile with avatar, dashboard
- Blog: articles (rich text), short posts, polls with votes and results
- Polls: scheduling (start/end), multi-select with max choices, AJAX voting
- UI: Bootstrap 5, sticky navbar, type badges, avatars in navbar/comments
- API: DRF ready with auth and pagination

### Quickstart
1) Install deps and migrate
```
pip install -r requirements.txt  # or use uv/pip
python manage.py makemigrations && python manage.py migrate
```
2) Run server
```
python manage.py runserver
```
3) Optional assets
```
python manage.py collectstatic --noinput
```

### WebSockets (Channels) setup
- Install packages with uv:
```
uv add channels daphne
```
- Verify installation:
```
uv pip show channels
uv run python -c "import channels, importlib.metadata as m; print(m.version('channels'))"
uv run daphne --version
```
- Run the ASGI server locally:
```
uv run daphne -b 127.0.0.1 -p 8000 config.asgi:application
```

### Rich Text & Media
- CKEditor enabled for articles. Uploads saved under `media/uploads/`.
- Configure `MEDIA_URL` and `MEDIA_ROOT` (already set) for local dev.

### Polls
- Create via `New Poll`, add up to 4 options (extendable), set `max_choices`.
- Votes update live; results bars show counts/percent.

### Changelog
- [Notifications] Black bell icon with badge using Bootstrap translate-middle (perfect positioning); dropdown shows recent notifications with "username followed you"; unread items with subtle blue background; mark-all-read at bottom; full list at /notifications/; WebSocket toasts via Channels.
- [Follows] Following/Explore feeds; People directory; follow/unfollow; follower/following counts on profile; realtime follow notifications.
- [UI] Avatars in navbar/comments; sticky header; active nav for all links; Bootstrap toasts for messages; blog search with debounce and type filters; poll option preview in lists; card/badge polish.


