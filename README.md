# Project Icarus 🦅

**Modular AI-Powered OSINT Intelligence Suite**

Project Icarus is an advanced Open Source Intelligence (OSINT) tool designed to aggregate, correlate, and analyze digital footprints. From simple email lookups to deep recursive investigations, Icarus provides a comprehensive view of a target's online presence.

![Project Icarus](https://img.shields.io/badge/Status-Beta-blue)
![Python](https://img.shields.io/badge/Language-Python%203.9%2B-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Key Features

- **Multi-Input Detection**: Automatically identifies Emails, Phone Numbers, Social Handles, and URLs.
- **Recursive Investigation**: Detailed `--depth` search finds new entities (e.g., a handle in a bio) and automatically investigates them.
- **Identity Graph**: Visualizes connections between emails, social profiles, and web mentions.
- **Document Discovery**: Automatically hunts for related documents (PDF, DOCX, XLSX, CSV).
- **AI Analyst Integration** 🧠: Connects to local LLMs (via Ollama) to summarize findings and highlight risks.
- **Module Ecosystem**:
  - **Email**: Breach checks (HIBP), DNS MX analysis, and Social Link discovery.
  - **Phone**: Carrier/Location data (NumVerify) and Web Mention tracking.
  - **Social**: Checks existence across 50+ platforms and scrapes metadata.

---

## 📦 Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/MutentMan/Project-Icarus.git
    cd Project-Icarus
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration**:
    - Rename/Edit `config.yaml` to add your API keys.
    - **HaveIBeenPwned**: [Get Key](https://haveibeenpwned.com/API/v3) (Optional)
    - **NumVerify**: [Get Key](https://numverify.com/) (Optional)

---

## 🛠️ Usage

### Basic Search
Perform a quick lookup on a single target.
```bash
python core.py --input target@example.com
```

### Full Investigation (Recursive)
Dig deeper! This mode extracts new leads (e.g., handles found in bios) and searches them too.
```bash
python core.py --input target@example.com --depth 2
```

### Phone Number Intelligence
Find carrier details and web mentions.
```bash
python core.py --input +14155552671
```

---

## 🧠 AI Analyst Setup (Optional)

Project Icarus can use a local LLM to analyze the final report.

1.  **Install Ollama**: Download from [ollama.com](https://ollama.com/).
2.  **Pull a Model**:
    ```bash
    ollama run llama3
    ```
3.  **Enable in `config.yaml`**:
    ```yaml
    ai_engine:
      enabled: true
      base_url: "http://localhost:11434/v1"
      model: "llama3"
    ```

---

## 📂 Modules

| Module | Description |
| :--- | :--- |
| `core.py` | The brain. Orchestrates searches, handles recursion, and generates reports. |
| `email_search` | checks HIBP breaches, DNS records, and social accounts linked to the email. |
| `phone_search` | Validates numbers, checks carrier/location, and searches the web for mentions. |
| `social_search` | Checks username availability across major sites and scrapes profiles for info. |
| `web_search` | Uses DuckDuckGo to find public mentions and related documents. |
| `ai_analyst` | Connects to an LLM to generate an intelligence summary. |

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**. The user is responsible for ensuring that their activities comply with all applicable local, state, and federal laws. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

---

**Developed by MutentMan**
