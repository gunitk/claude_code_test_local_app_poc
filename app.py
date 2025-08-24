import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from services.app_analyzer import AppAnalyzer
from services.test_generator import TestGenerator
from services.test_executor import TestExecutor

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_app():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        analyzer = AppAnalyzer()
        context = analyzer.analyze_app(url)
        
        session_id = str(uuid.uuid4())
        
        return jsonify({
            'success': True,
            'context': context,
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-tests', methods=['POST'])
def generate_tests():
    data = request.get_json()
    context = data.get('context')
    session_id = data.get('session_id')
    provider = data.get('provider', None)  # Optional AI provider selection
    
    if not context or not session_id:
        return jsonify({'error': 'Context and session ID are required'}), 400
    
    try:
        generator = TestGenerator()
        test_cases = generator.generate_test_cases(context, provider=provider)
        
        session_dir = f'downloads/{session_id}'
        os.makedirs(session_dir, exist_ok=True)
        
        with open(f'{session_dir}/test_cases.json', 'w') as f:
            json.dump(test_cases, f, indent=2)
        
        return jsonify({
            'success': True,
            'test_cases': test_cases,
            'download_url': f'/download-tests/{session_id}',
            'provider_used': provider or 'default'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/providers', methods=['GET'])
def get_providers():
    """Get available AI providers"""
    try:
        generator = TestGenerator()
        providers = generator.get_available_providers()
        
        return jsonify({
            'success': True,
            'providers': providers
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/execute-tests', methods=['POST'])
def execute_tests():
    data = request.get_json()
    test_cases = data.get('test_cases')
    url = data.get('url')
    session_id = data.get('session_id')
    
    if not test_cases or not url or not session_id:
        return jsonify({'error': 'Test cases, URL, and session ID are required'}), 400
    
    try:
        executor = TestExecutor()
        execution_results = executor.execute_top_tests(test_cases, url, limit=10)
        
        session_dir = f'downloads/{session_id}'
        with open(f'{session_dir}/execution_history.json', 'w') as f:
            json.dump(execution_results, f, indent=2)
        
        return jsonify({
            'success': True,
            'execution_results': execution_results,
            'download_url': f'/download-execution/{session_id}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-tests/<session_id>')
def download_tests(session_id):
    try:
        return send_file(f'downloads/{session_id}/test_cases.json', as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/download-execution/<session_id>')
def download_execution(session_id):
    try:
        return send_file(f'downloads/{session_id}/execution_history.json', as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)