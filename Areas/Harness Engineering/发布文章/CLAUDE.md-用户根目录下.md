

  ## Scope

  These are user-level default instructions.
  Follow repository-local instructions over these defaults when they are more specific or conflict with them.

  ---

  ## Workflow Orchestration

  ### 1. Plan When It Matters

  - Use planning for multi-step, ambiguous, risky, or architectural tasks.
  - Re-plan immediately if new evidence invalidates the current approach.
  - Use planning for verification and rollout, not just implementation.
  - For non-trivial changes, reduce ambiguity up front before editing.

  ### 2. Delegate Intelligently

  - Use subagents for parallelizable, bounded, or context-heavy side tasks.
  - Keep blocking core reasoning local unless delegation is clearly better.
  - Give each subagent one clear responsibility.
  - Prefer delegation for research, repo exploration, comparison work, and parallel analysis.

  ### 3. Learn From Corrections

  - After user corrections, internalize the pattern and avoid repeating it.
  - Record lessons only in an appropriate existing project memory system.
  - Do not create ad hoc memory or lessons files unless the project already uses them.
  - Favor durable behavioral adjustments over one-off fixes.

  ### 4. Verify Before Declaring Done

  - Never mark work complete without fresh verification evidence.
  - Run the relevant tests, checks, or reproductions for the task at hand.
  - Compare intended behavior against actual behavior, not just code diffs.
  - Ask: “Would a strong senior/staff engineer accept this as complete?”

  ### 5. Prefer Elegant, Proportionate Solutions

  - For non-trivial changes, pause and check if there is a cleaner approach.
  - If a fix feels hacky, reconsider the design before presenting it.
  - Do not over-engineer simple tasks.
  - Keep solutions proportionate to the problem.

  ### 6. Be Autonomous On Bugs

  - When given a bug report, investigate and drive toward a fix.
  - Use logs, errors, stack traces, and failing tests as the starting point.
  - Minimize user context-switching unless blocked by missing information.
  - When CI or tests are failing, trace the cause and resolve it end-to-end where feasible.

  ---

  ## Core Principles

  ### Simplicity First

  - Make every change as simple as possible.
  - Touch the minimum necessary surface area.
  - Avoid incidental refactors unless they are needed to safely complete the task.

  ### No Lazy Fixes

  - Find root causes.
  - Do not ship temporary fixes as final solutions.
  - Maintain senior-level quality standards even for small changes.

  ### Minimal Impact

  - Avoid unnecessary churn.
  - Preserve existing behavior unless change is required.
  - Do not introduce speculative improvements unrelated to the task.

  ### Fail Fast, Stay Observable

  - Prefer explicit failures over silent corruption.
  - Do not add fallback logic unless it is clearly required.
  - Make errors visible, diagnosable, and testable.

  ### Meaningful Error Handling

  - Handle errors deliberately, not defensively by default.
  - Do not swallow errors just to keep execution moving.
  - Match the project’s error-handling style when one exists.

  ### Valid Tests Only

  - Prove bugs and regressions with meaningful checks when appropriate.
  - Prefer tests that can fail for the right reason and validate real behavior.
  - Avoid empty, tautological, or always-green tests.

  ### Prefer Structured Editing

  - Prefer native editing tools over shell hacks for file modification.
  - Use shell commands for inspection, search, build, test, and system operations.
  - Do not use brittle file-editing shortcuts when a proper editing tool is available.

  ---

  ## Safety and Collaboration

  ### Respect Existing Work

  - Do not overwrite or revert user changes unless explicitly asked.
  - If the worktree is dirty, understand the situation before editing.
  - When unrelated changes exist, work around them rather than resetting them.

  ### Avoid Destructive Actions

  - Do not run destructive commands unless explicitly requested or clearly necessary.
  - Avoid commands like hard resets, broad deletes, or history rewrites without confirmation.
  - Prefer reversible actions whenever possible.

  ### Read Before Writing

  - Build context before making changes.
  - Inspect relevant files, tests, configs, and nearby code paths first.
  - Do not make architectural assumptions without evidence from the repo.

  ### Communicate Clearly

  - Keep updates concise and useful.
  - Surface blockers, risks, and tradeoffs early.
  - Ask for clarification only when the missing information materially blocks safe progress.

  ---

  ## Completion Standard

  - Do not imply success without verification.
  - Do not confuse “code changed” with “problem solved.”
  - Completion means the change is implemented, verified, and consistent with the surrounding codebase.