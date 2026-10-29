# *******************************************************************************
# Copyright (c) 2026 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
# *******************************************************************************
"""Issue the certificate of completion of the onboarding training.

The certificate is only issued when every issue in the repository meets rule 1 of TRAINING.md:
closed by a merged pull request, or closed by hand and linked to a merged pull request in either
direction. The continuous improvement issue may stay open and is not checked. Any other issue is
listed with what to do about it, and the run fails.

Runs in the "Certificate" workflow. It needs only the Python standard library: the PDF is written
by hand, with the standard fonts every PDF viewer has.

Environment: GITHUB_TOKEN, GITHUB_REPOSITORY, GITHUB_SHA, GITHUB_STEP_SUMMARY (optional).
"""

import argparse
import datetime
import json
import os
import re
import sys
import urllib.request

STAGES = [
    ("Environment", "development environment, Eclipse Contributor Agreement"),
    ("Git", "upstream synchronisation, commits that carry their reasoning"),
    ("Build", "clean documentation build, defect branches repaired"),
    ("Process", "the process behind a work product, project decisions"),
    ("Review", "form and content review, answering a review"),
    ("Module", "template update with rebase, track document filled in"),
    ("Wrap-up", "cross-review, formal document review, retrospective"),
]
ROLES = {"quality": "Quality", "safety": "Safety", "security": "Security"}
# Issues the forms of eclipse-score/contributor_training create; opened in a copy by mistake, they are no tasks.
FORM_LABELS = {"feedback", "bug-report", "training-completed"}
TASK_TITLE = re.compile(r"^\d\.\d")
CONTINUOUS_IMPROVEMENT = re.compile(r"^Continuous improvement\b")

QUERY = """
query($owner: String!, $name: String!, $after: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(states: MERGED) { totalCount }
    issues(first: 100, after: $after) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title state body
        comments(last: 50) { nodes { body } }
        labels(first: 20) { nodes { name } }
        timelineItems(itemTypes: [CLOSED_EVENT, CROSS_REFERENCED_EVENT], first: 100) {
          nodes {
            __typename
            ... on ClosedEvent { closer {
              __typename
              ... on PullRequest { number merged }
              ... on Commit { associatedPullRequests(first: 5) { nodes { number merged } } }
            } }
            ... on CrossReferencedEvent { source { ... on PullRequest { number merged } } }
          }
        }
      }
    }
  }
}
"""

MERGED_QUERY = """
query($owner: String!, $name: String!, $after: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(states: MERGED, first: 100, after: $after) {
      pageInfo { hasNextPage endCursor }
      nodes { number }
    }
  }
}
"""


def graphql(token, variables, query=QUERY):
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        result = json.load(response)
    if "errors" in result:
        sys.exit(f"GitHub API: {result['errors']}")
    return result["data"]["repository"]


def done_by_pr(issue, merged):
    """The merged pull request the issue was done in, or None.

    Either the merged pull request (or a commit of one) that closed the issue, or, for an issue
    closed by hand, a merged pull request that mentions it or that the issue names in its text or
    in a comment.
    """
    if issue["state"] != "CLOSED":
        return None
    events = issue["timelineItems"]["nodes"]
    closed = [event for event in events if event["__typename"] == "ClosedEvent"]
    closer = (closed[-1].get("closer") or {}) if closed else {}
    if closer.get("__typename") == "PullRequest" and closer["merged"]:
        return closer["number"]
    if closer.get("__typename") == "Commit":
        prs = [pr["number"] for pr in closer["associatedPullRequests"]["nodes"] if pr["merged"]]
        if prs:
            return prs[0]
    mentioned_by = [event["source"]["number"] for event in events
                    if event["__typename"] == "CrossReferencedEvent" and event["source"].get("merged")]
    if mentioned_by:
        return mentioned_by[0]
    texts = [issue["body"] or ""] + [comment["body"] or "" for comment in issue["comments"]["nodes"]]
    named = [int(n) for text in texts for n in re.findall(r"(?<![\w/])#(\d+)\b", text) if int(n) in merged]
    return named[0] if named else None


def collect(token, repository):
    owner, name = repository.split("/")
    issues, after = [], None
    while True:
        data = graphql(token, {"owner": owner, "name": name, "after": after})
        issues += data["issues"]["nodes"]
        if not data["issues"]["pageInfo"]["hasNextPage"]:
            break
        after = data["issues"]["pageInfo"]["endCursor"]
    merged, after = set(), None
    while True:
        prs = graphql(token, {"owner": owner, "name": name, "after": after}, MERGED_QUERY)["pullRequests"]
        merged |= {pr["number"] for pr in prs["nodes"]}
        if not prs["pageInfo"]["hasNextPage"]:
            return issues, merged
        after = prs["pageInfo"]["endCursor"]


