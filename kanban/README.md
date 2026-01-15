# Minimal Kanban Board

A simple kanban board with optional backend for persistent storage.

## Features

- 4 columns: Backlog, To Do, Blocked, Done
- Drag and drop cards between columns
- Drag to reorder priority within columns
- Mobile touch support
- Cards with title, description, and context fields
- Dark theme

## Storage Options

### Browser Only (localStorage)
Just open `index.html` in a browser. Data stays in your browser.

```bash
python3 -m http.server 8000
# Open http://localhost:8000
```

### With Backend (JSON file persistence)
Use the Python server for persistent storage that syncs across devices.

```bash
python3 server.py
# Open http://localhost:8744
```

Data is stored in `data/cards.json`.

### Docker
```bash
docker-compose up -d
# Open http://localhost:8744
```

Data persists in a Docker volume.

## API Endpoints

- `GET /api/cards` - Get all cards
- `PUT /api/cards` - Bulk update all cards
- `POST /api/cards` - Add a card
- `PUT /api/cards/:id` - Update a card
- `DELETE /api/cards/:id` - Delete a card
- `GET /api/health` - Health check

## Why?

Sometimes you just want a kanban board without signing up for anything, without complexity. This is that.

## License

MIT - do whatever you want with it.

---

Built by [Zephyr](https://github.com/Zephyr210287)
