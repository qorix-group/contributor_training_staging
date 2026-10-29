#!/usr/bin/env python3
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
"""Prepare your copy of the S-CORE contributor training.

Run it yourself, from a clone of your copy. The copy must already exist, made from
eclipse-score/contributor_training with "Use this template" (only ``main`` is copied).

It creates, in your copy:

* the labels ``stage-0`` .. ``stage-6`` and the three track labels,
* the branches ``defect/build-1`` .. ``defect/build-3`` from ``patches/build-*.patch``,
* the prepared pull requests from ``patches/r1``, ``r2``, ``r3``, ``r4`` and the ``r5`` variant
  of another track, and the two review comments on the r3 pull request,
* the task issues from ``issues/*.md``, with the track texts and pull request numbers filled in.

The pull requests and the review are posted under your own account.

Usage::

    python3 training/setup.py <you>/<copy> <quality|safety|security>
    python3 training/setup.py ... --dry-run    # everything local, nothing pushed or created

It refuses a repository that was not made from the template, and is safe to run again: what an
interrupted run created (branches, pull requests, the review, issues) is taken over, not duplicated.

Only ``git`` and ``gh`` are needed; all GitHub writes go through ``gh api``, which works with
old ``gh`` releases that have no ``gh label``.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = "eclipse-score/contributor_training"

LABELS = [(f"stage-{n}", "0e8a16", f"Training stage {n}") for n in range(7)] + [
    ("quality", "1d76db", "Quality track"),
    ("safety", "d93f0b", "Safety track"),
    ("security", "5319e7", "Security track"),
    ("improvement", "fbca04", "Continuous improvement of the training"),
]

ROLES = {
    "quality": {
        "ROLE_TOPIC": "the module verification report",
        "ROLE_DOC": "the module verification report, `docs/verification_report/module_verification_report.rst`,"
        " and the release note, `docs/module/release/release_note.rst`",
        "r5": "r5-safety",
    },
    "safety": {
        "ROLE_TOPIC": "the FMEA",
        "ROLE_DOC": "the module safety plan, `docs/module/safety_mgt/module_safety_plan.rst`",
        "r5": "r5-security",
    },
    "security": {
        "ROLE_TOPIC": "the security analysis (threat analysis and risk assessment)",
        "ROLE_DOC": "the module security plan, `docs/module/security_mgt/module_security_plan.rst`",
        "r5": "r5-safety",
    },
}

PR_BODY = "Please review."

# Protect main only. A ruleset on all branches would reject every new branch the script pushes,
# because a new branch cannot have a green check yet. The API, unlike the web form, accepts check
# names that have never run in the repository, so the checks can be required from the start.
# GitHub offers rulesets for public repositories, and for private ones only on paid plans.
RULESET = {
    "name": "Main",
    "target": "branch",
    "enforcement": "active",
    "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
    "bypass_actors": [],
    "rules": [
        {"type": "deletion"},
        {"type": "non_fast_forward"},
        {"type": "pull_request", "parameters": {
            "required_approving_review_count": 0,
            "dismiss_stale_reviews_on_push": False,
            "require_code_owner_review": False,
            "require_last_push_approval": False,
            "required_review_thread_resolution": False,
        }},
        {"type": "required_status_checks", "parameters": {
            "strict_required_status_checks_policy": False,
            "required_status_checks": [
                {"context": "build-docs / Build Documentation"},
                {"context": "🔬 Pre-Commit"},
            ],
        }},
    ],
}


def run(cmd: list[str], cwd: Path | None = None, stdin: str | None = None) -> str:
    result = subprocess.run(cmd, cwd=cwd, input=stdin, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed:\n{result.stdout}{result.stderr}")
    return result.stdout


def api(method: str, path: str, payload: dict | None = None, ok_codes: tuple[int, ...] = ()) -> dict:
    """Call the GitHub REST API through gh, retrying what the secondary rate limit rejects."""
    cmd = ["gh", "api", "-X", method, path, "--include"]
    if payload is not None:
        cmd += ["--input", "-"]
    for attempt in range(4):
        result = subprocess.run(
            cmd, input=json.dumps(payload) if payload is not None else None, text=True, capture_output=True
        )
        # gh prints the status line with \n and the headers with \r\n
        head, body = (re.split(r"\r?\n\r?\n", result.stdout, maxsplit=1) + [""])[:2]
        status = int(re.search(r"HTTP/\S+ (\d+)", head).group(1)) if head.startswith("HTTP") else 0
        if result.returncode == 0:
            time.sleep(1)  # stay well below the secondary rate limit for content creation
            return json.loads(body) if body.strip() else {}
        if status in ok_codes:
            return {}
        if status == 403 and "secondary rate limit" in body.lower() and attempt < 3:
            time.sleep(60 * (attempt + 1))
            continue
        raise RuntimeError(f"gh api {method} {path} -> {status}\n{body or result.stderr}")
    raise AssertionError("unreachable")


def patch_subject(patch: Path) -> str:
    """The commit subject, unfolded: format-patch wraps long headers onto indented lines."""
    match = re.search(r"^Subject: (?:\[PATCH[^\]]*\] )?(.*(?:\n[ \t].*)*)", patch.read_text(), re.MULTILINE)
    if not match:
        raise ValueError(f"no subject in {patch}")
    return re.sub(r"\n[ \t]+", " ", match.group(1)).strip()


def make_branch(work: Path, branch: str, patch: Path, push: bool) -> str:
    """Create the branch from the patch, or take the one an earlier run already pushed.

    The branch starts at the first commit of the copy, which is the state every patch was made
    against, so that a later run still applies cleanly after pull requests were merged.
    """
    remote = run(["git", "branch", "-r", "--list", f"origin/{branch}"], cwd=work).strip()
    if remote:
        return run(["git", "rev-parse", f"origin/{branch}"], cwd=work).strip()
    root = run(["git", "rev-list", "--max-parents=0", "origin/main"], cwd=work).split()[-1]
    run(["git", "switch", "-q", "-c", branch, root], cwd=work)
    run(["git", "am", "-q", str(patch)], cwd=work)
    if push:
        run(["git", "push", "-q", "origin", branch], cwd=work)
    sha = run(["git", "rev-parse", "HEAD"], cwd=work).strip()
    run(["git", "switch", "-q", "--detach", "origin/main"], cwd=work)
    return sha


def review_comments(work: Path, sha: str) -> list[dict]:
    spec = json.loads((HERE / "reviews" / "r3.json").read_text())
    comments = []
    for c in spec["comments"]:
        lines = run(["git", "show", f"{sha}:{c['path']}"], cwd=work).splitlines()
        matches = [i + 1 for i, line in enumerate(lines) if line == c["line_text"]]
        if len(matches) != 1:
            raise ValueError(f"{c['path']}: expected one line {c['line_text']!r}, found {len(matches)}")
        comments.append({"path": c["path"], "line": matches[0], "side": "RIGHT", "body": c["body"]})
    return comments


def render_issue(path: Path, values: dict[str, str]) -> tuple[str, list[str], str]:
    text = re.sub(r"\A<!--.*?-->\s*", "", path.read_text(), flags=re.DOTALL)  # licence header
    head, _, body = text.partition("\n---\n")
    fields = dict(line.split(": ", 1) for line in head.splitlines())
    for key, value in values.items():
        body = body.replace("{{" + key + "}}", value)
        fields["title"] = fields["title"].replace("{{" + key + "}}", value)
    left = re.findall(r"\{\{\w+\}\}", fields["title"] + body)
    if left:
        raise ValueError(f"{path.name}: unfilled {left}")
    return fields["title"], [label.strip() for label in fields["labels"].split(",")], body.strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", help="your copy, owner/name")
    parser.add_argument("role", metavar="track", choices=sorted(ROLES))
    parser.add_argument("--dry-run", action="store_true", help="apply everything locally, push and create nothing")
    parser.add_argument("--clone-url", help="clone from here instead of GitHub (for testing)")
    parser.add_argument("--ruleset", action="store_true",
                        help="also create a ruleset on main (pull request, no approvals, two required checks);"
                        " public copies only, unless your plan offers rulesets for private repositories")
    parser.add_argument("--template", default=TEMPLATE,
                        help=f"the template the copy must be made from (default {TEMPLATE})")
    args = parser.parse_args()

    role = ROLES[args.role]
    push = not args.dry_run
    url = args.clone_url or f"git@github.com:{args.repo}.git"

    if not args.clone_url:
        info = json.loads(run(["gh", "api", f"repos/{args.repo}"]))
        source = (info.get("template_repository") or {}).get("full_name")
        if source != args.template:
            print(f"{args.repo} was not made from {args.template} (template: {source}). An empty repository or a"
                  " plain copy cannot be used: create it with \"Use this template\".", file=sys.stderr)
            return 1

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "repo"
        run(["git", "clone", "-q", url, str(work)])
        # "Include all branches" copies every branch of the template into the copy.
        extra = [b for b in run(["git", "branch", "-r", "--format=%(refname:short)"], cwd=work).split()
                 if b not in ("origin/main", "origin/HEAD", "origin")
                 and not b.startswith(("origin/defect/", "origin/review/"))]
        if extra:
            print(f"{args.repo} has branches that do not belong in a training copy: {', '.join(extra)}."
                  " It was probably created with \"Include all branches\". Delete them first.", file=sys.stderr)
            return 1

        # An earlier run may have stopped half-way; take over what it created instead of duplicating it.
        prs: dict[str, int] = {}
        titles: set[str] = set()
        if push:
            for pr in api("GET", f"repos/{args.repo}/pulls?state=all&per_page=100"):
                prs[pr["head"]["ref"]] = pr["number"]
            for issue in api("GET", f"repos/{args.repo}/issues?state=all&per_page=100"):
                if "pull_request" not in issue:
                    titles.add(issue["title"])

        if args.ruleset:
            if not push:
                print("ruleset: would create \"Main\" on the default branch")
            elif any(r["name"] == RULESET["name"] for r in api("GET", f"repos/{args.repo}/rulesets")):
                print("ruleset exists: Main")
            else:
                api("POST", f"repos/{args.repo}/rulesets", RULESET)
                print("ruleset: Main")

        if push:
            for name, color, description in LABELS:
                api("POST", f"repos/{args.repo}/labels",
                    {"name": name, "color": color, "description": description}, ok_codes=(422,))
        print(f"labels: {len(LABELS)}")

        for n in (1, 2, 3):
            make_branch(work, f"defect/build-{n}", HERE / "patches" / f"build-{n}.patch", push)
            print(f"branch defect/build-{n}")

        numbers: dict[str, str] = {}
        for key, patch_name in (("R1", "r1"), ("R2", "r2"), ("R3", "r3"), ("R4", "r4"), ("R5", role["r5"])):
            patch = HERE / "patches" / f"{patch_name}.patch"
            branch = f"review/{patch_name}"
            sha = make_branch(work, branch, patch, push)
            title = patch_subject(patch)
            if push and branch in prs:
                numbers[f"PR_{key}"] = str(prs[branch])
            elif push:
                pr = api("POST", f"repos/{args.repo}/pulls",
                         {"title": title, "head": branch, "base": "main", "body": PR_BODY})
                numbers[f"PR_{key}"] = str(pr["number"])
            else:
                numbers[f"PR_{key}"] = f"<{key}>"
            if key == "R3":
                comments = review_comments(work, sha)
                if push and not api("GET", f"repos/{args.repo}/pulls/{numbers['PR_R3']}/reviews"):
                    api("POST", f"repos/{args.repo}/pulls/{numbers['PR_R3']}/reviews",
                        {"commit_id": sha, "event": "COMMENT", "comments": comments})
                print(f"  review comments on lines {[c['line'] for c in comments]}")
            print(f"pull request #{numbers[f'PR_{key}']} {branch}: {title}")

        values = {**numbers, "ROLE_TOPIC": role["ROLE_TOPIC"], "ROLE_DOC": role["ROLE_DOC"]}
        for path in sorted((HERE / "issues").glob("*.md")):
            title, labels, body = render_issue(path, values)
            labels.append(args.role)
            if push and title in titles:
                print(f"issue exists: {title}")
            elif push:
                issue = api("POST", f"repos/{args.repo}/issues", {"title": title, "body": body, "labels": labels})
                print(f"issue #{issue['number']} {title}")
            else:
                print(f"issue {title}  {labels}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
