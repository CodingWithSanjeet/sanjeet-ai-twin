"""Visual layer for the AI Digital Twin (Gradio 6.29.1).

Everything that the Gradio theme API can express lives in ``THEME``; ``CSS`` only
covers what themes can't (hero header, chat card, bubble shapes, starter cards,
input pill, footer, responsive tweaks). Selectors were taken from the rendered
Gradio 6.29.1 DOM, not guessed.
"""

import os
import shutil
import tempfile

import gradio as gr

# --------------------------------------------------------------------------- #
# Starter prompts (sent verbatim to the model when clicked)
# --------------------------------------------------------------------------- #
EXAMPLES = [
    "Tell me about your background and experience.",
    "What kinds of projects are you working on now?",
    "What are your strongest technical skills?",
    "How can I get in touch with you?",
]

# Shown inside the empty chat, above the starter cards (Markdown).
CHAT_PLACEHOLDER = (
    "### 👋 Hi, I'm Sanjeet's AI twin\n"
    "Ask me about my experience, the products I've shipped, my tech stack, "
    "or what I'm looking for next. Pick a question below or type your own."
)

# --------------------------------------------------------------------------- #
# Theme: does the heavy lifting (colors, fonts, radii, inputs, buttons)
# --------------------------------------------------------------------------- #
_SANS = [gr.themes.GoogleFont("Plus Jakarta Sans"), "ui-sans-serif", "system-ui", "sans-serif"]
_MONO = [gr.themes.GoogleFont("JetBrains Mono"), "ui-monospace", "SFMono-Regular", "monospace"]

# Brand hues from the portfolio (sanjeet-kumar-nitt.netlify.app): aqua #08fdd8,
# steel blue #539cd4, pink #fd1056. Used here as light tints + darker readable text shades.
PORTFOLIO_BLUE = gr.themes.Color(
    c50="#eef6fc", c100="#d4e7f6", c200="#b0d3ef", c300="#8cc0e8", c400="#6eaede", c500="#539cd4",
    c600="#3a83c4", c700="#2a6aa6", c800="#1d5f97", c900="#134e7c", c950="#0b3558", name="portfolio_blue",
)
PORTFOLIO_AQUA = gr.themes.Color(
    c50="#e6fffb", c100="#c9fbf3", c200="#9ff7e9", c300="#5ff2dc", c400="#22e3c6", c500="#0fc5ab",
    c600="#0a9a86", c700="#04776a", c800="#065f55", c900="#084e47", c950="#022f2b", name="portfolio_aqua",
)

THEME = gr.themes.Soft(
    primary_hue=PORTFOLIO_BLUE,
    secondary_hue=PORTFOLIO_AQUA,
    neutral_hue=gr.themes.colors.slate,
    radius_size=gr.themes.sizes.radius_lg,
    text_size=gr.themes.sizes.text_md,
    font=_SANS,
    font_mono=_MONO,
).set(
    # page + surfaces
    body_background_fill="#f7fafc",
    body_text_color="#0f172a",
    body_text_color_subdued="#64748b",
    background_fill_primary="#ffffff",
    background_fill_secondary="#f8fbfd",
    border_color_primary="#e3eaf2",
    border_color_accent_subdued="transparent",
    color_accent_soft="#eef6fc",
    # blocks
    block_background_fill="#ffffff",
    block_border_width="0px",
    block_shadow="none",
    block_radius="20px",
    layout_gap="16px",
    # chat
    chatbot_text_size="15px",
    code_background_fill="#eef6fc",
    link_text_color="#1d5f97",
    link_text_color_hover="#134e7c",
    link_text_color_visited="#1d5f97",
    # input
    input_background_fill="#ffffff",
    input_background_fill_focus="#ffffff",
    input_border_color="#dbe4ee",
    input_border_color_focus="#8cc0e8",
    input_border_width="1px",
    input_shadow="none",
    input_shadow_focus="0 0 0 4px rgba(83, 156, 212, .18)",
    input_placeholder_color="#94a3b8",
    input_radius="16px",
    # buttons
    button_primary_background_fill="linear-gradient(135deg, #dcfdf7 0%, #dbeafa 100%)",
    button_primary_background_fill_hover="linear-gradient(135deg, #c3faf0 0%, #c4dcf5 100%)",
    button_primary_text_color="#134e7c",
    button_secondary_background_fill="#ffffff",
    button_secondary_background_fill_hover="#f1f5f9",
    button_secondary_border_color="#dbe4ee",
    button_transition="all .18s ease",
    loader_color="#539cd4",
)

