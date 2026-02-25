# Vulnerability Assessment & Penetration Testing Automation

## Description
An AI-assisted security analysis project that uses LangGraph orchestration to run OWASP Top 10:2025 vulnerability assessments on source code repositories. It generates a consolidated PDF report and can push findings back to your repository workflow.


## Use Cases

- **DevSecOps Integration**: Automate security audits in CI/CD pipelines
- **Code Review Assistance**: Quick vulnerability assessment before production deployment
- **Compliance Reporting**: Generate detailed VAPT reports for security compliance
- **Learning & Training**: Understand common security vulnerabilities in codebases
- **Penetration Testing**: Initial automated reconnaissance for security teams
- **Open Source Auditing**: Analyze third-party dependencies and public repositories

---

## Tech Stack

### Backend & Framework
- **FastAPI** - Modern web framework for REST API
- **Uvicorn** - ASGI server for production deployment
- **Python 3.12+** - Core programming language

### AI & Orchestration
- **LangChain** - AI framework for building LLM applications
- **LangGraph** - Workflow orchestration for multi-agent systems
- **LangSmith** - Observability and monitoring 
- **Ollama** - Local LLM inference server
- **ChatOllama** - LangChain integration for Ollama

### Security Analysis Tools
- **Custom AI Agents** - LLM-powered code analysis for 10 OWASP categories

### Document Generation
- **Markdown2** - Markdown processing for reports

### Version Control
- **GitPython** - Repository cloning and git operations

### Frontend
- **Single-file UI** - `index.html` with inline HTML, CSS, and JavaScript

---

## Web Interface Preview

### User Interface

The VAPT tool features a clean, professional web interface designed for simplicity and efficiency. The single-page application provides an intuitive form-based approach to submit repository analysis requests.

<img width="1152" height="820" alt="Screenshot 2026-02-24 220248" src="https://github.com/user-attachments/assets/e168dbd5-e9ba-478f-b80b-e1041f2b8dcb" />

**Key UI Features:**
- Minimal and modern single-page design
- Responsive layout for all device sizes
- Runtime feedback through status messages
- Clear success/error message display
- Clean professional color scheme


**UI Components:**
1. **Header Section** - Application title with security icon
2. **Input Form**:
   - Repository URL field (GitHub/GitLab)
   - Branch name field (default: main)
   - Access token field (secure input)
3. **Action Button** - "Perform VAPT" with loading state
4. **Status Display** - Success/error messages with appropriate styling

### User Workflow
1. User accesses the web interface at `http://127.0.0.1:8000/`
2. Fills in the repository details (URL, branch, token)
3. Clicks "Perform VAPT" button
4. Status message updates during analysis
5. Receives success message with instructions to check the `vapt_report` branch
6. Can immediately submit another analysis request

---

## Architecture
### System Flow Diagram

<img width="777" height="743" alt="Screenshot 2026-02-25 205225" src="https://github.com/user-attachments/assets/aa473413-1113-4e07-baa3-c6b4f3973a70" />


### Component Interaction
1. **User Interface**: Web form for repository submission
2. **FastAPI Backend**: REST API endpoint to trigger analysis
3. **LangGraph Workflow**: Orchestrates 10 sequential vulnerability analysis nodes
4. **AI Agents**: Each node uses LLM to analyze specific OWASP vulnerability category
5. **Tools**: Two primary tools for file identification and code analysis
6. **Report Generation**: Consolidates findings into professional PDF
7. **Git Integration**: Automatically pushes report to dedicated branch

---

## Project Structure

```
gaurav_vapt/
â”‚
â”œâ”€â”€ graph.py                      # Main LangGraph workflow orchestration
â”œâ”€â”€ langgraph.json                # LangGraph configuration
â”œâ”€â”€ requirements.txt              # Python dependencies
â”‚
â”œâ”€â”€ utils/                        # Core utility modules
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ Agentschema.py           # VAPTState TypedDict schema
â”‚   â”œâ”€â”€ Clonning.py              # Repository cloning with OAuth
â”‚   â”œâ”€â”€ Nodes.py                 # 10 OWASP vulnerability analysis nodes
â”‚   â”œâ”€â”€ Push.py                  # Git push to vapt_report branch
â”‚   â”œâ”€â”€ Reportgen.py             # PDF report generation
â”‚   â”œâ”€â”€ Structfile.py            # Repository structure analyzer
â”‚   â””â”€â”€ Tools.py                 # LangChain tools for file & code analysis
â”‚
â”œâ”€â”€ webui_fastapi/               # Web interface
â”‚   â”œâ”€â”€ main.py                  # FastAPI application
â”‚   â”œâ”€â”€ index.html               # Frontend UI
â”‚
â”œâ”€â”€ .gitignore                   # Git ignore rules
â””â”€â”€ README.md                    # This file
```

