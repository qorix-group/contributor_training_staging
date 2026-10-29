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

title: 0.1 Set up your environment
labels: stage-0
---
Set up the environment S-CORE uses and prove that it works.

**Skip any step you have already done**, for example from earlier work on S-CORE. Write "already in place" for it on your participant page, so that skipped can be told from forgotten.

1. Ubuntu 24.04 (native, VM or WSL), VS Code, Bazel via Bazelisk, `gh`, `pre-commit`.
2. `gh auth login`, and an SSH key registered on GitHub.
3. An Eclipse Foundation account with a signed **Eclipse Contributor Agreement (ECA)**, and your GitHub username entered in your Eclipse account profile. What the ECA is: https://www.eclipse.org/legal/eca/ · sign it: https://accounts.eclipse.org/user/eca · edit your profile: https://accounts.eclipse.org/user/edit Use the same e-mail address for the Eclipse account and for your git commits (`git config user.email`). This repository does not need it, but you do once you contribute to S-CORE after the training: S-CORE only accepts commits whose author has a signed ECA.
4. Clone your copy as described in `TRAINING.md`, including the `upstream` remote.
5. `bazel run //:ide_support`, then select `.venv_docs/bin/python` as the Python interpreter in VS Code, and start `bazel run //:live_preview`.
6. In this repository, **Settings → General → Features**: check that Issues are enabled.

**Done when** a merged pull request adds your page `docs/participants/<name>.rst` and adds the page to the toctree in `docs/participants/index.rst`. The page lists the versions of Bazel, `gh`, VS Code and Python, and states that your ECA is signed and linked to your GitHub username. CI must be green.
