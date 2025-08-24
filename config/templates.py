"""
Configuration for test case templates and execution plans
This module defines the structure for future template support
"""

# Default test case template structure
DEFAULT_TEST_TEMPLATE = {
    "template_id": "default",
    "name": "Default Test Template",
    "description": "Standard web application testing template",
    "categories": [
        "functional",
        "ui",
        "security",
        "performance",
        "accessibility",
        "data_validation",
        "error_handling"
    ],
    "priority_weights": {
        "High": 3,
        "Medium": 2, 
        "Low": 1
    },
    "test_case_structure": {
        "required_fields": ["name", "description", "priority", "steps", "expected_result"],
        "optional_fields": ["category", "test_data", "estimated_time", "prerequisites", "tags"],
        "validation_rules": {
            "priority": ["High", "Medium", "Low"],
            "category": ["Functional", "UI", "Security", "Performance", "Accessibility", "Data Validation", "Error Handling"],
            "steps": "list",
            "test_data": "dict"
        }
    }
}

# Template for API testing (future feature)
API_TEST_TEMPLATE = {
    "template_id": "api",
    "name": "API Testing Template",
    "description": "Template for REST API testing",
    "categories": [
        "endpoint_testing",
        "authentication",
        "data_validation",
        "error_handling",
        "performance",
        "security"
    ],
    "test_case_structure": {
        "required_fields": ["name", "description", "method", "endpoint", "expected_status", "expected_response"],
        "optional_fields": ["headers", "payload", "authentication", "parameters"],
        "validation_rules": {
            "method": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            "expected_status": "integer",
            "headers": "dict",
            "payload": "dict"
        }
    }
}

# Template for mobile app testing (future feature)
MOBILE_TEST_TEMPLATE = {
    "template_id": "mobile",
    "name": "Mobile App Testing Template", 
    "description": "Template for mobile application testing",
    "categories": [
        "ui_elements",
        "gestures",
        "device_orientation",
        "network_conditions",
        "performance",
        "compatibility"
    ],
    "test_case_structure": {
        "required_fields": ["name", "description", "device_type", "orientation", "expected_result"],
        "optional_fields": ["gestures", "network_condition", "device_model"],
        "validation_rules": {
            "device_type": ["phone", "tablet"],
            "orientation": ["portrait", "landscape"],
            "network_condition": ["wifi", "3g", "4g", "offline"]
        }
    }
}

class TemplateManager:
    """Manager class for handling test templates"""
    
    def __init__(self):
        self.templates = {
            "default": DEFAULT_TEST_TEMPLATE,
            "api": API_TEST_TEMPLATE,
            "mobile": MOBILE_TEST_TEMPLATE
        }
    
    def get_template(self, template_id):
        """Get a template by ID"""
        return self.templates.get(template_id, DEFAULT_TEST_TEMPLATE)
    
    def list_templates(self):
        """List all available templates"""
        return [
            {
                "id": template_id,
                "name": template["name"],
                "description": template["description"]
            }
            for template_id, template in self.templates.items()
        ]
    
    def add_custom_template(self, template_id, template_config):
        """Add a custom template (future feature)"""
        # Validate template structure
        required_keys = ["name", "description", "categories", "test_case_structure"]
        
        for key in required_keys:
            if key not in template_config:
                raise ValueError(f"Template missing required field: {key}")
        
        self.templates[template_id] = template_config
        return True
    
    def validate_test_case(self, test_case, template_id="default"):
        """Validate a test case against a template"""
        template = self.get_template(template_id)
        structure = template["test_case_structure"]
        
        # Check required fields
        for field in structure["required_fields"]:
            if field not in test_case:
                return False, f"Missing required field: {field}"
        
        # Validate field values
        validation_rules = structure.get("validation_rules", {})
        for field, rule in validation_rules.items():
            if field in test_case:
                if isinstance(rule, list):
                    if test_case[field] not in rule:
                        return False, f"Invalid value for {field}: {test_case[field]}"
                elif rule == "list" and not isinstance(test_case[field], list):
                    return False, f"Field {field} must be a list"
                elif rule == "dict" and not isinstance(test_case[field], dict):
                    return False, f"Field {field} must be a dictionary"
                elif rule == "integer" and not isinstance(test_case[field], int):
                    return False, f"Field {field} must be an integer"
        
        return True, "Valid test case"