### Generated Runtime Files (Not in Git)
```
cloned_code/                     # Cloned repository for analysis
Node_results/                    # Individual node analysis results (rv1.md - rv10.md)
repo_structure.txt               # Generated repository structure
VAPT_Final_Report.pdf            # Final consolidated report
```

---

## Installation & Setup

### Prerequisites
- **Python 3.12+**
- **Git**
- **Ollama** (for running local LLM)
- **Active Internet Connection** (for cloning repositories)

### Step 1: Clone the Repository
```bash
git clone https://github.com/gauravbondegit/vapt_automation.git
cd gaurav_vapt
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Ollama (Local LLM)

#### Install Ollama
Visit [Ollama.ai](https://ollama.ai) and download for your OS.

**Windows/Mac:**
```bash
# Download and install from https://ollama.ai/download
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Pull the Required Model
```bash
ollama pull gpt-oss:20b
```

#### Start Ollama Server
```bash
ollama serve
```
The server will run on `http://localhost:11434` by default.

#### Configure Ollama IP (For Remote/Network Setup)
Edit `utils/Nodes.py` and `utils/Tools.py`:
```python
# For local setup
OLLAMA_IP = "localhost"  # or "127.0.0.1"

# For remote network host
OLLAMA_IP = "192.168.1.100"  # Your Ollama server IP
```

### Step 5: Setup LangSmith (Optional - For Observability)

