"""Central fail-closed Factory policy interpreter. Git objects are authoritative."""
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

import yaml

from policy import contract_change_reason, latest_non_comment_reviews

PROVENANCE_POLICY = 'merge-commit-only policy requires preserved implementation/evidence ancestry; no squash/rebase or shallow history'
# Well-formed non-PASS results accepted as non-authorising history (AC07 vocabulary).
HISTORY_NONPASS = ('FAIL', 'NOT_EXECUTED', 'UNKNOWN', 'PENDING_PO', 'PARTIAL', 'PASS WITH BLOCKERS')
COMPLETION = 'INVALID DONE completion snapshot'
# The single independent Validation gate (ADR-0001 D4): independent identity, per-AC results, zero Critical/Major.
INDEPENDENT_GATES = ('Validation',)


class Block(Exception):
    pass


def require(condition, reason):
    if not condition:
        raise Block(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def parse(data):
    value = yaml.safe_load(data)
    require(isinstance(value, dict), 'INVALID mapping required')
    if isinstance(value.get("timestamp"), datetime.datetime):
        value["timestamp"] = value["timestamp"].isoformat().replace("+00:00", "Z")
    return value


class Factory:
    def __init__(self, root, revision='HEAD', github=None, archive=None, verify_review=True):
        self.root = Path(root).resolve()
        self.revision = self.git('rev-parse', '--verify', revision + '^{commit}').decode().strip()
        self.github = github
        self.archive = archive
        self.verify_review = verify_review
        self._gate_cache = {}
        self._prior_cache = {}
        self._provenance_cache = {}
        self._history_cache = {}
        self.workflow = parse(self.blob('factory/workflow.yaml'))
        self.schema()

    def git(self, *args):
        p = subprocess.run(['git', '-c', f'safe.directory={self.root}', '-C', str(self.root), *args], capture_output=True)
        require(p.returncode == 0, 'INVALID Git object unavailable')
        return p.stdout

    def schema(self):
        w = self.workflow
        require(w.get('version') == 1, 'INVALID workflow version')
        for key in ('states', 'non_implementation', 'material_keys', 'external_systems', 'implementing_roles', 'unit_scenarios'):
            require(isinstance(w.get(key), list) and w[key] and len(set(w[key])) == len(w[key]), f'INVALID workflow {key}')
        for key in ('gates', 'transitions', 'failure_paths', 'dispatch', 'commands'):
            require(isinstance(w.get(key), dict) and w[key], f'INVALID workflow {key}')
        require(isinstance(w.get('story_implementers'), dict), 'INVALID story implementing roles')
        review = w.get('github_review')
        if review is not None:
            require(isinstance(review, dict) and re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', review.get('repository', '')), 'INVALID review repository')
            require(isinstance(review.get('approved_reviewers'), list) and review['approved_reviewers'] and all(isinstance(x, str) and x for x in review['approved_reviewers']), 'INVALID approved reviewers')
        for roles in w['story_implementers'].values():
            require(isinstance(roles, list) and roles and all(r in w['implementing_roles'] for r in roles), 'INVALID implementing role mapping')
        names = set(w['gates']) | {'DoR', 'DoD', 'dependencies', 'blockers'}
        for rule in w['failure_paths'].values():
            require(isinstance(rule, dict) and all(isinstance(rule.get(k), list) and rule[k] and all(x in w['states'] for x in rule[k]) for k in ('from', 'to')), 'INVALID failure path')
        for commands in w['commands'].values():
            if isinstance(commands, dict):
                require(all(k in w['gates'] and isinstance(v, str) and v.strip() for k, v in commands.items()), 'INVALID command map')
                required_commands = {name for name, gate in w['gates'].items() if 'IMPLEMENTER' in gate.get('producers', [])}
                require(required_commands <= commands.keys(), 'INVALID incomplete implementing gate command map')
            else:
                require(isinstance(commands, str) and commands.strip(), 'INVALID command')
        for name, gate in w['gates'].items():
            require(isinstance(gate, dict), f'INVALID gate {name}')
            require(isinstance(gate.get('producers'), list) and gate['producers'], f'INVALID producers {name}')
            for field in ('implementation', 'contract', 'na'):
                require(type(gate.get(field)) is bool, f'INVALID {name} {field}')
            require(isinstance(gate.get('prerequisites'), list) and all(x in w['gates'] and x != name for x in gate['prerequisites']), f'INVALID prerequisites {name}')
        for edge, gates in w['transitions'].items():
            require(len(edge.split('->')) == 2 and all(x in w['states'] for x in edge.split('->')), 'INVALID transition')
            require(isinstance(gates, list) and all(x in names for x in gates), 'INVALID transition prerequisites')
        for rule in w['dispatch'].values():
            require(rule.get('state') in w['states'] and isinstance(rule.get('prerequisites'), list) and all(x in names for x in rule['prerequisites']), 'INVALID dispatch')
        def visit(name, stack):
            require(name not in stack, 'INVALID cyclic gates')
            for parent in w['gates'][name]['prerequisites']:
                visit(parent, stack + [name])
        for name in w['gates']:
            visit(name, [])

    def blob(self, path, revision=None):
        self.path(path)
        entry = self.git("ls-tree", revision or self.revision, "--", path).split(b"\t", 1)
        require(len(entry) == 2 and (entry[0].startswith(b"100644 ") or entry[0].startswith(b"100755 ")), "INVALID tracked regular blob required")
        return self.git('show', f'{revision or self.revision}:{path}')

    def path(self, path):
        require(isinstance(path, str) and path and not PurePosixPath(path).is_absolute() and '..' not in PurePosixPath(path).parts, 'non-durable artifact path')
        require(not (self.root / path).is_symlink(), 'non-durable symlink')
        require((self.root / path).resolve() == self.root / path, "non-durable symlink parent")
        return self.root / path

    def story(self, story, revision=None):
        require(re.fullmatch(r'US-(?:FACTORY-)?[0-9]+', story) is not None, 'unknown Story')
        s = parse(self.blob(f'safe/stories/{story}.yaml', revision))
        require(s.get('id') == story and s.get('status') in self.workflow['states'], 'INVALID Story')
        return s

    def implementation(self, revision=None):
        entries = []
        for item in self.git('ls-tree', '-rz', revision or self.revision).split(b'\0'):
            if not item:
                continue
            meta, path = item.split(b'\t', 1)
            p = path.decode()
            if not any(p.startswith(c) if c.endswith('/') else p == c for c in self.workflow['non_implementation']):
                entries.append([p, meta.decode()])
        return digest(canonical(sorted(entries)))

    def contract(self, story, revision=None):
        s = self.story(story, revision)
        material = {k: s.get(k) for k in self.workflow['material_keys']}
        refs = s.get('contract_refs', [])
        require(isinstance(refs, list), 'INVALID contract_refs')
        material['contract_refs'] = {p: self.git('rev-parse', f'{revision or self.revision}:{p}').decode().strip() for p in sorted(refs)}
        return digest(canonical(material))

    def dor(self, s, check_status=True):
        require(isinstance(s, dict) and isinstance(s.get("definition_of_ready"), dict), "DoR mapping required")
        template = parse(self.blob('safe/templates/definition-of-ready.yaml'))['definition_of_ready']
        require(isinstance(template, dict) and template, 'INVALID empty DoR template')
        errors = [f'DoR {k} must be boolean true' for k in template if s.get('definition_of_ready', {}).get(k) is not True]
        errors.extend(f"DoR missing required section {key}" for key in ("id", "title", "status", "acceptance_criteria", "test_scenarios", "definition_of_ready") if key not in s)
        if not isinstance(s.get("id"), str) or re.fullmatch(r"US-(?:FACTORY-)?[0-9]+", s["id"]) is None:
            errors.append("DoR unknown Story id")
        if check_status and s.get('status') not in ('REFINED', 'READY'):
            errors.append('DoR status must be REFINED or READY')
        ac = s.get('acceptance_criteria')
        if not isinstance(ac, list) or not ac or any(not isinstance(a, dict) or not str(a.get('description', '')).strip() for a in ac):
            errors.append('DoR acceptance_criteria empty description')
        if not s.get('test_scenarios'):
            errors.append('DoR test_scenarios empty')
        if s.get('open_questions', []):
            errors.append('DoR open_questions non-empty')
        return errors

    def introduced(self, path):
        """Trace immutable blobs across every parent, including true merges."""
        revision = self.git('rev-parse', self.revision).decode().strip()
        key = (revision, path)
        if key in self._provenance_cache:
            return self._provenance_cache[key]
        policy = PROVENANCE_POLICY
        require(self.git('rev-parse', '--is-shallow-repository').strip() == b'false', f'INVALID {policy}')
        if revision not in self._history_cache:
            graph = {}
            trees = {}
            for line in self.git('rev-list', '--parents', revision).decode().splitlines():
                commit, *parents = line.split()
                graph[commit] = parents
                trees[commit] = {}
                for entry in self.git('ls-tree', '-rz', commit, '--', 'factory/evidence/').split(b'\0'):
                    if entry:
                        meta, name = entry.split(b'\t', 1)
                        trees[commit][name.decode()] = meta
            self._history_cache[revision] = graph, trees
        graph, trees = self._history_cache[revision]
        expected = trees[revision].get(path)
        require(expected is not None, 'INVALID missing evidence blob')
        additions = []
        for commit, parents in graph.items():
            present = trees[commit].get(path)
            inherited = [trees[parent].get(path) for parent in parents]
            require(present in (None, expected), 'INVALID evidence history rewritten; append a new record')
            require(present is not None or not any(inherited), 'INVALID evidence history rewritten; record deleted')
            if present is not None and not any(inherited):
                require(len(parents) <= 1, f'INVALID ambiguous merge introduction; {policy}')
                additions.append(commit)
        require(len(additions) == 1, f'INVALID ambiguous evidence introduction; {policy}')
        introduction = additions[0]
        self._provenance_cache[key] = introduction
        return introduction

    def ancestor(self, earlier, later, strict=False):
        if strict and earlier == later:
            return False
        result = subprocess.run(['git', '-C', str(self.root), 'merge-base', '--is-ancestor', earlier, later], capture_output=True)
        require(result.returncode in (0, 1), f'INVALID ancestry unavailable; {PROVENANCE_POLICY}')
        return result.returncode == 0

    def records(self, story):
        prefix = f'factory/evidence/{story}/'
        records = []
        for raw in self.git('ls-tree', '-rz', self.revision, '--', prefix).split(b'\0'):
            if not raw:
                continue
            meta, path = raw.split(b'\t', 1)
            p = path.decode()
            require(meta.startswith(b'100644 ') or meta.startswith(b'100755 '), 'INVALID evidence file mode')
            require(Path(p).suffix in ('.yaml', '.yml', '.json', '.md'), 'INVALID evidence file type')
            if Path(p).suffix != '.md':
                record = parse(self.blob(p))
                if 'gate' in record or 'action' not in record:
                    # Reserved provenance is derived, never supplied by a producer.
                    record['_path'] = p
                    record['_introduced'] = self.introduced(p)
                    records.append(record)
        return records

    def external(self, artifact):
        require(artifact.get('system') in self.workflow['external_systems'], 'external reference unknown system')
        for field in ('system', 'job', 'build', 'path', 'sha256'):
            require(artifact.get(field) not in (None, ''), f'external reference incomplete {field}')
        self.path(artifact['path'])
        require(re.fullmatch('[a-f0-9]{64}', artifact['sha256']) is not None, 'external hash invalid')
        require(not any(x in canonical(artifact).decode().lower() for x in ('://', 'token', 'password', 'credential', '@')), 'external reference credential or URL')
        if self.archive is not None:
            require(digest(self.archive(artifact)) == artifact['sha256'], 'external archive hash mismatch')

    def artifact(self, a):
        require(isinstance(a, dict), 'INVALID artifact')
        if 'system' in a:
            self.external(a)
        else:
            p = a.get('path')
            self.path(p)
            ignored = subprocess.run(["git", "-C", str(self.root), "check-ignore", "--no-index", "--quiet", "--", p], capture_output=True)
            require(ignored.returncode == 1, "non-durable gitignored artifact")
            require(not p.startswith('factory/logs/'), 'non-durable ignored artifact')
            require(digest(self.blob(p)) == a.get('sha256'), 'non-durable artifact hash mismatch')

    def implementing_roles(self, story):
        return self.workflow["story_implementers"].get(story, self.workflow["implementing_roles"])

    def command(self, story, gate):
        commands = self.workflow['commands'].get(story, {})
        require(isinstance(commands, dict) and isinstance(commands.get(gate), str) and commands[gate].strip(), f'NOT_EXECUTED gate command missing for {story}/{gate}')
        return commands[gate]

    def identity(self, story, revision=None):
        state = parse(self.blob(f'factory/state/{story}.json', revision))
        require(state.get('implementing_identity') and state.get('implementing_role') in self.implementing_roles(story), 'implementing identity missing')
        return state

    def review(self, story, record):
        require(self.github is not None, 'NOT_EXECUTED GitHub review not verified')
        policy = self.workflow.get('github_review')
        require(policy is not None, 'NOT_EXECUTED review authority policy unavailable at revision')
        require(record.get('repository', '').casefold() == policy['repository'].casefold(), 'review wrong repository')
        pr, commits, reviews = self.github(record)
        require(pr['base']['repo']['full_name'].casefold() == policy['repository'].casefold(), 'review wrong base repository')
        implementing_role = self.identity(story)['implementing_role']
        require(pr['head']['ref'] == f'feature/{story}-' + implementing_role.removeprefix('CODEX_').lower(), 'review wrong PR head branch')
        require(pr.get('commits') == len(commits), 'review incomplete commit list')
        require(all((c.get('author') or {}).get('login') and (c.get('committer') or {}).get('login') for c in commits), 'review unresolved commit login')
        reviews = sorted((r for r in reviews if r.get('state') != 'PENDING'), key=lambda r: (r['submitted_at'], r['id']))
        non_comment = latest_non_comment_reviews(reviews)
        require(not any(r['state'] == 'CHANGES_REQUESTED' for r in non_comment.values()), 'review CHANGES_REQUESTED')
        r = next((r for r in non_comment.values() if r['id'] == record.get('review_id') and r['state'] == 'APPROVED'), None)
        require(r is not None, 'review not verified APPROVED')
        forbidden = {pr['user']['login'], self.identity(story)['implementing_identity']}
        forbidden.update(c[k]['login'] for c in commits for k in ('author', 'committer'))
        login = r['user']['login'].casefold()
        require(login not in {x.casefold() for x in forbidden}, 'review self-approval')
        require(login in {x.casefold() for x in policy['approved_reviewers']}, 'review unapproved reviewer')
        require(r.get('author_association') in ('OWNER', 'MEMBER', 'COLLABORATOR'), 'review association lacks write authority')
        require(record['producer_identity'].casefold() == login, 'review identity mismatch')
        require(record.get('review_submitted_at') == r['submitted_at'], 'review server submission mismatch')
        submitted = datetime.datetime.fromisoformat(r['submitted_at'].replace('Z', '+00:00'))
        claimed = datetime.datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
        require(submitted.tzinfo is not None and claimed >= submitted, 'review record predates server submission')
        # The server-reviewed snapshot must already contain valid Unit evidence.
        snapshot = Factory(self.root, r['commit_id'], github=self.github)
        require(not snapshot.preconditions(story, self.workflow['gates']['Code Review']['prerequisites']), 'review out-of-order reviewed snapshot')
        require(self.implementation(r['commit_id']) == self.implementation(), 'STALE_IMPLEMENTATION reviewed commit')

    def record(self, story, gate, r, allow_nonpass=False, history=False):
        config = self.workflow['gates'][gate]
        for field in ('story_id', 'gate', 'result', 'producer_role', 'producer_identity', 'timestamp', 'source_commit', 'implementation_fingerprint', 'artifacts'):
            require(r.get(field) not in (None, '', []), f'INVALID {gate} field {field}')
        require(re.fullmatch('[a-f0-9]{40}', r['source_commit']) is not None, 'INVALID source commit')
        try:
            self.git('cat-file', '-e', r['source_commit'] + '^{commit}')
        except Block:
            raise Block(f'INVALID source commit unavailable; {PROVENANCE_POLICY}') from None
        if '_introduced' in r:
            require(self.ancestor(r['source_commit'], r['_introduced'], strict=True), f'INVALID execution snapshot provenance; {PROVENANCE_POLICY}')
        require(r['story_id'] == story and r['gate'] == gate, 'INVALID Story/gate record')
        require(isinstance(r["timestamp"], str) and "T" in r["timestamp"], "INVALID UTC timestamp")
        timestamp = datetime.datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00"))
        require(timestamp.tzinfo is not None and timestamp.utcoffset() == datetime.timedelta(0), "INVALID UTC timestamp")
        producer_state = self.identity(story, r['source_commit'] if history else None) if 'IMPLEMENTER' in config['producers'] else None
        roles = [producer_state['implementing_role'] if x == 'IMPLEMENTER' else x for x in config['producers']]
        require(r['producer_role'] in roles, 'wrong producer')
        if 'IMPLEMENTER' in config['producers']:
            require(r['producer_identity'] == producer_state['implementing_identity'], 'wrong producer identity')
        if gate in INDEPENDENT_GATES:
            require(r['producer_identity'].casefold() != self.identity(story, r['source_commit'] if history else None)['implementing_identity'].casefold(), 'wrong producer independent identity')
        require(r['implementation_fingerprint'] == self.implementation(r['source_commit']), 'INVALID source fingerprint')
        if config['implementation'] and not history:
            require(r['implementation_fingerprint'] == self.implementation(), 'STALE_IMPLEMENTATION')
        if config['contract']:
            require(r.get('acceptance_contract_fingerprint') == self.contract(story, r['source_commit']), 'INVALID contract field')
            if not history and r["acceptance_contract_fingerprint"] != self.contract(story):
                reason = contract_change_reason(r["acceptance_contract_fingerprint"], self.contract(story))
                require(reason is None, reason)
        if 'IMPLEMENTER' in config['producers']:
            require(r.get('command') == self.command(story, gate), 'INVALID gate command')
        artifact_factory = Factory(self.root, r['source_commit'], github=self.github, archive=self.archive) if history else self
        for a in r['artifacts']:
            artifact_factory.artifact(a)
        nonpass_results = ('FAIL', 'NOT_EXECUTED', 'UNKNOWN', 'PENDING_PO') if allow_nonpass is True else (allow_nonpass or ())
        if r['result'] in nonpass_results:
            require(isinstance(r.get("checks"), dict) and r["checks"], "INVALID structured checks")
            return r["result"]
        if r['result'] == 'N/A':
            s = self.story(story)
            require(config['na'] and gate in s.get('na_permitted', []) and story != 'US-FACTORY-003', 'N/A not permitted')
            require(r.get('po_approval', {}).get('identity') and r['po_approval'].get('date') and r.get('reason') and r.get('decision_reference'), 'N/A approval incomplete')
            require(r.get('execution_status') == 'NOT_APPLICABLE', 'N/A failed or missing execution')
            artifact_factory.artifact(r['decision_reference'])
            return 'N/A-APPROVED'
        require(r['result'] == 'PASS', f'{r["result"]} result not PASS')
        require(isinstance(r.get('checks'), dict) and r['checks'] and all(x == 'PASS' for x in r['checks'].values()), 'INVALID structured checks')
        if gate in INDEPENDENT_GATES:
            expected = {a['id'] for a in self.story(story, r['source_commit'] if history else None)['acceptance_criteria']}
            require(set(r.get('ac_results', {})) == expected and all(x == 'PASS' for x in r['ac_results'].values()), 'INVALID per-AC results')
            findings = r.get('findings')
            require(isinstance(findings, dict) and all(type(findings.get(k)) is int and findings[k] == 0 for k in ('critical', 'major')), 'INVALID Validation verdict: Critical and Major findings must be 0')
        if gate == 'Unit Test':
            expected = {t['id'] for t in self.story(story, r['source_commit'] if history else None)['test_scenarios']} - {'TS24', 'TS25'}
            require(set(r.get('ts_results', {})) == expected and all(x == 'PASS' for x in r['ts_results'].values()), 'INVALID per-TS results')
        if gate == 'Code Review' and not history and self.verify_review:
            self.review(story, r)
        if gate == 'Jenkins':
            require(r['checks'].get('Factory Validation') == 'PASS', 'Jenkins Factory Validation missing')
        return 'PASS'

    def prior_record_valid(self, story, gate, record, history=False):
        key = (gate, repr(record), history)
        if key in self._prior_cache:
            return self._prior_cache[key]
        result = self._prior_record_valid(story, gate, record, history)
        self._prior_cache[key] = result
        return result

    def _prior_record_valid(self, story, gate, record, history=False):
        try:
            require(self.ancestor(record['source_commit'], record['_introduced'], strict=True), f'INVALID execution snapshot provenance; {PROVENANCE_POLICY}')
            self.record(story, gate, record, history=history)
            for parent in self.workflow["gates"][gate]["prerequisites"]:
                earlier = [r for r in self.records(story) if r.get("gate") == parent and self.precedes(r, record)]
                if history:
                    # Historical PASS must have had fresh prerequisites at its
                    # declared execution snapshot, rather than at today's tip.
                    config = self.workflow['gates'][parent]
                    earlier = [r for r in earlier if
                               (not config['implementation'] or r['implementation_fingerprint'] == self.implementation(record['source_commit'])) and
                               (not config['contract'] or r.get('acceptance_contract_fingerprint') == self.contract(story, record['source_commit']))]
                if not any(self.prior_record_valid(story, parent, r, history=history) for r in earlier):
                    return False
            return True
        except (Block, ValueError, KeyError, TypeError):
            return False

    def precedes(self, prerequisite, dependent):
        """Prerequisite was committed before the dependent's execution snapshot."""
        return self.ancestor(prerequisite['_introduced'], dependent['source_commit']) and self.ancestor(dependent['source_commit'], dependent['_introduced'], strict=True)

    def latest_record(self, records):
        require(records, 'missing evidence')
        newest = [r for r in records if all(x is r or self.ancestor(x['_introduced'], r['_introduced'], strict=True) for x in records)]
        require(len(newest) == 1, 'INVALID ambiguous latest evidence')
        return newest[0]

    def rerun_order(self, story):
        order = []
        def visit(gate):
            if gate in order:
                return
            for parent in self.workflow['gates'][gate]['prerequisites']:
                visit(parent)
            order.append(gate)
        for gate in self.workflow['gates']:
            visit(gate)
        return [g for g in order if self.gate(story, g)[0] not in ('PASS', 'N/A-APPROVED')]

    def gate(self, story, gate, stack=()):
        if not stack:
            self._gate_cache.clear()
            self._prior_cache.clear()
        key = (self.git("rev-parse", self.revision), story, gate)
        if key in self._gate_cache:
            return self._gate_cache[key]
        result = self._gate(story, gate, stack)
        self._gate_cache[key] = result
        return result

    def _gate(self, story, gate, stack=()):
        self.story(story)
        require(gate in self.workflow['gates'], 'unknown gate')
        errors = []
        for parent in self.workflow['gates'][gate]['prerequisites']:
            state, reasons = self.gate(story, parent, stack + (gate,))
            if state not in ('PASS', 'N/A-APPROVED'):
                errors.extend([f'{parent}: {state} {x}' for x in reasons])
        candidates = [r for r in self.records(story) if r.get('gate') == gate]
        if not candidates:
            return 'MISSING', errors + ['missing evidence']
        try:
            r = self.latest_record(candidates)
            require(self.ancestor(r['source_commit'], r['_introduced'], strict=True), f'INVALID execution snapshot provenance; {PROVENANCE_POLICY}')
            state = self.record(story, gate, r)
            for parent in self.workflow['gates'][gate]['prerequisites']:
                prior = [x for x in self.records(story) if x.get('gate') == parent]
                require(any(self.precedes(x, r) and self.prior_record_valid(story, parent, x) for x in prior), "out-of-order record")
            if errors:
                return 'INVALID', errors
            return state, []
        except (Block, ValueError, KeyError, TypeError) as e:
            reason = str(e)
            state = next((x for x in ('STALE_IMPLEMENTATION', 'STALE_CONTRACT', 'NOT_EXECUTED') if x in reason), 'INVALID')
            return state, errors + [reason]

    def preconditions(self, story, names):
        errors = []
        for name in names:
            try:
                errors.extend(self._preconditions(story, [name]))
            except (Block, OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as e:
                errors.append(f"{name}: {e}")
        return errors

    def _preconditions(self, story, names):
        s = self.story(story)
        errors = []
        for name in names:
            if name == 'DoR':
                errors.extend(self.dor(s))
            elif name == 'dependencies':
                for dep in s.get('depends_on', []):
                    if self.story(dep)['status'] != 'DONE':
                        errors.append(f'dependency {dep} not DONE')
            elif name == 'blockers':
                raid = parse(self.blob('safe/raid.yaml'))
                if s.get('blocked_by'):
                    errors.append('open blocker blocked_by')
                for section in raid.values():
                    if isinstance(section, list):
                        errors.extend(f'open blocker {r.get("id")}' for r in section if isinstance(r, dict) and r.get('status') == 'OPEN' and story in r.get('blocks', []))
            elif name == 'DoD':
                dod = s.get('definition_of_done', {})
                keys = parse(self.blob('safe/templates/definition-of-done.yaml'))['definition_of_done']
                require(isinstance(keys, dict) and keys, 'INVALID empty DoD template')
                refs = dod.get('evidence', {})
                errors.extend(f'DoD {k} missing true/evidence' for k in keys if dod.get(k) is not True or not isinstance(refs, dict) or not refs.get(k))
                if isinstance(refs, dict):
                    for artifact in refs.values():
                        self.artifact(artifact)
            else:
                state, reasons = self.gate(story, name)
                if state not in ('PASS', 'N/A-APPROVED'):
                    errors.extend(f'{name}: {state} {r}' for r in reasons)
        return errors

    def transition(self, story, source, target, reason=None):
        s = self.story(story)
        require(s['status'] == source and source != 'DONE', 'INVALID source state')
        if target == 'BLOCKED':
            require(source in self.pre_done() and s.get('blocked_from') == source and s.get('blocked_by'), 'BLOCKED requires blocked_from and blocked_by')
            return []
        if source == 'BLOCKED':
            require(s.get('blocked_from') in self.pre_done(), 'INVALID blocked_from must be a state before DONE')
            require(target == s.get('blocked_from'), 'BLOCKED returns only blocked_from')
            return []
        edge = f'{source}->{target}'
        if edge in self.workflow['transitions']:
            return self.preconditions(story, self.workflow['transitions'][edge])
        for name, rule in self.workflow['failure_paths'].items():
            if reason and reason.startswith(name + ':') and source in rule['from'] and target in rule['to']:
                return []
        raise Block('INVALID transition or failure reason')

    def dispatch(self, story, role):
        s = self.story(story)
        require(role != 'IMPLEMENTER', 'unknown role: IMPLEMENTER is a policy marker, not an agent role')
        key = 'IMPLEMENTER' if role in self.workflow['implementing_roles'] else role
        require(key != "IMPLEMENTER" or role in self.implementing_roles(story), "wrong implementing role")
        require(key in self.workflow['dispatch'], 'unknown role')
        rule = self.workflow['dispatch'][key]
        require(s['status'] == rule['state'], 'INVALID dispatch state')
        return self.preconditions(story, rule['prerequisites'])

    def pre_done(self):
        return [x for x in self.workflow['states'] if x not in ('DONE', 'BLOCKED')]

    def status_at(self, story, commit):
        """Story status at a commit; None when the Story file is absent."""
        path = f'safe/stories/{story}.yaml'
        entry = self.git('ls-tree', commit, '--', path)
        if not entry.strip():
            return None
        oid = entry.split()[2].decode()
        cache = self.__dict__.setdefault('_status_cache', {})
        if oid not in cache:
            cache[oid] = self.story(story, commit)['status']
        return cache[oid]

    def completion_snapshot(self, story):
        """Unique commit that introduced DONE; fail closed on none/many/merge/removal."""
        require(self.git('rev-parse', '--is-shallow-repository').strip() == b'false', f'{COMPLETION}: {PROVENANCE_POLICY}')
        require(self.story(story)['status'] == 'DONE', f'{COMPLETION}: Story not DONE at evaluated revision')
        graph = {}
        for line in self.git('rev-list', '--parents', self.revision).decode().splitlines():
            commit, *parents = line.split()
            graph[commit] = parents
        done = {c: self.status_at(story, c) == 'DONE' for c in graph}
        introductions = []
        for commit, parents in graph.items():
            require(done[commit] or not any(done[p] for p in parents), f'{COMPLETION}: DONE removed in history at {commit[:12]} (AC04)')
            if done[commit] and not any(done[p] for p in parents):
                introductions.append(commit)
        require(introductions, f'{COMPLETION}: none')
        require(len(introductions) == 1, f'{COMPLETION}: ambiguous ({len(introductions)} introductions); {PROVENANCE_POLICY}')
        commit = introductions[0]
        require(len(graph[commit]) == 1, f'{COMPLETION}: merge or root introduction; {PROVENANCE_POLICY}')
        require(self.status_at(story, graph[commit][0]) == 'QA', f'{COMPLETION}: not entered from QA (AC04)')
        require(self.ancestor(commit, self.revision), f'{COMPLETION}: not an ancestor; {PROVENANCE_POLICY}')
        return commit

    def completion_errors(self, story):
        """AC06 as evaluated at the completion snapshot (ADR-0001 D1)."""
        try:
            commit = self.completion_snapshot(story)
            snapshot = Factory(self.root, commit, github=self.github, archive=self.archive, verify_review=self.verify_review)
            return [f'DONE completion snapshot {commit[:12]}: {e}' for e in snapshot.preconditions(story, snapshot.workflow['transitions']['QA->DONE'])]
        except (Block, ValueError, KeyError, TypeError, IndexError) as e:
            return [str(e)]

    def history_errors(self, story, notices):
        """Integrity of every record at the evaluated revision; history never authorises."""
        errors = []
        records = self.records(story)
        for record in records:
            if 'gate' not in record:
                continue
            try:
                require(record['gate'] in self.workflow['gates'], 'unknown gate')
                state = self.record(story, record['gate'], record, allow_nonpass=HISTORY_NONPASS, history=True)
                if state in ('PASS', 'N/A-APPROVED') and not self.prior_record_valid(story, record['gate'], record, history=True):
                    notices.append(f"HISTORY {record['gate']}: out-of-order record {record['_path']} kept, non-authorising (AC16)")
            except (Block, ValueError, KeyError, TypeError) as e:
                errors.append(str(e))
        for gate in sorted({r['gate'] for r in records if 'gate' in r}):
            try:
                self.latest_record([r for r in records if r.get('gate') == gate])
            except Block as e:
                errors.append(str(e))
        return errors

    def arrived(self, story):
        """True when the completion snapshot is not reachable from the first parent (newly integrated here)."""
        commit = self.completion_snapshot(story)
        parents = self.git('rev-list', '--parents', '-n', '1', self.revision).decode().split()[1:]
        return not parents or not self.ancestor(commit, parents[0])
