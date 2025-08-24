import os
import json
from abc import ABC, abstractmethod
from anthropic import Anthropic
import google.generativeai as genai
from config.prompts import PromptManager

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate_test_cases(self, context, template=None):
        """Generate test cases based on application context"""
        pass
    
    @abstractmethod
    def is_available(self):
        """Check if the provider is properly configured"""
        pass
    
    @abstractmethod
    def get_provider_info(self):
        """Get provider information"""
        pass

class ClaudeProvider(AIProvider):
    """Claude AI provider using Anthropic API"""
    
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.client = None
        self.prompt_manager = PromptManager()
        if self.api_key:
            try:
                self.client = Anthropic(api_key=self.api_key)
            except Exception as e:
                print(f"Failed to initialize Claude client: {e}")
    
    def is_available(self):
        return bool(self.api_key and self.client)
    
    def get_provider_info(self):
        return {
            "name": "Claude",
            "provider": "Anthropic",
            "model": "claude-3-sonnet-20240229",
            "description": "Advanced reasoning and analysis capabilities"
        }
    
    def generate_test_cases(self, context, template=None):
        if not self.is_available():
            raise ValueError("Claude API key not configured")
        
        prompt = self.prompt_manager.get_prompt("claude", "web", context, template)
        
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            test_cases_text = response.content[0].text
            return self._parse_test_cases(test_cases_text)
            
        except Exception as e:
            raise Exception(f"Failed to generate test cases using Claude API: {str(e)}")
    
    
    def _parse_test_cases(self, response_text):
        """Parse Claude's response to extract test cases"""
        try:
            start_marker = response_text.find('[')
            end_marker = response_text.rfind(']') + 1
            
            if start_marker == -1 or end_marker == 0:
                if '```json' in response_text:
                    json_start = response_text.find('```json') + 7
                    json_end = response_text.find('```', json_start)
                    json_content = response_text[json_start:json_end].strip()
                else:
                    raise ValueError("No JSON content found in response")
            else:
                json_content = response_text[start_marker:end_marker]
            
            test_cases = json.loads(json_content)
            return self._validate_test_cases(test_cases)
            
        except (json.JSONDecodeError, ValueError) as e:
            return self._create_fallback_test_cases()
    
    def _validate_test_cases(self, test_cases):
        """Validate and enhance test cases from Claude"""
        validated_cases = []
        for i, test_case in enumerate(test_cases):
            validated_case = {
                'id': i + 1,
                'name': test_case.get('name', f'Test Case {i + 1}'),
                'description': test_case.get('description', 'Generated test case'),
                'priority': test_case.get('priority', 'Medium'),
                'category': test_case.get('category', 'Functional'),
                'steps': test_case.get('steps', ['Execute test']),
                'expected_result': test_case.get('expected_result', 'Test should pass'),
                'test_data': test_case.get('test_data', {}),
                'estimated_time': test_case.get('estimated_time', '5 minutes')
            }
            
            # Ensure steps is a list
            if isinstance(validated_case['steps'], str):
                validated_case['steps'] = [validated_case['steps']]
            
            # Validate priority
            if validated_case['priority'] not in ['High', 'Medium', 'Low']:
                validated_case['priority'] = 'Medium'
            
            validated_cases.append(validated_case)
        
        return validated_cases
    
    def _create_fallback_test_cases(self):
        """Create basic fallback test cases if API fails"""
        return [
            {
                'id': 1,
                'name': 'Basic Page Load Test',
                'description': 'Verify the application loads successfully',
                'priority': 'High',
                'category': 'Functional',
                'steps': [
                    'Open the application URL',
                    'Wait for page to load completely',
                    'Verify page content is displayed'
                ],
                'expected_result': 'Application loads without errors',
                'test_data': {},
                'estimated_time': '2 minutes'
            }
        ]

