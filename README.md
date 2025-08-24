# Local App Test Generator

A Python web application that uses AI models (Claude and Gemini) to automatically analyze local web applications and generate comprehensive test cases.

## Features

- **URL Analysis**: Takes a locally hosted app URL (e.g., http://localhost:8080)
- **Smart Browsing**: Uses Selenium to browse and analyze the web application
- **Multi-AI Support**: Choose between Claude (Anthropic) and Gemini (Google) for test generation
- **AI-Powered Context Generation**: Uses advanced AI models to understand the application structure
- **Comprehensive Test Case Generation**: Creates functional, UI, security, and performance test cases
- **Test Case Download**: Export generated test cases as JSON
- **Automated Test Execution**: Executes top 10 test cases and shows results
- **Execution History**: View and download test execution history
- **Future-Ready Architecture**: Designed for template support and internet app testing

## Quick Start

### 1. Prerequisites

- Python 3.8+
- Chrome browser (for Selenium)
- AI API keys:
  - Anthropic Claude API key (recommended)
  - Google Gemini API key (alternative/additional)

### 2. Installation

```bash
# Clone or download this project
cd claude_code_test_local_app_poc

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Get AI API Keys

#### For Claude (Anthropic) - Recommended
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create an account and get your API key
3. Add it to your `.env` file:
```
ANTHROPIC_API_KEY=your_claude_api_key_here
```

#### For Gemini (Google) - Alternative
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an account and generate an API key
3. Add it to your `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

#### Configure Default Provider (Optional)
```
DEFAULT_AI_PROVIDER=claude  # or 'gemini'
```

**Note**: You can configure both API keys and choose between them in the web interface, or set only one.

### 4. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Usage

1. **Enter URL**: Input your local app URL (e.g., `http://localhost:8080`)
2. **Analyze**: Click "Analyze App" to browse and understand your application
3. **Choose AI Provider**: Select between Claude or Gemini for test generation
4. **Generate Tests**: Click "Generate Test Cases" to create comprehensive test cases using AI
5. **Download Tests**: Download the generated test cases as JSON
6. **Execute Tests**: Run the top 10 test cases automatically
7. **View Results**: See execution history and download the results

## Architecture

### Core Components

- **Flask Web App** (`app.py`): Main web application with REST endpoints
- **App Analyzer** (`services/app_analyzer.py`): Browses and analyzes web applications
- **Test Generator** (`services/test_generator.py`): Coordinates AI providers for test generation
- **AI Providers** (`services/ai_providers.py`): Abstraction layer for Claude and Gemini APIs
- **Test Executor** (`services/test_executor.py`): Executes test cases using Selenium
- **Templates** (`config/templates.py`): Extensible template system for test cases
- **App Types** (`config/app_types.py`): Handler system for different application types

### Test Categories Generated

- **Functional Testing**: Forms, buttons, navigation, user workflows
- **UI/UX Testing**: Layout, responsiveness, visual elements
- **Data Validation**: Input validation, form validation
- **Error Handling**: Invalid inputs, edge cases, error messages
- **Security Testing**: Basic security headers, XSS protection
- **Performance Testing**: Page load times, response times
- **Accessibility Testing**: Basic accessibility checks

## Future Features (Roadmap)

### Template Support
- Custom test case templates
- Domain-specific testing patterns
- Configurable test execution plans
- Template marketplace

### Internet Apps Support
- Support for public web applications
- Rate limiting and respectful crawling
- Authentication handling
- CORS and security compliance

### Advanced Features
- API testing capabilities
- Mobile app testing
- Visual regression testing
- Integration with CI/CD pipelines
- Advanced reporting and analytics

## Configuration

### Application Types

The system is designed to support different application types:

- **Local Applications**: ✅ Currently supported
  - `http://localhost:*`
  - `http://127.0.0.1:*`  
  - Local network IPs (`192.168.*`, `10.*`, etc.)

- **Internet Applications**: 🚧 Future release
  - Public websites with proper rate limiting
  - Authentication-required applications
  - API endpoints

### Templates

Custom test templates can be added via the `config/templates.py` system:

```python
# Example custom template
CUSTOM_TEMPLATE = {
    "template_id": "ecommerce",
    "name": "E-commerce Testing Template",
    "categories": ["product_catalog", "shopping_cart", "checkout"],
    # ... additional configuration
}
```

## API Endpoints

- `POST /analyze` - Analyze an application URL
- `POST /generate-tests` - Generate test cases using AI (supports provider selection)
- `POST /execute-tests` - Execute test cases
- `GET /providers` - Get available AI providers and their status
- `GET /download-tests/<session_id>` - Download test cases
- `GET /download-execution/<session_id>` - Download execution history

## Dependencies

- **Flask**: Web application framework
- **Selenium**: Web browser automation
- **BeautifulSoup**: HTML parsing
- **Anthropic**: Claude AI API client
- **Google Generative AI**: Gemini API client
- **Requests**: HTTP library
- **WebDriver Manager**: Automatic ChromeDriver management

## Contributing

This is a proof-of-concept application. For production use, consider:

- Adding authentication and session management
- Implementing proper error handling and logging
- Adding rate limiting for API calls
- Implementing proper file cleanup
- Adding comprehensive tests
- Security hardening

## License

MIT License - see LICENSE file for details.

## Support

For issues or questions:
1. Check the existing documentation
2. Review the code comments
3. Create an issue with detailed information about your setup and the problem

## Troubleshooting

### Common Issues

1. **ChromeDriver Issues**: The app automatically downloads ChromeDriver, but ensure Chrome browser is installed

2. **AI API Errors**: 
   - For Claude: Verify your API key is correct and has sufficient credits
   - For Gemini: Ensure your API key is valid and the model is accessible
   - Check the provider selection in the web interface

3. **Local App Not Accessible**: Ensure your target application is running and accessible

4. **Port Conflicts**: If port 5000 is in use, modify the port in `app.py`

### Debug Mode

Run with debug mode for detailed error information:
```bash
FLASK_DEBUG=1 python app.py
```