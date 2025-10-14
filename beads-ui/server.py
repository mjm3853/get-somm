#!/usr/bin/env python3
"""
Simple HTTP server to serve the Beads UI and provide API endpoints
for querying the Beads SQLite database.
"""

import os
import sqlite3
import json
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

class BeadsAPIHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, db_path=None, **kwargs):
        self.db_path = db_path
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # API endpoints
        if path.startswith('/api/'):
            self.handle_api_request(path, parsed_url.query)
        # Serve static files
        else:
            self.serve_static_file(path)

    def handle_api_request(self, path, query_string):
        """Handle API requests"""
        try:
            if path == '/api/issues':
                self.serve_issues(query_string)
            elif path == '/api/dependencies':
                self.serve_dependencies()
            elif path == '/api/stats':
                self.serve_stats()
            else:
                self.send_error(404, 'API endpoint not found')
        except Exception as e:
            print(f"API Error: {e}")
            self.send_error(500, f'Internal server error: {str(e)}')

    def serve_issues(self, query_string):
        """Serve issues from the database"""
        params = parse_qs(query_string)

        # Build query based on parameters
        query = """
        SELECT id, title, description, design, acceptance_criteria, notes,
               status, priority, issue_type, assignee, estimated_minutes,
               created_at, updated_at, closed_at, external_ref
        FROM issues
        """

        conditions = []
        query_params = []

        # Add filters based on query parameters
        if 'status' in params and params['status'][0]:
            conditions.append('status = ?')
            query_params.append(params['status'][0])

        if 'priority' in params and params['priority'][0]:
            conditions.append('priority = ?')
            query_params.append(int(params['priority'][0]))

        if 'view' in params:
            view_type = params['view'][0]
            if view_type == 'ready':
                # Use the ready_issues view
                query = """
                SELECT id, title, description, design, acceptance_criteria, notes,
                       status, priority, issue_type, assignee, estimated_minutes,
                       created_at, updated_at, closed_at, external_ref
                FROM ready_issues
                """
            elif view_type == 'blocked':
                # Use the blocked_issues view
                query = """
                SELECT id, title, description, design, acceptance_criteria, notes,
                       status, priority, issue_type, assignee, estimated_minutes,
                       created_at, updated_at, closed_at, external_ref, blocked_by_count
                FROM blocked_issues
                """

        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

        query += ' ORDER BY priority ASC, created_at DESC'

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, query_params)
            rows = cursor.fetchall()

            issues = [dict(row) for row in rows]

        self.send_json_response(issues)

    def serve_dependencies(self):
        """Serve dependencies from the database"""
        query = """
        SELECT issue_id, depends_on_id, type, created_at, created_by
        FROM dependencies
        ORDER BY issue_id, depends_on_id
        """

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            dependencies = [dict(row) for row in rows]

        self.send_json_response(dependencies)

    def serve_stats(self):
        """Serve statistics about the issues"""
        queries = {
            'total': 'SELECT COUNT(*) as count FROM issues',
            'by_status': '''
                SELECT status, COUNT(*) as count
                FROM issues
                GROUP BY status
                ORDER BY count DESC
            ''',
            'by_priority': '''
                SELECT priority, COUNT(*) as count
                FROM issues
                GROUP BY priority
                ORDER BY priority ASC
            ''',
            'ready_count': 'SELECT COUNT(*) as count FROM ready_issues',
            'blocked_count': 'SELECT COUNT(*) as count FROM blocked_issues'
        }

        stats = {}

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Total count
            cursor.execute(queries['total'])
            stats['total'] = cursor.fetchone()['count']

            # By status
            cursor.execute(queries['by_status'])
            stats['by_status'] = [dict(row) for row in cursor.fetchall()]

            # By priority
            cursor.execute(queries['by_priority'])
            stats['by_priority'] = [dict(row) for row in cursor.fetchall()]

            # Ready count
            cursor.execute(queries['ready_count'])
            stats['ready'] = cursor.fetchone()['count']

            # Blocked count
            cursor.execute(queries['blocked_count'])
            stats['blocked'] = cursor.fetchone()['count']

        self.send_json_response(stats)

    def serve_static_file(self, path):
        """Serve static files"""
        # Default to index.html for root path
        if path == '/':
            path = '/index.html'

        file_path = Path(__file__).parent / path.lstrip('/')

        if not file_path.exists():
            self.send_error(404, 'File not found')
            return

        # Get MIME type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type is None:
            mime_type = 'application/octet-stream'

        # Serve the file
        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', len(content))
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            print(f"Error serving file {file_path}: {e}")
            self.send_error(500, 'Error reading file')

    def send_json_response(self, data):
        """Send a JSON response"""
        json_data = json.dumps(data, indent=2, default=str)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(json_data))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))

    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"{self.client_address[0]} - {format % args}")

def find_beads_db():
    """Find the Beads database file"""
    # Look for .beads directory in current directory and parents
    current = Path.cwd()

    while current != current.parent:
        beads_dir = current / '.beads'
        if beads_dir.exists():
            # Look for .db files in the directory
            db_files = list(beads_dir.glob('*.db'))
            if db_files:
                return str(db_files[0])
        current = current.parent

    # Fallback to default location
    home_beads = Path.home() / '.beads' / 'default.db'
    if home_beads.exists():
        return str(home_beads)

    return None

def main():
    """Main function to start the server"""
    # Find the Beads database
    db_path = find_beads_db()

    if not db_path:
        print("Error: Could not find Beads database file.")
        print("Make sure you're in a directory with a .beads/ folder or have initialized Beads.")
        return

    print(f"Using Beads database: {db_path}")

    # Verify database exists and has tables
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='issues'")
            if not cursor.fetchone():
                print("Error: Database doesn't appear to contain Beads tables.")
                return
    except Exception as e:
        print(f"Error accessing database: {e}")
        return

    # Start the server
    port = 8080
    server_address = ('localhost', port)

    # Create handler class with database path
    def handler(*args, **kwargs):
        return BeadsAPIHandler(*args, db_path=db_path, **kwargs)

    httpd = HTTPServer(server_address, handler)

    print(f"Beads UI server starting at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()

if __name__ == '__main__':
    main()