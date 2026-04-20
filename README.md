# 🛡️ PSIP: Password Strength Intelligence Platform

**Password Strength Intelligence Platform (PSIP)** is a premium, enterprise-grade cybersecurity tool designed to evaluate password integrity using advanced cryptographic entropy models and real-world attack simulations.

![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Security](https://img.shields.io/badge/Security-Zero--Trust-green)
![Tech](https://img.shields.io/badge/Stack-FastAPI%20%7C%20Vanilla%20JS-orange)

## 🌟 Executive Overview
In an era of sophisticated credential stuffing and GPU-accelerated brute force attacks, simple "strength bars" are no longer sufficient. PSIP provides users with deep technical insights into *why* their password is weak, simulating how an attacker's machine would perceive it.

### Core Features
- **Entropy Analysis**: Real-time Shannon Entropy calculation.
- **Attack Simulation**: Estimates crack time for Offline (GPU) vs. Online (Throttled) scenarios.
- **Pattern Intelligence**: Detects sequences, repetitions, and keyboard adjacency.
- **AI Security Advisor**: Provides actionable, human-readable security reasoning.
- **Privacy-First**: No data persistence, no logs, and no tracking.

---

## 🛠️ Installation & Setup (Windows 11 / Linux)

### Prerequisites
- **Python 3.9+**
- **VS Code** (Recommended)
- **Node.js** (Optional, for serving frontend)

### 1. Backend Setup
```bash
# Navigate to backend
cd backend

# Install dependencies
pip install fastapi uvicorn pydantic

# Start the API server
python main.py
```
The server will start at `http://localhost:8000`.

### 2. Frontend Setup
Simply open `frontend/index.html` in any modern browser (Chrome/Edge/Brave).
*Alternatively, use "Live Server" extension in VS Code.*

---

## 🏗️ Architecture
- **Frontend**: Modular CSS3 (Glassmorphism), Vanilla ES6+ JavaScript.
- **Backend**: Python FastAPI with a modular `SecurityIntelligenceEngine`.
- **Logic**: Custom-built entropy and pattern matching algorithms.

---

## 🎓 Interview & Portfolio Guide
If presenting this in an interview, focus on these points:
1. **The Entropy Calculation**: Explain how $E = L \cdot \log_2(R)$ works ($L$=length, $R$=range of characters).
2. **Performance**: Why you used `debounce` on the input to minimize API latency.
3. **Security**: How you ensured no sensitive data is logged or stored.
4. **UX**: The rationale behind the glassmorphism UI—creating a "command center" feel for security.

---

## 🚀 Future Roadmap
- [ ] **Breach Prediction**: API integration with *Have I Been Pwned*.
- [ ] **Web Workers**: Move analysis logic to the client-side background thread for offline mode.
- [ ] **Passphrase Generator**: Generating secure, memorable word combinations.

---

## 📝 License
This project is open-source and intended for educational and security awareness purposes.
