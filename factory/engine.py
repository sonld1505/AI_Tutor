"""Central fail-closed Factory policy interpreter. Git objects are authoritative."""
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path, PurePosixPath

import yaml

from policy import contract_change_reason, latest_non_comment_reviews


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


def timestamp_key(record):
    try:
        value = datetime.datetime.fromisoformat(str(record.get("timestamp", "")).replace("Z", "+00:00"))
        return value if value.tzinfo is not None else datetime.datetime.max.replace(tzinfo=datetime.UTC)
    except (ValueError, TypeError):
        return datetime.datetime.max.replace(tzinfo=datetime.UTC)


class Factory:
    def __init__(self, root, revision='HEAD', workflow=None, github=None, archive=None):
        self.root = Path(root).resolve()
        self.revision = revision
        self.github = github
        self.archive = archive
        self._gate_cache = {}
        self._prior_cache = {}
        self.workflow = parse((Path(workflow) if workflow else self.root / 'factory/workflow.yaml').read_text())
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

    def dor(self, s):
        require(isinstance(s, dict) and isinstance(s.get("definition_of_ready"), dict), "DoR mapping required")
        template = parse(self.blob('safe/templates/definition-of-ready.yaml'))['definition_of_ready']
        errors = [f'DoR {k} must be boolean true' for k in template if s.get('definition_of_ready', {}).get(k) is not True]
        errors.extend(f"DoR missing required section {key}" for key in ("id", "title", "status", "acceptance_criteria", "test_scenarios", "definition_of_ready") if key not in s)
        if not isinstance(s.get("id"), str) or re.fullmatch(r"US-(?:FACTORY-)?[0-9]+", s["id"]) is None:
            errors.append("DoR unknown Story id")
        if s.get('status') not in ('REFINED', 'READY'):
            errors.append('DoR status must be REFINED or READY')
        ac = s.get('acceptance_criteria')
        if not isinstance(ac, list) or not ac or any(not isinstance(a, dict) or not str(a.get('description', '')).strip() for a in ac):
            errors.append('DoR acceptance_criteria empty description')
        if not s.get('test_scenarios'):
            errors.append('DoR test_scenarios empty')
        if s.get('open_questions', []):
            errors.append('DoR open_questions non-empty')
        return errors

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
        pr, commits, reviews = self.github(record)
        require(all((c.get('author') or {}).get('login') and (c.get('committer') or {}).get('login') for c in commits), 'review unresolved commit login')
        reviews = sorted(reviews, key=lambda r: (r['submitted_at'], r['id']))
        non_comment = latest_non_comment_reviews(reviews)
        require(not any(r['state'] == 'CHANGES_REQUESTED' for r in non_comment.values()), 'review CHANGES_REQUESTED')
        r = next((r for r in non_comment.values() if r['id'] == record.get('review_id') and r['state'] == 'APPROVED'), None)
        require(r is not None, 'review not verified APPROVED')
        forbidden = {pr['user']['login'], self.identity(story)['implementing_identity']}
        forbidden.update(c[k]['login'] for c in commits for k in ('author', 'committer'))
        require(r['user']['login'] not in forbidden, 'review self-approval')
        require(record['producer_identity'] == r['user']['login'], 'review identity mismatch')
        require(self.implementation(r['commit_id']) == self.implementation(), 'STALE_IMPLEMENTATION reviewed commit')

    def record(self, story, gate, r, allow_nonpass=False, history=False):
        config = self.workflow['gates'][gate]
        for field in ('story_id', 'gate', 'result', 'producer_role', 'producer_identity', 'timestamp', 'source_commit', 'implementation_fingerprint', 'artifacts'):
            require(r.get(field) not in (None, '', []), f'INVALID {gate} field {field}')
        require(re.fullmatch('[a-f0-9]{40}', r['source_commit']) is not None, 'INVALID source commit')
        self.git('cat-file', '-e', r['source_commit'] + '^{commit}')
        require(r['story_id'] == story and r['gate'] == gate, 'INVALID Story/gate record')
        require(isinstance(r["timestamp"], str) and "T" in r["timestamp"], "INVALID UTC timestamp")
        timestamp = datetime.datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00"))
        require(timestamp.tzinfo is not None and timestamp.utcoffset() == datetime.timedelta(0), "INVALID UTC timestamp")
        producer_state = self.identity(story, r['source_commit'] if history else None) if 'IMPLEMENTER' in config['producers'] else None
        roles = [producer_state['implementing_role'] if x == 'IMPLEMENTER' else x for x in config['producers']]
        require(r['producer_role'] in roles, 'wrong producer')
        if 'IMPLEMENTER' in config['producers']:
            require(r['producer_identity'] == producer_state['implementing_identity'], 'wrong producer identity')
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
        for a in r['artifacts']:
            self.artifact(a)
        if allow_nonpass and r["result"] in ("FAIL", "NOT_EXECUTED", "UNKNOWN", "PENDING_PO"):
            require(isinstance(r.get("checks"), dict) and r["checks"], "INVALID structured checks")
            return r["result"]
        if r['result'] == 'N/A':
            s = self.story(story)
            require(config['na'] and gate in s.get('na_permitted', []) and story != 'US-FACTORY-003', 'N/A not permitted')
            require(r.get('po_approval', {}).get('identity') and r['po_approval'].get('date') and r.get('reason') and r.get('decision_reference'), 'N/A approval incomplete')
            require(r.get('execution_status') == 'NOT_APPLICABLE', 'N/A failed or missing execution')
            self.artifact(r['decision_reference'])
            return 'N/A-APPROVED'
        require(r['result'] == 'PASS', f'{r["result"]} result not PASS')
        require(isinstance(r.get('checks'), dict) and r['checks'] and all(x == 'PASS' for x in r['checks'].values()), 'INVALID structured checks')
        if gate in ('Tester', 'QA'):
            expected = {a['id'] for a in self.story(story)['acceptance_criteria']}
            require(set(r.get('ac_results', {})) == expected and all(x == 'PASS' for x in r['ac_results'].values()), 'INVALID per-AC results')
        if gate == 'Unit Test':
            expected = {t['id'] for t in self.story(story)['test_scenarios']} - {'TS24', 'TS25'}
            require(set(r.get('ts_results', {})) == expected and all(x == 'PASS' for x in r['ts_results'].values()), 'INVALID per-TS results')
        if gate == 'Code Review' and not history:
            self.review(story, r)
        if gate == 'Jenkins':
            require(r['checks'].get('Factory Validation') == 'PASS', 'Jenkins Factory Validation missing')
        return 'PASS'

    def prior_record_valid(self, story, gate, record):
        key = (gate, repr(record))
        if key in self._prior_cache:
            return self._prior_cache[key]
        result = self._prior_record_valid(story, gate, record)
        self._prior_cache[key] = result
        return result

    def _prior_record_valid(self, story, gate, record):
        try:
            self.record(story, gate, record)
            for parent in self.workflow["gates"][gate]["prerequisites"]:
                earlier = [r for r in self.records(story) if r.get("gate") == parent and timestamp_key(r) <= timestamp_key(record)]
                if not any(self.prior_record_valid(story, parent, r) for r in earlier):
                    return False
            return True
        except (Block, ValueError, KeyError, TypeError):
            return False

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
        # Newest record wins. Older records remain immutable history.
        r = max(candidates, key=timestamp_key)
        try:
            state = self.record(story, gate, r)
            for parent in self.workflow['gates'][gate]['prerequisites']:
                prior = [x for x in self.records(story) if x.get('gate') == parent]
                require(any(timestamp_key(x) <= timestamp_key(r) and self.prior_record_valid(story, parent, x) for x in prior), "out-of-order record")
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
            require(s.get('blocked_from') == source and s.get('blocked_by'), 'BLOCKED requires blocked_from and blocked_by')
            return []
        if source == 'BLOCKED':
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
