import os
from openai import OpenAI
from .context import TWIN_SYSTEM_PROMPT
from .tools import tools, handle_tool_calls
from .styles import CSS, JS, EXAMPLES, HEAD, THEME, CHAT_PLACEHOLDER, avatar_images
from dotenv import load_dotenv
from html import escape
from pathlib import Path
import base64
import gradio as gr

load_dotenv(override=True)

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5.4-mini")
openai = OpenAI()
system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]

# --------------------------------------------------------------------------- #
# Profile constants (loaded from environment variables / .env)
# --------------------------------------------------------------------------- #
OWNER_NAME = os.getenv("OWNER_NAME", "Sanjeet Kumar")
OWNER_INITIALS = os.getenv("OWNER_INITIALS", "SK")
# Profile photo used for the header logo mark and the bot chat avatar.
# Put it at <this package>/assets/profile.jpg (square, ~400x400; .png/.jpeg/.webp also work).
# Missing file -> initials badge + a printed warning with the expected path.
_HERE = Path(__file__).resolve().parent
PROFILE_IMAGE_CANDIDATES = [
    _HERE / "assets" / "profile.png",
    _HERE / "assets" / "profile.jpg",
    _HERE / "assets" / "profile.jpeg",
    _HERE / "assets" / "profile.webp",
    Path.cwd() / "assets" / "profile.png",
    Path.cwd() / "assets" / "profile.jpg",
]


def _find_profile_image():
    for candidate in PROFILE_IMAGE_CANDIDATES:
        if candidate.is_file():
            return candidate
    print(
        "[ai-twin] WARNING: profile photo not found, falling back to initials.\n"
        f"[ai-twin]   Expected: {PROFILE_IMAGE_CANDIDATES[0]}\n"
        "[ai-twin]   Also tried: " + ", ".join(str(c) for c in PROFILE_IMAGE_CANDIDATES[1:])
    )
    return None


PROFILE_IMAGE = _find_profile_image()  # Path or None
OWNER_ROLE = os.getenv("OWNER_ROLE", "AI Engineer")
OWNER_EXPERIENCE = os.getenv("OWNER_EXPERIENCE", "7+ years experience")
OPEN_TO = os.getenv("OPEN_TO", "Open to AI Engineer roles")
TAGLINE = os.getenv("TAGLINE", "")

LINKEDIN_URL = os.getenv("LINKEDIN_URL", "https://www.linkedin.com/in/ksanjeet")
GITHUB_URL = os.getenv("GITHUB_URL", "https://github.com/CodingWithSanjeet")
EMAIL = os.getenv("EMAIL", "sanjeet.kumar.nitt@gmail.com")
RESUME_URL = os.getenv("RESUME_URL", "")

FOOTER_TEXT = os.getenv("FOOTER_TEXT", "Powered by OpenAI · Answers grounded in my resume & LinkedIn")

# --------------------------------------------------------------------------- #
# Header / footer HTML (built from the constants above)
# --------------------------------------------------------------------------- #
_ICONS = {
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>',
    "github": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .3a12 12 0 0 0-3.8 23.38c.6.12.83-.26.83-.57L9 21.07c-3.34.72-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.08-.74.09-.73.09-.73 1.2.09 1.83 1.24 1.83 1.24 1.07 1.83 2.81 1.3 3.49 1 .1-.78.42-1.31.76-1.6-2.67-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.14-.3-.54-1.52.1-3.18 0 0 1-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.28-1.55 3.29-1.23 3.29-1.23.64 1.66.24 2.88.12 3.18a4.65 4.65 0 0 1 1.23 3.22c0 4.61-2.8 5.63-5.48 5.92.42.36.81 1.1.81 2.22l-.01 3.29c0 .31.2.69.82.57A12 12 0 0 0 12 .3"/></svg>',
    "email": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="3"/><path d="m22 7-10 6L2 7"/></svg>',
    "resume": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M12 18v-6M9 15l3 3 3-3"/></svg>',
}


def _btn(url, label, icon, kind="ghost", icon_only=False):
    if not url:
        return ""
    ext = "" if url.startswith("mailto:") else ' target="_blank" rel="noopener noreferrer"'
    cls = f"twin-btn twin-btn-{kind}" + (" twin-btn-icon" if icon_only else "")
    return (
        f'<a class="{cls}" href="{escape(url)}"{ext} title="{escape(label)}" aria-label="{escape(label)}">'
        f"{_ICONS[icon]}<span>{escape(label)}</span></a>"
    )


