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
    "User-Agent": "research-page-patch",
}


def request_json(url, method="GET", payload=None):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request) as response:
        return json.load(response)


index_url = f"https://api.github.com/repos/{repo}/contents/index.html?ref={branch}"
index = request_json(index_url)
text = base64.b64decode(index["content"]).decode("utf-8")

research_start = text.index('        <div class="modal-view research-view" data-panel="research">')
teaching_start = text.index('\n        <div class="modal-view teaching-view"', research_start)

new_research = '''        <div class="modal-view research-view" data-panel="research">
          <div class="modal-hero">
            <div class="modal-hero-copy">
              <span class="modal-kicker">research // citation-contract systems</span>
              <h2 id="researchTitle">Separate evidence selection from answer release.</h2>
              <p>My dissertation studies a narrow failure in compliance RAG: relevant evidence can be retrieved, yet a model-written final answer can still introduce unsupported compliance content.</p>
            </div>
          </div>
          <div class="modal-body">
            <div class="modal-intro">
              <span class="section-label">dissertation // compliancegpt</span>
              <p>ComplianceGPT is a citation-contract answerer for audit-facing QA over NIST SP 800-53 Rev. 4 and Rev. 5. The language model selects evidence IDs from a revision-scoped candidate pool; it does not write the evidence-bearing final answer. A deterministic orchestrator assembles the answer from canonical clauses, approved organization-profile values, or explicit unresolved states, then a rule-based verifier checks the released artifact.</p>
            </div>
            <div class="detail-grid">
              <article class="detail-card">
                <span class="detail-number">01 / FAILURE BOUNDARY</span>
                <h3>Retrieval is not the last risk</h3>
                <p>Even with relevant context, generated prose can loosen obligations, attach unsupported citations, mix revisions, or invent organization-defined values.</p>
              </article>
              <article class="detail-card">
                <span class="detail-number">02 / ANSWER PATH</span>
                <h3>Retrieve → select IDs → assemble → verify</h3>
                <p>S7 retrieval builds a clause pool. An LLM selects source IDs. The Contract Orchestrator resolves them against the Canonical Clause Store and ODP policy; the Runtime Verifier checks citation linkage, revision scope, source spans, status, and ODP behavior.</p>
              </article>
              <article class="detail-card">
                <span class="detail-number">03 / RESULTS</span>
                <h3>Strict pass: 0.22 → 0.64 / 0.75</h3>
                <p>Under matched S7 retrieval, strict answer-pass rose from 0.22 to 0.64 on Rev. 5 and 0.75 on Rev. 4. In no-profile ODP cases, the baseline false-completed 60/63 and 19/19; ComplianceGPT made no false-complete ODP insertions in those evaluated subsets.</p>
              </article>
            </div>
            <div class="modal-intro" style="margin-top: clamp(38px, 6vw, 68px);">
              <span class="section-label">claim boundary</span>
              <p>ComplianceGPT does not determine whether an organization is compliant and does not prove selected evidence is complete. Its claim is narrower: conditioned on selected source IDs and approved profile values, final-answer realization should not introduce unsupported compliance content.</p>
            </div>
            <div class="modal-cta-row">
              <button class="modal-cta" type="button" data-modal="publications">view publications</button>
              <a class="modal-cta" href="https://scholar.google.com/citations?user=Zl-yM-kAAAAJ&amp;hl=en&amp;oi=ao" target="_blank" rel="noopener">google scholar ↗</a>
            </div>
          </div>
        </div>
'''

text = text[:research_start] + new_research + text[teaching_start:]

required = [
    "research // citation-contract systems",
    "Separate evidence selection from answer release.",
    "dissertation // compliancegpt",
    "Retrieve → select IDs → assemble → verify",
    "Strict pass: 0.22 → 0.64 / 0.75",
    "claim boundary",
]
for item in required:
    if item not in text:
        raise SystemExit(f"Research page patch missing required text: {item}")

update_url = f"https://api.github.com/repos/{repo}/contents/index.html"
request_json(
    update_url,
    method="PUT",
    payload={
        "message": "Sharpen dissertation research page",
        "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
        "sha": index["sha"],
        "branch": branch,
    },
)

marker_url = f"https://api.github.com/repos/{repo}/contents/.research-page-trigger?ref={branch}"
marker = request_json(marker_url)
delete_url = f"https://api.github.com/repos/{repo}/contents/.research-page-trigger"
request_json(
    delete_url,
    method="DELETE",
    payload={
        "message": "Remove temporary research page trigger",
        "sha": marker["sha"],
        "branch": branch,
    },
)
