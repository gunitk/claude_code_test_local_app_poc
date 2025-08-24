"""
Prompt templates for AI providers
This module contains all prompt templates used for test case generation
"""

import json

class PromptTemplates:
    """Container for all AI prompt templates"""
    
    @staticmethod
    def get_claude_test_generation_prompt(context, template=None):
        """Get Claude-specific prompt for test case generation"""
        
        base_prompt = f"""
Based on the following web application analysis, generate comprehensive test cases for testing this application. 

Application Context:
{context}

Please generate test cases that cover:
1. Functional testing (forms, buttons, navigation)
2. UI/UX testing (layout, responsiveness)
3. Data validation testing
4. Error handling testing
5. Security testing (basic)
6. Performance testing (basic)
7. Accessibility testing (basic)

For each test case, provide:
- name: A clear, descriptive name
- description: What the test case validates
- priority: High/Medium/Low
- category: Functional/UI/Security/Performance/Accessibility/Data Validation/Error Handling
- steps: Detailed step-by-step instructions
- expected_result: What should happen when the test passes
- test_data: Any specific data needed for the test (if applicable)

Please format your response as a valid JSON array of test case objects. Ensure the JSON is properly formatted and parseable.

Example format:
[
  {{
    "name": "Login Form Validation",
    "description": "Verify that login form validates required fields",
    "priority": "High",
    "category": "Functional",
    "steps": [
      "Navigate to login page",
      "Leave username field empty",
      "Leave password field empty", 
      "Click submit button"
    ],
    "expected_result": "Form should display validation errors for both fields",
    "test_data": {{
      "username": "",
      "password": ""
    }}
  }}
]

Generate at least 15-20 comprehensive test cases covering all aspects of the application.
"""
        
        if template:
            base_prompt += f"\n\nCustom Template Requirements:\n{json.dumps(template, indent=2)}"
        
        return base_prompt
    
    @staticmethod
    def get_gemini_test_generation_prompt(context, template=None):
        """Get Gemini-specific prompt for test case generation"""
        
        base_prompt = f"""
You are a QA expert tasked with creating comprehensive test cases for a web application.

Application Analysis:
{context}

Generate test cases covering these categories:
1. Functional Testing: Forms, buttons, navigation, core features
2. UI/UX Testing: Layout, responsiveness, visual elements
3. Data Validation: Input validation, form validation, data integrity
4. Error Handling: Invalid inputs, edge cases, error messages
5. Security Testing: Basic security checks, XSS prevention, authentication
6. Performance Testing: Page load times, response times
7. Accessibility Testing: Screen readers, keyboard navigation

For each test case, provide these fields:
- name: Clear, descriptive test name
- description: What the test validates
- priority: "High", "Medium", or "Low"
- category: One of the categories above
- steps: Array of detailed step-by-step instructions
- expected_result: Expected outcome when test passes
- test_data: Object with any test data needed (can be empty {{}})

IMPORTANT: Respond with ONLY a valid JSON array. No additional text, explanations, or markdown formatting.

Example structure:
[
  {{
    "name": "Page Load Validation",
    "description": "Verify the main page loads correctly",
    "priority": "High",
    "category": "Functional",
    "steps": [
      "Navigate to the application URL",
      "Wait for page to fully load",
      "Verify page title is displayed"
    ],
    "expected_result": "Page loads without errors and shows expected content",
    "test_data": {{}}
  }}
]

Generate 15-20 comprehensive test cases as a JSON array:
"""
        
        if template:
            base_prompt += f"\n\nAdditional template requirements:\n{json.dumps(template, indent=2)}"
        
        return base_prompt

    @staticmethod
    def get_api_test_generation_prompt(context, template=None):
        """Get prompt for API testing (future feature)"""
        
        base_prompt = f"""
You are an API testing expert. Generate comprehensive API test cases based on the following analysis.

API Context:
{context}

Generate test cases covering:
1. Endpoint Testing: Valid requests, response validation
2. Authentication: Token validation, permission checks
3. Data Validation: Request payload validation, response format
4. Error Handling: Invalid requests, error response codes
5. Performance: Response times, concurrent requests
6. Security: Input sanitization, authorization

For each API test case, provide:
- name: Clear test name
- description: What the test validates
- method: HTTP method (GET, POST, PUT, DELETE, PATCH)
- endpoint: API endpoint path
- headers: Required headers (can be empty {{}})
- payload: Request body (can be empty {{}})
- expected_status: Expected HTTP status code
- expected_response: Expected response structure or content
- test_data: Test data variations

Respond with a valid JSON array of API test cases.
"""
        
        if template:
            base_prompt += f"\n\nTemplate requirements:\n{json.dumps(template, indent=2)}"
        
        return base_prompt

    @staticmethod
    def get_mobile_test_generation_prompt(context, template=None):
        """Get prompt for mobile testing (future feature)"""
        
        base_prompt = f"""
You are a mobile app testing specialist. Create comprehensive mobile test cases.

Mobile App Context:
{context}

Generate test cases covering:
1. UI Elements: Buttons, forms, navigation, gestures
2. Device Orientation: Portrait and landscape modes
3. Network Conditions: WiFi, 3G, 4G, offline scenarios
4. Performance: App startup, memory usage, battery consumption
5. Compatibility: Different devices, OS versions
6. Gestures: Tap, swipe, pinch, long press

For each mobile test case, provide:
- name: Clear test name
- description: What the test validates
- device_type: "phone" or "tablet"
- orientation: "portrait" or "landscape"
- network_condition: "wifi", "3g", "4g", or "offline"
- gestures: Array of required gestures
- steps: Detailed test steps
- expected_result: Expected behavior
- device_requirements: Specific device or OS requirements

Respond with a valid JSON array of mobile test cases.
"""
        
        if template:
            base_prompt += f"\n\nTemplate requirements:\n{json.dumps(template, indent=2)}"
        
        return base_prompt

class PromptManager:
    """Manager class for handling different prompt templates"""
    
    def __init__(self):
        self.templates = PromptTemplates()
    
    def get_prompt(self, provider, test_type="web", context="", template=None):
        """
        Get appropriate prompt for given provider and test type
        
        Args:
            provider (str): AI provider name ('claude', 'gemini')
            test_type (str): Type of testing ('web', 'api', 'mobile')
            context (str): Application context
            template (dict, optional): Custom template requirements
        
        Returns:
            str: Formatted prompt
        """
        
        if test_type == "web":
            if provider.lower() == "claude":
                return self.templates.get_claude_test_generation_prompt(context, template)
            elif provider.lower() == "gemini":
                return self.templates.get_gemini_test_generation_prompt(context, template)
        elif test_type == "api":
            return self.templates.get_api_test_generation_prompt(context, template)
        elif test_type == "mobile":
            return self.templates.get_mobile_test_generation_prompt(context, template)
        
        # Default to Claude web testing prompt
        return self.templates.get_claude_test_generation_prompt(context, template)
    
    def add_custom_prompt(self, provider, test_type, prompt_template):
        """Add custom prompt template (future feature)"""
        # Future implementation for custom prompts
        pass
    
    def list_available_prompts(self):
        """List all available prompt types"""
        return {
            "web_testing": {
                "providers": ["claude", "gemini"],
                "description": "Comprehensive web application testing"
            },
            "api_testing": {
                "providers": ["claude", "gemini"],
                "description": "REST API testing (future feature)"
            },
            "mobile_testing": {
                "providers": ["claude", "gemini"], 
                "description": "Mobile application testing (future feature)"
            }
        }