# Fonts for display headings (theme already loads Plus Jakarta Sans / JetBrains Mono).
# Page-level CSS that must NOT go through Gradio's css= processing: Gradio re-scopes
# @media rules under the app container and silently drops @supports, which would break
# body/html pseudo-element layers, prefers-reduced-motion and the Firefox scrollbar rule.
BACKGROUND_CSS = r"""
/* ===== animated dark backdrop (page only; the card is above it and static) =====
   6 fixed, pointer-events:none layers on html/body/gradio-app pseudo-elements.
   Orbs are soft radial gradients (no filter: blur) animated with transform only. */
gradio-app { background: transparent !important; }
.gradio-container { position: relative; z-index: 1; }

html::before, html::after, body::before, gradio-app::before {
  content: ""; position: fixed; z-index: 0; pointer-events: none;
  border-radius: 50%; will-change: transform; backface-visibility: hidden;
}
/* aqua orb, top-left */
html::before {
  width: 62vmax; height: 52vmax; left: -18vmax; top: -22vmax;
  background: radial-gradient(ellipse at center, rgba(8, 253, 216, .17) 0%, rgba(8, 253, 216, .06) 38%, transparent 68%);
  animation: twin-orb-a 32s ease-in-out infinite alternate;
}
/* steel-blue orb, right */
html::after {
  width: 58vmax; height: 64vmax; right: -22vmax; top: 4vmax;
  background: radial-gradient(ellipse at center, rgba(83, 156, 212, .20) 0%, rgba(83, 156, 212, .07) 40%, transparent 68%);
  animation: twin-orb-b 38s ease-in-out infinite alternate;
}
/* pink orb, bottom-right */
body::before {
  width: 50vmax; height: 42vmax; right: -10vmax; bottom: -24vmax;
  background: radial-gradient(ellipse at center, rgba(253, 16, 86, .13) 0%, rgba(253, 16, 86, .045) 40%, transparent 68%);
  animation: twin-orb-c 27s ease-in-out infinite alternate;
}
/* blue/aqua orb, bottom-left */
gradio-app::before {
  width: 46vmax; height: 46vmax; left: -16vmax; bottom: -20vmax;
  background: radial-gradient(circle at center, rgba(83, 156, 212, .12) 0%, rgba(8, 253, 216, .05) 42%, transparent 68%);
  animation: twin-orb-d 23s ease-in-out infinite alternate;
}
/* drifting star field (tiles of 200/300/600px -> seamless 600px loop) */
body::after {
  content: ""; position: fixed; z-index: 0; pointer-events: none;
  left: 0; right: 0; top: -600px; height: calc(100vh + 600px);
  background-image:
    radial-gradient(1px 1px at 20px 30px, rgba(255, 255, 255, .55), transparent 60%),
    radial-gradient(1px 1px at 140px 120px, rgba(8, 253, 216, .55), transparent 60%),
    radial-gradient(1.5px 1.5px at 90px 170px, rgba(255, 255, 255, .45), transparent 60%),
    radial-gradient(1px 1px at 230px 60px, rgba(83, 156, 212, .6), transparent 60%),
    radial-gradient(1.5px 1.5px at 260px 250px, rgba(255, 255, 255, .35), transparent 60%),
    radial-gradient(1px 1px at 420px 380px, rgba(253, 16, 86, .5), transparent 60%),
    radial-gradient(1px 1px at 510px 140px, rgba(255, 255, 255, .4), transparent 60%);
  background-size: 200px 200px, 200px 200px, 300px 300px, 300px 300px, 300px 300px, 600px 600px, 600px 600px;
  will-change: transform, opacity;
  animation: twin-stars-drift 140s linear infinite, twin-stars-twinkle 7s ease-in-out infinite alternate;
}
/* faint grid, slowly panning, faded towards the edges */
gradio-app::after {
  content: ""; position: fixed; z-index: 0; pointer-events: none;
  left: -64px; top: -64px; width: calc(100vw + 128px); height: calc(100vh + 128px);
  background-image:
    linear-gradient(rgba(255, 255, 255, .035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, .035) 1px, transparent 1px);
  background-size: 64px 64px;
  -webkit-mask-image: radial-gradient(ellipse 70% 60% at 50% 45%, #000 20%, transparent 75%);
  mask-image: radial-gradient(ellipse 70% 60% at 50% 45%, #000 20%, transparent 75%);
  will-change: transform;
  animation: twin-grid-pan 24s linear infinite;
}

@keyframes twin-orb-a { 0% { transform: translate3d(0, 0, 0) rotate(0deg) scale(1); }
  50% { transform: translate3d(14vw, 10vh, 0) rotate(25deg) scale(1.12); }
  100% { transform: translate3d(6vw, 22vh, 0) rotate(-10deg) scale(.94); } }
@keyframes twin-orb-b { 0% { transform: translate3d(0, 0, 0) rotate(0deg) scale(1); }
  50% { transform: translate3d(-12vw, 14vh, 0) rotate(-30deg) scale(1.1); }
  100% { transform: translate3d(-4vw, -8vh, 0) rotate(15deg) scale(.92); } }
@keyframes twin-orb-c { 0% { transform: translate3d(0, 0, 0) rotate(0deg) scale(1); }
  50% { transform: translate3d(-16vw, -10vh, 0) rotate(20deg) scale(1.15); }
  100% { transform: translate3d(-6vw, -18vh, 0) rotate(-15deg) scale(1); } }
@keyframes twin-orb-d { 0% { transform: translate3d(0, 0, 0) scale(1); }
  50% { transform: translate3d(12vw, -12vh, 0) scale(1.18); }
  100% { transform: translate3d(20vw, -4vh, 0) scale(.9); } }
@keyframes twin-stars-drift { from { transform: translate3d(0, 0, 0); } to { transform: translate3d(0, 600px, 0); } }
@keyframes twin-stars-twinkle { from { opacity: .55; } to { opacity: 1; } }
@keyframes twin-grid-pan { from { transform: translate3d(0, 0, 0); } to { transform: translate3d(64px, 64px, 0); } }

@media (prefers-reduced-motion: reduce) {
  html::before, html::after, body::before, body::after, gradio-app::before, gradio-app::after { animation: none !important; }
  body::after { opacity: .7; }
  #twin-card, #twin-chatbot .message-row.bubble, .twin-status { animation: none !important; }
}

/* Firefox scrollbars (Chromium would ignore ::-webkit-scrollbar if this applied there) */
@supports (-moz-appearance: none) {
  #twin-card *, #twin-chatbot .bubble-wrap { scrollbar-width: thin; scrollbar-color: #9ec7ea transparent; }
}
"""