def evaluate(issues, merged):
    """Per stage: tasks and own findings done; the role; the issues that block the certificate."""
    stages = [{"tasks": 0, "findings": 0} for _ in STAGES]
    roles, blocking = {}, []
    for issue in issues:
        labels = [label["name"] for label in issue["labels"]["nodes"]]
        for label in labels:
            if label in ROLES:
                roles[label] = roles.get(label, 0) + 1
        if CONTINUOUS_IMPROVEMENT.match(issue["title"]) or FORM_LABELS & set(labels):
            continue
        if done_by_pr(issue, merged) is None:
            reason = "open" if issue["state"] == "OPEN" else "closed by hand, not linked to a merged pull request"
            blocking.append((issue["number"], issue["title"], reason))
            continue
        stage = next((int(label[6:]) for label in labels if re.fullmatch(r"stage-[0-6]", label)), None)
        if stage is not None:
            stages[stage]["tasks" if TASK_TITLE.match(issue["title"]) else "findings"] += 1
    for number, stage in enumerate(stages):
        if stage["tasks"] == 0:
            blocking.append((None, f"Stage {number}", "no task of this stage closed by a merged pull request"))
    role = ROLES[max(roles, key=roles.get)] if roles else None
    return stages, role, blocking


# Advance widths of the standard fonts (Adobe font metrics), characters 32-126.
_HELVETICA = (
    "278 278 355 556 556 889 667 191 333 333 389 584 278 333 278 278 556 556 556 556 556 556 556 556 "
    "556 556 278 278 584 584 584 556 1015 667 667 722 722 667 611 778 722 278 500 667 556 833 722 778 "
    "667 778 722 667 611 722 667 944 667 667 611 278 278 278 469 556 333 556 556 500 556 556 278 556 "
    "556 222 222 500 222 833 556 556 556 556 333 500 278 556 500 722 500 500 500 334 260 334 584"
)
_HELVETICA_BOLD = (
    "278 333 474 556 556 889 722 238 333 333 389 584 278 333 278 278 556 556 556 556 556 556 556 556 "
    "556 556 333 333 584 584 584 611 975 722 722 722 722 667 611 778 722 278 556 722 611 833 722 778 "
    "667 778 722 667 611 722 667 944 667 667 611 333 278 333 584 556 333 556 611 556 611 556 333 611 "
    "611 278 278 556 278 889 611 611 611 611 389 556 333 611 556 778 556 556 500 389 280 389 584"
)
WIDTHS = {
    "F1": [int(w) for w in _HELVETICA.split()],
    "F2": [int(w) for w in _HELVETICA_BOLD.split()],
}


def text_width(text, font, size):
    widths = WIDTHS[font]
    total = sum(widths[ord(c) - 32] if 32 <= ord(c) <= 126 else (278 if c == "·" else 556) for c in text)
    return total * size / 1000


class Page:
    """A4 landscape, drawn with PDF operators."""

    WIDTH, HEIGHT = 842, 595

    def __init__(self):
        self.ops = []

    def text(self, x, y, text, font="F1", size=12, colour=(0.2, 0.2, 0.2), align="left"):
        if align == "center":
            x -= text_width(text, font, size) / 2
        elif align == "right":
            x -= text_width(text, font, size)
        raw = text.encode("cp1252", "replace")
        escaped = raw.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)").decode("latin-1")
        self.ops.append(f"{colour[0]} {colour[1]} {colour[2]} rg BT /{font} {size} Tf {x:.1f} {y:.1f} Td ({escaped}) Tj ET")

    def rect(self, x, y, w, h, width, colour, fill=None):
        if fill:
            self.ops.append(f"{fill[0]} {fill[1]} {fill[2]} rg {x} {y} {w} {h} re f")
        self.ops.append(f"{colour[0]} {colour[1]} {colour[2]} RG {width} w {x} {y} {w} {h} re S")

    def line(self, x1, y1, x2, y2, width, colour):
        self.ops.append(f"{colour[0]} {colour[1]} {colour[2]} RG {width} w {x1} {y1} m {x2} {y2} l S")

    def pdf(self):
        stream = "\n".join(self.ops).encode("latin-1")
        objects = [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.WIDTH} {self.HEIGHT}] /Contents 4 0 R "
            "/Resources << /Font << /F1 5 0 R /F2 6 0 R /F3 7 0 R >> >> >>".encode(),
            b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /ZapfDingbats >>",
        ]
        out, offsets = bytearray(b"%PDF-1.4\n"), []
        for number, body in enumerate(objects, 1):
            offsets.append(len(out))
            out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
        xref = len(out)
        out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
        out += b"".join(b"%010d 00000 n \n" % offset for offset in offsets)
        out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref)
        return bytes(out)


