"""Permission sandbox system for Gopa."""

from typing import Set


class Permissions:
    """Manages permissions for Gopa runtime."""
    
    def __init__(self, perm_string: str = ""):
        """Initialize permissions from comma-separated string.
        
        Default safe permissions: packages on, everything else off.
        """
        self.network = False
        self.files = False
        self.graphics = False
        self.sound = False
        self.packages = True
        self.python_ffi = False
        self.server = False
        self.timers = False
        self.cron = False
        self.state = False
        
        if perm_string:
            perms = [p.strip().lower() for p in perm_string.split(',')]
            self.network = 'network' in perms
            self.files = 'files' in perms
            self.graphics = 'graphics' in perms
            self.sound = 'sound' in perms
            self.packages = 'packages' in perms
            self.python_ffi = 'python' in perms or 'python_ffi' in perms
            self.server = 'server' in perms
            self.timers = 'timers' in perms
            self.cron = 'cron' in perms
            self.state = 'state' in perms
    
    def check_network(self):
        if not self.network:
            raise RuntimeError("Network access not allowed")
    
    def check_files(self):
        if not self.files:
            raise RuntimeError("File access not allowed")
    
    def check_graphics(self):
        if not self.graphics:
            raise RuntimeError("Graphics access not allowed")
    
    def check_sound(self):
        if not self.sound:
            raise RuntimeError("Sound access not allowed")
    
    def check_packages(self):
        if not self.packages:
            raise RuntimeError("Package access not allowed")
    
    def check_python_ffi(self):
        if not self.python_ffi:
            raise RuntimeError("Python interop not allowed")
    
    def check_server(self):
        if not self.server:
            raise RuntimeError("Server access not allowed")
    
    def check_timers(self):
        if not self.timers and not self.graphics:
            raise RuntimeError("Timer access not allowed")
    
    def check_cron(self):
        if not self.cron and not self.timers:
            raise RuntimeError("Cron access not allowed")

