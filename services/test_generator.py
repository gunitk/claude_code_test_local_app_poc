import os
import json
from services.ai_providers import AIProviderManager

class TestGenerator:
    def __init__(self):
        self.ai_manager = AIProviderManager()
    
    def generate_test_cases(self, context, template=None, provider=None):
        """
        Generate comprehensive test cases based on application context using AI providers
        
        Args:
            context (str): The application context analysis
            template (dict, optional): Future feature - custom test case template
            provider (str, optional): AI provider to use ('claude', 'gemini')
        
        Returns:
            list: List of test case dictionaries
        """
        
        try:
            test_cases = self.ai_manager.generate_test_cases(context, provider, template)
            return test_cases
            
        except Exception as e:
            raise Exception(f"Failed to generate test cases using AI: {str(e)}")
    
    def get_available_providers(self):
        """Get list of available AI providers"""
        return self.ai_manager.get_available_providers()