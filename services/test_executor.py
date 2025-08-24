import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class TestExecutor:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--window-size=1920,1080')
        
    def execute_top_tests(self, test_cases, base_url, limit=10):
        """
        Execute the top test cases based on priority
        
        Args:
            test_cases (list): List of test case dictionaries
            base_url (str): The base URL of the application
            limit (int): Maximum number of tests to execute
            
        Returns:
            dict: Execution results with summary and individual test results
        """
        
        # Sort test cases by priority (High > Medium > Low)
        priority_order = {'High': 3, 'Medium': 2, 'Low': 1}
        sorted_tests = sorted(
            test_cases,
            key=lambda x: priority_order.get(x.get('priority', 'Low'), 1),
            reverse=True
        )
        
        # Execute top N test cases
        tests_to_execute = sorted_tests[:limit]
        
        start_time = datetime.now()
        results = []
        passed = 0
        failed = 0
        
        for test_case in tests_to_execute:
            result = self._execute_single_test(test_case, base_url)
            results.append(result)
            
            if result['status'] == 'passed':
                passed += 1
            else:
                failed += 1
        
        end_time = datetime.now()
        execution_time = str(end_time - start_time)
        
        return {
            'summary': {
                'total_tests': len(tests_to_execute),
                'passed': passed,
                'failed': failed,
                'execution_time': execution_time,
                'timestamp': start_time.isoformat()
            },
            'results': results
        }
    
    def _execute_single_test(self, test_case, base_url):
        """
        Execute a single test case
        
        Args:
            test_case (dict): Test case information
            base_url (str): Base URL of the application
            
        Returns:
            dict: Test execution result
        """
        
        test_start = time.time()
        result = {
            'test_id': test_case.get('id', 0),
            'test_name': test_case.get('name', 'Unknown Test'),
            'category': test_case.get('category', 'Functional'),
            'priority': test_case.get('priority', 'Medium'),
            'status': 'failed',
            'execution_time': '0s',
            'details': '',
            'error': None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Execute test based on category
            category = test_case.get('category', 'Functional').lower()
            
            if category == 'functional':
                self._execute_functional_test(test_case, base_url, result)
            elif category == 'ui':
                self._execute_ui_test(test_case, base_url, result)
            elif category == 'performance':
                self._execute_performance_test(test_case, base_url, result)
            elif category == 'security':
                self._execute_security_test(test_case, base_url, result)
            else:
                # Default to functional test
                self._execute_functional_test(test_case, base_url, result)
                
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            result['details'] = f"Test execution failed: {str(e)}"
        
        test_end = time.time()
        result['execution_time'] = f"{test_end - test_start:.2f}s"
        
        return result
    
    def _execute_functional_test(self, test_case, base_url, result):
        """Execute functional test cases using Selenium"""
        
        driver = None
        try:
            driver = webdriver.Chrome(options=self.chrome_options)
            driver.set_page_load_timeout(30)
            
            # Navigate to the application
            driver.get(base_url)
            time.sleep(2)
            
            # Basic checks
            page_title = driver.title
            page_source = driver.page_source
            
            # Execute test steps based on test case name and steps
            test_name = test_case.get('name', '').lower()
            
            if 'page load' in test_name or 'loading' in test_name:
                # Page load test
                if page_title and len(page_source) > 100:
                    result['status'] = 'passed'
                    result['details'] = f"Page loaded successfully. Title: '{page_title}'"
                else:
                    result['details'] = "Page failed to load properly"
                    
            elif 'navigation' in test_name:
                # Navigation test
                links = driver.find_elements(By.TAG_NAME, "a")
                working_links = 0
                
                for link in links[:5]:  # Test first 5 links
                    href = link.get_attribute('href')
                    if href and not href.startswith(('mailto:', 'tel:', 'javascript:')):
                        try:
                            link.click()
                            time.sleep(1)
                            working_links += 1
                            driver.back()
                            time.sleep(1)
                        except:
                            continue
                
                if working_links > 0:
                    result['status'] = 'passed'
                    result['details'] = f"Navigation test passed. {working_links} links tested successfully"
                else:
                    result['details'] = "No working navigation links found"
                    
            elif 'form' in test_name:
                # Form test
                forms = driver.find_elements(By.TAG_NAME, "form")
                
                if forms:
                    form = forms[0]
                    inputs = form.find_elements(By.TAG_NAME, "input")
                    
                    # Try to fill and submit form
                    filled_inputs = 0
                    for inp in inputs:
                        input_type = inp.get_attribute('type')
                        if input_type in ['text', 'email', 'password']:
                            try:
                                inp.clear()
                                inp.send_keys("test_data")
                                filled_inputs += 1
                            except:
                                continue
                    
                    if filled_inputs > 0:
                        result['status'] = 'passed'
                        result['details'] = f"Form test passed. Filled {filled_inputs} form fields"
                    else:
                        result['details'] = "Form found but couldn't fill any fields"
                else:
                    result['details'] = "No forms found on the page"
                    
            elif 'button' in test_name:
                # Button test
                buttons = driver.find_elements(By.TAG_NAME, "button")
                buttons.extend(driver.find_elements(By.CSS_SELECTOR, "input[type='button']"))
                buttons.extend(driver.find_elements(By.CSS_SELECTOR, "input[type='submit']"))
                
                clickable_buttons = 0
                for button in buttons[:3]:  # Test first 3 buttons
                    try:
                        if button.is_enabled() and button.is_displayed():
                            clickable_buttons += 1
                    except:
                        continue
                
                if clickable_buttons > 0:
                    result['status'] = 'passed'
                    result['details'] = f"Button test passed. Found {clickable_buttons} clickable buttons"
                else:
                    result['details'] = "No clickable buttons found"
                    
            else:
                # Generic functional test
                if page_title and len(page_source) > 100:
                    result['status'] = 'passed'
                    result['details'] = "Generic functional test passed - page loads and has content"
                else:
                    result['details'] = "Generic functional test failed - page appears empty"
        
        finally:
            if driver:
                driver.quit()
    
    def _execute_ui_test(self, test_case, base_url, result):
        """Execute UI/UX related test cases"""
        
        driver = None
        try:
            driver = webdriver.Chrome(options=self.chrome_options)
            driver.get(base_url)
            time.sleep(2)
            
            test_name = test_case.get('name', '').lower()
            
            if 'responsive' in test_name or 'mobile' in test_name:
                # Responsive design test
                # Test different screen sizes
                sizes = [(1920, 1080), (768, 1024), (375, 667)]  # Desktop, Tablet, Mobile
                responsive_works = True
                
                for width, height in sizes:
                    driver.set_window_size(width, height)
                    time.sleep(1)
                    
                    # Check if page is still usable
                    body = driver.find_element(By.TAG_NAME, "body")
                    if not body.is_displayed():
                        responsive_works = False
                        break
                
                if responsive_works:
                    result['status'] = 'passed'
                    result['details'] = "Responsive design test passed - page adapts to different screen sizes"
                else:
                    result['details'] = "Responsive design test failed - page doesn't adapt properly"
                    
            else:
                # Generic UI test
                elements = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, p, div, button, input")
                if len(elements) > 5:
                    result['status'] = 'passed'
                    result['details'] = f"UI test passed - page has {len(elements)} UI elements"
                else:
                    result['details'] = "UI test failed - insufficient UI elements found"
        
        finally:
            if driver:
                driver.quit()
    
    def _execute_performance_test(self, test_case, base_url, result):
        """Execute performance related test cases"""
        
        try:
            # Measure page load time
            start_time = time.time()
            response = requests.get(base_url, timeout=30)
            load_time = time.time() - start_time
            
            if response.status_code == 200 and load_time < 5.0:  # 5 second threshold
                result['status'] = 'passed'
                result['details'] = f"Performance test passed - page loaded in {load_time:.2f}s"
            else:
                result['details'] = f"Performance test failed - page took {load_time:.2f}s to load or returned error {response.status_code}"
                
        except Exception as e:
            result['details'] = f"Performance test failed: {str(e)}"
    
    def _execute_security_test(self, test_case, base_url, result):
        """Execute basic security test cases"""
        
        try:
            # Basic security headers check
            response = requests.get(base_url, timeout=10)
            headers = response.headers
            
            security_headers = ['X-Content-Type-Options', 'X-Frame-Options', 'X-XSS-Protection']
            found_headers = sum(1 for header in security_headers if header in headers)
            
            if found_headers > 0:
                result['status'] = 'passed'
                result['details'] = f"Security test passed - found {found_headers} security headers"
            else:
                result['details'] = "Security test failed - no common security headers found"
                
        except Exception as e:
            result['details'] = f"Security test failed: {str(e)}"