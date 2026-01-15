#!/usr/bin/env python3
"""
Kanban Board Backend Server
Serves static files and provides REST API for persistent card storage.
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
import threading

DATA_FILE = os.environ.get('KANBAN_DATA_FILE', 'data/cards.json')
PORT = int(os.environ.get('KANBAN_PORT', 8744))

# Thread lock for file operations
file_lock = threading.Lock()


def ensure_data_dir():
    """Ensure data directory exists."""
    data_dir = os.path.dirname(DATA_FILE)
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir)


def load_cards():
    """Load cards from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []


def save_cards(cards):
    """Save cards to JSON file."""
    ensure_data_dir()
    with file_lock:
        with open(DATA_FILE, 'w') as f:
            json.dump(cards, f, indent=2)


class KanbanHandler(SimpleHTTPRequestHandler):
    """HTTP handler for kanban board with REST API."""

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == '/api/cards':
            self.send_json_response(load_cards())
        elif parsed.path == '/api/health':
            self.send_json_response({'status': 'ok'})
        else:
            # Serve static files
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == '/api/cards':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            card = json.loads(body)

            cards = load_cards()
            cards.append(card)
            save_cards(cards)

            self.send_json_response(card, 201)
        else:
            self.send_error(404)

    def do_PUT(self):
        parsed = urlparse(self.path)

        if parsed.path == '/api/cards':
            # Bulk update - replace all cards
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            cards = json.loads(body)
            save_cards(cards)
            self.send_json_response({'status': 'saved', 'count': len(cards)})
        elif parsed.path.startswith('/api/cards/'):
            # Update single card
            card_id = parsed.path.split('/')[-1]
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            updated_card = json.loads(body)

            cards = load_cards()
            for i, card in enumerate(cards):
                if card.get('id') == card_id:
                    cards[i] = updated_card
                    break
            save_cards(cards)

            self.send_json_response(updated_card)
        else:
            self.send_error(404)

    def do_DELETE(self):
        parsed = urlparse(self.path)

        if parsed.path.startswith('/api/cards/'):
            card_id = parsed.path.split('/')[-1]

            cards = load_cards()
            cards = [c for c in cards if c.get('id') != card_id]
            save_cards(cards)

            self.send_json_response({'status': 'deleted'})
        else:
            self.send_error(404)

    def send_json_response(self, data, status=200):
        """Send JSON response with CORS headers."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        """Suppress default logging for cleaner output."""
        pass


def main():
    ensure_data_dir()
    server = HTTPServer(('0.0.0.0', PORT), KanbanHandler)
    print(f'Kanban server running on http://0.0.0.0:{PORT}')
    print(f'Data file: {DATA_FILE}')
    server.serve_forever()


if __name__ == '__main__':
    main()
