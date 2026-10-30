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

# Maintaining the training

This folder holds everything the setup puts into a training copy: the defect patches, the prepared
pull requests, the task issues and the solution key. It is open on purpose: anyone can check the
training and improve it. Participants start with `TRAINING.md`.

| Path | What it is |
| --- | --- |
| `SOLUTIONS.md` | Every built-in defect, where it is, why it is wrong, and the expected reaction |
| `patches/build-*.patch` | Stage 2 defect branches `defect/build-1` .. `defect/build-3` |
| `patches/r*.patch` | Prepared pull requests #R1–#R5, branches `review/<name>`; `r5-safety` / `r5-security` by track |
| `reviews/r3.json` | The two review comments the setup posts on the r3 pull request |
| `issues/*.md` | The task issues and the continuous improvement issue, with `{{…}}` placeholders the setup fills in |
| `setup.py` | Creates all of the above in one copy |

Patch commit messages are neutral on purpose: they end up in the participant's history. Every patch
applies to the first commit of a copy, the state "Use this template" creates.

## Changing the training

1. Make the change on a branch from the commit the patches apply to, build it clean
   (`rm -rf _build && bazel run //:docs`) and run `pre-commit run --all-files`.
2. Export it with `git format-patch -1 <branch> --stdout > training/patches/<name>.patch`, and
   update `SOLUTIONS.md` in the same commit: what the defect is, how it shows, the expected fix,
   and what you checked.
3. Run the setup with `--dry-run` for every track. It applies every patch and renders every issue.
4. Before a release, run the whole training once in a real copy: the setup without `--dry-run`,
   then every prepared pull request's CI.

A change to anything outside `training/` changes the first commit of every new copy, and with it
the base the patches apply to. Check that every patch still applies (`--dry-run`), and that the
stage 5 conflict still happens (see `SOLUTIONS.md`, PR #R4).

## Adding a track

A track is an entry in `ROLES` in `setup.py` and a label in `LABELS`:

* `ROLE_TOPIC`: the topic for task 3.2,
* `ROLE_DOC`: the document the participant fills in in task 5.4,
* `ROLE_CHECKLIST`: the checklist for the formal review of that document in task 6.2,
* `r5`: the cross-review pull request (6.1) of another track.

Then add the track's defects to the module's documents (one per track is enough, see
`SOLUTIONS.md`, stage 5), add the track to the table in `TRAINING.md`, and run the dry run for it.
A track whose work is not a document, such as testing, also needs its own task texts in `issues/`;
the setup takes every file there for every track today.

## The S-CORE issue forms

`.github/ISSUE_TEMPLATE/5_Bug.yml` and `4_Task.yml` are copies of the organisation forms in
`eclipse-score/.github`, so that participants practise the forms S-CORE uses. Each names the commit
it was copied from. Before a release, compare them with the organisation's current forms and copy
them again if they changed; keep the two deviations their header states and nothing else.

## Feedback, bug reports, completed trainings

They arrive as issues in `eclipse-score/contributor_training`, through the forms in
`.github/ISSUE_TEMPLATE/`. The maintainers read them and fix the training; there is no support.
The "Training completed" issues are the record of conducted trainings, evidence for
`wp__training_path`. Close each one once read; do not delete them.
