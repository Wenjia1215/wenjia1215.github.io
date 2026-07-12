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
    "User-Agent": "portrait-date-spacing-patch",
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

old_css = '''      .signal-meta {
        position: absolute;
        z-index: 4;
        right: 18px;
        bottom: 16px;
        left: 18px;
        display: flex;
        justify-content: flex-end;
        gap: 18px;
        color: rgba(255, 255, 255, 0.66);
        font-size: clamp(9px, 0.62vw, 11px);
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
      }

      .signal-date {
        color: rgba(255, 255, 255, 0.9);
      }'''

new_css = '''      .signal-meta {
        position: absolute;
        z-index: 4;
        right: 18px;
        bottom: 16px;
        left: 18px;
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        align-items: center;
        gap: 0;
        color: rgba(255, 255, 255, 0.66);
        font-size: clamp(9px, 0.62vw, 11px);
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
      }

      .signal-date {
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
      }'''

if old_css in text:
    if text.count(old_css) != 1:
        raise SystemExit(f"Expected at most one old CSS block, found {text.count(old_css)}")
    text = text.replace(old_css, new_css, 1)
elif new_css not in text:
    raise SystemExit("Neither expected portrait CSS block was found")

old_date = '<span class="signal-date">20211004</span>'
new_date = '<span class="signal-date">20211006</span>'
if old_date in text:
    if text.count(old_date) != 1:
        raise SystemExit(f"Expected at most one old portrait date, found {text.count(old_date)}")
    text = text.replace(old_date, new_date, 1)
elif new_date not in text:
    raise SystemExit("Neither expected final portrait date was found")

if text == original:
    raise SystemExit(0)

update_url = f"https://api.github.com/repos/{repo}/contents/index.html"
request_json(
    update_url,
    method="PUT",
    payload={
        "message": "Preserve corrected portrait date with equal spacing",
        "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
        "sha": index["sha"],
        "branch": branch,
    },
)