def _profile_data_uri():
    """Embed the photo as a data URI so the header needs no Gradio file serving."""
    if not PROFILE_IMAGE or not PROFILE_IMAGE.is_file():
        return ""
    mime = {".png": "image/png", ".webp": "image/webp"}.get(PROFILE_IMAGE.suffix.lower(), "image/jpeg")
    return f"data:{mime};base64," + base64.b64encode(PROFILE_IMAGE.read_bytes()).decode("ascii")


def build_header_html():
    first, _, rest = OWNER_NAME.partition(" ")
    wordmark = f'<span class="first">{escape(first)}</span>' + (f' <span class="last">{escape(rest)}</span>' if rest else "")
    open_pill = f'<span class="twin-pill twin-pill-open"><i></i>{escape(OPEN_TO)}</span>' if OPEN_TO else ""
    exp = f'<i class="sep"></i><span>{escape(OWNER_EXPERIENCE)}</span>' if OWNER_EXPERIENCE else ""
    tagline = f'<p class="twin-tagline">{escape(TAGLINE)}</p>' if TAGLINE else ""
    photo = _profile_data_uri()
    status = '<span class="twin-status" title="Online"></span>'
    if photo:
        mark = f'<div class="twin-mark has-photo"><span class="twin-photo"><img src="{photo}" alt="{escape(OWNER_NAME)}"></span>{status}</div>'
    else:
        mark = f'<div class="twin-mark" aria-hidden="true"><b>{escape(OWNER_INITIALS)}</b>{status}</div>'
    actions = "".join([
        _btn(f"mailto:{EMAIL}" if EMAIL else "", "Get in touch", "email", "primary"),
        _btn(LINKEDIN_URL, "LinkedIn", "linkedin", icon_only=True),
        _btn(GITHUB_URL, "GitHub", "github", icon_only=True),
        _btn(RESUME_URL, "Resume", "resume", icon_only=True),
    ])
    return f"""
<header class="twin-hero">
  <div class="twin-hero-main">
    {mark}
    <div class="twin-id">
      <div class="twin-eyebrow"><span class="twin-pill twin-pill-ai">✦ AI Digital Twin</span>{open_pill}</div>
      <h1 class="twin-name">{wordmark}</h1>
      <p class="twin-role">{escape(OWNER_ROLE)}{exp}</p>
    </div>
    <nav class="twin-actions" aria-label="Contact links">{actions}</nav>
  </div>
  {tagline}
</header>"""


CHAT_HEAD_HTML = f"""
<div class="twin-chat-head">
  <div class="twin-chat-head-left"><span class="dot"></span><b>Chat with my AI twin</b><small>· usually replies in a few seconds</small></div>
  <span class="twin-kbd">Enter to send · Shift+Enter for new line</span>
</div>"""

# FOOTER_HTML = f'<div class="twin-footer">{"<span class=sep>·</span>".join(f"<span>{escape(p.strip())}</span>" for p in FOOTER_TEXT.split("·"))}</div>'


def chat(message, history):
    messages = system + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(message)
        messages.extend(results)
        response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
    return response.choices[0].message.content


def build_demo():
    with gr.Blocks(title=f"{OWNER_NAME} | AI Twin", fill_height=True) as demo:
        with gr.Column(elem_id="twin-card"):  # one card: header on top, chat below
            gr.HTML(build_header_html(), elem_id="twin-hero")
            gr.HTML(CHAT_HEAD_HTML, elem_id="twin-chat-head")
            gr.ChatInterface(
                chat,
                examples=EXAMPLES,
                chatbot=gr.Chatbot(
                    show_label=False,
                    elem_id="twin-chatbot",
                    height="100%",
                    scale=1,
                    layout="bubble",
                    placeholder=CHAT_PLACEHOLDER,
                    avatar_images=avatar_images(OWNER_INITIALS, bot_image=PROFILE_IMAGE),
                    feedback_options=None,
                ),
                textbox=gr.Textbox(
                    placeholder="Ask about my experience, skills or projects…",
                    show_label=False,
                    lines=1,
                    max_lines=6,
                    elem_id="twin-input",
                    submit_btn=True,
                    stop_btn=True,
                ),
                fill_height=True,
            )
        # gr.HTML(FOOTER_HTML, elem_id="twin-footer")
    return demo


def main():
    build_demo().launch(css=CSS, js=JS, head=HEAD, theme=THEME, footer_links=[])


if __name__ == "__main__":
    main()
