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
    - Use the **Settings** sidebar in the Web UI or edit `config.yaml` manually.
    - **HaveIBeenPwned**: [Get Key](https://haveibeenpwned.com/API/v3)
    - **NumVerify**: [Get Key](https://numverify.com/)

---

## 🛠️ Usage

### Web Dashboard (Recommended)
Launch the professional OSINT dashboard:
```bash
streamlit run app.py
```

### CLI Mode
Perform a quick lookup from your terminal.
```bash
python core.py --input target@example.com
```

### Full Investigation (Recursive)
Dig deeper! This mode extracts new leads (e.g., handles found in bios) and searches them too.
```bash
python core.py --input target@example.com --depth 2
```

### Full Command List

| Command | Description |
| :--- | :--- |
| `python core.py --input <target>` | **Basic Search**: Detects type and runs standard modules. |
| `python core.py -i <target>` | Short flag for input. |
| `python core.py -i <target> --depth 2` | **Recursive Search**: Finds new entities and searches them (Level 2). |
| `python core.py -i <target> -d 3` | Deep recursive search (Level 3). |

### Examples

**1. Email Investigation**
Checks breaches, social accounts, and DNS records.
```bash
python core.py --input target@example.com
```

**2. Phone Number Investigation**
Checks carrier, location, and web mentions.
```bash
python core.py --input +14155552671
```

**3. Social Handle Investigation**
Checks 50+ sites and scrapes profiles.
```bash
python core.py --input octocat
```

**4. Full Recursive Investigation**
Ideal for deep dives. Finds an email > finds a handle > searches handle > finds a new email...
```bash
python core.py --input target@example.com --depth 2
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
| `core.py` | The brain. Orchestrates searches for CLI and UI. |
| `app.py` | **Streamlit Dashboard**. Professional web interface. |
| `email_search` | Checks HIBP breaches, DNS records, and social accounts. |
| `phone_search` | Validates numbers, checks carrier, and web mentions. |
| `social_search` | OSINT handle check across 50+ sites. |
| `web_search` | Hunts for mentions and related documents. |
| `ai_analyst` | AI-powered intelligence summary generator. |

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**. The user is responsible for ensuring that their activities comply with all applicable local, state, and federal laws. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

---

**Developed by MutentMan**
