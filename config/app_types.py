"""
Configuration for different application types
This module defines how to handle different types of applications (local, internet, etc.)
"""

from abc import ABC, abstractmethod

class AppHandler(ABC):
    """Abstract base class for handling different types of applications"""
    
    @abstractmethod
    def can_handle(self, url):
        """Check if this handler can process the given URL"""
        pass
    
    @abstractmethod
    def analyze_app(self, url):
        """Analyze the application and return context"""
        pass
    
    @abstractmethod
    def is_accessible(self, url):
        """Check if the application is accessible"""
        pass

class LocalAppHandler(AppHandler):
    """Handler for local applications (localhost, 127.0.0.1, etc.)"""
    
    def can_handle(self, url):
        """Check if URL points to a local application"""
        local_indicators = [
            'localhost',
            '127.0.0.1',
            '0.0.0.0',
            '192.168.',
            '10.',
            '172.16.',
            '172.17.',
            '172.18.',
            '172.19.',
            '172.20.',
            '172.21.',
            '172.22.',
            '172.23.',
            '172.24.',
            '172.25.',
            '172.26.',
            '172.27.',
            '172.28.',
            '172.29.',
            '172.30.',
            '172.31.'
        ]
        
        return any(indicator in url.lower() for indicator in local_indicators)
    
    def analyze_app(self, url):
        """Use the existing AppAnalyzer for local apps"""
        from services.app_analyzer import AppAnalyzer
        analyzer = AppAnalyzer()
        return analyzer.analyze_app(url)
    
    def is_accessible(self, url):
        """Check if local app is running and accessible"""
        import requests
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except:
            return False

class InternetAppHandler(AppHandler):
    """Handler for internet applications (future feature)"""
    
    def can_handle(self, url):
        """Check if URL points to an internet application"""
        # This is for future implementation
        # Currently, we'll be conservative and only handle local apps
        return False
    
    def analyze_app(self, url):
        """Analyze internet applications (future implementation)"""
        # Future implementation would include:
        # - Rate limiting
        # - Robots.txt checking
        # - Terms of service compliance
        # - CORS handling
        # - Authentication handling
        raise NotImplementedError("Internet app support coming in future release")
    
    def is_accessible(self, url):
        """Check if internet app is accessible (future implementation)"""
        # Future implementation would include proper permission checking
        return False

class AppTypeManager:
    """Manager for different application types"""
    
    def __init__(self):
        self.handlers = [
            LocalAppHandler(),
            InternetAppHandler(),  # Future feature
        ]
    
    def get_handler(self, url):
        """Get the appropriate handler for a given URL"""
        for handler in self.handlers:
            if handler.can_handle(url):
                return handler
        
        # Default to local handler for now
        return self.handlers[0]
    
    def is_url_supported(self, url):
        """Check if the URL is supported by any handler"""
        for handler in self.handlers:
            if handler.can_handle(url):
                return True, handler.__class__.__name__
        
        return False, "No handler available"
    
    def get_supported_types(self):
        """Get list of supported application types"""
        return [
            {
                "type": "Local Applications",
                "description": "Applications running on localhost or local network",
                "examples": [
                    "http://localhost:8080",
                    "http://127.0.0.1:3000",
                    "http://192.168.1.100:8000"
                ],
                "supported": True
            },
            {
                "type": "Internet Applications", 
                "description": "Public web applications on the internet",
                "examples": [
                    "https://example.com",
                    "https://myapp.herokuapp.com"
                ],
                "supported": False,
                "note": "Coming in future release with proper permissions and rate limiting"
            }
        ]

# Configuration for different app characteristics
APP_TYPE_CONFIG = {
    "local": {
        "timeout": 30,
        "retry_attempts": 3,
        "analysis_depth": "full",
        "security_checks": ["basic"],
        "performance_thresholds": {
            "page_load": 10.0,  # seconds
            "response_time": 5.0  # seconds
        }
    },
    "internet": {  # Future configuration
        "timeout": 60,
        "retry_attempts": 2,
        "analysis_depth": "limited",  # Respect rate limits
        "security_checks": ["basic", "headers"],
        "performance_thresholds": {
            "page_load": 30.0,  # seconds
            "response_time": 15.0  # seconds
        },
        "rate_limit": {
            "requests_per_minute": 30,
            "concurrent_requests": 3
        },
        "compliance": {
            "check_robots_txt": True,
            "respect_crawl_delay": True,
            "user_agent": "TestGeneratorBot/1.0"
        }
    }
}