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

# S-CORE contributor training

A self-paced, hands-on training for people who want to contribute to
[Eclipse S-CORE](https://projects.eclipse.org/projects/automotive.score): build, review, fix and
rebase in a realistic S-CORE module, without any risk to a real project.

## Purpose

S-CORE work products are typed, linked and checked by the build, and every change reaches a
repository through a reviewed pull request. Someone who has only read the process description
meets the consequences for the first time in a real pull request. This training lets you meet
them first in a module where nothing can break.

**For whom:** people who will review or write work products in S-CORE in a quality, safety or
security role. Further tracks are planned; `training/README.md` says how one is added.

**After the training you can:**

| Stage | You can | Tasks | Material | Solution |
| --- | --- | --- | --- | --- |
| 0 Environment | set up the S-CORE toolchain and sign the Eclipse Contributor Agreement | [0.1](training/issues/01-task-0.1.md) | — | — |
| 1 Git | follow an upstream, write a commit that carries its reasoning, raise an issue with the S-CORE form | [1.1](training/issues/02-task-1.1.md), [1.2-1.3](training/issues/03-task-1.2.md) | the module itself | in the task |
| 2 Build | build clean, tell what the build checks from what only pre-commit checks, find the cause of a red build, recognise a stale incremental build | [2.1](training/issues/04-task-2.1.md), [2.2-2.4](training/issues/05-task-2.4.md) | [`patches/build-*`](training/patches/) | [Stage 2](training/SOLUTIONS.md#stage-2--build-defects) |
| 3 Process | trace a work product to its workflow and template, find what the project decided about it, record an open point with owner and trigger | [3.1](training/issues/06-task-3.1.md), [3.2](training/issues/07-task-3.2.md) | process description, `eclipse-score/score` | open research, none |
| 4 Review | review a pull request for form and for content, and answer a review with evidence | [4.1](training/issues/08-task-4.1.md), [4.2](training/issues/09-task-4.2.md), [4.3](training/issues/10-task-4.3.md) | [`patches/r1`–`r3`](training/patches/), [`reviews/r3.json`](training/reviews/r3.json) | [Stage 4](training/SOLUTIONS.md#stage-4--prepared-pull-requests) |
| 5 Module | bring a document to the current template state through a rebase conflict, and fill it in | [5.1-5.3](training/issues/11-task-5.1-5.3.md), [5.4](training/issues/12-task-5.4.md) | [`patches/r4`](training/patches/r4.patch), your track's document | [PR #R4](training/SOLUTIONS.md#pr-r4-task-53--conflict-r4patch), [Stage 5](training/SOLUTIONS.md#stage-5--track-defects-on-main) |
| 6 Wrap-up | review another track's work, perform a formal document review with a checklist, reflect | [6.1](training/issues/14-task-6.1.md), [6.2-6.3](training/issues/15-task-6.2-6.3.md) | [`patches/r5-*`](training/patches/) | [PR #R5](training/SOLUTIONS.md#pr-r5-task-61--cross-review) |

**What it does not teach:** the S-CORE architecture, writing code, or how to become a committer.

## How it works

- **Your own copy.** You make a copy of this repository in your own GitHub account and run the
  setup there. It fills the copy with defect branches, prepared pull requests and about fifteen
  task issues.
- **A fictive module.** `Training_Module` is made from the S-CORE module template and follows the
  S-CORE process description. Some of its documents are wrong on purpose.
- **Tracks:** quality, safety, security. About five working days.
- **Self-organised.** There is no tutor and no support. When something breaks, you repair it
  yourself; `TRAINING.md` says how.
- **Open solutions.** [`training/SOLUTIONS.md`](training/SOLUTIONS.md) lists every defect.
  Reading it first only shortens what you learn.
- **Certificate.** When every task is done, a workflow in your copy issues a certificate of
  completion.

**Start here: [`TRAINING.md`](TRAINING.md).** Maintaining or extending the training:
[`training/README.md`](training/README.md). Feedback and bug reports: the issue forms of this
repository.
