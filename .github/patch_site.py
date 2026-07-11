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
    "User-Agent": "one-shot-site-patch",
}


def request_json(url, method="GET", payload=None):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request) as response:
        return json.load(response)


index_url = f"https://api.github.com/repos/{repo}/contents/index.html?ref={branch}"
index = request_json(index_url)
text = base64.b64decode(index["content"]).decode("utf-8")

identity_old = "wenjia wang . geeker . teacher . adventurer"
identity_new = "wenjia wang . builder . teacher . researcher"
if text.count(identity_old) != 1:
    raise SystemExit(f"Expected one identity match, found {text.count(identity_old)}")
text = text.replace(identity_old, identity_new, 1)

date_old = '              <span class="signal-date">20211004</span>'
date_new = "\n".join(
    [
        '              <span class="signal-date">19930209</span>',
        '              <span class="signal-date">20120817</span>',
        '              <span class="signal-date">20191215</span>',
        '              <span class="signal-date">20211004</span>',
    ]
)
if text.count(date_old) != 1:
    raise SystemExit(f"Expected one portrait-date match, found {text.count(date_old)}")
text = text.replace(date_old, date_new, 1)

teaching_view = text.index('<div class="modal-view teaching-view"')
body_start = text.index('          <div class="modal-body">', teaching_view)
publications_start = text.index('\n        <div class="modal-view publications-view"', body_start)
body_end = text.rfind('\n        </div>', body_start, publications_start)
if body_end == -1:
    raise SystemExit("Could not locate teaching modal body end")

new_teaching_body = "\n".join(
    [
        '          <div class="modal-body">',
        '            <div class="modal-intro">',
        '              <span class="section-label">courses i can teach</span>',
        '              <p>Courses I am prepared to teach across applied AI, cybersecurity, and software systems.</p>',
        '            </div>',
        '            <div class="detail-grid">',
        '              <article class="detail-card">',
        '                <span class="detail-number">01 / AI &amp; APPLIED AI</span>',
        '                <h3>Artificial Intelligence</h3>',
        '                <p>Introduction to Artificial Intelligence, Applied Generative AI / LLM Systems, and Machine Learning Applications.</p>',
        '              </article>',
        '              <article class="detail-card">',
        '                <span class="detail-number">02 / CYBERSECURITY</span>',
        '                <h3>Cybersecurity</h3>',
        '                <p>Security in Computing, Software Vulnerabilities and Security, and Cybersecurity Compliance and Governance.</p>',
        '              </article>',
        '              <article class="detail-card">',
        '                <span class="detail-number">03 / SOFTWARE SYSTEMS</span>',
        '                <h3>Software Systems</h3>',
        '                <p>Software Engineering, Web Application Development, Database Systems, Data Structures, and Programming I / II.</p>',
        '              </article>',
        '            </div>',
        '            <div class="modal-intro" style="margin-top: clamp(38px, 6vw, 68px);">',
        '              <span class="section-label">teaching in practice</span>',
        '              <p>My classroom and mentoring work spans security, software vulnerabilities, capstone engineering, architecture review, technical presentations, and interdisciplinary software projects.</p>',
        '            </div>',
        '            <div class="detail-grid">',
        '              <article class="detail-card">',
        '                <span class="detail-number">01 / CLASSROOM</span>',
        '                <h3>Security in Computing</h3>',
        '                <p>Teaching assistant for CEN 5013 and CEN 5079, Software Vulnerabilities and Security, at Florida International University.</p>',
        '              </article>',
        '              <article class="detail-card">',
        '                <span class="detail-number">02 / CAPSTONE</span>',
        '                <h3>From requirements to demo</h3>',
        '                <p>Mentors teams through architecture, implementation, testing, documentation, technical presentations, and final demonstrations.</p>',
        '              </article>',
        '              <article class="detail-card">',
        '                <span class="detail-number">03 / EVALUATION</span>',
        '                <h3>Showcase judge since 2023</h3>',
        '                <p>Evaluates interdisciplinary capstone projects for system design, technical execution, communication, and real-world usefulness.</p>',
        '              </article>',
        '            </div>',
        '            <div class="modal-cta-row">',
        '              <span class="modal-cta">guided work: peer-to-peer file sharing</span>',
        '              <span class="modal-cta">guided work: Baby-Feed health platform</span>',
        '            </div>',
        '          </div>',
    ]
)
text = text[:body_start] + new_teaching_body + text[body_end:]

if identity_new not in text:
    raise SystemExit("Identity patch missing after replacement")
for date in ("19930209", "20120817", "20191215", "20211004"):
    if f'<span class="signal-date">{date}</span>' not in text:
        raise SystemExit(f"Portrait date missing after replacement: {date}")
if '<span class="section-label">courses i can teach</span>' not in text:
    raise SystemExit("Courses section missing after replacement")
if '<span class="section-label">teaching in practice</span>' not in text:
    raise SystemExit("Teaching-in-practice section missing after replacement")

update_url = f"https://api.github.com/repos/{repo}/contents/index.html"
request_json(
    update_url,
    method="PUT",
    payload={
        "message": "Update profile dates and teaching content",
        "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
        "sha": index["sha"],
        "branch": branch,
    },
)

marker_url = f"https://api.github.com/repos/{repo}/contents/.site-patch-trigger?ref={branch}"
marker = request_json(marker_url)
delete_url = f"https://api.github.com/repos/{repo}/contents/.site-patch-trigger"
request_json(
    delete_url,
    method="DELETE",
    payload={
        "message": "Remove temporary patch trigger",
        "sha": marker["sha"],
        "branch": branch,
    },
)
