// PSIP Dashboard Logic
const passwordInput = document.getElementById('password-input');
const toggleVisibility = document.getElementById('toggle-visibility');
const strengthBar = document.getElementById('strength-bar');
const strengthLabel = document.getElementById('strength-label');
const entropyVal = document.getElementById('entropy-val');
const scoreVal = document.getElementById('score-val');
const riskVal = document.getElementById('risk-val');
const adviceContainer = document.getElementById('advice-container');
const findingsContainer = document.getElementById('findings-container');
const simGpu = document.getElementById('sim-gpu');
const simOnline = document.getElementById('sim-online');
const simSteps = document.getElementById('sim-steps');

// Generator elements
const lengthSlider = document.getElementById('length-slider');
const lengthVal = document.getElementById('length-val');
const generateBtn = document.getElementById('generate-btn');
const generatedPwdDisplay = document.getElementById('generated-pwd');

const API_BASE = "http://localhost:8000";

// Toggle password visibility
toggleVisibility.addEventListener('click', () => {
    const isPassword = passwordInput.type === 'password';
    passwordInput.type = isPassword ? 'text' : 'password';
    toggleVisibility.textContent = isPassword ? 'HIDE' : 'SHOW';
});

// Debounce function to limit API calls
function debounce(func, timeout = 300) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => { func.apply(this, args); }, timeout);
    };
}

const analyzePassword = async (password) => {
    if (!password) {
        resetDashboard();
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password })
        });
        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error("API Error:", error);
    }
};

const updateUI = (data) => {
    // Strength Bar & Score
    strengthBar.style.width = `${data.score}%`;
    strengthBar.style.backgroundColor = data.color;
    strengthBar.style.boxShadow = `0 0 15px ${data.color}`;
    
    strengthLabel.textContent = data.label;
    strengthLabel.style.color = data.color;
    
    scoreVal.textContent = `${data.score}%`;
    entropyVal.textContent = data.entropy;
    riskVal.textContent = data.label;
    riskVal.style.color = data.color;

    // AI Advice
    adviceContainer.innerHTML = data.advice.map(adv => `<p class="advice-item">${adv}</p>`).join('');

    // Findings
    if (data.findings.length > 0) {
        findingsContainer.innerHTML = data.findings.map(f => `<p style="color: #ff4d4d; margin-bottom: 0.5rem;">⚠️ ${f}</p>`).join('');
    } else {
        findingsContainer.innerHTML = `<p style="color: var(--success);">✅ No patterns or leaks detected.</p>`;
    }

    // Simulations
    simGpu.textContent = data.crack_time.offline_fast || '-';
    simOnline.textContent = data.crack_time.online_throttled || '-';
    simSteps.textContent = data.crack_time.brute_force_guess ? Number(data.crack_time.brute_force_guess).toExponential(2) : '-';
};

const resetDashboard = () => {
    strengthBar.style.width = '0%';
    strengthLabel.textContent = 'Enter Password';
    strengthLabel.style.color = 'var(--text-dim)';
    scoreVal.textContent = '0%';
    entropyVal.textContent = '0';
    riskVal.textContent = 'N/A';
    riskVal.style.color = 'var(--text-dim)';
    adviceContainer.innerHTML = `<p class="advice-item">Enter a password to begin analysis.</p>`;
    findingsContainer.innerHTML = `<p style="color: var(--text-dim);">No threats detected yet.</p>`;
    simGpu.textContent = '-';
    simOnline.textContent = '-';
    simSteps.textContent = '-';
};

passwordInput.addEventListener('input', debounce((e) => {
    analyzePassword(e.target.value);
}, 300));

// Generator Logic
lengthSlider.addEventListener('input', (e) => {
    lengthVal.textContent = e.target.value;
});

generateBtn.addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_BASE}/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ length: parseInt(lengthSlider.value), use_symbols: true })
        });
        const data = await response.json();
        
        generatedPwdDisplay.textContent = data.password;
        generatedPwdDisplay.style.display = 'block';
        
        // Auto-analyze generated password
        passwordInput.value = data.password;
        analyzePassword(data.password);
    } catch (error) {
        console.error("Generator Error:", error);
    }
});
