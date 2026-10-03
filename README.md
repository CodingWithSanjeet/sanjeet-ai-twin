
# ⚡ AI Digital Twin — Sanjeet Kumar

**🔗 Live demo: [sanjeet-ai-twin.onrender.com](https://sanjeet-ai-twin.onrender.com)** _(hosted on Render's free tier — the first load after inactivity may take ~30–60s to wake up)_

An interactive AI Digital Twin web application built with **Gradio 6**, the **OpenAI API** (default model `gpt-5.4-mini`, configurable via `MODEL_NAME`), and **Python 3.12+**. Its answers are grounded in my LinkedIn profile export (`Linkedin.pdf`) and a written career summary (`summary.txt`), so visitors can chat about my experience, projects, technical skills, and background.

---

## ✨ Features

- **Grounded AI Persona**: Answers career, background, and technical questions using only the LinkedIn PDF and career summary loaded into the system prompt, and steers off-topic questions back to professional topics.
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
sanjeet-ai-twin/
├── app.py                      # Main entrypoint
├── pyproject.toml              # UV / Python dependencies
├── requirements.txt            # Dependency specs for deployment
├── .env                        # Your local secrets & config (not committed)
├── src/
│   └── ai_twin/
│       ├── app.py              # Main Gradio Blocks UI layout & chat handler
│       ├── context.py          # System prompt & PDF context loader
│       ├── Linkedin.pdf        # LinkedIn profile export used as grounding context
│       ├── summary.txt         # Career summary used as grounding context
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
MODEL_NAME=gpt-5.4-mini
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

Open your browser at `http://127.0.0.1:7860` (Gradio's default port; set `GRADIO_SERVER_PORT` to change it).

---

## ☁️ Deployment

The live demo runs on **[Render](https://render.com)** as a free Python web service (auto-deploys from `main`):

- **Build command**: `pip install -r requirements.txt`
- **Start command**: `PYTHONPATH=src python app.py`
- **Environment variables**: `PYTHON_VERSION` (3.12.x), `GRADIO_SERVER_NAME=0.0.0.0`, `GRADIO_SERVER_PORT=7860`, `PORT=7860`, `MODEL_NAME`, plus the secrets `OPENAI_API_KEY`, `PUSHOVER_USER`, `PUSHOVER_TOKEN`

Alternatively, deploy to **Hugging Face Spaces**:

```bash
uv run gradio deploy --app-file app.py --title ai-twin
```
