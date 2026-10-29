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

title: 5.1-5.3 Bring your document to the current template state
labels: stage-5
---
Your document: **{{ROLE_DOC}}**. Do this task **before** you fill the document in (task 5.4). Follow the steps in this order; the order is part of the task.

**5.1 Find the deviation.** Compare your document with the module template it came from: `git fetch upstream`, then `git diff main upstream/main -- <your file>`. Which template commit is your document missing? Raise an issue for it with the "Training finding" template (on GitHub: **Issues → New issue → Training finding**).

**5.2 Update on a branch.** Create a branch from `main`, bring the document to the current template state, commit, push and open a pull request that closes your issue and this one. **Do not merge it yet.**

**5.3 A colleague was faster.** While your pull request was open, pull request #{{PR_R4}} changed the same file. Merge #{{PR_R4}} into `main` now. Then bring your branch up to date **by rebasing** onto `main`, resolve the conflict in VS Code's merge editor and push with `git push --force-with-lease`. When you resolve the conflict, decide which side is right. Do not just pick one.

**Done when** your pull request is merged on top of #{{PR_R4}} with a linear history and a green build, and it closes your issue and this one.
