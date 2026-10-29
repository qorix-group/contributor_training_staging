<!-- ----------------------------------------------------------------------------
  Copyright (c) 2026 Contributors to the Eclipse Foundation

  See the NOTICE file(s) distributed with this work for additional
  information regarding copyright ownership.

  This program and the accompanying materials are made available under the
  terms of the Apache License Version 2.0 which is available at
  https://www.apache.org/licenses/LICENSE-2.0

  AI Disclosure: This file was largely AI-generated. The AI-generated
  portions are made available under CC0-1.0 and not subject to the
  project's licence. The human contributor has reviewed and verified
  that the content is correct.

  SPDX-License-Identifier: Apache-2.0 AND CC0-1.0
  Assisted-by: Claude Code (claude-opus-5-5)
----------------------------------------------------------------------------- -->

# Training solutions

Every built-in defect, where it is, why it is wrong, and the expected reaction. This file is open
on purpose, and it is in every copy of the training: it lets anyone check and improve the training.
If you are doing the training, reading it first only shortens what you learn.

Each patch in `patches/` becomes one branch in a training copy. Its commit message is deliberately
neutral, because it ends up in the participant's history.

## Stage 2 — build defects

All results below were checked on 2026-10-14 against the initial state of the training module
(module_template `b60778b`, score_docs_as_code 8.4.0). Warnings are treated as errors, so every
docs warning fails `bazel run //:docs`.

Re-checked 2026-10-29 on the first commit of the S-CORE version (`4dc60d8`): `main` builds
green, and every defect branch shows exactly the messages and the `_build` content below.

### `defect/build-1` (task 2.2) — two issues expected

| Defect | What the build says | Expected fix |
| --- | --- | --- |
| The user manual refers to `doc__training_module_release_note`, an id that does not exist | `user_manual.rst:121: WARNING: linked need doc__training_module_release_note not found [needs.link_ref]` | Refer to the release note's real id, `doc__mod_temp_module_name_release_note` |
| `comp_req__component_example__heartbeat_status` is QM but derived from the ASIL_B `feat_req__example_feature__example_req` | `Parent need ... does not fulfill condition safety == QM. Explanation: QM requirements cannot be derived from ASIL requirements. [score_metamodel]` | Classify the requirement ASIL_B. Removing `derived_from` also turns the build green but leaves an orphan requirement — reject that fix |

Checked: with both fixes the build is green with an empty `warnings.txt`.

### `defect/build-2` (task 2.3) — four issues expected

| Defect | Found by | Expected fix |
| --- | --- | --- |
| Safety manual retitled to "Training_Module Safety Manual" without lengthening the `===` underline | docs build: `Title underline too short. [docutils]` | Underline as long as the title |
| Security manual `:status: released` | docs build: `status (released): does not follow pattern ^(valid\|draft\|invalid)$ [score_metamodel]` | `draft` (or `valid` with an approving PR) — the allowed values come from the metamodel |
| Release note has no copyright header | **pre-commit only** (hook `copyright`); `bazel run //:copyright.check` does not scan `docs/` | Restore the header, or let `pre-commit run` add it |
| Trailing whitespace in the user manual | **pre-commit only** (hook `trailing-whitespace`) | `pre-commit run` fixes it |

The lesson is that a green docs build is not a green CI: two of the four defects only show up in
the Pre-Commit job. Both hooks fix the file themselves — the participant should notice that and commit
the result.

### `defect/build-3` (task 2.4) — one issue expected

