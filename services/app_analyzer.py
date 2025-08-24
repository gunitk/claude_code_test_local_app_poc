import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class AppAnalyzer:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--window-size=1920,1080')
    
    def analyze_app(self, url):
        """
        Analyze a web application by browsing it and extracting context information
        """
        context_info = {
            'url': url,
            'title': '',
            'description': '',
            'pages': [],
            'forms': [],
            'buttons': [],
            'links': [],
            'technologies': [],
            'structure': ''
        }
        
        try:
            # First, try simple HTTP request to check if app is accessible
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                raise Exception(f"App not accessible. Status code: {response.status_code}")
            
            # Use Selenium for dynamic content analysis
            driver = webdriver.Chrome(options=self.chrome_options)
            driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            # Extract basic page information
            context_info['title'] = driver.title
            
            # Get page structure using BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                context_info['description'] = meta_desc.get('content', '')
            
            # Find all forms
            forms = soup.find_all('form')
            for form in forms:
                form_info = {
                    'action': form.get('action', ''),
                    'method': form.get('method', 'GET'),
                    'inputs': []
                }
                
                inputs = form.find_all(['input', 'textarea', 'select'])
                for inp in inputs:
                    form_info['inputs'].append({
                        'type': inp.get('type', inp.name),
                        'name': inp.get('name', ''),
                        'placeholder': inp.get('placeholder', ''),
                        'required': 'required' in inp.attrs
                    })
                
                context_info['forms'].append(form_info)
            
            # Find all buttons
            buttons = soup.find_all(['button', 'input'])
            for btn in buttons:
                if btn.name == 'input' and btn.get('type') in ['submit', 'button']:
                    context_info['buttons'].append({
                        'text': btn.get('value', ''),
                        'type': btn.get('type', ''),
                        'id': btn.get('id', ''),
                        'class': btn.get('class', [])
                    })
                elif btn.name == 'button':
                    context_info['buttons'].append({
                        'text': btn.get_text(strip=True),
                        'type': btn.get('type', 'button'),
                        'id': btn.get('id', ''),
                        'class': btn.get('class', [])
                    })
            
            # Find all navigation links
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href', '')
                if href and not href.startswith(('http', 'mailto:', 'tel:')):
                    context_info['links'].append({
                        'text': link.get_text(strip=True),
                        'href': href,
                        'id': link.get('id', ''),
                        'class': link.get('class', [])
                    })
            
            # Detect technologies (basic detection)
            page_source = driver.page_source.lower()
            tech_indicators = {
                'React': ['react', 'jsx', 'react-dom'],
                'Angular': ['angular', 'ng-app', 'ng-controller'],
                'Vue.js': ['vue', 'v-if', 'v-for'],
                'Bootstrap': ['bootstrap', 'btn-primary', 'container-fluid'],
                'jQuery': ['jquery', '$(', 'jquery.min.js'],
                'Express.js': ['express'],
                'Flask': ['flask'],
                'Django': ['django', 'csrfmiddlewaretoken']
            }
            
            for tech, indicators in tech_indicators.items():
                if any(indicator in page_source for indicator in indicators):
                    context_info['technologies'].append(tech)
            
            # Create a structural summary
            context_info['structure'] = self._create_structure_summary(soup)
            
            driver.quit()
            
            # Convert to readable context string
            return self._format_context(context_info)
            
        except Exception as e:
            if 'driver' in locals():
                driver.quit()
            raise Exception(f"Failed to analyze app: {str(e)}")
    
    def _create_structure_summary(self, soup):
        """Create a summary of the page structure"""
        structure = []
        
        # Header information
        header = soup.find('header') or soup.find('nav')
        if header:
            structure.append("Header/Navigation section present")
        
        # Main content areas
        main = soup.find('main') or soup.find('div', class_=lambda x: x and 'main' in str(x).lower())
        if main:
            structure.append("Main content area identified")
        
        # Sidebar
        sidebar = soup.find('aside') or soup.find('div', class_=lambda x: x and 'sidebar' in str(x).lower())
        if sidebar:
            structure.append("Sidebar present")
        
        # Footer
        footer = soup.find('footer')
        if footer:
            structure.append("Footer section present")
        
        return "; ".join(structure) if structure else "Basic HTML structure"
    
    def _format_context(self, context_info):
        """Format the context information into a readable string"""
        formatted = f"""
Web Application Analysis Report:

URL: {context_info['url']}
Title: {context_info['title']}
Description: {context_info['description']}

Structure: {context_info['structure']}

Technologies Detected: {', '.join(context_info['technologies']) if context_info['technologies'] else 'None detected'}

Forms Found ({len(context_info['forms'])}):
"""
        
        for i, form in enumerate(context_info['forms'], 1):
            formatted += f"\n  Form {i}: {form['method']} to {form['action'] or 'same page'}"
            for inp in form['inputs']:
                required = " (required)" if inp['required'] else ""
                formatted += f"\n    - {inp['type']} field: {inp['name']}{required}"
        
        formatted += f"\n\nButtons Found ({len(context_info['buttons'])}):"
        for btn in context_info['buttons']:
            formatted += f"\n  - {btn['text']} ({btn['type']})"
        
        formatted += f"\n\nNavigation Links ({len(context_info['links'])}):"
        for link in context_info['links'][:10]:  # Limit to first 10 links
            formatted += f"\n  - {link['text']} -> {link['href']}"
        
        if len(context_info['links']) > 10:
            formatted += f"\n  ... and {len(context_info['links']) - 10} more links"
        
        return formatted.strip()