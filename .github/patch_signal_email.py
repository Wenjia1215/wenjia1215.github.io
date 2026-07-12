import base64
import json
import os
import urllib.request


token = os.environ["GH_TOKEN"]
repo = os.environ["REPOSITORY"]
branch = os.environ["BRANCH"]
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "signal-email-site-patch",
}


def request_json(url, method="GET", payload=None):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request) as response:
        return json.load(response)


index_url = f"https://api.github.com/repos/{repo}/contents/index.html?ref={branch}"
index = request_json(index_url)
text = base64.b64decode(index["content"]).decode("utf-8")
original = text

email_old = '          email: "mailto:wenjiabusiness@gmail.com"'
email_new = '          email: "https://mail.google.com/mail/?view=cm&fs=1&to=wenjiabusiness@gmail.com"'
if email_old in text:
    if text.count(email_old) != 1:
        raise SystemExit(f"Expected one email link match, found {text.count(email_old)}")
    text = text.replace(email_old, email_new, 1)
elif email_new not in text:
    raise SystemExit("Could not find the expected email link")

css_start = text.index("      .signal-meta {")
css_end = text.index("      .portrait-actions {", css_start)
signal_css = '''      .signal-meta {
        position: absolute;
        z-index: 4;
        top: 16px;
        right: 16px;
        display: grid;
        justify-items: end;
        gap: 6px;
        color: rgba(255, 255, 255, 0.66);
        font-size: clamp(9px, 0.62vw, 11px);
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        text-shadow: 0 1px 8px rgba(0, 0, 0, 0.95);
      }

      .signal-label {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 2px;
        color: var(--accent);
        font-size: 0.9em;
        font-weight: 800;
        letter-spacing: 0.18em;
      }

      .signal-label::before {
        content: "";
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 8px rgba(216, 106, 43, 0.75);
      }

      .signal-date {
        color: rgba(255, 255, 255, 0.9);
        text-align: right;
      }

'''
text = text[:css_start] + signal_css + text[css_end:]

mobile_start = text.index("      @media (max-width: 560px)")
mobile_signal_start = text.index("        .signal-meta {", mobile_start)
mobile_signal_end = text.index("        }", mobile_signal_start) + len("        }")
mobile_signal_css = '''        .signal-meta {
          top: 12px;
          right: 12px;
          bottom: auto;
          left: auto;
          gap: 5px;
        }'''
text = text[:mobile_signal_start] + mobile_signal_css + text[mobile_signal_end:]

signal_open = '            <div class="signal-meta" aria-hidden="true">'
signal_label = '              <span class="signal-label">SIGNAL</span>'
if text.count(signal_open) != 1:
    raise SystemExit(f"Expected one signal metadata block, found {text.count(signal_open)}")
if signal_label not in text:
    text = text.replace(signal_open, signal_open + "\n" + signal_label, 1)

for date in ("19930209", "20120817", "20191215", "20211006"):
    marker = f'<span class="signal-date">{date}</span>'
    if text.count(marker) != 1:
        raise SystemExit(f"Expected one date marker for {date}, found {text.count(marker)}")

if email_new not in text:
    raise SystemExit("Gmail compose URL missing after patch")
if text.count(signal_label) != 1:
    raise SystemExit("SIGNAL label missing or duplicated after patch")

if text == original:
    raise SystemExit(0)

update_url = f"https://api.github.com/repos/{repo}/contents/index.html"
request_json(
    update_url,
    method="PUT",
    payload={
        "message": "Refine contact link and portrait signal dates",
        "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
        "sha": index["sha"],
        "branch": branch,
    },
)
