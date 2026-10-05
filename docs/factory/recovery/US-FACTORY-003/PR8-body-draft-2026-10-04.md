US-FACTORY-003 enforces the approved Lean Factory workflow while preserving fail-closed gates. Out-of-order history remains non-authorising without permanently blocking recovery; DONE is validated at its completion snapshot, with remote verification on feature branches and arrival builds.

Round 4 replaces separate Tester/QA gates with independent Validation, binds the read-only Jenkins GitHub credential, and runs the Factory CI composite (validator, canonical build/lint/full unit suite, pinned security scanners). Real integration uses two canonical phases with host Bash running the actual composite on the same disposable clone. Backend stages remain fail-closed and deployment stays blocked.

Validation: targeted canonical tests passed; real gitleaks/trivy/bandit scan passed; independent review plus one fix/re-review completed with zero Critical/Major findings. Jenkins feature build #3 (TS25, real) checked out exactly 36f95d5: Factory Validation stage PASS: validator PASS, canonical build/lint PASS, full Factory unit suite Ran 107 tests, OK (TS01-TS23, TS26-TS28: 0 failed, 0 not-executed), gitleaks "no leaks found", trivy/bandit executed, SECURITY SCAN PASSED, FACTORY CI PASS. The overall build result is FAILURE because the backend Build stage fails closed ("No supported project detected", I-005) and later stages were skipped: PIPELINE FAILED, DEPLOYMENT BLOCKED. Under ADR-0001 D6 this is Factory CI PASS, not deployment permission. No local full-suite rerun.

Limits: Story remains IN_PROGRESS; no DONE claim. TS24 is required after PO approval. Overall Jenkins backend failure is distinct from Factory Validation stage success under ADR-0001 D6. US-FACTORY-002 was not modified. Human approval and merge commit are required.

Review: docs/factory/US-FACTORY-003-round4-review.md. Design: ADR-0001 and its recovery addendum. Recovery/status: docs/factory/CURRENT-STATE.md.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
