<!-- ----------------------------------------------------------------------------
  Copyright (c) 2026 Contributors to the Eclipse Foundation

  See the NOTICE file(s) distributed with this work for additional
  information regarding copyright ownership.

  This program and the accompanying materials are made available under the
  terms of the Apache License Version 2.0 which is available at
  https://www.apache.org/licenses/LICENSE-2.0

  SPDX-License-Identifier: Apache-2.0
----------------------------------------------------------------------------- -->

# S-CORE contributor training

You work in your own copy of a training module, `Training_Module`. It is built like a real S-CORE
module: the module template, the S-CORE process description and the S-CORE tooling. Nothing you do
in your copy can break a real project, so try things, break the build and repair it.

The module is fictive. Some of its documents are wrong on purpose. Finding out what is wrong, and
proving it, is the training.

**The training is self-organised.** There is no tutor and no support. You set up your copy
yourself, you work through it at your own pace, and when something breaks, you repair it yourself:
see [When something breaks](#when-something-breaks). Repairing it is part of the training.

**The solutions are open.** `training/SOLUTIONS.md` lists every built-in defect. The training is
voluntary: if you read the solutions first, you only shorten what you learn.

## Tracks

Choose one track. The tasks are the same for every track; the documents you review and fill in are
your track's.

| Track | Your document in stage 5 |
| --- | --- |
| `quality` | module verification report and release note |
| `safety` | module safety plan |
| `security` | module security plan |

More tracks can be added; `training/README.md` says how.

## Set up your copy

You need a GitHub account, `git`, and `gh` logged in (`gh auth login`).

1. On this repository's GitHub page, choose **Use this template → Create a new repository**: owner
   your own account, any name, **Private** or **Public**. Leave **"Include all branches"
   unticked**; the setup refuses a copy with other branches than `main`.
2. Clone your copy and run the setup from it. Try it with `--dry-run` first: it clones, applies
   and renders everything without pushing or creating anything.

   ```bash
   git clone git@github.com:<you>/<copy>.git
   cd <copy>
   python3 training/setup.py <you>/<copy> <quality|safety|security> --dry-run
   python3 training/setup.py <you>/<copy> <quality|safety|security>
   ```

   It creates the labels, the defect branches, five prepared pull requests and the task issues in
   your copy. The prepared pull requests and the review comments on one of them are posted under
   your own account: read them as if a colleague had written them.
3. Then, in your clone:

   ```bash
   git pull
   git remote add upstream https://github.com/eclipse-score/module_template.git
   pre-commit install
   rm -rf _build && bazel run //:docs
   ```

   `upstream` is the public S-CORE module template this training module was made from. Open the
   issue labelled `stage-0`.

**Protect `main`**, if you can: a public copy can have a ruleset that requires a pull request and
the checks "Build Documentation" and "🔬 Pre-Commit" (`training/setup.py --ruleset` creates it). A
private copy on a free account cannot. Then "green CI before merging" is your own discipline.

## The week

Plan about **five working days**. Every task is an issue in your copy, labelled `stage-0` to
`stage-6`. Work through them in order.

| Day | Stages | Done in the evening |
| --- | --- | --- |
| 1 | 0 environment, 1 git | environment works, first pull request merged |
| 2 | 2 build | all defect branches are green |
| 3 | 3 process, 4 review | findings recorded, reviews submitted |
| 4 | 5 module | template update rebased and merged, your track's document filled in |
| 5 | 6 wrap-up | cross-review, formal review and retrospective done, certificate issued |

## Rules

1. **Every issue is closed by a merged pull request** whose description says `Closes #<n>`, with
   green CI. One pull request may close several issues, with one keyword per issue:
   `Closes #8, closes #23`. "Resolves #8 and #23" closes only #8. An issue you close by hand
   counts only when a merged pull request mentions it, or when the issue names a merged pull
   request as its result, in its text or in a comment. The continuous improvement issue is the
   exception: it may stay open.
2. **Some issues you create yourself.** The task tells you when. On GitHub, choose
   **Issues → New issue → Training finding** (the template is in
   `.github/ISSUE_TEMPLATE/training_finding.md`) and add the labels `stage-<n>` and your track.
   An issue must be workable without asking you: what is wrong, where, and how one recognises that
   it is fixed.
3. **The commit carries the reasoning.** Say what you checked and what it returned. In S-CORE a
   reviewer reads your pull request without you in the room; the reasoning has to be in it.
4. **You merge your own pull requests** once CI is green. Nobody reviews your copy: the closed
   issues and pull requests are your own record of what you did.

## Certificate

When every issue is closed, the last step is your **certificate of completion**: on GitHub, choose
**Actions → Certificate → Run workflow**, enter your full name and run it. The workflow checks rule 1
for every issue in your copy. If one does not meet it, the run fails and its summary lists the
issues and what to do; repair them and run it again. Otherwise download the PDF from the run's
**Artifacts**.

The certificate lists the stages you completed, your track, and how many tasks and own findings
your pull requests closed. It confirms that you completed the training, not that you are competent
in a role. It is not an Eclipse Foundation certification.

Then tell the training that you finished: in `eclipse-score/contributor_training`, open
**Issues → New issue → Training completed**. That issue is the record that the training was done.

## When something breaks

There is no support, so here is what to do yourself.

| What happened | What to do |
| --- | --- |
| `training/setup.py` stopped half-way | Run it again. It takes over what it already created instead of duplicating it. |
| A defect branch or prepared pull request is damaged beyond repair | Recreate it from your copy's first commit, which is where the setup made it: `git switch -C <branch> $(git rev-list --max-parents=0 HEAD) && git am training/patches/<name>.patch && git push -f origin <branch>`. The patch names are in `training/README.md`. |
| `main` is broken and you cannot find why | `git log` and `git revert` the merge that broke it, in a pull request. Finding that merge is a good exercise. |
| The copy is beyond repair | Delete the repository, make a new copy and run the setup again. Your progress is in the old copy's issues; read them before you delete it. |
| Actions minutes run out (private copies) | A free account has 2,000 minutes a month; the training needs a few hundred. Wait for the next month or make the copy public. |
| A task text is wrong, or a defect does not behave as described | That is a bug in the training: report it (below), work around it, and say so in your pull request. |

## Feedback, bugs and questions

- **Feedback or a bug in the training:** in `eclipse-score/contributor_training`, open
  **Issues → New issue → Feedback** or **Bug report**. Not in your copy: nobody else can see it.
  The maintainers read them; they do not give support.
- **Questions about S-CORE itself** go to the role that owns the topic, through the channels
  listed in the S-CORE User's Guide, "What's Next?":

  | Topic | Role |
  | --- | --- |
  | Process description | Process Community |
  | Quality, safety, security | Quality Manager, Safety Manager, Security Manager |
  | Code of a module | that module's Committers |
  | Tooling, CI, docs-as-code | Infrastructure Tooling Community |
  | Direction, getting involved | Project Leads |