HEAD = """
<meta name="color-scheme" content="light">
<meta name="description" content="Chat with Sanjeet Kumar's AI digital twin — AI Engineer.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<style id="twin-background">""" + BACKGROUND_CSS + """</style>
"""


# --------------------------------------------------------------------------- #
# Chat avatars (SVG files generated once; Gradio copies them into its cache)
# --------------------------------------------------------------------------- #
_BOT_AVATAR_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#dcfdf7"/><stop offset="1" stop-color="#dbeafa"/></linearGradient></defs>
<circle cx="32" cy="32" r="31" fill="url(#g)" stroke="#b9e3f2" stroke-width="2"/>
<text x="32" y="41" text-anchor="middle" font-family="Sora,Outfit,Plus Jakarta Sans,Arial,sans-serif"
 font-size="24" font-weight="800" fill="#1d5f97" letter-spacing="0.5">{initials}</text></svg>"""

_USER_AVATAR_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<circle cx="32" cy="32" r="32" fill="#eef2f7"/>
<circle cx="32" cy="25" r="10" fill="#a8b5c7"/>
<path d="M13 52c3-10 11-15 19-15s16 5 19 15" fill="#a8b5c7"/></svg>"""


def avatar_images(initials: str = "SK", bot_image=None):
    """Return (user_avatar_path, bot_avatar_path) for gr.Chatbot(avatar_images=...).

    If ``bot_image`` points to an existing file (e.g. the profile photo) it is used for
    the bot; otherwise a pastel initials badge is generated.
    """
    folder = os.path.join(tempfile.gettempdir(), "ai_twin_avatars")
    os.makedirs(folder, exist_ok=True)
    paths = []
    for name, svg in (("user.svg", _USER_AVATAR_SVG), (f"bot_{initials}.svg", _BOT_AVATAR_SVG.format(initials=initials))):
        path = os.path.join(folder, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        paths.append(path)
    if bot_image and os.path.isfile(str(bot_image)):
        # Copy next to the generated SVGs (system temp dir) so Gradio can always serve it,
        # regardless of the working directory the app is launched from.
        ext = os.path.splitext(str(bot_image))[1].lower() or ".jpg"
        dest = os.path.join(folder, f"bot_photo{ext}")
        shutil.copyfile(str(bot_image), dest)
        paths[1] = dest
    return tuple(paths)


# --------------------------------------------------------------------------- #
# CSS: only what the theme can't do
# --------------------------------------------------------------------------- #
CSS = r"""
/* ---------- 0. tokens + page ---------- */
:root, .dark {
  --twin-ink: #0f172a;
  --twin-muted: #64748b;
  --twin-line: #e3eaf2;
  --twin-primary: #1d5f97;
  --twin-on-pastel: #134e7c;
  --twin-accent: #04776a;      /* aqua-family text */
  --twin-pink: #c4083f;        /* pink-family text */
  --twin-grad: linear-gradient(135deg, #dcfdf7 0%, #dbeafa 100%);   /* pastel aqua -> pastel blue */
  --twin-grad-hover: linear-gradient(135deg, #c3faf0 0%, #c4dcf5 100%);
  --twin-accent-line: linear-gradient(90deg, #08fdd8 0%, #539cd4 55%, #fd1056 100%);   /* portfolio signature */
  --twin-brand-grad: linear-gradient(120deg, #0a9a86 0%, #3a83c4 60%, #e30e4d 100%);
  --twin-card-shadow:
    0 0 0 1px rgba(8, 253, 216, .10),          /* faint aqua hairline on the dark page */
    0 0 36px -6px rgba(83, 156, 212, .22),     /* soft steel-blue glow */
    0 30px 60px -20px rgba(0, 0, 0, .65);      /* deep drop shadow */
  --twin-brand: "Sora", "Outfit", "Plus Jakarta Sans", ui-sans-serif, system-ui, sans-serif;
  --twin-display: "Outfit", "Plus Jakarta Sans", ui-sans-serif, system-ui, sans-serif;
  color-scheme: light;
}
/* dark page (portfolio look) around a light card */
html, body, gradio-app {
  background-color: #1a1a1a !important;
}
body, gradio-app {
  background:
    radial-gradient(760px 460px at 6% -10%, rgba(8, 253, 216, .10), transparent 62%),
    radial-gradient(720px 440px at 104% 4%, rgba(83, 156, 212, .13), transparent 60%),
    radial-gradient(640px 420px at 92% 108%, rgba(253, 16, 86, .07), transparent 62%),
    radial-gradient(560px 380px at -6% 104%, rgba(83, 156, 212, .06), transparent 62%),
    linear-gradient(160deg, #1d1d1d 0%, #1a1a1a 100%) !important;
  background-attachment: fixed !important;
}

/* ---------- viewport fit: whole app = 100dvh, only the message list scrolls ---------- */
html, body { height: 100%; margin: 0; }
gradio-app { display: block; height: 100vh; height: 100dvh; }
.gradio-container {
  width: 100% !important;
  max-width: 1040px !important;
  margin: 0 auto !important;
  padding: 0 !important;
  background: transparent !important;
  height: 100vh !important; height: 100dvh !important;
  min-height: 0 !important;
  display: flex !important; flex-direction: column;
  overflow: hidden;
}
.gradio-container .main.app {
  flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column;
  padding: 20px 20px 6px !important; background: transparent;
}
.gradio-container .main.app > .wrap,
.gradio-container main.contain,
.gradio-container main.contain > .column {
  flex: 1 1 auto; min-height: 0 !important; display: flex; flex-direction: column; flex-wrap: nowrap; gap: 10px;
}
#twin-card > .column { flex: 1 1 auto; min-height: 0 !important; flex-wrap: nowrap; gap: 0 !important; }
#twin-chatbot { flex: 1 1 auto; min-height: 0 !important; height: auto !important; max-height: none !important; }
#twin-chatbot > .wrapper, #twin-chatbot .bubble-wrap { min-height: 0; }
#twin-footer { flex: 0 0 auto; }
#twin-footer, #twin-footer .html-container, #twin-footer .prose { background: transparent !important; border: none !important; box-shadow: none !important; }
/* note: inside @media blocks Gradio scopes rules as descendants of .gradio-container,
   so responsive rules target .main.app instead of .gradio-container itself */

@keyframes twin-rise { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
@keyframes twin-pulse { 0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, .55); } 70% { box-shadow: 0 0 0 9px rgba(34, 197, 94, 0); } 100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); } }

/* ---------- 1. one card: header (top) + chat (bottom) ---------- */
#twin-hero, #twin-footer, #twin-hero .html-container, #twin-footer .html-container, #twin-chat-head .html-container { padding: 0 !important; }
#twin-hero, #twin-chat-head { border: none !important; box-shadow: none !important; border-radius: 0 !important; margin: 0 !important; }
#twin-hero .prose, #twin-footer .prose { max-width: none; }
#twin-card {
  position: relative;
  background: #ffffff;
  border: 1px solid var(--twin-line);
  border-radius: 24px;
  box-shadow: var(--twin-card-shadow);
  padding: 0 !important;
  gap: 0 !important;
  overflow: hidden;
  flex: 1 1 auto; min-height: 0 !important; display: flex; flex-direction: column; flex-wrap: nowrap;
  animation: twin-rise .5s ease both;
}
#twin-card > div { flex-shrink: 0; }
#twin-card > .column { flex-shrink: 1; }
#twin-card::before {             /* gradient hairline across the top of the card */
  content: ""; position: absolute; inset: 0 0 auto 0; height: 4px; background: var(--twin-accent-line); z-index: 2;
}
.twin-hero {
  position: relative; overflow: hidden;
  padding: 26px 28px 22px;
  background:
    radial-gradient(520px 220px at 100% 0%, rgba(83, 156, 212, .12), transparent 70%),
    radial-gradient(420px 200px at 0% 0%, rgba(8, 253, 216, .10), transparent 70%),
    #ffffff;
}
.twin-hero-main { display: flex; align-items: center; gap: 20px; position: relative; z-index: 1; }

/* monogram mark */
.twin-mark {
  position: relative; flex: 0 0 auto;
  width: 72px; height: 72px; border-radius: 22px;
  display: grid; place-items: center;
  background: var(--twin-grad);
  color: var(--twin-primary); font-family: var(--twin-brand); font-weight: 800; font-size: 26px; letter-spacing: -.03em;
  border: 1px solid #b9e3f2;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, .8), 0 0 0 4px #fff, 0 0 0 5px #d4e7f6, 0 14px 28px -14px rgba(83, 156, 212, .45);
}
.twin-mark::after {              /* glossy highlight */
  content: ""; position: absolute; inset: 0; border-radius: inherit;
  background: linear-gradient(160deg, rgba(255, 255, 255, .6), rgba(255, 255, 255, 0) 50%); pointer-events: none;
}
.twin-mark b { position: relative; z-index: 1; font-weight: 800; }
/* photo variant: soft pastel ring, face-centred crop */
.twin-mark.has-photo {
  background: #fff; border: 2px solid #fff;
  box-shadow: 0 0 0 3px #b9e3f2, 0 0 0 6px #e6fffb, 0 14px 28px -14px rgba(83, 156, 212, .45);
}
.twin-mark.has-photo::after { display: none; }
.twin-photo { position: absolute; inset: 0; border-radius: 20px; overflow: hidden; }
.twin-photo img {
  width: 100%; height: 100%; margin: 0 !important; display: block;
  object-fit: cover; object-position: center center;
}
.twin-status {
  position: absolute; right: -4px; bottom: -4px; width: 18px; height: 18px; border-radius: 50%; z-index: 2;
  background: #22c55e; border: 3px solid #fff; animation: twin-pulse 2.4s infinite;
}

.twin-id { flex: 1 1 auto; min-width: 0; }
.twin-eyebrow { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 6px; }
.twin-pill {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 3px 10px; border-radius: 999px;
  font-size: 11px; font-weight: 700; letter-spacing: .05em; line-height: 1.5;
}
.twin-pill-ai { color: var(--twin-primary); background: #eef6fc; border: 1px solid #d4e7f6; text-transform: uppercase; }
.twin-pill-open { color: #15803d; background: #f0fdf4; border: 1px solid #dcfce7; letter-spacing: .01em; }
.twin-pill-open i { width: 7px; height: 7px; border-radius: 50%; background: #22c55e; display: inline-block; }

/* wordmark */
.twin-name {
  margin: 0; font-family: var(--twin-brand); font-weight: 800;
  font-size: 36px; line-height: 1.05; letter-spacing: -.045em; color: var(--twin-ink);
  white-space: nowrap;
}
.twin-name .first { color: #1e293b; }
.twin-name .last {
  background-image: var(--twin-brand-grad) !important;
  -webkit-background-clip: text; background-clip: text;
  color: transparent; -webkit-text-fill-color: transparent;
  padding-right: .04em;           /* keeps the last glyph from clipping */
}
.twin-name .dot { color: #fd1056; }
.twin-role {
  margin: 6px 0 0; font-size: 14.5px; font-weight: 600; color: #334155;
  display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
}
.twin-role span { color: var(--twin-muted); font-weight: 500; }
.twin-role .sep { width: 4px; height: 4px; border-radius: 50%; background: #cbd5e1; display: inline-block; }
.twin-tagline { margin: 14px 0 0; font-size: 14px; line-height: 1.6; color: var(--twin-muted); max-width: 640px; position: relative; z-index: 1; }

/* contact buttons */
.twin-actions { display: flex; align-items: center; gap: 8px; flex: 0 0 auto; }
.twin-btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  height: 40px; padding: 0 16px; border-radius: 12px;
  font-size: 13.5px; font-weight: 600; text-decoration: none !important; white-space: nowrap;
  transition: transform .18s ease, box-shadow .18s ease, background .18s ease, border-color .18s ease;
}
.twin-btn svg { width: 16px; height: 16px; flex: 0 0 auto; }
.twin-btn-icon { width: 40px; padding: 0; }
.twin-btn-icon span { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
.twin-btn-primary { color: var(--twin-on-pastel) !important; background: var(--twin-grad); border: 1px solid #b9e3f2; box-shadow: 0 8px 20px -12px rgba(83, 156, 212, .5); }
.twin-btn-primary:hover { transform: translateY(-1px); background: var(--twin-grad-hover); box-shadow: 0 12px 24px -12px rgba(83, 156, 212, .6); }
.twin-btn-ghost { color: #334155 !important; background: #fff; border: 1px solid var(--twin-line); }
.twin-btn-ghost:hover { transform: translateY(-1px); border-color: #b9e3f2; color: var(--twin-primary) !important; background: #f4f9fd; }

/* ---------- 2. chat card ---------- */
.twin-chat-head {
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  padding: 12px 20px; border-top: 1px solid var(--twin-line); border-bottom: 1px solid var(--twin-line);
  background: #f8fbfd;
}
.twin-chat-head-left { display: flex; align-items: center; gap: 10px; min-width: 0; }
.twin-chat-head .dot { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; box-shadow: 0 0 0 3px #dcfce7; flex: 0 0 auto; }
.twin-chat-head b { font-size: 14px; color: var(--twin-ink); font-weight: 700; }
.twin-chat-head small { font-size: 12.5px; color: var(--twin-muted); }
.twin-chat-head .twin-kbd {
  font-size: 11.5px; color: var(--twin-muted); background: #f1f5f9; border: 1px solid var(--twin-line);
  border-radius: 8px; padding: 3px 8px; white-space: nowrap;
}

/* chatbot block: flat, the card provides the frame (no double borders) */
#twin-chatbot { border: none !important; box-shadow: none !important; border-radius: 0 !important; background: #fff !important; }
#twin-chatbot .bubble-wrap { background: #fff; padding-top: 8px; }
#twin-chatbot .message-wrap .prose.chatbot.md { opacity: 1; }

/* empty state */
#twin-chatbot .placeholder-content { justify-content: center; gap: 0; padding: 8px 8px 4px; }
#twin-chatbot .placeholder { flex-grow: 0; height: auto; padding: 18px 12px 0; }
#twin-chatbot .placeholder .md { text-align: center; max-width: 560px; color: var(--twin-muted); font-size: 14.5px; line-height: 1.6; }
#twin-chatbot .placeholder .md h3 {
  font-family: var(--twin-display); font-size: 24px; font-weight: 700; letter-spacing: -.01em;
  color: var(--twin-ink); margin: 0 0 6px;
}

/* starter cards */
#twin-chatbot .examples {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  max-width: 720px; width: 100%; gap: 12px; padding: 20px 16px 16px;
  margin: 0 auto;
}
#twin-chatbot .example {
  position: relative; flex-direction: row; align-items: center; gap: 12px;
  padding: 14px 16px; border-radius: 16px;
  background: #fff; border: 1px solid var(--twin-line);
  box-shadow: 0 1px 2px rgba(15, 23, 42, .04);
  color: #334155; transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease, background .18s ease;
}
#twin-chatbot .example::before {
  content: "✦"; flex: 0 0 auto; width: 36px; height: 36px; border-radius: 11px;
  display: grid; place-items: center; font-size: 17px;
  background: #eef6fc; border: 1px solid #d4e7f6;
}
#twin-chatbot .example:nth-child(1)::before { content: "🧭"; }
#twin-chatbot .example:nth-child(2)::before { content: "🚀"; background: #e6fffb; border-color: #c9fbf3; }
#twin-chatbot .example:nth-child(3)::before { content: "🛠️"; background: #fff0f4; border-color: #ffd6e1; }
#twin-chatbot .example:nth-child(4)::before { content: "✉️"; background: #f0fdf4; border-color: #dcfce7; }
#twin-chatbot .example::after {
  content: "→"; margin-left: auto; padding-left: 4px; color: #8cc0e8; font-weight: 700;
  transition: transform .18s ease, color .18s ease;
}
#twin-chatbot .example:hover {
  transform: translateY(-2px); background: #f7fbfe; border-color: #b9e3f2;
  box-shadow: 0 10px 24px -14px rgba(83, 156, 212, .35);
}
#twin-chatbot .example:hover::after { transform: translateX(3px); color: var(--twin-primary); }
#twin-chatbot .example-content { flex: 1 1 auto; min-width: 0; }
#twin-chatbot .example-text-content { margin-top: 0; }
#twin-chatbot .example-text { font-size: 14px; font-weight: 600; line-height: 1.4; color: #334155; white-space: normal; }

/* message bubbles (outer bubble = div.user / div.bot inside .message-row) */
#twin-chatbot .message-row.bubble { margin: 18px 22px 4px; animation: twin-rise .35s ease both; }
#twin-chatbot .message-row .user,
#twin-chatbot .message-row .bot { padding: 12px 16px; box-shadow: none; }
#twin-chatbot .message-row .user {
  background: var(--twin-grad); border: 1px solid #b9e3f2; color: #134e7c;
  border-radius: 18px 18px 6px 18px;
  box-shadow: 0 8px 20px -14px rgba(83, 156, 212, .45);
}
#twin-chatbot .message-row .user .prose,
#twin-chatbot .message-row .user .prose * { color: #134e7c !important; }
#twin-chatbot .message-row .bot {
  background: #ffffff; border: 1px solid var(--twin-line); color: var(--twin-ink);
  border-radius: 18px 18px 18px 6px;
}
#twin-chatbot .avatar-container { width: 36px; height: 36px; border: none; box-shadow: 0 4px 10px -6px rgba(29, 95, 151, .3); }
#twin-chatbot .avatar-container img { padding: 0 !important; }
#twin-chatbot .bot-row .avatar-container { box-shadow: 0 0 0 2px #fff, 0 0 0 4px #b9e3f2, 0 4px 10px -6px rgba(29, 95, 151, .3); }
#twin-chatbot .bot-row .avatar-container img { object-fit: cover; object-position: center center; transform: none !important; }

/* markdown inside bot replies */
#twin-chatbot .bot .prose { line-height: 1.65; color: #1e293b; }
#twin-chatbot .bot .prose h1, #twin-chatbot .bot .prose h2, #twin-chatbot .bot .prose h3, #twin-chatbot .bot .prose h4 {
  font-family: var(--twin-display); color: var(--twin-ink); letter-spacing: -.01em; margin: .2em 0 .45em;
}
#twin-chatbot .bot .prose h1 { font-size: 1.3em; } #twin-chatbot .bot .prose h2 { font-size: 1.2em; } #twin-chatbot .bot .prose h3 { font-size: 1.08em; }
#twin-chatbot .bot .prose strong { color: var(--twin-ink); font-weight: 700; }
#twin-chatbot .bot .prose ul, #twin-chatbot .bot .prose ol { padding-left: 1.25em; margin: .4em 0; }
#twin-chatbot .bot .prose li { margin: .25em 0; }
#twin-chatbot .bot .prose li::marker { color: #539cd4; }
#twin-chatbot .bot .prose a { color: var(--twin-primary); text-decoration: none; font-weight: 600; border-bottom: 1px solid #b9e3f2; }
#twin-chatbot .bot .prose a:hover { border-bottom-color: var(--twin-primary); }
#twin-chatbot .bot .prose :not(pre) > code {
  font-size: .86em; padding: .12em .42em; border-radius: 6px;
  background: #eef6fc; color: #134e7c; border: 1px solid #d4e7f6;
}
#twin-chatbot .bot .prose pre { border-radius: 12px; border: 1px solid var(--twin-line); }

/* message action icons: quieter */
#twin-chatbot .message-buttons { opacity: .55; transition: opacity .18s ease; }
#twin-chatbot .message-buttons:hover { opacity: 1; }
#twin-chatbot .message-buttons-left.with-avatar { margin-left: 80px; }
#twin-chatbot .message-buttons-right { margin-right: 22px; }
#twin-chatbot .top-panel {
  top: 10px; right: 12px; padding: 2px; border-radius: 10px;
  background: rgba(255, 255, 255, .9); border: 1px solid var(--twin-line); backdrop-filter: blur(6px);
}
#twin-chatbot .bubble-wrap:has(.message-wrap) { padding-top: 34px; }

/* ---------- 3. input bar ---------- */
#twin-card .gr-group {
  border: none !important; background: transparent !important; border-radius: 0 !important; overflow: visible;
}
#twin-card .gr-group .styler { background: transparent !important; }
#twin-card .gr-group .form { border: none !important; background: transparent !important; }
#twin-card .gr-group .block {
  background: linear-gradient(180deg, rgba(248, 251, 253, 0), #f8fbfd 40%) !important;
  padding: 10px 18px 18px !important; border-radius: 0 !important;
}
#twin-input .input-container {
  align-items: center; gap: 8px;
  background: #fff; border: 1px solid #dbe4ee; border-radius: 18px;
  padding: 6px 6px 6px 8px;
  box-shadow: 0 1px 2px rgba(15, 23, 42, .04), 0 8px 24px -14px rgba(15, 23, 42, .18);
  transition: border-color .18s ease, box-shadow .18s ease;
}
#twin-input .input-container:focus-within { border-color: #8cc0e8; box-shadow: 0 0 0 4px rgba(83, 156, 212, .22); }
#twin-input textarea {
  background: transparent !important; border: none !important; box-shadow: none !important;
  font-size: 15px; line-height: 1.5; padding: 8px 8px !important; color: var(--twin-ink);
}
#twin-input .submit-button, #twin-input .stop-button {
  width: 42px; min-width: 42px; height: 42px; border-radius: 13px;
  background: var(--twin-grad) !important; color: #1d5f97 !important; border: 1px solid #b9e3f2 !important;
  box-shadow: 0 6px 16px -10px rgba(83, 156, 212, .55);
  transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
}
#twin-input .submit-button:hover, #twin-input .stop-button:hover { transform: translateY(-1px); filter: brightness(.97); }
#twin-input .submit-button svg { width: 20px; height: 20px; }
#twin-input .stop-button { background: #fff1f2 !important; color: #be123c !important; border-color: #fecdd3 !important; box-shadow: none; }

/* ---------- 3b. scrollbars (chat list = #twin-chatbot .bubble-wrap, plus textarea etc.) ---------- */
#twin-card ::-webkit-scrollbar, #twin-card::-webkit-scrollbar { width: 8px; height: 8px; }
#twin-card ::-webkit-scrollbar-track { background: transparent; margin: 6px 0; }
#twin-card ::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #8ff5e4 0%, #9ec7ea 100%);
  border-radius: 999px;
  border: 2px solid transparent; background-clip: padding-box;
}
#twin-card ::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #22e3c6 0%, #539cd4 100%);
  border: 2px solid transparent; background-clip: padding-box;
}
#twin-card ::-webkit-scrollbar-corner { background: transparent; }
/* Firefox scrollbar rule lives in BACKGROUND_CSS (HEAD): Gradio drops @supports from css= */

/* ---------- 4. footer ---------- */
.twin-footer {
  display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 6px 10px;
  padding: 6px 0 4px; font-size: 12.5px; color: #a3a3a3; text-align: center;
}
.twin-footer span { color: #a3a3a3 !important; }
.twin-footer b { color: #d4d4d4; font-weight: 600; }
.twin-footer .sep { color: #08fdd8 !important; opacity: .7; font-weight: 700; }

/* ---------- 5. responsive ---------- */
@media (max-width: 820px) {
  .twin-hero-main { flex-wrap: wrap; }
  .twin-actions { width: 100%; }
  .twin-actions .twin-btn-primary { flex: 1 1 auto; }
}
@media (max-width: 640px) {
  .main.app { padding: 10px 10px 4px !important; }
  .twin-hero { padding: 22px 16px 16px; }
  .twin-hero-main { gap: 14px; }
  .twin-mark { width: 56px; height: 56px; border-radius: 17px; font-size: 21px; }
  .twin-photo { border-radius: 15px; }
  .twin-status { width: 15px; height: 15px; border-width: 2px; right: -3px; bottom: -3px; }
  .twin-id { flex: 1 1 0; }
  .twin-pill-ai { display: none; }
  .twin-pill { font-size: 10.5px; }
  .twin-name { font-size: 28px; }
  .twin-role { font-size: 13.5px; margin-top: 4px; }
  .twin-tagline { font-size: 13.5px; margin-top: 12px; }
  .twin-btn { height: 38px; font-size: 13px; }
  .twin-btn-icon { width: 38px; }
  #twin-card { border-radius: 20px; }
  .twin-chat-head { padding: 12px 14px; }
  .twin-chat-head .twin-kbd, .twin-chat-head small { display: none; }
  #twin-chatbot .examples { grid-template-columns: 1fr; gap: 8px; padding: 14px 10px 10px; }
  #twin-chatbot .example { padding: 11px 12px; }
  #twin-chatbot .example::before { width: 32px; height: 32px; font-size: 15px; }
  #twin-chatbot .placeholder { padding-top: 10px; }
  #twin-chatbot .placeholder .md { font-size: 13.5px; }
  #twin-chatbot .placeholder .md h3 { font-size: 20px; }
  #twin-chatbot .message-row.bubble { margin: 14px 12px 4px; max-width: calc(100% - 24px); }
  #twin-input textarea { font-size: 14.5px; }
  .twin-footer { flex-direction: column; gap: 2px; }
  .twin-footer .sep { display: none; }
  #twin-chatbot .bot-row.bubble > .avatar-container { width: 28px; height: 28px; margin-right: 8px; }
  #twin-chatbot .user-row.bubble > .avatar-container { display: none; }
  #twin-chatbot .message-row .user, #twin-chatbot .message-row .bot { padding: 10px 13px; }
  #twin-chatbot .message-buttons-left.with-avatar { margin-left: 56px; }
  #twin-card .gr-group .block { padding: 8px 10px 12px !important; }
}
"""

# --------------------------------------------------------------------------- #
# JS: runs once on load (launch(js=...))
# --------------------------------------------------------------------------- #
JS = r"""
() => {
  document.title = 'Sanjeet Kumar | AI Twin';

  // Force light mode: the design is light-only, so undo Gradio's dark toggle.
  const forceLight = () => {
    for (const el of [document.documentElement, document.body, document.querySelector('.gradio-container')]) {
      if (el && el.classList.contains('dark')) el.classList.remove('dark');
    }
  };
  forceLight();
  new MutationObserver(forceLight).observe(document.documentElement, { attributes: true, subtree: true, attributeFilter: ['class'] });

  // Re-focus the message box once it becomes enabled again after a reply.
  const focusInput = () => {
    const boxes = document.querySelectorAll('textarea');
    const box = boxes[boxes.length - 1];
    if (box && !box.disabled) box.focus();
  };
  new MutationObserver((mutations) => {
    for (const m of mutations) {
      if (m.target.tagName === 'TEXTAREA' && m.attributeName === 'disabled' && !m.target.disabled) {
        setTimeout(focusInput, 50);
        break;
      }
    }
  }).observe(document.body, { attributes: true, subtree: true, attributeFilter: ['disabled'] });
}
"""