class GeminiProvider(AIProvider):
    """Gemini AI provider using Google Generative AI"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.prompt_manager = PromptManager()
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            except Exception as e:
                print(f"Failed to initialize Gemini client: {e}")
                self.model = None
        else:
            self.model = None
    
    def is_available(self):
        return bool(self.api_key and self.model)
    
    def get_provider_info(self):
        return {
            "name": "Gemini",
            "provider": "Google",
            "model": "gemini-1.5-flash",
            "description": "Fast and efficient AI model with strong reasoning"
        }
    
    def generate_test_cases(self, context, template=None):
        if not self.is_available():
            raise ValueError("Gemini API key not configured")
        
        prompt = self.prompt_manager.get_prompt("gemini", "web", context, template)
        
        try:
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise Exception("Empty response from Gemini API")
            
            return self._parse_test_cases(response.text)
            
        except Exception as e:
            raise Exception(f"Failed to generate test cases using Gemini API: {str(e)}")
    
    
    def _parse_test_cases(self, response_text):
        """Parse Gemini's response to extract test cases"""
        try:
            # Clean up the response text
            cleaned_text = response_text.strip()
            
            # Remove potential markdown formatting
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            
            # Find JSON array bounds
            start_idx = cleaned_text.find('[')
            end_idx = cleaned_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON array found in response")
            
            json_content = cleaned_text[start_idx:end_idx]
            test_cases = json.loads(json_content)
            
            return self._validate_test_cases(test_cases)
            
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Failed to parse Gemini response: {e}")
            return self._create_fallback_test_cases()

    def _validate_test_cases(self, test_cases):
        """Validate and enhance test cases from Gemini"""
        validated_cases = []
        for i, test_case in enumerate(test_cases):
            validated_case = {
                'id': i + 1,
                'name': test_case.get('name', f'Test Case {i + 1}'),
                'description': test_case.get('description', 'Generated test case'),
                'priority': test_case.get('priority', 'Medium'),
                'category': test_case.get('category', 'Functional'),
                'steps': test_case.get('steps', ['Execute test']),
                'expected_result': test_case.get('expected_result', 'Test should pass'),
                'test_data': test_case.get('test_data', {}),
                'estimated_time': test_case.get('estimated_time', '5 minutes')
            }
            
            # Ensure steps is a list
            if isinstance(validated_case['steps'], str):
                validated_case['steps'] = [validated_case['steps']]
            
            # Validate priority
            if validated_case['priority'] not in ['High', 'Medium', 'Low']:
                validated_case['priority'] = 'Medium'
            
            validated_cases.append(validated_case)
        
        return validated_cases

    def _create_fallback_test_cases(self):
        """Create basic fallback test cases if API fails"""
        return [
            {
                'id': 1,
                'name': 'Basic Page Load Test',
                'description': 'Verify the application loads successfully',
                'priority': 'High',
                'category': 'Functional',
                'steps': [
                    'Open the application URL',
                    'Wait for page to load completely',
                    'Verify page content is displayed'
                ],
                'expected_result': 'Application loads without errors',
                'test_data': {},
                'estimated_time': '2 minutes'
            }
        ]

class AIProviderManager:
    """Manager class for handling multiple AI providers"""
    
    def __init__(self):
        self.providers = {
            'claude': ClaudeProvider(),
            'gemini': GeminiProvider()
        }
        self.default_provider = os.getenv('DEFAULT_AI_PROVIDER', 'claude')
    
    def get_provider(self, provider_name=None):
        """Get a specific AI provider or the default one"""
        if provider_name is None:
            provider_name = self.default_provider
        
        provider = self.providers.get(provider_name.lower())
        if not provider:
            raise ValueError(f"Unknown provider: {provider_name}")
        
        if not provider.is_available():
            # Try to fall back to another available provider
            for name, alt_provider in self.providers.items():
                if alt_provider.is_available():
                    print(f"Falling back from {provider_name} to {name}")
                    return alt_provider
            
            raise ValueError(f"Provider {provider_name} is not available and no fallback found")
        
        return provider
    
    def get_available_providers(self):
        """Get list of available providers"""
        available = []
        for name, provider in self.providers.items():
            if provider.is_available():
                info = provider.get_provider_info()
                info['key'] = name
                info['available'] = True
                available.append(info)
            else:
                info = provider.get_provider_info()
                info['key'] = name
                info['available'] = False
                available.append(info)
        
        return available
    
    def generate_test_cases(self, context, provider_name=None, template=None):
        """Generate test cases using the specified or default provider"""
        provider = self.get_provider(provider_name)
        return provider.generate_test_cases(context, template)