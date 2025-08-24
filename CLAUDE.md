# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env file with your AI API keys
```

### Running the Application
```bash
# Run the Flask development server
python app.py
# Application runs on http://localhost:8000 by default
```

### Testing and Development
```bash
# Run in debug mode for detailed error information
FLASK_DEBUG=1 python app.py

# Test with different AI providers by setting environment variables
DEFAULT_AI_PROVIDER=claude python app.py    # Use Claude (Anthropic)
DEFAULT_AI_PROVIDER=gemini python app.py    # Use Gemini (Google)
```

## Architecture Overview

This is a Flask-based AI-powered test case generation system that analyzes local web applications and generates comprehensive test cases using multiple AI providers.

### Core Architecture Components

**Multi-Layer Service Architecture:**
- **Flask Web App** (`app.py`): REST API with session-based file management in `downloads/` directories
- **Service Layer** (`services/`): Modular services with dependency injection pattern
- **Configuration Layer** (`config/`): Extensible template and app type system for future scaling

**AI Provider Abstraction:**
- Abstract base class pattern in `AIProvider` with concrete implementations for Claude and Gemini
- Fallback provider system: automatically switches to available provider if primary fails
- Provider manager handles API key validation and provider selection
- Centralized prompt management in `config/prompts.py` with provider-specific templates
- Standardized test case format across all AI providers with validation and enhancement

**Application Analysis Pipeline:**
1. `AppAnalyzer` uses Selenium + BeautifulSoup for comprehensive web app analysis
2. `AppTypeManager` routes different URL types to appropriate handlers (currently local apps only)
3. Context generation extracts forms, buttons, navigation, technologies, and page structure
4. AI providers receive structured context and generate test cases using centralized prompt templates from `PromptManager`

### Key Architectural Patterns

**Provider Pattern:** `AIProviderManager` abstracts multiple AI APIs (Claude, Gemini) with automatic fallback
**Template System:** `config/templates.py` defines extensible test case templates for different application types  
**Prompt Management:** `config/prompts.py` centralizes all AI prompt templates with provider-specific formatting
**Handler Chain:** `config/app_types.py` contains handler classes for different app types (local vs internet)
**Session Management:** UUID-based sessions with file downloads stored in `downloads/{session_id}/`

### Test Case Generation Flow

1. **Analysis Phase:** Selenium browses target application, extracts DOM structure, forms, links, buttons
2. **Context Building:** Creates structured analysis report including detected technologies and page layout
3. **AI Generation:** Sends context to selected AI provider with category-specific prompts
4. **Validation:** Validates and enhances AI-generated test cases with required fields and proper formatting
5. **Execution:** `TestExecutor` runs top 10 test cases using Selenium automation

### File Organization

- **Services:** Independent modules with clear separation of concerns
- **Config:** Template and app type definitions for extensibility
- **Downloads:** Session-based file storage for test cases and execution results
- **Templates/Static:** Frontend assets for the web interface

### Environment Configuration

Required environment variables:
- `ANTHROPIC_API_KEY`: For Claude AI integration
- `GEMINI_API_KEY`: For Gemini AI integration  
- `DEFAULT_AI_PROVIDER`: Primary AI provider selection ("claude" or "gemini")

### Prompt Customization

Prompt templates are centralized in `config/prompts.py`:
- **PromptManager** handles provider-specific prompt formatting
- **Provider-specific prompts** optimize for each AI model's strengths (Claude vs Gemini)
- **Extensible design** supports future test types (API, mobile) and custom prompt templates
- **Template injection** allows runtime customization of test case requirements

### Future Architecture Considerations

The system is designed for expansion:
- **Internet App Support:** `InternetAppHandler` structure exists for future public web app testing
- **Template Marketplace:** `TemplateManager` supports custom templates for domain-specific testing
- **Mobile Testing:** `MOBILE_TEST_TEMPLATE` structure prepared for future mobile app support
- **API Testing:** `API_TEST_TEMPLATE` framework ready for REST API test generation

### Error Handling Strategy

- Provider fallback system ensures availability even if primary AI service fails
- Fallback test cases generated if AI providers are unavailable
- Session-based error isolation prevents cross-request contamination
- Graceful degradation with informative error messages to users