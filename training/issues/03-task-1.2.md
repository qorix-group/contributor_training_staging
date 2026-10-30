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

title: 1.2-1.3 Fix typos with a commit that carries its reasoning
labels: stage-1
---
The disclaimer in `docs/module/release/release_note.rst` contains the words "but the as the project". Fix the sentence.

- Create a branch with a meaningful name.
- Commit with an explicit pathspec: `git commit -m "<message>" -- docs/`.
- The commit message says what was wrong and how you checked the fix (build, rendered page).

Then find a **second** typo in the documentation yourself, raise an issue for it yourself (task 1.3): on GitHub, **Issues → New issue → Bug (S-CORE form)**, the form S-CORE uses for defects (see `TRAINING.md`, rule 2), and fix it in the same or in a second pull request.

**Done when** your pull requests are merged with green CI and close this issue and yours.
