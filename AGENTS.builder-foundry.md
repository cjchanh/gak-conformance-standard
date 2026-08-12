# Builder Foundry Instructions

When this kit is supplied for a build task:

1. Read `START_HERE.md` and `BUILDER_PRIME.md`.
2. Treat the operator's request as the mission and the target repository as the only writable project scope unless explicitly expanded.
3. Initialize `.builder-foundry/` with the supplied scripts.
4. Use research, product design, architecture, implementation, QA, security, performance, red-team, holdout, and release lanes as applicable.
5. Parallelize independent read-only work. Use one writer per overlapping scope or isolated git worktrees.
6. Preserve dirty worktrees and unrelated processes. Never fabricate evidence or weaken failing gates.
7. Do not push, deploy, publish, upload, spend money, expose secrets, or perform destructive cleanup without explicit operator authorization.
8. Do not stop at a plan, scaffold, prototype, green unit test, or summary. Stop only when the executable guard passes or a real blocker is documented with evidence.
