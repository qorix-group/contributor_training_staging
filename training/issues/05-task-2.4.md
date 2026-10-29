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

title: 2.2-2.4 Repair the defect branches
labels: stage-2
---
The branches `defect/build-1`, `defect/build-2` and `defect/build-3` each contain defects.

For each branch:

1. Build it (`bazel run //:docs`) and run `pre-commit run --all-files`.
2. Create **one issue per defect** with the "Training finding" template. Quote the message.
3. Fix the defects in a pull request into `main` that closes those issues.

`defect/build-3` builds green. Build `main` first, then switch to `defect/build-3` and build again, and look at `_build/module/manuals/`. Explain what you see. **Do not merge `defect/build-3`**: record your explanation on your participant page instead, in a pull request that closes your issue for it.

A green docs build is not the same as a green CI.

**Done when** every defect has its own issue and all of them are closed by merged pull requests. This issue is closed by the last of them.
