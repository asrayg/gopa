"""Graphics, events, and timer stubs for Gopa."""

import time
import threading
from typing import List, Dict, Callable, Any, Optional
from datetime import datetime
import re


class Scheduler:
    """Scheduler for timers, jobs, and cron tasks."""

    def __init__(self, virtual_time: bool = False):
        self.virtual_time = virtual_time
        self.current_time = 0.0
        self.jobs: Dict[str, dict] = {}
        self.after_tasks: List[dict] = []
        self.every_tasks: List[dict] = []
        self.cron_tasks: List[dict] = []
        self.running = False
        self.thread: Optional[threading.Thread] = None

    def wait(self, seconds: float):
        """Wait for specified seconds."""
        if self.virtual_time:
            self.current_time += seconds
        else:
            time.sleep(seconds)

    def after(self, seconds: float, body: List, interpreter):
        """Schedule a task to run after seconds."""
        if self.virtual_time:
            run_time = self.current_time + seconds
        else:
            run_time = time.time() + seconds

        self.after_tasks.append({
            'time': run_time,
            'body': body,
            'interpreter': interpreter
        })

    def every(self, seconds: float, body: List, interpreter):
        """Schedule a task to run every seconds."""
        if self.virtual_time:
            last_run = self.current_time
        else:
            last_run = time.time()

        self.every_tasks.append({
            'interval': seconds,
            'body': body,
            'interpreter': interpreter,
            'last_run': last_run
        })

    def job(self, name: str, seconds: float, body: List, interpreter):
        """Register a named job."""
        if self.virtual_time:
            last_run = self.current_time
        else:
            last_run = time.time()

        self.jobs[name] = {
            'interval': seconds,
            'body': body,
            'interpreter': interpreter,
            'last_run': last_run
        }

    def stop_job(self, name: str):
        """Stop a named job."""
        if name in self.jobs:
            del self.jobs[name]

    def cron(self, schedule: str, body: List, interpreter):
        """Register a cron task."""
        cron_fields = self.parse_cron(schedule)
        self.cron_tasks.append({
            'schedule': schedule,
            'cron_fields': cron_fields,
            'body': body,
            'interpreter': interpreter
        })

    def parse_cron(self, schedule: str) -> Dict[str, Any]:
        """Parse cron schedule string."""
        friendly_patterns = {
            r'every minute': {'minute': '*', 'hour': '*', 'day': '*', 'month': '*', 'dow': '*'},
            r'every hour': {'minute': '0', 'hour': '*', 'day': '*', 'month': '*', 'dow': '*'},
            r'every day at (\d{1,2}):(\d{2})': lambda m: {
                'minute': m.group(2),
                'hour': m.group(1),
                'day': '*',
                'month': '*',
                'dow': '*'
            },
            r'every (monday|tuesday|wednesday|thursday|friday|saturday|sunday) at (\d{1,2}):(\d{2})': lambda m: {
                'minute': m.group(3),
                'hour': m.group(2),
                'day': '*',
                'month': '*',
                'dow': str(['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].index(m.group(1).lower()))
            },
        }

        for pattern, result in friendly_patterns.items():
            match = re.match(pattern, schedule.lower())
            if match:
                if callable(result):
                    return result(match)
                return result

        parts = schedule.split()
        if len(parts) == 5:
            return {
                'minute': parts[0],
                'hour': parts[1],
                'day': parts[2],
                'month': parts[3],
                'dow': parts[4]
            }

        raise ValueError(f"Invalid cron schedule: {schedule}")

    def step(self, dt: float = 0.1):
        """Step virtual time forward."""
        if not self.virtual_time:
            return

        self.current_time += dt

        for task in self.after_tasks[:]:
            if self.current_time >= task['time']:
                try:
                    for stmt in task['body']:
                        task['interpreter'].execute(stmt)
                except Exception:
                    pass
                self.after_tasks.remove(task)

        for task in self.every_tasks:
            if self.current_time >= task['last_run'] + task['interval']:
                try:
                    for stmt in task['body']:
                        task['interpreter'].execute(stmt)
                except Exception:
                    pass
                task['last_run'] = self.current_time

        for name, job in list(self.jobs.items()):
            if self.current_time >= job['last_run'] + job['interval']:
                try:
                    for stmt in job['body']:
                        job['interpreter'].execute(stmt)
                except Exception:
                    pass
                job['last_run'] = self.current_time

        now = datetime.fromtimestamp(self.current_time)
        for task in self.cron_tasks:
            fields = task['cron_fields']
            if self.matches_cron(now, fields):
                try:
                    for stmt in task['body']:
                        task['interpreter'].execute(stmt)
                except Exception:
                    pass

    def matches_cron(self, dt: datetime, fields: Dict[str, str]) -> bool:
        """Check if datetime matches cron fields."""
        def matches(value: int, field: str) -> bool:
            if field == '*':
                return True
            try:
                return int(field) == value
            except ValueError:
                return False

        return (matches(dt.minute, fields.get('minute', '*')) and
                matches(dt.hour, fields.get('hour', '*')) and
                matches(dt.day, fields.get('day', '*')) and
                matches(dt.month, fields.get('month', '*')) and
                matches(dt.weekday(), fields.get('dow', '*')))

    def start(self):
        """Start scheduler in background thread."""
        if self.running:
            return

        self.running = True

        def run():
            while self.running:
                if not self.virtual_time:
                    now = time.time()

                    for task in self.after_tasks[:]:
                        if now >= task['time']:
                            try:
                                for stmt in task['body']:
                                    task['interpreter'].execute(stmt)
                            except Exception:
                                pass
                            self.after_tasks.remove(task)

                    for task in self.every_tasks:
                        if now >= task['last_run'] + task['interval']:
                            try:
                                for stmt in task['body']:
                                    task['interpreter'].execute(stmt)
                            except Exception:
                                pass
                            task['last_run'] = now

                    for name, job in list(self.jobs.items()):
                        if now >= job['last_run'] + job['interval']:
                            try:
                                for stmt in job['body']:
                                    job['interpreter'].execute(stmt)
                            except Exception:
                                pass
                            job['last_run'] = now

                    dt = datetime.now()
                    for task in self.cron_tasks:
                        fields = task['cron_fields']
                        if self.matches_cron(dt, fields):
                            try:
                                for stmt in task['body']:
                                    task['interpreter'].execute(stmt)
                            except Exception:
                                pass

                time.sleep(0.1)

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop scheduler."""
        self.running = False


class GraphicsStub:
    """Stub implementation for graphics operations."""

    def __init__(self, output_stream=None):
        self.output_stream = output_stream
        self.canvases: Dict[Any, dict] = {}
        self.mouse_handlers: List[dict] = []

    def create_canvas(self, width: int, height: int) -> dict:
        """Create a canvas."""
        canvas = {
            'type': 'canvas',
            'width': width,
            'height': height,
            'id': id(canvas)
        }
        self.canvases[canvas['id']] = canvas
        print(f"[canvas] created {width}x{height}", file=self.output_stream)
        return canvas

    def draw_circle(self, x: int, y: int, size: int, color: str):
        """Draw a circle."""
        print(f"[canvas] circle x={x} y={y} size={size} color={color}", file=self.output_stream)

    def draw_rectangle(self, x1: int, y1: int, x2: int, y2: int, color: str):
        """Draw a rectangle."""
        print(f"[canvas] rectangle from {x1},{y1} to {x2},{y2} color={color}", file=self.output_stream)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: str):
        """Draw a line."""
        print(f"[canvas] line from {x1},{y1} to {x2},{y2} color={color}", file=self.output_stream)

    def draw_text(self, text: str, x: int, y: int, size: int, color: str):
        """Draw text."""
        print(f"[canvas] text '{text}' at {x},{y} size={size} color={color}", file=self.output_stream)

    def register_mouse_click(self, canvas: Any, body: List, interpreter):
        """Register a mouse click handler."""
        self.mouse_handlers.append({
            'canvas': canvas,
            'body': body,
            'interpreter': interpreter
        })
        print(f"[event] registered mouse click handler", file=self.output_stream)

    def simulate_click(self, x: int, y: int):
        """Simulate a mouse click."""
        for handler in self.mouse_handlers:
            handler['interpreter'].runtime.set('mouse', {'x': x, 'y': y})
            try:
                for stmt in handler['body']:
                    handler['interpreter'].execute(stmt)
            except Exception:
                pass

    def start_server(self, port: int, handlers: List, interpreter):
        """Start HTTP server."""
        try:
            from http.server import HTTPServer, BaseHTTPRequestHandler
            import json

            class Handler(BaseHTTPRequestHandler):
                def do_GET(self):
                    self.handle_request('GET')

                def do_POST(self):
                    self.handle_request('POST')

                def handle_request(self, method):
                    path = self.path.split('?')[0]
                    query = {}
                    if '?' in self.path:
                        query_str = self.path.split('?')[1]
                        for pair in query_str.split('&'):
                            if '=' in pair:
                                k, v = pair.split('=', 1)
                                query[k] = v

                    for h_method, h_path, h_body in handlers:
                        if h_method == method and h_path == path:
                            interpreter.runtime.set('request', {
                                'path': path,
                                'query': query,
                                'headers': dict(self.headers),
                                'body': {}
                            })

                            result = None
                            try:
                                for stmt in h_body:
                                    interpreter.execute(stmt)
                            except ReturnSignal as ret:
                                result = ret.value

                            if result is not None:
                                if isinstance(result, (dict, list)):
                                    response = json.dumps(result)
                                    self.send_response(200)
                                    self.send_header('Content-Type', 'application/json')
                                    self.end_headers()
                                    self.wfile.write(response.encode())
                                else:
                                    self.send_response(200)
                                    self.send_header('Content-Type', 'text/plain')
                                    self.end_headers()
                                    self.wfile.write(str(result).encode())
                            else:
                                self.send_response(200)
                                self.end_headers()
                            return

                    self.send_response(404)
                    self.end_headers()

                def log_message(self, format, *args):
                    pass

            server = HTTPServer(('localhost', port), Handler)
            print(f"[server] started on port {port}", file=self.output_stream)
            server.serve_forever()
        except Exception as e:
            print(f"[server] error: {e}", file=self.output_stream)