The branch renames `user_manual.rst` to `user_guide.rst` and retitles it. Built incrementally after
a build of `main`, `_build/module/manuals/` holds both `user_guide.html` ("Training_Module User
Guide") and the orphan `user_manual.html` ("[Module Name] User Manual"). The build is green and
`needs.json` is correct; only the HTML output is stale.

Expected explanation: `bazel run //:docs` is incremental and never deletes the output of a source
file that has gone away. Fix: `rm -rf _build && bazel run //:docs`.

## Stage 4 — prepared pull requests

Every prepared pull request builds green and passes pre-commit (checked 2026-10-14 on top of the initial state). Nothing in them is found by a tool; the participant has to read.

### PR #R1 (task 4.1) — form, `r1.patch`, release note

| Defect | Where | How it shows |
| --- | --- | --- |
| Typo "Relase" in the page **and** the need title | title and `.. document::` | The typo appears in every needtable that lists the document |
| Typo "adressed" | Known Issues | — |
| Typo "seperately" | Known Issues, Issue 1 | — |
| Single backticks around `score/component_example` | Known Issues, Issue 1 | Rendered in italics (`<cite>`), not as code; RST needs double backticks |
| No blank line between "The following issues are known …:" and the list | Known Issues | The whole list renders as **one paragraph** with literal "- " — only visible in the rendered page |

### PR #R2 (task 4.2) — content, `r2.patch`, feature safety plan + requirements

Seven defects; the pass mark is five.

| # | Defect | Where | Why it is wrong |
| --- | --- | --- | --- |
| 1 | Qualification "as required by ISO 26262-8 clause 12 (see its EXAMPLE)" for `component_example` as an "in-house component already in service" | new section "Qualification of software components" | An EXAMPLE is informative, it obliges nothing. And a component developed within the ISO 26262 process is not clause 12's population. Clause 12 is for software developed outside it; a project that reads it so records that reading, for example in its tailoring |
| 2 | Tool qualification tailored out "according to `std_req__iso26262__support_6421`" | Tailoring | "support" is Part 8, but clause 6 is the specification of safety requirements. Tool confidence is clause 11 (`support_1141`, `support_1142`). A manual review is also no argument by itself |
| 3 | `comp_req__component_example__hb_missing` (ASIL_B) derived from `feat_req__component_example__hb_supervision` (QM), itself from a QM stakeholder requirement | `requirements.rst` | Child classified above its parent; the build only checks the opposite direction |
| 4 | "All review findings … closed within 24 hours of being raised" | Feature Safety Package | Unrealistic; becomes a deviation in the first audit |
| 5 | `:status: valid` while the document still says "See TBD." and contains a TBD open point | document header | The approval of the pull request releases what is written, including the TBD |
| 6 | DFA tailored out by "In the project meeting on 2026-10-20 we decided …" | Tailoring | A decision only in prose; no decision record, nothing the graph can see. "Runs in a single process" is also no DFA argument |
| 7 | "Open point: TBD - clarify who performs the feature FMEA." | Feature Safety Package | No owner, no trigger |

### PR #R3 (task 4.3) — answering a review, `r3.patch` + `reviews/r3.json`

The change itself is clean. The setup script posts two review comments, under the participant's own account:

| Comment | Correct reaction |
| --- | --- |
| "`.bazelversion` pins Bazel 8.7.0 …" on the Build System line | **Accept**: state Bazel 8.7.0 |
| "Training_Module does not support QNX …" on the Operating Systems line | **Reject with evidence**: `MODULE.bazel` registers the QNX toolchains `score_qnx_x86_64_ifs_toolchain` and `score_qnx_aarch64_ifs_toolchain` (module_template #199) |

### PR #R4 (task 5.3) — conflict, `r4.patch`

Changes "succeeded by" to "followed by" in the `id` instruction line of the release note, the module
safety plan and the module security plan — the same line template commit #198 rewrites. Checked by
simulation: a branch carrying the #198 change, rebased onto `main` with #R4 merged, conflicts in all
three files. The correct resolution keeps the template's line (lower snake case, `doc__`,
`_<suffix>`).

The setup script opens #R4. Issue 5.1-5.3 makes the order explicit: open the template-update pull
request, do **not** merge it, merge #R4, then rebase. Template update comes before filling in the
document (task 5.4), because a participant who fills in first may delete the `.. attention::` blocks,
and #R4 would then no longer merge cleanly into `main`.

Checked 2026-10-15 by a local simulation of a whole participant week: `main` after realistic merges of
stages 1-4 (typo fix, build-1 and build-2 with fixes, r1 with fixes, r2, r3 with the Bazel fix,
r5-security); then for each track document a branch with the #198 change; #R4 applied to `main`
cleanly; rebasing each branch onto it conflicted in its own file - release note, module safety
plan, module security plan.

Re-checked 2026-10-29 on `4dc60d8` with `main` + r1, r2, r3, r5-security, then r4: the same
three conflicts.

### PR #R5 (task 6.1) — cross-review

A participant reviews the variant that is **not** their track: Quality and Security participants get
`r5-safety.patch`, Safety participants get `r5-security.patch`.

| Variant | Defect | Why it is wrong |
| --- | --- | --- |
| safety (feature AoU) | Restart "within 1 microsecond" | Unrealistic metric |
| safety | `:status: valid` with "a heartbeat period of TBD ms" | Released with an open value |
| safety | "No further Assumptions of Use are needed; we agreed on this … in the call" | Decision only in prose |
| security (feature security AoU) | CI pipeline "as required by `std_req__isosae21434__continual_8321`" | "continual" is clause 8, continual cybersecurity activities (monitoring, event evaluation, vulnerabilities) — not continuous integration |
| security | Fix "to all vehicles in the field within 24 hours" | Unrealistic metric |
| security | "Open point: TBD - decide where the authentication keys are stored." | No owner, no trigger |

## Stage 5 — track defects on `main`

These are on `main` (PR #3) and therefore in every participant repository from the start. The participant meets them in task 5.4.

| Track | Document | Defect | Why it is wrong |
| --- | --- | --- | --- |
| Quality | Module verification report, 4.1 | 100 % C0 and C1 coverage for every unit at every merge, zero open findings at any time | Unrealistic; a target nobody meets becomes a deviation in the first audit |
| Safety | Module safety plan, scope | Module declared QM while the plan and the component documents carry ASIL_B | Child classified above its parent. The metamodel check only flags the other direction, so the build stays green |
| Security | Module security plan, tailoring | Cybersecurity assessment tailored out with reference `std_req__isosae21434__assessment_15621` | The stem "assessment" belongs to clause 15 (TARA methods); the cybersecurity assessment is clause 6.4.9 (`prj_management_649x`) |

The template defect for tasks 5.1-5.3: `docs/` and `score/component_example/docs/` are at the parent
of module_template `775aad3c` (#198), except the quick-start commands in `docs/index.rst`, which
are taken from #218; `git diff upstream/main -- docs` against the public template shows the
difference.

The template commit does more than the participant's document. #198 also renames the user manual's
id from `doc__user_manual` to `doc__mod_temp_module_name_user_manual`, and the safety and security
plans it brings refer to the new id. A Safety or Security participant who updates only the plan gets
`linked need doc__mod_temp_module_name_user_manual not found`. Expected reaction: read #198, take its
id change in `user_manual.rst` into the same pull request, and check that nothing else refers to the
old id. The Quality documents at #198 build without it. Checked 2026-10-29 by a clean build of each
track's documents at `775aad3c`: quality green, safety and security with exactly this warning.

Task 6.2: Safety and Security review their plan with the module's FDR checklist; the module has none
for the verification report or the release note, so Quality uses the process description's
`gd_chklst__review_checklist`.
