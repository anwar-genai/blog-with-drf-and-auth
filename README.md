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

### Rich Text & Media
- CKEditor enabled for articles. Uploads saved under `media/uploads/`.
- Configure `MEDIA_URL` and `MEDIA_ROOT` (already set) for local dev.

### Polls
- Create via `New Poll`, add up to 4 options (extendable), set `max_choices`.
- Votes update live; results bars show counts/percent.

### Changelog
- [UI] Avatars in navbar/comments; sticky header with active nav; search + type filters on blog index.