#### Create LangSmith Account
1. Visit [smith.langchain.com](https://smith.langchain.com)
2. Create a free account
3. Generate an API key from settings

#### Configure Environment Variables
Create a `.env` file in the project root:
```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your-langsmith-api-key-here
LANGCHAIN_PROJECT=gaurav-vapt
```

**Note:** By default, tracing is disabled in `graph.py`:
```python
os.environ["LANGCHAIN_TRACING_V2"] = "false"
```

To enable LangSmith tracing, change to `"true"` or load from `.env`.

## How to Run

### Method 1: Web UI (Recommended)

#### Start the FastAPI Server
```bash
uvicorn webui_fastapi.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Access the Web Interface
Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

#### Submit Analysis Request
1. **Repository URL**: Enter the Git repository URL (GitHub/GitLab)
2. **Branch Name**: Specify the branch (e.g., `main`, `master`, `develop`)
3. **Access Token**: Provide your Git access token for private repos
4. Click **"Perform VAPT"**

#### Check Results
The system will:
- Clone the repository
- Analyze for 10 OWASP vulnerability categories
- Generate a PDF report
- Push the report to a new branch: `vapt_report`

You'll receive a success message once complete.

### Method 2: Direct Graph Execution (CLI)

Edit `graph.py` with your repository details:
```python
initial_state = {
    "repo_url": "https://github.com/username/repo.git",
    "branch_name": "main",
    "access_token": "your-token-here",
    # ... other fields
}
```

Run:
```bash
python graph.py
```

---

## Features

### Comprehensive OWASP Top 10 Coverage
- **v1: Broken Access Control** - Privilege escalation, IDOR, unprotected routes
- **v2: Security Misconfiguration** - Default credentials, debug mode, weak headers
- **v3: Supply Chain Failures** - Vulnerable dependencies, outdated libraries
- **v4: Cryptographic Failures** - Weak algorithms, hardcoded keys, insecure modes
- **v5: Injection Vulnerabilities** - SQL injection, command injection, XSS
- **v6: Insecure Design** - Logic flaws, trust boundary violations
- **v7: Authentication Failures** - Weak sessions, JWT issues, credential exposure
- **v8: Integrity Failures** - Insecure deserialization, unsigned updates
- **v9: Logging & Alerting Failures** - Missing audit logs, log injection
- **v10: Exception Mishandling** - Information leakage, fail-open logic

### AI-Powered Analysis
- **LLM-Driven Code Review**: Uses Ollama's `gpt-oss:20b` model for intelligent analysis
- **Context-Aware Detection**: Understands code patterns beyond simple regex matching
- **Actionable Remediation**: Provides secure code fixes with explanations

### Professional Reporting
- **PDF Generation**: Clean, structured vulnerability reports
- **Severity Scoring**: 0-10 scale with Low/Medium/High/Critical ratings
- **Code Snippets**: Exact vulnerable code locations with line numbers
- **Technical Descriptions**: Clear explanations of security implications

### Automated Workflow
- **One-Click Analysis**: Simple web form submission
- **Git Integration**: Automatic cloning and report push
- **Stateful Orchestration**: LangGraph manages complex multi-step workflow
- **Error Handling**: Graceful failure recovery and user notifications

### Developer-Friendly
- **FastAPI REST API**: Easy integration with CI/CD pipelines
- **Minimal Dependencies**: Lightweight tech stack
- **Customizable Agents**: Easily extend or modify analysis nodes
- **LangSmith Support**: Optional observability for debugging

### Security & Privacy
- **Local LLM**: Code analysis happens on your infrastructure (Ollama)
- **No Data Leakage**: Repository data never sent to external APIs
- **Token Security**: Access tokens used only for Git operations
- **Clean Workspace**: Automatic cleanup of cloned repositories

---

## Configuration

### Customizing Ollama Model
Edit `utils/Nodes.py` and `utils/Tools.py`:
```python
model = ChatOllama(
    model="gpt-oss:20b",  # Change to your preferred model
    temperature=0,         # Adjust randomness (0 = deterministic)
    timeout=300           # Request timeout in seconds
)
```

### Adjusting Analysis Depth
In each node function (e.g., `v1_bac`), modify prompts in `system_prompt` to:
- Increase/decrease focus areas
- Add custom vulnerability patterns
- Change report format

### Changing Output Paths
Edit `graph.py`:
```python
initial_state = {
    "repo_path": os.path.abspath("cloned_code"),           # Clone destination
    "file_struct_path": os.path.abspath("repo_structure.txt"),  # Structure file
    "node_results": "Node_results",                        # Individual results
    "final_report": "VAPT_Final_Report.pdf",              # Final report name
}
```

---

## API Documentation

### REST API Endpoint

#### `GET /health`

**Response (200):**
```json
{
  "status": "ok"
}
```

#### `POST /perform`

**Request Body:**
```json
{
  "repo_url": "https://github.com/username/repository.git",
  "branch_name": "main",
  "access_token": "your_github_token_here"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "VAPT analysis completed.",
  "report_url": "/reports/VAPT_Final_Report_3df0e109-83a8-4928-a170-9c8cb7f6c57d.pdf"
}
```

#### `GET /reports/{report_file_name}`

Downloads the generated PDF report returned in `report_url`.

**Error Response (400/404):**
```json
{
  "detail": "Error message"
}
```

---


### Areas for Enhancement
- [ ] Add support for more LLM providers (OpenAI, Anthropic)
- [ ] Implement real-time progress updates via WebSockets
- [ ] Add database storage for historical reports
- [ ] Create Docker containerization
- [ ] Integrate more security scanning tools (Trivy, Snyk)
- [ ] Add authentication to web UI
- [ ] Implement scheduled scans

---

## License

This project is licensed under the MIT License. 

---

## End Note

**AI-Powered VAPT Tool** represents a modern approach to automated security analysis, combining the power of Large Language Models with established security principles. By leveraging local LLM inference through Ollama, this tool ensures your code never leaves your infrastructure while still benefiting from advanced AI-driven vulnerability detection.

Whether you're a solo developer looking to improve code security, a security professional conducting audits, or a DevOps engineer building secure CI/CD pipelines, this tool provides actionable insights to strengthen your application's security posture.

**Remember:** Automated tools complement but don't replace human security expertise. Always review findings critically and conduct thorough manual testing for production systems.

Stay secure! ðŸ›¡ï¸

---

**â­ Star this repository if you find it useful!**

**ðŸ”„ Keep your dependencies updated and scan regularly!**

**ðŸš€ Happy Secure Coding!**

