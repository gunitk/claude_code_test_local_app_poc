let sessionId = null;
let currentContext = null;
let currentTestCases = null;
let availableProviders = [];

document.addEventListener('DOMContentLoaded', function() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const generateTestsBtn = document.getElementById('generateTestsBtn');
    const executeTestsBtn = document.getElementById('executeTestsBtn');
    const downloadTestsBtn = document.getElementById('downloadTestsBtn');
    const downloadResultsBtn = document.getElementById('downloadResultsBtn');

    analyzeBtn.addEventListener('click', analyzeApp);
    generateTestsBtn.addEventListener('click', generateTests);
    executeTestsBtn.addEventListener('click', executeTests);
    downloadTestsBtn.addEventListener('click', downloadTests);
    downloadResultsBtn.addEventListener('click', downloadResults);
    
    // Load AI providers on page load
    loadAIProviders();
});

async function analyzeApp() {
    const url = document.getElementById('appUrl').value;
    if (!url) {
        alert('Please enter a URL');
        return;
    }

    showSpinner('analyzeSpinner');
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();
        
        if (data.success) {
            sessionId = data.session_id;
            currentContext = data.context;
            displayContext(data.context);
            showSection('context-section');
            // Refresh AI providers when context section is shown
            loadAIProviders();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error analyzing app: ' + error.message);
    } finally {
        hideSpinner('analyzeSpinner');
    }
}

async function generateTests() {
    if (!currentContext || !sessionId) {
        alert('Please analyze the app first');
        return;
    }

    const selectedProvider = document.getElementById('aiProvider').value;
    showSpinner('generateSpinner');

    try {
        const response = await fetch('/generate-tests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                context: currentContext,
                session_id: sessionId,
                provider: selectedProvider || null
            })
        });

        const data = await response.json();
        
        if (data.success) {
            currentTestCases = data.test_cases;
            displayTestCases(data.test_cases);
            showSection('testcases-section');
            
            // Show which provider was used
            const providerUsed = data.provider_used || 'default';
            const providerInfo = availableProviders.find(p => p.key === providerUsed);
            if (providerInfo) {
                console.log(`Test cases generated using ${providerInfo.name} (${providerInfo.provider})`);
            }
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error generating tests: ' + error.message);
    } finally {
        hideSpinner('generateSpinner');
    }
}

async function loadAIProviders() {
    try {
        const response = await fetch('/providers');
        const data = await response.json();
        
        if (data.success) {
            availableProviders = data.providers;
            populateProviderSelect(data.providers);
        } else {
            console.error('Failed to load AI providers:', data.error);
        }
    } catch (error) {
        console.error('Error loading AI providers:', error);
    }
}

function populateProviderSelect(providers) {
    const select = document.getElementById('aiProvider');
    select.innerHTML = '';
    
    // Add default option
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Auto (Use Default)';
    select.appendChild(defaultOption);
    
    // Add available providers
    providers.forEach(provider => {
        const option = document.createElement('option');
        option.value = provider.key;
        option.textContent = `${provider.name} (${provider.provider})`;
        
        if (!provider.available) {
            option.disabled = true;
            option.textContent += ' - Not Available';
        }
        
        select.appendChild(option);
    });
}

async function executeTests() {
    if (!currentTestCases || !sessionId) {
        alert('Please generate test cases first');
        return;
    }

    const url = document.getElementById('appUrl').value;
    showSpinner('executeSpinner');

    try {
        const response = await fetch('/execute-tests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                test_cases: currentTestCases,
                url: url,
                session_id: sessionId 
            })
        });

        const data = await response.json();
        
        if (data.success) {
            displayExecutionResults(data.execution_results);
            showSection('results-section');
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error executing tests: ' + error.message);
    } finally {
        hideSpinner('executeSpinner');
    }
}

function downloadTests() {
    if (sessionId) {
        window.location.href = `/download-tests/${sessionId}`;
    }
}

function downloadResults() {
    if (sessionId) {
        window.location.href = `/download-execution/${sessionId}`;
    }
}

function displayContext(context) {
    const contextDiv = document.getElementById('appContext');
    contextDiv.innerHTML = `<div class="app-context">${context}</div>`;
}

function displayTestCases(testCases) {
    const container = document.getElementById('testCasesList');
    container.innerHTML = '';

    testCases.forEach((testCase, index) => {
        const priorityClass = testCase.priority === 'High' ? 'priority-high' : 
                            testCase.priority === 'Medium' ? 'priority-medium' : 'priority-low';
        
        const testDiv = document.createElement('div');
        testDiv.className = `test-case ${priorityClass}`;
        testDiv.innerHTML = `
            <h5>Test Case ${index + 1}: ${testCase.name}</h5>
            <p><strong>Description:</strong> ${testCase.description}</p>
            <p><strong>Priority:</strong> <span class="badge bg-${getPriorityColor(testCase.priority)}">${testCase.priority}</span></p>
            <p><strong>Steps:</strong></p>
            <ol>
                ${testCase.steps.map(step => `<li>${step}</li>`).join('')}
            </ol>
            <p><strong>Expected Result:</strong> ${testCase.expected_result}</p>
        `;
        container.appendChild(testDiv);
    });
}

function displayExecutionResults(results) {
    const container = document.getElementById('executionResults');
    container.innerHTML = '';

    const summary = document.createElement('div');
    summary.className = 'mb-4';
    summary.innerHTML = `
        <h5>Execution Summary</h5>
        <p><strong>Total Tests:</strong> ${results.summary.total_tests}</p>
        <p><strong>Passed:</strong> <span class="text-success">${results.summary.passed}</span></p>
        <p><strong>Failed:</strong> <span class="text-danger">${results.summary.failed}</span></p>
        <p><strong>Execution Time:</strong> ${results.summary.execution_time}</p>
    `;
    container.appendChild(summary);

    results.results.forEach((result, index) => {
        const resultDiv = document.createElement('div');
        resultDiv.className = `test-result ${result.status}`;
        resultDiv.innerHTML = `
            <h6>Test ${index + 1}: ${result.test_name}</h6>
            <p><strong>Status:</strong> <span class="badge bg-${result.status === 'passed' ? 'success' : 'danger'}">${result.status.toUpperCase()}</span></p>
            <p><strong>Execution Time:</strong> ${result.execution_time}</p>
            ${result.error ? `<p><strong>Error:</strong> ${result.error}</p>` : ''}
            <p><strong>Details:</strong> ${result.details}</p>
        `;
        container.appendChild(resultDiv);
    });
}

function showSpinner(spinnerId) {
    document.getElementById(spinnerId).classList.remove('d-none');
}

function hideSpinner(spinnerId) {
    document.getElementById(spinnerId).classList.add('d-none');
}

function showSection(sectionId) {
    document.getElementById(sectionId).classList.remove('d-none');
}

function getPriorityColor(priority) {
    switch(priority) {
        case 'High': return 'danger';
        case 'Medium': return 'warning';
        case 'Low': return 'success';
        default: return 'secondary';
    }
}