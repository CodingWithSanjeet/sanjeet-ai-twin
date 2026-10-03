
# ⚡ AI Digital Twin — Sanjeet Kumar

An interactive AI Digital Twin web application built with **Gradio 6**, **OpenAI GPT-4o / GPT-5**, and **Python**. Grounded in professional career context, resume data, and LinkedIn history, this AI twin allows visitors to chat about experience, projects, technical skills, and background.

---

## ✨ Features

- **Grounded AI Persona**: Answers career, background, and technical questions strictly using verified resume and LinkedIn context.
- **Function Calling (Tools)**:
  - `record_user_details`: Collects visitor contact interest and sends real-time notifications via Pushover.
  - `record_unknown_question`: Logs unanswered questions to track missing knowledge gaps.
- **Modern UI & Aesthetic**:
  - Custom dark theme with animated CSS background & glowing visual effects.
  - Responsive single-card chat layout optimized for desktop and mobile devices.
- **Environment Configurable**: All profile details, social links, and model parameters are dynamically configured via `.env`.

---

## 🛠️ Tech Stack

- **Framework**: [Gradio 6.29.1](https://www.gradio.app/)
- **LLM Engine**: [OpenAI API](https://platform.openai.com/)
- **PDF Extraction**: `pypdf`
- **Package Manager**: [`uv`](https://github.com/astral-sh/uv)

---

## 📂 Project Structure

```text
ai-twin/
├── app.py                      # Main entrypoint
├── pyproject.toml              # UV / Python dependencies
├── requirements.txt            # Dependency specs for deployment
├── .env                        # Environment variables & configuration
├── src/
│   └── ai_twin/
│       ├── app.py              # Main Gradio Blocks UI layout & chat handler
│       ├── context.py          # System prompt & PDF context loader
│       ├── tools.py            # OpenAI function tools & Pushover integration
│       ├── styles.py           # Custom CSS styling, theme, and animations
│       └── assets/             # Profile photo & static media
```

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have [`uv`](https://docs.astral.sh/uv/) installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Environment Variables Setup

Create or update your `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_app_token
HF_TOKEN=your_huggingface_write_token

# Application Configs
MODEL_NAME=gpt-4o-mini
OWNER_NAME=Sanjeet Kumar
OWNER_INITIALS=SK
OWNER_ROLE=AI Engineer
OWNER_EXPERIENCE=7+ years experience
OPEN_TO=Open to AI Engineer roles
LINKEDIN_URL=https://www.linkedin.com/in/ksanjeet
GITHUB_URL=https://github.com/CodingWithSanjeet
EMAIL=sanjeet.kumar.nitt@gmail.com
```

### 3. Run Locally

Start the development server using `uv`:

```bash
uv run app.py
```

Open your browser at `http://127.0.0.1:7863`.

---

## ☁️ Deployment

Deploy directly to **Hugging Face Spaces**:

```bash
uv run gradio deploy --app-file app.py --title ai-twin
```