def render(name, account, role, stages, merged_prs, repository, commit, date):
    navy, gold, grey = (0.09, 0.18, 0.36), (0.72, 0.56, 0.18), (0.4, 0.4, 0.4)
    page, centre = Page(), Page.WIDTH / 2
    page.rect(18, 18, Page.WIDTH - 36, Page.HEIGHT - 36, 4, navy)
    page.rect(28, 28, Page.WIDTH - 56, Page.HEIGHT - 56, 0.8, gold)

    page.text(centre, 515, "CERTIFICATE OF COMPLETION", "F2", 30, navy, "center")
    page.text(centre, 488, "S-CORE contributor training", "F1", 14, grey, "center")
    page.text(centre, 450, "This certifies that", "F1", 12, grey, "center")
    page.text(centre, 415, name, "F2", 26, navy, "center")
    page.line(centre - 190, 405, centre + 190, 405, 0.8, gold)
    as_role = f" on the {role} track" if role else ""
    page.text(centre, 385, f"(GitHub @{account}) has completed every stage of the training{as_role}:", "F1", 12, grey, "center")

    top, left = 352, 150
    for number, ((title, content), stage) in enumerate(zip(STAGES, stages)):
        y = top - number * 24
        if number % 2 == 0:
            page.rect(left - 12, y - 7, Page.WIDTH - 2 * left + 24, 22, 0, (1, 1, 1), fill=(0.95, 0.96, 0.98))
        page.ops.append(f"0.13 0.55 0.13 rg BT /F3 12 Tf {left} {y:.1f} Td (4) Tj ET")
        page.text(left + 24, y, f"Stage {number} · {title}", "F2", 11, navy)
        page.text(left + 160, y, content, "F1", 10, grey)
        findings = f" · {stage['findings']} own finding{'s' if stage['findings'] != 1 else ''}" if stage["findings"] else ""
        page.text(Page.WIDTH - left, y, f"{stage['tasks']} task{'s' if stage['tasks'] != 1 else ''}{findings}", "F1", 10, grey, "right")

    tasks = sum(stage["tasks"] for stage in stages)
    findings = sum(stage["findings"] for stage in stages)
    page.text(centre, 165, f"{tasks} tasks and {findings} own findings, closed by {merged_prs} merged pull requests",
              "F2", 12, navy, "center")

    page.text(80, 112, date.strftime("%d %B %Y"), "F2", 12, navy)
    page.line(80, 106, 260, 106, 0.6, gold)
    page.text(80, 94, "Date of issue", "F1", 9, grey)
    page.text(Page.WIDTH - 80, 112, "eclipse-score/contributor_training", "F2", 12, navy, "right")
    page.line(Page.WIDTH - 260, 106, Page.WIDTH - 80, 106, 0.6, gold)
    page.text(Page.WIDTH - 80, 94, "Training", "F1", 9, grey, "right")

    page.text(centre, 58, f"Issued by the Certificate workflow of {repository} at commit {commit[:7]}.", "F1", 8, grey, "center")
    page.text(centre, 47, "It confirms that every training issue was completed through a merged pull request. It is not a proof of "
              "competence, and not an Eclipse Foundation certification.", "F1", 8, grey, "center")
    return page.pdf()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name", help="full name as it shall appear on the certificate")
    parser.add_argument("account", help="GitHub account of the participant")
    parser.add_argument("--output", default="certificate.pdf")
    args = parser.parse_args()

    repository, commit = os.environ["GITHUB_REPOSITORY"], os.environ.get("GITHUB_SHA", "unknown")
    issues, merged = collect(os.environ["GITHUB_TOKEN"], repository)
    stages, role, blocking = evaluate(issues, merged)
    merged_prs = len(merged)

    summary = []
    if blocking:
        summary += ["## No certificate yet", "",
                    "Every issue must be closed by a merged pull request whose description says `Closes #<n>` "
                    "(rule 1 of `TRAINING.md`). An issue closed by hand counts when a merged pull request "
                    "mentions it, or when the issue names a merged pull request as its result: if the work is "
                    "in a merged pull request, add a comment naming it; otherwise reopen the issue and close "
                    "it with a pull request. "
                    "Then run this workflow again.", "",
                    "| Issue | Title | Why it blocks |", "| --- | --- | --- |"]
        summary += [f"| {f'#{n}' if n else '–'} | {title} | {reason} |" for n, title, reason in blocking]
    else:
        date = datetime.date.today()
        with open(args.output, "wb") as file:
            file.write(render(args.name, args.account, role, stages, merged_prs, repository, commit, date))
        summary += ["## Certificate issued", "",
                    f"Download it from **Artifacts** below. Track: {role or 'none found'}.", "",
                    "| Stage | Tasks | Own findings |", "| --- | --- | --- |"]
        summary += [f"| {n} {title} | {s['tasks']} | {s['findings']} |" for n, ((title, _), s) in enumerate(zip(STAGES, stages))]

    print("\n".join(summary))
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as file:
            file.write("\n".join(summary) + "\n")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
