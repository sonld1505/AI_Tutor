# Repository settings and identity separation (gap A1 / G-14, RAID R-003)

| Field | Value |
|---|---|
| Purpose | Make the PO merge/release gate a technical control, not a convention |
| Prepared by | Claude orchestrator (SM), 2026-10-04 |
| Executed by | **Human PO only.** These are GitHub admin operations and credential changes. The Factory does not run them and has no credential that could |
| Status | PREPARED, NOT APPLIED |

## 1. Current state (checked 2026-10-04)

| Check | Result | How |
|---|---|---|
| `develop` protected | **No** | `curl -s https://api.github.com/repos/sonld1505/AI_Tutor/branches/develop` → `"protected": false` |
| `main` protected | **No** | same for `main` |
| Merge methods (squash/rebase allowed?) | UNVERIFIED (needs auth) | unauthenticated API returns `null` |
| Host default SSH key | Authenticates as the **PO login** `sonld1505`. **No passphrase** | `ssh -T -o BatchMode=yes git@github.com` → `Hi sonld1505!`; `ssh-keygen -y -P "" -f ~/.ssh/id_ed25519` succeeds |
| Implementation identity | `AI Tutor Agent` / `sonldfkr2911`, separate key, `IdentitiesOnly=yes`, set per worktree (D-006) | `config.worktree` of `US-FACTORY-003-devops` |
| Management commits by Claude | Made with the PO key (for example `dbe7278..b779eef`) | `config.worktree` of `US-FACTORY-003-MGMT`: `user.name sonld1505`, no `core.sshCommand` |
| `gh` on host | Not logged in | `gh auth status` |

**Risk.** Any process on this host can push to or merge into `develop`/`main` as the PO. Nothing on GitHub requires a
review or a status check.

## 2. Order of operations (Lean mode, 2026-10-04)

GitHub never lets a PR's author approve their own PR. **All Factory commits and PRs (implementation and management)
use the existing bot identity `sonldfkr2911` (AI Tutor Agent)**, and the PO approves them. No new account is needed. The
orchestrator configures the management worktrees with the bot identity (worktree-scoped config, same as D-006) before
the PO applies protection.

1. Step A: management worktrees use the bot identity (orchestrator, no PO action).
2. Step B: take the PO key out of unattended use on the host (§4).
3. Step C: repository merge settings (§5).
4. Step D: branch protection on `develop` and `main` (§6).
5. Step E: required status check after the Jenkins job exists (D-001) (§7).
6. Step F: verify (§8).

## 3. Step A: bot identity for management worktrees (orchestrator)

```bash
for W in /home/ubuntu/AI_Tutor-worktrees/US-FACTORY-003-MGMT /home/ubuntu/AI_Tutor-worktrees/US-FACTORY-004-MGMT; do
  git -C "$W" config --worktree user.name  "AI Tutor Agent"
  git -C "$W" config --worktree user.email "337536168+sonldfkr2911@users.noreply.github.com"
  git -C "$W" config --worktree core.sshCommand "ssh -i /home/ubuntu/.ssh/id_ed25519_ai_tutor_agent -o IdentitiesOnly=yes"
done
```

The bot is never on the approver list. The PO (`sonld1505`) is the only approver.

## 4. Step B: take the PO key out of unattended use (PO)

Pick one option. Option 1 is the strongest.

- **Option 1: remove it from the host.** Copy `~/.ssh/id_ed25519` to your own machine if you need it, then on the
  host run `shred -u ~/.ssh/id_ed25519 ~/.ssh/id_ed25519.pub`. Use SSH agent forwarding (`ssh -A`) when you personally
  need to push as `sonld1505` from the host.
- **Option 2: protect it with a passphrase you don't store on the host:** `ssh-keygen -p -f ~/.ssh/id_ed25519`.
  Unattended processes can't use it any more.

Verify (expect a failure for unattended use):
```bash
ssh -T -o BatchMode=yes -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 git@github.com   # expect: Permission denied / passphrase required
```

## 5. Step C: merge methods (PO, from a machine logged in as `sonld1505`)

```bash
gh api -X PATCH repos/sonld1505/AI_Tutor \
  -F allow_merge_commit=true -F allow_squash_merge=false -F allow_rebase_merge=false \
  -F allow_auto_merge=false -F delete_branch_on_merge=false
```

## 6. Step D: branch protection on `develop` and `main` (PO)

`required_linear_history` must stay **false** (merge commits are required). Admins are included (`enforce_admins: true`),
so the PO can't bypass it by accident either.

```bash
for B in develop main; do
gh api -X PUT repos/sonld1505/AI_Tutor/branches/$B/protection --input - <<'JSON'
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1,
    "require_last_push_approval": true
  },
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true,
  "lock_branch": false,
  "allow_fork_syncing": false
}
JSON
done
```

Notes:
- `restrictions` (who may push) is only available for organisation repositories. On a personal repository, the
  required review plus `enforce_admins` is what stops direct pushes.
- With these settings, every merge needs a PR approved by someone other than its author and last pusher. Implementation
  PRs and management PRs are all authored by the bot `sonldfkr2911` and approved by `sonld1505`.

## 7. Step E: required status checks (after D-001)

When the Jenkins multibranch job reports to GitHub, add its context (the exact name is known only after the first build):

```bash
for B in develop main; do
gh api -X PATCH repos/sonld1505/AI_Tutor/branches/$B/protection/required_status_checks \
  --input - <<'JSON'
{ "strict": false, "contexts": ["<jenkins-context-name>"] }
JSON
done
```

`strict: true` (branch must be up to date before merging) is a technical choice that depends on the R3-02 decision for
US-FACTORY-003. Leave it false unless the SA decides otherwise.

## 8. Step F: verification (PO or Factory, read-only)

```bash
gh api repos/sonld1505/AI_Tutor --jq '{allow_merge_commit,allow_squash_merge,allow_rebase_merge}'
# expect {"allow_merge_commit":true,"allow_squash_merge":false,"allow_rebase_merge":false}
for B in develop main; do gh api repos/sonld1505/AI_Tutor/branches/$B/protection \
  --jq '{admins:.enforce_admins.enabled, reviews:.required_pull_request_reviews.required_approving_review_count, linear:.required_linear_history.enabled, force:.allow_force_pushes.enabled}'; done
# expect admins true, reviews 1, linear false, force false
curl -s https://api.github.com/repos/sonld1505/AI_Tutor/branches/develop | grep '"protected"'   # expect true
ssh -T -o BatchMode=yes git@github.com      # from the host as ubuntu: must NOT print "Hi sonld1505!"
```

Record the results (commands plus output, no tokens) in CHANGELOG, and close R-003 only after all checks pass.

## 9. Interim rule until applied

- Factory agents never push to `develop`/`main` and never merge PRs (convention, already in AGENTS.md).
- Management pushes with the PO key happen only on an explicit PO instruction for that push.
