"""MOCK automated Unit Test suite: disposable repositories only."""
import copy
import os
import unittest
from argparse import Namespace
from pathlib import Path

import yaml

from cli import jenkins, orchestrate
from engine import Block, Factory, digest
from fixtures import Fixture, STORY


class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.x = Fixture()
        self.f = self.x.f
        print('MOCK disposable repository ' + self.id())

    def tearDown(self):
        self.x.close()

    def assertGate(self, gate, state='PASS'):
        self.assertEqual(self.f.gate(STORY, gate)[0], state, self.f.gate(STORY, gate))

    def test_TS01_MOCK_happy_path(self):
        self.x.all_gates()
        for gate in self.f.workflow['gates']:
            self.assertGate(gate)
        self.x.s['status'] = 'QA'
        a = f'factory/evidence/{STORY}/summary.md'
        self.x.s['definition_of_done']['evidence'] = {'implementation_complete': {'path': a, 'sha256': digest(self.f.blob(a))}}
        self.x.save()
        self.assertEqual(self.f.transition(STORY, 'QA', 'DONE'), [])

    def test_TS02_MOCK_missing_review(self):
        for g in ('build', 'lint', 'Unit Test'):
            self.x.record(g)
        self.x.s['status'] = 'DEV_COMPLETE'
        self.x.save()
        for role in ('Integration Test', 'CODEX_TESTER'):
            self.assertTrue(self.f.dispatch(STORY, role))
        self.assertTrue(self.f.transition(STORY, 'DEV_COMPLETE', 'TESTING'))

    def test_TS03_MOCK_missing_tester(self):
        for g in ('build', 'lint', 'Unit Test', 'Code Review', 'Integration Test'):
            self.x.record(g)
        self.x.s['status'] = 'TESTING'
        self.x.save()
        self.assertTrue(self.f.dispatch(STORY, 'CODEX_QA'))
        self.assertTrue(self.f.transition(STORY, 'TESTING', 'QA'))

    def test_TS04_MOCK_tester_without_review(self):
        self.x.record('Tester')
        self.assertGate('Tester', 'INVALID')

    def test_TS05_MOCK_completion_blockers(self):
        self.x.all_gates()
        self.x.s['status'] = 'QA'
        self.x.save()
        self.assertTrue(self.f.transition(STORY, 'QA', 'DONE'))
        self.x.s['blocked_by'] = ['MOCK blocker']
        self.x.save()
        self.assertIn('open blocker blocked_by', self.f.transition(STORY, 'QA', 'DONE'))
        (self.x.root / 'safe/raid.yaml').write_text(f'issues:\n - id: MOCK_I\n   status: OPEN\n   blocks: [{STORY}]\n')
        self.x.commit()
        self.assertTrue(any('MOCK_I' in x for x in self.f.transition(STORY, 'QA', 'DONE')))

    def test_TS06_MOCK_mandatory_fields(self):
        r, path = self.x.record('build')
        for key in ('story_id', 'gate', 'result', 'producer_role', 'producer_identity', 'timestamp', 'source_commit', 'implementation_fingerprint', 'artifacts'):
            broken = copy.deepcopy(r)
            del broken[key]
            with self.assertRaises((Block, KeyError)):
                self.f.record(STORY, 'build', broken)
        for result in ('UNKNOWN', 'PARTIAL', 'NOT_EXECUTED', 'PASS WITH BLOCKERS'):
            with self.assertRaises(Block):
                self.f.record(STORY, 'build', dict(r, result=result))
        path.write_text('not: [valid')
        self.x.commit()
        with self.assertRaises(yaml.YAMLError):
            self.f.records(STORY)

    def test_TS07_MOCK_committed_implementation_change(self):
        self.x.all_gates()
        (self.x.root / 'app.txt').write_text('changed')
        self.x.commit()
        for g in self.f.workflow['gates']:
            self.assertGate(g, 'STALE_IMPLEMENTATION')

    def test_TS08_MOCK_stale_blocks_completion(self):
        self.x.all_gates()
        self.x.s['status'] = 'QA'
        (self.x.root / 'app.txt').write_text('changed')
        self.x.save()
        self.assertTrue(self.f.transition(STORY, 'QA', 'DONE'))

    def test_TS09_MOCK_nonimplementation_commit(self):
        self.x.all_gates()
        before = self.f.implementation()
        (self.x.root / 'safe/other.md').write_text('MOCK metadata')
        self.x.commit()
        self.assertEqual(before, self.f.implementation())
        self.assertGate('Code Review')

    def test_TS10_MOCK_artifact_durability(self):
        for path in ('/tmp/a', '../a', 'factory/logs/a', 'missing.md'):
            with self.assertRaises(Block):
                self.f.artifact({'path': path, 'sha256': '0' * 64})
        (self.x.root / f'factory/evidence/{STORY}/raw.log').write_text('MOCK')
        self.x.commit()
        with self.assertRaises(Block):
            self.f.records(STORY)

    def test_TS11_MOCK_recovery_path(self):
        for gate in ('build', 'lint', 'Unit Test', 'Tester', 'QA'):
            self.x.record(gate)
        self.x.s['status'] = 'QA'
        self.x.save()
        self.assertEqual(self.f.transition(STORY, 'QA', 'DEV_COMPLETE', 'DoD FAIL: MOCK missing review'), [])
        self.x.s['status'] = 'DEV_COMPLETE'
        self.x.save()
        self.assertTrue(self.f.transition(STORY, 'DEV_COMPLETE', 'TESTING'))
        for gate in ('Code Review', 'Integration Test', 'Tester', 'QA'):
            self.x.record(gate)
        self.assertEqual(self.f.transition(STORY, 'DEV_COMPLETE', 'TESTING'), [])

    def test_TS12_MOCK_classified_paths(self):
        self.x.all_gates()
        implementation, contract = self.f.implementation(), self.f.contract(STORY)
        (self.x.root / 'docs').mkdir()
        for path in ('docs/readme.md', 'safe/unrelated.md', f'factory/evidence/{STORY}/extra.md'):
            (self.x.root / path).write_text('MOCK non-material document')
            self.x.commit()
            self.assertEqual(implementation, self.f.implementation())
            self.assertEqual(contract, self.f.contract(STORY))
            for gate in self.f.workflow['gates']:
                self.assertGate(gate)
        self.x.s['business_value'] = 'MOCK updated metadata'
        self.x.save()
        for gate in self.f.workflow['gates']:
            self.assertGate(gate)
        (self.x.root / 'unknown.bin').write_bytes(b'new implementation')
        self.x.commit()
        for gate in self.f.workflow['gates']:
            self.assertGate(gate, 'STALE_IMPLEMENTATION')

    def test_TS12_C3_MOCK_approved_contract(self):
        reference = self.x.root / 'safe/reference.md'
        reference.write_text('MOCK contract')
        self.x.s['contract_refs'] = ['safe/reference.md']
        self.x.save()
        self.x.all_gates()
        implementation = self.f.implementation()
        for change in ('material Story key', 'contract_refs file'):
            with self.subTest(change=change):
                if change == 'material Story key':
                    self.x.s['acceptance_criteria'][0]['description'] += ' changed'
                    self.x.save()
                else:
                    reference.write_text('MOCK changed contract')
                    self.x.commit()
                self.assertEqual(implementation, self.f.implementation())
                for gate in self.f.workflow['gates']:
                    self.assertGate(gate, 'STALE_CONTRACT' if gate in ('Tester', 'QA') else 'PASS')
                self.x.all_gates()

    def test_TS13_MOCK_independence(self):
        self.x.all_gates()
        r = next(r for r in self.f.records(STORY) if r['gate'] == 'Code Review')
        self.f.review(STORY, r)
        def self_review(record):
            pr, commits, reviews = self.x.mock_github(record)
            reviews[0]['user']['login'] = pr['user']['login']
            return pr, commits, reviews
        self.f.github = self_review
        with self.assertRaisesRegex(Block, 'self-approval'):
            self.f.review(STORY, r)
        self.f.github = None
        with self.assertRaisesRegex(Block, 'NOT_EXECUTED'):
            self.f.review(STORY, r)
        r['producer_role'] = 'CODEX_DEVOPS'
        with self.assertRaisesRegex(Block, 'wrong producer'):
            self.f.record(STORY, 'Code Review', r)

    def test_TS13_C1_MOCK_approval_then_comment(self):
        self.x.all_gates()
        record = next(r for r in self.f.records(STORY) if r['gate'] == 'Code Review')
        def commented(r):
            pr, commits, reviews = self.x.mock_github(r)
            reviews.append(dict(reviews[0], id=2, state='COMMENTED', submitted_at='2026-10-03T00:00:01Z'))
            return pr, commits, reviews
        self.f.github = commented
        self.f.review(STORY, record)
        self.assertGate('Code Review')

    def test_TS13_C2_MOCK_changes_request_survives_comment(self):
        self.x.all_gates()
        record = next(r for r in self.f.records(STORY) if r['gate'] == 'Code Review')
        for login in ('MOCK_reviewer', 'MOCK_other_reviewer'):
            for later_comment in (False, True):
                with self.subTest(login=login, later_comment=later_comment):
                    def requested(r):
                        pr, commits, reviews = self.x.mock_github(r)
                        request = dict(reviews[0], id=2, user={'login': login}, state='CHANGES_REQUESTED', submitted_at='2026-10-03T00:00:01Z')
                        reviews.append(request)
                        if later_comment:
                            reviews.append(dict(request, id=3, state='COMMENTED', submitted_at='2026-10-03T00:00:02Z'))
                        return pr, commits, reviews
                    self.f.github = requested
                    with self.assertRaisesRegex(Block, 'CHANGES_REQUESTED'):
                        self.f.review(STORY, record)

    def test_TS14_MOCK_na_approval(self):
        self.x.all_gates()
        self.x.s['na_permitted'] = ['Integration Test']
        self.x.save()
        r = next(r for r in self.f.records(STORY) if r['gate'] == 'Integration Test')
        r.update(result='N/A', po_approval={'identity': 'MOCK_PO', 'date': '2026-10-03'}, reason='MOCK no integration target', decision_reference=r['artifacts'][0], execution_status='NOT_APPLICABLE')
        self.assertEqual(self.f.record(STORY, 'Integration Test', r), 'N/A-APPROVED')
        for key in ('po_approval', 'reason', 'decision_reference', 'execution_status'):
            broken = dict(r)
            del broken[key]
            with self.assertRaises(Block):
                self.f.record(STORY, 'Integration Test', broken)

    def test_TS15_MOCK_transitions(self):
        for source, target in (('DRAFT', 'IN_PROGRESS'), ('DONE', 'READY')):
            self.x.s['status'] = source
            self.x.save()
            with self.assertRaises(Block):
                self.f.transition(STORY, source, target)
        self.x.s.update(status='READY', blocked_from='READY', blocked_by=['MOCK'])
        self.x.save()
        self.assertEqual(self.f.transition(STORY, 'READY', 'BLOCKED'), [])
        self.x.s['status'] = 'BLOCKED'
        self.x.save()
        self.assertEqual(self.f.transition(STORY, 'BLOCKED', 'READY'), [])
        with self.assertRaises(Block):
            self.f.transition(STORY, 'BLOCKED', 'QA')

    def test_TS16_MOCK_orchestrator_atomic_block(self):
        before = {p: p.read_bytes() for p in self.x.root.rglob('*') if p.is_file() and '.git' not in p.parts}
        args = Namespace(story=STORY, action='dispatch', role='CODEX_QA', source=None, target=None, reason=None, identity=None)
        with self.assertRaises(Block):
            orchestrate(self.f, args)
        self.assertEqual(before, {p: p.read_bytes() for p in before})
        args.role = 'CODEX_DEVOPS'
        args.identity = 'MOCK_implementer'
        orchestrate(self.f, args)
        self.assertEqual(len(list((self.x.root / f'factory/evidence/{STORY}').glob('event-*.json'))), 1)

    def test_TS17_MOCK_invalid_workflow(self):
        p = self.x.root / 'factory/workflow.yaml'
        p.write_text('version: 1\n')
        with self.assertRaises(Block):
            Factory(self.x.root)
        p.unlink()
        with self.assertRaises(OSError):
            Factory(self.x.root)

    def test_TS19_MOCK_material_contract(self):
        self.x.all_gates()
        self.x.s['description'] = 'MOCK revised contract'
        self.x.save()
        self.assertGate('Tester', 'STALE_CONTRACT')
        self.assertGate('QA', 'STALE_CONTRACT')
        self.assertGate('Integration Test')
        self.x.s['description'] = 'MOCK contract'
        self.x.s.update(priority='low', business_value='MOCK non-material', open_questions=['MOCK'])
        self.x.save()
        self.assertGate('QA')

    def test_TS20_MOCK_external_archive(self):
        a = {'system': 'jenkins', 'job': 'MOCK-job', 'build': 1, 'path': 'MOCK-summary.json', 'sha256': digest(b'MOCK archive')}
        self.f.external(a)
        for key in a:
            broken = dict(a)
            del broken[key]
            with self.assertRaises((Block, KeyError)):
                self.f.external(broken)
        a['sha256'] = '0' * 64
        with self.assertRaises(Block):
            self.f.external(a)

    def test_TS21_MOCK_jenkins_status(self):
        self.x.s['status'] = 'DEV_COMPLETE'
        self.x.save()
        self.assertTrue(jenkins(self.f, f'feature/{STORY}-devops'))
        for gate in ('build', 'lint', 'Unit Test'):
            self.x.record(gate)
        self.assertEqual(jenkins(self.f, f'feature/{STORY}-devops'), [])
        self.x.s['status'] = 'DONE'
        self.x.save()
        self.assertTrue(jenkins(self.f, 'develop'))

    def test_TS22_MOCK_dor_defect(self):
        self.assertEqual(self.f.dor(self.x.s), [])
        for change in ({'definition_of_ready': {}}, {'status': 'DRAFT', 'acceptance_criteria': [{'id': 'AC01', 'description': ''}], 'test_scenarios': []}, {'open_questions': ['MOCK unresolved']}):
            s = copy.deepcopy(self.x.s)
            s.update(change)
            self.assertTrue(self.f.dor(s))
        for key in self.x.s['definition_of_ready']:
            s = copy.deepcopy(self.x.s)
            del s['definition_of_ready'][key]
            self.assertTrue(self.f.dor(s))

    def test_TS23_MOCK_runtime_contract_and_installed_versions(self):
        import importlib.metadata
        import platform
        import re
        import subprocess
        source = Path(__file__).resolve().parents[1]
        contract = (source / 'runtime/contract.env').read_text()
        self.assertRegex(contract, r'FACTORY_IMAGE=python:3\.12@sha256:[a-f0-9]{64}')
        values = dict(line.split('=', 1) for line in contract.splitlines() if '=' in line and not line.startswith('#'))
        self.assertEqual(platform.python_version(), values['FACTORY_PYTHON'])
        pins = (source / 'runtime/requirements.txt').read_text().splitlines()
        for pin in pins:
            package, version = pin.split()[0].split('==')
            self.assertEqual(importlib.metadata.version(package), version)
        paths = subprocess.run(['git', '-C', str(source.parent), 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], capture_output=True, check=True).stdout.split(b'\0')
        definitions = []
        declaration = re.compile(r'^\s*(?:FACTORY_IMAGE=|image:\s*)python:3\.12@sha256:', re.MULTILINE)
        for raw in paths:
            if not raw:
                continue
            path = raw.decode()
            if path.startswith(('safe/', 'factory/state/', 'factory/evidence/', 'factory/logs/')):
                continue
            if Path(path).suffix in ('.env', '.sh', '.yaml', '.yml', '.py'):
                if declaration.search((source.parent / path).read_text()):
                    definitions.append(path)
        self.assertEqual(definitions, ['factory/runtime/contract.env'])

    def test_TS26_MOCK_producer_order(self):
        self.x.all_gates()
        r = next(r for r in self.f.records(STORY) if r['gate'] == 'Integration Test')
        for role in ('CODEX_TESTER', 'CODEX_QA'):
            with self.assertRaisesRegex(Block, 'wrong producer'):
                self.f.record(STORY, 'Integration Test', dict(r, producer_role=role))
        self.x.s['status'] = 'DEV_COMPLETE'
        self.x.save()
        self.assertEqual(self.f.dispatch(STORY, 'CODEX_TESTER'), [])

    def test_TS27_MOCK_linked_worktree(self):
        linked = self.x.root / 'linked'
        self.x.git('worktree', 'add', '--detach', str(linked), 'HEAD')
        self.assertEqual(self.f.implementation(), Factory(linked).implementation())
        self.assertEqual(os.getuid(), (self.x.root / f'factory/state/{STORY}.json').stat().st_uid)

    def test_TS28_MOCK_actual_build_and_lint_failures(self):
        import subprocess
        import sys
        cli = str(Path(__file__).resolve().parents[1] / 'cli.py')
        bad = self.x.root / 'factory/bad.py'
        bad.write_text('def invalid(:\n')
        result = subprocess.run([sys.executable, cli, 'build', '--root', str(self.x.root)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        bad.write_text('import os\n')
        result = subprocess.run([sys.executable, cli, 'lint', '--root', str(self.x.root)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        bad.write_text('value = 1\n')
        for command in ('build', 'lint'):
            result = subprocess.run([sys.executable, cli, command, '--root', str(self.x.root)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_TS27_MOCK_actual_readonly_mount(self):
        source = Path(__file__).resolve().parents[1]
        with self.assertRaises(OSError):
            (source / 'readonly-probe').write_text('MOCK write must fail')
        self.assertFalse((source / 'readonly-probe').exists())

    def test_TS13_MOCK_approval_withdrawn_or_comment_only(self):
        self.x.all_gates()
        record = next(r for r in self.f.records(STORY) if r['gate'] == 'Code Review')
        for state in ('COMMENTED', 'DISMISSED'):
            with self.subTest(state=state):
                def withdrawn(r):
                    pr, commits, reviews = self.x.mock_github(r)
                    if state == 'COMMENTED':
                        reviews[0]['state'] = state
                    else:
                        reviews.append(dict(reviews[0], id=2, state=state, submitted_at='2026-10-03T00:00:01Z'))
                        reviews.append(dict(reviews[0], id=3, state='COMMENTED', submitted_at='2026-10-03T00:00:02Z'))
                    return pr, commits, reviews
                self.f.github = withdrawn
                with self.assertRaisesRegex(Block, 'not verified APPROVED'):
                    self.f.review(STORY, record)

    def test_TS18_MOCK_actual_base_diff(self):
        import subprocess
        root = Path(__file__).resolve().parents[2]
        base = '05004fc5d3ed1022fea2695f62c9d6d54dc233c5'
        for name in ('deploy', 'build', 'lint', 'unit-test', 'integration-test', 'security-scan', 'quality-gate', 'build-artifact', 'create-worktree'):
            path = f'scripts/{name}.sh'
            original = subprocess.run(['git', '-C', str(root), 'show', f'{base}:{path}'], capture_output=True, check=True).stdout
            self.assertEqual(original, (root / path).read_bytes())
        original = subprocess.run(['git', '-C', str(root), 'show', f'{base}:Jenkinsfile'], capture_output=True, check=True).stdout.decode()
        stage = "        stage('Factory Validation') {\n            steps {\n                sh './scripts/factory-jenkins.sh'\n            }\n        }\n\n"
        current = (root / 'Jenkinsfile').read_text()
        self.assertEqual(current.count(stage), 1)
        self.assertEqual(current.replace(stage, ''), original)
        self.assertFalse((root / 'docker-compose.test.yml').exists())

    def test_TS28_MOCK_actual_unit_entry(self):
        import subprocess
        import sys
        cli = str(Path(__file__).resolve().parents[1] / 'cli.py')
        directory = self.x.root / 'factory/tests'
        directory.mkdir()
        definition = self.f.workflow.copy()
        definition['unit_scenarios'] = ['TS01']
        (self.x.root / 'factory/workflow.yaml').write_text(yaml.safe_dump(definition))
        test_file = directory / 'test_command.py'
        variants = [
            ('', False),
            ('import unittest\nclass Tests(unittest.TestCase):\n def test_TS01_MOCK_fail(self): self.fail("MOCK deliberate")\n', False),
            ('import unittest\nclass Tests(unittest.TestCase):\n @unittest.skip("MOCK NOT_EXECUTED")\n def test_TS01_MOCK_skip(self): pass\n', False),
            ('import unittest\nclass Tests(unittest.TestCase):\n def test_TS01_MOCK_pass(self): self.assertEqual(2+2,4)\n', True)]
        for content, expected in variants:
            test_file.write_text(content)
            result = subprocess.run([sys.executable, cli, 'unit', '--root', str(self.x.root)], capture_output=True)
            self.assertEqual(result.returncode == 0, expected, result.stdout + result.stderr)

    def test_TS05_MOCK_remaining_completion_rules(self):
        self.x.all_gates()
        qa = next(r for r in self.f.records(STORY) if r['gate'] == 'QA')
        for ac in ({}, {'AC01': 'FAIL'}, {'AC01': 'PASS', 'AC02': 'PASS'}):
            with self.assertRaisesRegex(Block, 'per-AC'):
                self.f.record(STORY, 'QA', dict(qa, ac_results=ac))
        self.x.s['status'] = 'QA'
        self.x.s['depends_on'] = ['US-998']
        self.x.save()
        self.assertTrue(any('dependencies' in r for r in self.f.transition(STORY, 'QA', 'DONE')))

    def test_TS13_MOCK_all_review_rejection_rules(self):
        self.x.all_gates()
        record = next(r for r in self.f.records(STORY) if r['gate'] == 'Code Review')
        for login in ('MOCK_author', 'MOCK_committer', 'MOCK_implementer'):
            def mock_forbidden(r):
                pr, commits, reviews = self.x.mock_github(r)
                reviews[0]['user']['login'] = login
                commits[0]['committer']['login'] = 'MOCK_committer'
                return pr, commits, reviews
            self.f.github = mock_forbidden
            with self.assertRaisesRegex(Block, 'self-approval'):
                self.f.review(STORY, record)
        for review_state in ('COMMENTED', 'DISMISSED', 'CHANGES_REQUESTED'):
            def mock_state(r):
                pr, commits, reviews = self.x.mock_github(r)
                reviews[0]['state'] = review_state
                return pr, commits, reviews
            self.f.github = mock_state
            with self.assertRaises(Block):
                self.f.review(STORY, record)
        for field in ('author', 'committer'):
            def mock_unresolved(r):
                pr, commits, reviews = self.x.mock_github(r)
                commits[0][field] = None
                return pr, commits, reviews
            self.f.github = mock_unresolved
            with self.assertRaisesRegex(Block, 'unresolved'):
                self.f.review(STORY, record)
        def mock_missing_commit(r):
            pr, commits, reviews = self.x.mock_github(r)
            reviews[0]['commit_id'] = '0' * 40
            return pr, commits, reviews
        self.f.github = mock_missing_commit
        with self.assertRaises(Block):
            self.f.review(STORY, record)
        self.f.github = self.x.mock_github
        with self.assertRaises(Block):
            self.f.review(STORY, dict(record, review_id=200))
        for gate in ('build', 'lint', 'Unit Test', 'Integration Test', 'Tester', 'QA'):
            r = next(r for r in self.f.records(STORY) if r['gate'] == gate)
            wrong_roles = ('CODEX_DEVOPS', 'UNKNOWN') if gate in ('Tester', 'QA') else ('CODEX_TESTER', 'CODEX_QA')
            for wrong in wrong_roles:
                with self.assertRaisesRegex(Block, 'wrong producer'):
                    self.f.record(STORY, gate, dict(r, producer_role=wrong))

    def test_TS13_MOCK_github_unavailable(self):
        from unittest.mock import patch
        from remotes import GitHub
        self.x.all_gates()
        record = next(r for r in self.f.records(STORY) if r['gate'] == 'Code Review')
        record.update(repository='MOCK/repository', pull_request=1)
        self.f.github = GitHub(None)
        with self.assertRaisesRegex(Block, 'NOT_EXECUTED GitHub credential unavailable'):
            self.f.review(STORY, record)
        self.f.github = GitHub('MOCK credential')
        with patch('remotes.urllib.request.urlopen', side_effect=OSError('MOCK unreachable')):
            with self.assertRaisesRegex(Block, 'NOT_EXECUTED GitHub verification unavailable'):
                self.f.review(STORY, record)

    def test_TS13_MOCK_reviewed_commit_different_fingerprint(self):
        self.x.all_gates()
        record = next(r for r in self.f.records(STORY) if r['gate'] == 'Code Review')
        (self.x.root / 'app.txt').write_text('MOCK new implementation')
        self.x.commit()
        with self.assertRaisesRegex(Block, 'STALE_IMPLEMENTATION reviewed commit'):
            self.f.review(STORY, record)

    def test_TS15_MOCK_failure_paths(self):
        for reason, rule in self.f.workflow['failure_paths'].items():
            for source in rule['from']:
                for target in rule['to']:
                    self.x.s['status'] = source
                    self.x.save()
                    self.assertEqual(self.f.transition(STORY, source, target, reason + ': MOCK recorded cause'), [])
        self.x.s.update(status='READY', blocked_from=None, blocked_by=[])
        self.x.save()
        with self.assertRaises(Block):
            self.f.transition(STORY, 'READY', 'BLOCKED')

    def test_TS17_MOCK_all_cli_entrypoints(self):
        import subprocess
        import sys
        cli = str(Path(__file__).resolve().parents[1] / 'cli.py')
        (self.x.root / 'factory/workflow.yaml').write_text('version: INVALID\n')
        for command in ('build', 'lint', 'unit', 'integration', 'dor', 'status', 'validate-gate', 'can-transition', 'can-dispatch', 'orchestrate', 'write-evidence', 'jenkins'):
            result = subprocess.run([sys.executable, cli, command, '--root', str(self.x.root)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b'BLOCK', result.stdout)

    def test_TS19_MOCK_all_material_keys_and_refs(self):
        initial = self.f.contract(STORY)
        for key in self.f.workflow['material_keys']:
            old = copy.deepcopy(self.x.s)
            if key == 'acceptance_criteria':
                self.x.s[key][0]['description'] += ' modified'
            elif key == 'test_scenarios':
                self.x.s[key][0]['scenario'] += ' modified'
            else:
                self.x.s[key] = 'MOCK changed value'
            self.x.save()
            self.assertNotEqual(initial, self.f.contract(STORY), key)
            self.x.s = old
            self.x.save()
        ref = self.x.root / 'safe/reference.md'
        ref.write_text('MOCK spec')
        self.x.s['contract_refs'] = ['safe/reference.md']
        self.x.save()
        old = self.f.contract(STORY)
        ref.write_text('MOCK changed spec')
        self.x.commit()
        self.assertNotEqual(old, self.f.contract(STORY))

    def test_TS20_MOCK_external_reference_credentials(self):
        a = {'system': 'jenkins', 'job': 'MOCK-job', 'build': 1, 'path': 'MOCK.json', 'sha256': digest(b'MOCK archive')}
        for changes in ({'system': 'unknown'}, {'path': '/tmp/a'}, {'path': '../a'}, {'job': 'MOCK@invalid'}, {'sha256': 'invalid'}):
            with self.assertRaises(Block):
                self.f.external(dict(a, **changes))
        self.f.archive = lambda artifact: b'MOCK wrong archive'
        with self.assertRaisesRegex(Block, 'hash mismatch'):
            self.f.external(a)

    def test_TS23_MOCK_missing_docker_invalid_image_and_digest(self):
        import shutil
        import subprocess
        source = Path(__file__).resolve().parents[2]
        (self.x.root / 'scripts').mkdir()
        (self.x.root / 'factory/runtime').mkdir()
        for name in ('contract.env', 'requirements.txt'):
            shutil.copyfile(source / 'factory/runtime' / name, self.x.root / 'factory/runtime' / name)
        helper = self.x.root / 'scripts/factory-runtime.sh'
        shutil.copyfile(source / 'scripts/factory-runtime.sh', helper)
        environment = dict(os.environ, FACTORY_CANONICAL_REENTRY='')
        # The canonical image contains no Docker executable; there is no host Python fallback.
        result = subprocess.run(['bash', str(helper), 'build'], cwd=self.x.root, env=environment, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b'Docker unavailable', result.stdout)
        (self.x.root / 'factory/runtime/contract.env').write_text('FACTORY_IMAGE=invalid\nFACTORY_PYTHON=3.12.15\n')
        result = subprocess.run(['bash', str(helper), 'build'], cwd=self.x.root, env=environment, capture_output=True)
        self.assertIn(b'invalid image contract', result.stdout)
        shutil.copyfile(source / 'factory/runtime/contract.env', self.x.root / 'factory/runtime/contract.env')
        binaries = self.x.root / 'MOCK-bin'
        binaries.mkdir()
        docker = binaries / 'docker'
        docker.write_text('#!/bin/sh\necho "MOCK Docker digest unavailable"\nexit 1\n')
        docker.chmod(0o755)
        environment['PATH'] = str(binaries) + ':' + os.environ['PATH']
        result = subprocess.run(['bash', str(helper), 'build'], cwd=self.x.root, env=environment, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b'MOCK Docker digest unavailable', result.stdout)

    def test_TS23_MOCK_dependency_hash_mismatch(self):
        import subprocess
        import sys
        requirements = self.x.root / 'bad-hash.txt'
        requirements.write_text('PyYAML==6.0.3 --hash=sha256:' + '0' * 64 + '\n')
        result = subprocess.run([sys.executable, '-m', 'pip', 'download', '--disable-pip-version-check', '--no-cache-dir', '--no-deps', '--only-binary=:all:', '--require-hashes', '-r', str(requirements), '--dest', str(self.x.root / 'wheels')], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b'HASHES', result.stderr.upper())

    def test_TS23_MOCK_python_names_removed_from_PATH(self):
        import shutil
        import subprocess
        source = Path(__file__).resolve().parents[2]
        (self.x.root / 'scripts').mkdir()
        (self.x.root / 'factory/runtime').mkdir()
        shutil.copyfile(source / 'scripts/factory-runtime.sh', self.x.root / 'scripts/factory-runtime.sh')
        shutil.copyfile(source / 'factory/runtime/contract.env', self.x.root / 'factory/runtime/contract.env')
        shutil.copyfile(source / 'factory/cli.py', self.x.root / 'factory/cli.py')
        bins = self.x.root / 'MOCK-no-python-bin'
        bins.mkdir()
        for command in ('bash', 'git'):
            (bins / command).symlink_to(shutil.which(command))
        env = dict(os.environ, PATH=str(bins))
        result = subprocess.run([str(bins / 'bash'), str(self.x.root / 'scripts/factory-runtime.sh'), 'build'], cwd=self.x.root, env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(b'canonical container reentry', result.stdout)

    def test_TS10_MOCK_symlink_parent_escape(self):
        import tempfile
        directory = self.x.root / 'factory/evidence'
        directory.rename(self.x.root / 'factory/evidence-original')
        with tempfile.TemporaryDirectory(prefix='factory-MOCK-outside-') as outside:
            directory.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(Block, 'symlink parent'):
                self.f.path(f'factory/evidence/{STORY}/forbidden.json')
            self.assertFalse((Path(outside) / STORY).exists())

    def test_TS07_MOCK_rerun_keeps_history_valid_for_jenkins(self):
        self.x.all_gates()
        old_records = {p: p.read_bytes() for p in (self.x.root / f'factory/evidence/{STORY}').glob('*.json')}
        (self.x.root / 'app.txt').write_text('MOCK changed implementation')
        self.x.commit()
        self.x.all_gates()
        self.x.s['status'] = 'DEV_COMPLETE'
        self.x.save()
        self.assertEqual(jenkins(self.f, f'feature/{STORY}-devops'), [])
        self.assertEqual(old_records, {p: p.read_bytes() for p in old_records})
        for gate in self.f.workflow['gates']:
            self.assertGate(gate)

    def test_TS12_MOCK_state_metadata_commit_keeps_gates(self):
        import json
        self.x.all_gates()
        initial = self.f.implementation()
        state_path = self.x.root / f'factory/state/{STORY}.json'
        state = json.loads(state_path.read_text())
        state['status'] = 'DEV_COMPLETE'
        state_path.write_text(json.dumps(state))
        self.x.commit()
        self.assertEqual(initial, self.f.implementation())
        for gate in self.f.workflow['gates']:
            self.assertGate(gate)

    def test_TS06_MOCK_iso_utc_timestamp_forms(self):
        from engine import parse
        r, _ = self.x.record('build')
        r['timestamp'] = '2026-10-03T00:00:00+00:00'
        self.assertEqual(self.f.record(STORY, 'build', r), 'PASS')
        loaded = parse(yaml.safe_dump(r))
        self.assertEqual(self.f.record(STORY, 'build', loaded), 'PASS')
        for timestamp in ('2026-10-03T00:00:00+07:00', '2026-10-03T00:00:00', 'invalid'):
            with self.assertRaises((Block, ValueError)):
                self.f.record(STORY, 'build', dict(r, timestamp=timestamp))

    def test_TS06_MOCK_fractional_timestamp_selects_latest_failure(self):
        self.x.record('build', timestamp='2026-10-03T00:00:01Z')
        self.x.record('build', timestamp='2026-10-03T00:00:01.500000+00:00', result='FAIL')
        self.assertGate('build', 'INVALID')
        self.assertIn('FAIL result not PASS', self.f.gate(STORY, 'build')[1][-1])

    def test_TS22_MOCK_required_story_sections_preserved(self):
        for field in ('id', 'title', 'status', 'acceptance_criteria', 'test_scenarios', 'definition_of_ready'):
            s = copy.deepcopy(self.x.s)
            del s[field]
            if field == 'definition_of_ready':
                with self.assertRaises(Block):
                    self.f.dor(s)
            else:
                self.assertTrue(self.f.dor(s), field)

    def test_TS06_MOCK_unknown_story_with_existing_records_blocks(self):
        self.x.all_gates()
        (self.x.root / f'safe/stories/{STORY}.yaml').unlink()
        self.x.commit()
        with self.assertRaises(Block):
            self.f.gate(STORY, 'build')

    def test_TS12_MOCK_later_unit_pass_preserves_valid_prior_chain(self):
        self.x.all_gates()
        self.x.record('Unit Test')
        for gate in self.f.workflow['gates']:
            self.assertGate(gate)

    def test_TS19_MOCK_outside_safe_ref_is_stale_without_pending(self):
        (self.x.root / 'docs').mkdir()
        reference = self.x.root / 'docs/contract.md'
        reference.write_text('MOCK contract reference')
        self.x.s['contract_refs'] = ['docs/contract.md']
        self.x.save()
        self.x.all_gates()
        reference.write_text('MOCK changed contract reference')
        self.x.commit()
        state, reasons = self.f.gate(STORY, 'Tester')
        self.assertEqual(state, 'STALE_CONTRACT')
        self.assertTrue(all('STALE_CONTRACT' in reason for reason in reasons))

    def test_TS13_MOCK_later_approval_clears_historical_comment_case(self):
        self.x.all_gates()
        record = next(r for r in self.f.records(STORY) if r['gate'] == 'Code Review')
        for first_state in ('APPROVED', 'CHANGES_REQUESTED'):
            def mock_reapproved(r):
                pr, commits, reviews = self.x.mock_github(r)
                reviews[0]['state'] = first_state
                reviews.append(dict(reviews[0], id=2, state='COMMENTED', submitted_at='2026-10-03T00:00:01Z'))
                reviews.append(dict(reviews[0], id=3, state='APPROVED', submitted_at='2026-10-03T00:00:02Z'))
                return pr, commits, reviews
            self.f.github = mock_reapproved
            self.f.review(STORY, dict(record, review_id=3))

    def test_TS16_MOCK_review_request_is_not_a_new_agent_role(self):
        import contextlib
        import io
        import json
        with self.assertRaisesRegex(Block, 'unknown role'):
            self.f.dispatch(STORY, 'IMPLEMENTER')
        self.x.all_gates()
        self.x.s['status'] = 'DEV_COMPLETE'
        state_path = self.x.root / f'factory/state/{STORY}.json'
        state = json.loads(state_path.read_text())
        state['status'] = 'DEV_COMPLETE'
        state_path.write_text(json.dumps(state))
        self.x.save()
        args = Namespace(story=STORY, action='dispatch', role='Code Review', source=None, target=None, reason=None, identity=None)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            orchestrate(self.f, args)
        self.assertIn('Request an independent GitHub PR review', output.getvalue())
        self.assertNotIn('Act as Code Review', output.getvalue())

    def test_TS06_MOCK_missing_or_wrong_gate_command_blocks(self):
        r, _ = self.x.record('build')
        for command in (None, '', 'MOCK unknown command'):
            with self.assertRaisesRegex(Block, 'gate command'):
                self.f.record(STORY, 'build', dict(r, command=command))
        del self.f.workflow['commands'][STORY]
        with self.assertRaisesRegex(Block, 'NOT_EXECUTED gate command missing'):
            self.f.record(STORY, 'build', r)
