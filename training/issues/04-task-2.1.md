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

title: 2.1 Build the documentation clean and read the result
labels: stage-2
---
Run `rm -rf _build && bazel run //:docs` on `main`.

- How many warnings does the build report? Where is the list written?
- Why do we delete `_build` first?
- Run `pre-commit run --all-files` and list the hooks it runs. For each hook: would a violation also make `bazel run //:docs` fail, or does only pre-commit find it?

**Done when** a merged pull request records the answers on your participant page.
