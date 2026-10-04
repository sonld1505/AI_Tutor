"""MOCK review regressions, confined to disposable repositories."""
import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import unittest
from argparse import Namespace
from pathlib import Path

import yaml

from cli import jenkins, orchestrate
from engine import Block, Factory
from fixtures import STORY, Fixture


class ReworkTests(unittest.TestCase):
    def setUp(self):
        self.x = Fixture()
        self.f = self.x.f
        print('MOCK disposable review regression ' + self.id())

    def tearDown(self):
        self.x.close()

    def test_TS17_MOCK_uncommitted_policy_cannot_weaken_gates(self):
        for gate in ('build', 'lint', 'Unit Test'):
            self.x.record(gate)
        self.x.s['status'] = 'DEV_COMPLETE'
        self.x.save()
        before = self.f.transition(STORY, 'DEV_COMPLETE', 'TESTING')
        workflow = copy.deepcopy(self.f.workflow)
        workflow['transitions']['DEV_COMPLETE->TESTING'] = ['Unit Test']
        workflow['dispatch']['CODEX_TESTER']['prerequisites'] = ['Unit Test']
        path = self.x.root / 'factory/workflow.yaml'
        path.write_text(yaml.safe_dump(workflow))
        evaluated = Factory(self.x.root)
        self.assertEqual(evaluated.transition(STORY, 'DEV_COMPLETE', 'TESTING'), before)
        self.assertTrue(evaluated.dispatch(STORY, 'CODEX_TESTER'))
        cli = Path(__file__).resolve().parents[1] / 'cli.py'
        result = subprocess.run([sys.executable, str(cli), 'can-transition', '--root', str(self.x.root), '--workflow', str(path), '--story', STORY, '--from', 'DEV_COMPLETE', '--to', 'TESTING'], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b'unrecognized arguments: --workflow', result.stderr)

    def test_TS17_MOCK_unreadable_workflow_object_blocks(self):
        path = self.x.root / 'factory/workflow.yaml'
        path.unlink()
        path.symlink_to('missing-definition')
        self.x.commit()
        with self.assertRaises(Block):
            Factory(self.x.root)

    def test_TS11_MOCK_backdated_and_future_records_cannot_reorder(self):
        for future in (False, True):
            with self.subTest(future=future):
                fixture = Fixture()
                try:
                    for gate in ('build', 'lint', 'Unit Test'):
                        fixture.record(gate)
                    early, path = fixture.record('Tester', timestamp='2099-01-01T00:00:00Z' if future else '2026-10-03T12:00:00Z')
                    immutable = path.read_bytes()
                    for gate in ('Code Review', 'Integration Test'):
                        if future:
                            fixture.record(gate)
                        else:
                            fixture.record(gate, timestamp='2026-10-02T00:00:00Z')
                    fixture.s['status'] = 'TESTING'
                    fixture.save()
                    self.assertEqual(fixture.f.gate(STORY, 'Tester')[0], 'INVALID')
                    self.assertTrue(fixture.f.transition(STORY, 'TESTING', 'QA'))
                    self.assertTrue(fixture.f.dispatch(STORY, 'CODEX_QA'))
                    self.assertEqual(path.read_bytes(), immutable)
                    if not future:
                        self.assertEqual(fixture.f.gate(STORY, 'Code Review')[0], 'INVALID')
                        for gate in ('Code Review', 'Integration Test'):
                            fixture.record(gate)
                    fixture.record('Tester', timestamp='2026-10-01T00:00:00Z')
                    self.assertEqual(fixture.f.gate(STORY, 'Tester'), ('PASS', []))
                    self.assertEqual(fixture.f.transition(STORY, 'TESTING', 'QA'), [])
                    self.assertEqual(fixture.f.dispatch(STORY, 'CODEX_QA'), [])
                    self.assertEqual(early['gate'], 'Tester')
                finally:
                    fixture.close()

    def test_TS11_MOCK_rewritten_record_cannot_gain_provenance(self):
        self.x.all_gates()
        path = self.x.root / f'factory/evidence/{STORY}/006.json'
        record = json.loads(path.read_text())
        record['timestamp'] = '2099-01-01T00:00:00Z'
        path.write_text(json.dumps(record))
        self.x.commit()
        with self.assertRaisesRegex(Block, 'rewritten'):
            self.f.records(STORY)

    def test_TS13_MOCK_authorized_reviewer_repository_and_branch(self):
        self.x.all_gates()
        record = next(r for r in self.f.records(STORY) if r['gate'] == 'Code Review')
        self.f.review(STORY, record)
        for case in ('arbitrary login', 'NONE', 'CONTRIBUTOR', 'wrong base', 'wrong branch', 'truncated commits', 'server submission'):
            with self.subTest(case=case):
                def response(r):
                    pr, commits, reviews = self.x.mock_github(r)
                    if case == 'arbitrary login':
                        reviews[0]['user']['login'] = 'MOCK_arbitrary'
                    elif case in ('NONE', 'CONTRIBUTOR'):
                        reviews[0]['author_association'] = case
                    elif case == 'wrong base':
                        pr['base']['repo']['full_name'] = 'MOCK/fork'
                    elif case == 'wrong branch':
                        pr['head']['ref'] = 'feature/US-998-devops'
                    elif case == 'truncated commits':
                        pr['commits'] = 251
                    else:
                        reviews[0]['submitted_at'] = '2026-10-04T00:00:00Z'
                    return pr, commits, reviews
                self.f.github = response
                with self.assertRaises(Block):
                    self.f.review(STORY, record)
        self.f.github = self.x.mock_github
        with self.assertRaisesRegex(Block, 'wrong repository'):
            self.f.review(STORY, dict(record, repository='MOCK/fork'))
        with self.assertRaisesRegex(Block, 'predates server submission'):
            self.f.review(STORY, dict(record, timestamp='2026-10-02T00:00:00Z'))

    def test_TS13_MOCK_case_insensitive_logins_and_pending(self):
        self.x.all_gates()
        record = next(r for r in self.f.records(STORY) if r['gate'] == 'Code Review')
        def mixed_case(r):
            pr, commits, reviews = self.x.mock_github(r)
            reviews[0]['user']['login'] = 'mock_REVIEWER'
            reviews.append({'id': 2, 'state': 'PENDING', 'user': {'login': 'MOCK_other'}})
            reviews.append(dict(reviews[0], id=3, state='COMMENTED', user={'login': 'MOCK_REVIEWER'}, submitted_at='2026-10-03T00:00:01Z'))
            return pr, commits, reviews
        self.f.github = mixed_case
        self.f.review(STORY, dict(record, producer_identity='MOCK_REVIEWER'))
        for field in ('PR author', 'author', 'committer'):
            with self.subTest(field=field):
                def collision(r):
                    pr, commits, reviews = mixed_case(r)
                    if field == 'PR author':
                        pr['user']['login'] = 'MOCK_REVIEWER'
                    else:
                        commits[0][field]['login'] = 'MOCK_REVIEWER'
                    return pr, commits, reviews
                self.f.github = collision
                with self.assertRaisesRegex(Block, 'self-approval'):
                    self.f.review(STORY, record)
        def dismissed(r):
            pr, commits, reviews = mixed_case(r)
            reviews.append(dict(reviews[0], id=4, state='DISMISSED', user={'login': 'MOCK_REVIEWER'}, submitted_at='2026-10-03T00:00:02Z'))
            return pr, commits, reviews
        self.f.github = dismissed
        with self.assertRaisesRegex(Block, 'not verified APPROVED'):
            self.f.review(STORY, record)
        self.f.github = mixed_case
        state_path = self.x.root / f'factory/state/{STORY}.json'
        state = json.loads(state_path.read_text())
        state['implementing_identity'] = 'MOCK_REVIEWER'
        state_path.write_text(json.dumps(state))
        self.x.commit()
        with self.assertRaisesRegex(Block, 'self-approval'):
            self.f.review(STORY, record)

    def test_TS13_MOCK_unlisted_collaborator_matching_identity(self):
        self.x.all_gates()
        record = next(r for r in self.f.records(STORY) if r['gate'] == 'Code Review')
        record['producer_identity'] = 'MOCK_unlisted_collaborator'
        def response(r):
            pr, commits, reviews = self.x.mock_github(r)
            reviews[0]['user']['login'] = record['producer_identity']
            self.assertEqual(reviews[0]['author_association'], 'COLLABORATOR')
            return pr, commits, reviews
        self.f.github = response
        with self.assertRaisesRegex(Block, '^review unapproved reviewer$'):
            self.f.review(STORY, record)
        # Mutation proof in a disposable scratch copy only: every other check
        # passes, so deleting the allow-list check defeats the assertion above.
        source = Path(__file__).resolve().parents[1] / 'engine.py'
        original = source.read_text()
        check = "        require(login in {x.casefold() for x in policy['approved_reviewers']}, 'review unapproved reviewer')\n"
        self.assertEqual(original.count(check), 1)
        scratch = self.x.root / 'MOCK-mutant-engine.py'
        scratch.write_text(original.replace(check, ''))
        spec = importlib.util.spec_from_file_location('MOCK_mutant_engine', scratch)
        mutant = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mutant)
        mutant.Factory(self.x.root, github=response).review(STORY, record)

    def test_TS21_MOCK_in_progress_status_and_next_transition(self):
        self.x.s['status'] = 'IN_PROGRESS'
        self.x.save()
        self.assertEqual(jenkins(self.f, f'feature/{STORY}-devops'), [])
        self.assertTrue(self.f.transition(STORY, 'IN_PROGRESS', 'DEV_COMPLETE'))
        for gate in ('build', 'lint', 'Unit Test'):
            self.x.record(gate)
        self.assertEqual(jenkins(self.f, f'feature/{STORY}-devops'), [])
        self.assertEqual(self.f.transition(STORY, 'IN_PROGRESS', 'DEV_COMPLETE'), [])
        self.x.s['definition_of_ready']['architecture_reviewed'] = False
        self.x.save()
        self.assertIn('DoR architecture_reviewed must be boolean true', jenkins(self.f, f'feature/{STORY}-devops'))

    def test_TS16_MOCK_transition_preserves_complete_yaml(self):
        path = self.x.root / f'safe/stories/{STORY}.yaml'
        original = '# PO decisions A–F\n# AD-02\n# C1–C3\n' + path.read_text().replace('status: READY\n', 'status: READY        # admission note\n') + '# Keep this block LAST\n'
        path.write_text(original)
        self.x.commit()
        args = Namespace(story=STORY, action='transition', source='READY', target='IN_PROGRESS', reason=None, role=None, identity=None)
        orchestrate(self.f, args)
        expected = original.replace('status: READY        # admission note', 'status: IN_PROGRESS        # admission note')
        self.assertEqual(path.read_text(), expected)
        self.assertEqual(yaml.safe_load(expected), dict(self.x.s, status='IN_PROGRESS'))

    def test_TS16_MOCK_old_revision_refused_without_writes(self):
        old = self.x.git('rev-parse', 'HEAD').decode().strip()
        (self.x.root / 'app.txt').write_text('MOCK newer implementation')
        self.x.commit()
        previous = Factory(self.x.root, old)
        before = {p: p.read_bytes() for p in self.x.root.rglob('*') if p.is_file() and '.git' not in p.parts}
        args = Namespace(story=STORY, action='transition', source='READY', target='IN_PROGRESS', reason=None, role=None, identity=None)
        with self.assertRaisesRegex(Block, 'revision must equal HEAD'):
            orchestrate(previous, args)
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_TS16_MOCK_uncommitted_state_refused_without_writes(self):
        state = self.x.root / f'factory/state/{STORY}.json'
        value = json.loads(state.read_text())
        value['implementing_identity'] = 'MOCK_uncommitted_claim'
        state.write_text(json.dumps(value))
        before = {p: p.read_bytes() for p in self.x.root.rglob('*') if p.is_file() and '.git' not in p.parts}
        args = Namespace(story=STORY, action='transition', source='READY', target='IN_PROGRESS', reason=None, role=None, identity=None)
        with self.assertRaisesRegex(Block, 'uncommitted state changes'):
            orchestrate(self.f, args)
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_TS14_MOCK_na_ineligible_not_permitted_and_failed(self):
        self.x.all_gates()
        record = next(r for r in self.f.records(STORY) if r['gate'] == 'Integration Test')
        record.update(result='N/A', po_approval={'identity': 'MOCK_PO', 'date': '2026-10-03'}, reason='MOCK no integration target', decision_reference=record['artifacts'][0], execution_status='NOT_APPLICABLE')
        with self.assertRaisesRegex(Block, 'N/A not permitted'):
            self.f.record(STORY, 'Integration Test', record)
        self.x.s['na_permitted'] = ['Integration Test', 'Tester']
        self.x.save()
        self.assertEqual(self.f.record(STORY, 'Integration Test', record), 'N/A-APPROVED')
        tester = next(r for r in self.f.records(STORY) if r['gate'] == 'Tester')
        tester.update({k: v for k, v in record.items() if k in ('result', 'po_approval', 'reason', 'decision_reference', 'execution_status')})
        with self.assertRaisesRegex(Block, 'N/A not permitted'):
            self.f.record(STORY, 'Tester', tester)
        for status in ('FAIL', 'MISSING_TOOL', 'MISSING_CONFIGURATION'):
            with self.assertRaisesRegex(Block, 'failed or missing execution'):
                self.f.record(STORY, 'Integration Test', dict(record, execution_status=status))

    def test_TS26_MOCK_factory_003_contract_forbids_na(self):
        # Sanitized fixture of 003's mandatory Integration contract, no real safe/ read.
        self.x.all_gates()
        story = 'US-FACTORY-003'
        fixture = copy.deepcopy(self.x.s)
        fixture.update(id=story, na_permitted=[])
        (self.x.root / f'safe/stories/{story}.yaml').write_text(yaml.safe_dump(fixture))
        (self.x.root / f'factory/state/{story}.json').write_text((self.x.root / f'factory/state/{STORY}.json').read_text())
        self.x.commit()
        record = next(r for r in self.f.records(STORY) if r['gate'] == 'Integration Test')
        self.assertTrue(self.f.ancestor(record['source_commit'], record['_introduced'], strict=True))
        self.assertEqual(self.f.record(STORY, 'Integration Test', record), 'PASS')
        # This is a new candidate for another fixture Story, not a rewrite of
        # the loaded record. Its later source snapshot needs its own later
        # introduction; reserved metadata must be derived from that Git path.
        record = {k: v for k, v in record.items() if not k.startswith('_')}
        record.update(story_id=story, result='N/A', source_commit=self.x.git('rev-parse', 'HEAD').decode().strip(), acceptance_contract_fingerprint=self.f.contract(story), execution_status='NOT_APPLICABLE', po_approval={'identity': 'MOCK_PO', 'date': '2026-10-03'}, reason='MOCK attempted waiver', decision_reference=record['artifacts'][0])
        directory = self.x.root / f'factory/evidence/{story}'
        directory.mkdir()
        (directory / 'MOCK-na-candidate.json').write_text(json.dumps(record))
        self.x.commit()
        record = self.f.records(story)[0]
        self.assertTrue(self.f.ancestor(record['source_commit'], record['_introduced'], strict=True))
        with self.assertRaisesRegex(Block, 'N/A not permitted'):
            self.f.record(story, 'Integration Test', record)
        fixture['na_permitted'] = ['Integration Test']
        (self.x.root / f'safe/stories/{story}.yaml').write_text(yaml.safe_dump(fixture))
        self.x.commit()
        with self.assertRaisesRegex(Block, 'N/A not permitted'):
            self.f.record(story, 'Integration Test', record)

    def test_TS11_MOCK_hash_object_linear_history_provenance_passes(self):
        self.x.all_gates()
        graph = self.x.git('rev-list', '--parents', 'HEAD').decode().splitlines()
        self.assertTrue(all(len(line.split()) <= 2 for line in graph))
        for record in self.f.records(STORY):
            self.assertTrue(self.f.ancestor(record['source_commit'], record['_introduced'], strict=True))
            self.assertEqual(self.f.record(STORY, record['gate'], record), 'PASS')
            self.assertEqual(self.f.gate(STORY, record['gate']), ('PASS', []))

    def test_TS13_MOCK_adapter_rejects_github_commit_cap(self):
        from remotes import GitHub
        class MockGitHub(GitHub):
            def get(self, path):
                return {'commits': 251}

            def pages(self, path):
                return [{}] * 250
        with self.assertRaisesRegex(Block, 'incomplete commit list'):
            MockGitHub('MOCK credential')({'repository': 'sonld1505/AI_Tutor', 'pull_request': 1})

    def test_TS07_MOCK_history_artifacts_use_execution_revision(self):
        self.x.all_gates()
        history = {p: p.read_bytes() for p in (self.x.root / f'factory/evidence/{STORY}').glob('*.json')}
        (self.x.root / f'factory/evidence/{STORY}/summary.md').write_text('MOCK updated supporting summary')
        self.x.commit()
        self.x.all_gates()
        self.x.s['status'] = 'DEV_COMPLETE'
        self.x.save()
        self.assertEqual(jenkins(self.f, f'feature/{STORY}-devops'), [])
        self.assertEqual(history, {p: p.read_bytes() for p in history})

    def test_TS13_MOCK_tester_and_qa_require_independent_identity(self):
        self.x.all_gates()
        for gate in ('Tester', 'QA'):
            record = next(r for r in self.f.records(STORY) if r['gate'] == gate)
            with self.assertRaisesRegex(Block, 'independent identity'):
                self.f.record(STORY, gate, dict(record, producer_identity='mock_IMPLEMENTER'))

    def test_TS22_MOCK_empty_dor_and_dod_templates_block(self):
        for name, key in (('ready', 'definition_of_ready'), ('done', 'definition_of_done')):
            path = self.x.root / f'safe/templates/definition-of-{name}.yaml'
            old = path.read_bytes()
            path.write_text(f'{key}: {{}}\n')
            self.x.commit()
            if name == 'ready':
                with self.assertRaisesRegex(Block, 'empty DoR template'):
                    self.f.dor(self.x.s)
            else:
                self.assertEqual(self.f.preconditions(STORY, ['DoD']), ['DoD: INVALID empty DoD template'])
            path.write_bytes(old)
            self.x.commit()

    def test_TS08_MOCK_contract_rerun_order_only_invalid_gates(self):
        self.x.all_gates()
        self.x.s['description'] += ' MOCK contract change'
        self.x.save()
        self.assertEqual(self.f.rerun_order(STORY), ['Tester', 'QA'])

    def test_TS23_MOCK_container_exit_status_propagates_all_subcommands(self):
        source = Path(__file__).resolve().parents[2]
        scripts = self.x.root / 'scripts'
        scripts.mkdir()
        runtime = self.x.root / 'factory/runtime'
        runtime.mkdir()
        helper = scripts / 'factory-runtime.sh'
        shutil.copyfile(source / 'scripts/factory-runtime.sh', helper)
        shutil.copyfile(source / 'factory/runtime/contract.env', runtime / 'contract.env')
        # Only exit propagation is mocked here; TS27 retains real Docker probes.
        (scripts / 'factory-runtime-test.sh').write_text('set -eu\nprintf "{}\\n" > "$2/report.json"\nprintf "%s" "$2" > "$FACTORY_MOCK_REPORT_DIRECTORY"\n')
        bins = self.x.root / 'MOCK-bin'
        bins.mkdir()
        docker = bins / 'docker'
        docker.write_text('#!/bin/bash\nif [[ "$1" == image ]]; then exit 0; fi\n[[ "$1" == run ]] || exit 99\nfor value in "$@"; do\n if [[ "$value" == TMPDIR=* ]]; then printf "%s" "${value#TMPDIR=}" > "$FACTORY_MOCK_INTEGRATION_DIRECTORY"; fi\ndone\nexit "$FACTORY_MOCK_CONTAINER_EXIT"\n')
        docker.chmod(0o755)
        report = self.x.root / 'MOCK-report-directory.txt'
        integration = self.x.root / 'MOCK-integration-directory.txt'
        environment = dict(os.environ, PATH=str(bins) + ':' + os.environ['PATH'], FACTORY_CANONICAL_REENTRY='', FACTORY_MOCK_REPORT_DIRECTORY=str(report), FACTORY_MOCK_INTEGRATION_DIRECTORY=str(integration))
        commands = ('build', 'lint', 'unit', 'integration', 'dor', 'status', 'validate-gate', 'can-transition', 'can-dispatch', 'orchestrate', 'write-evidence', 'jenkins')
        for command in commands:
            for status in (0, 1, 37, 127):
                with self.subTest(command=command, status=status):
                    environment['FACTORY_MOCK_CONTAINER_EXIT'] = str(status)
                    arguments = ['--write', STORY, command] if command in ('orchestrate', 'write-evidence') else [command]
                    result = subprocess.run(['bash', str(helper), *arguments], cwd=self.x.root, env=environment, capture_output=True)
                    self.assertEqual(result.returncode, status, result.stdout + result.stderr)
                    if command == 'unit':
                        self.assertFalse(Path(report.read_text()).exists(), 'unit EXIT cleanup did not run')
                    if command == 'integration':
                        shutil.rmtree(integration.read_text())
        # Cleanup failure must not replace the container exit code either.
        cleanup = bins / 'rm'
        cleanup.write_text('#!/bin/bash\nexit 88\n')
        cleanup.chmod(0o755)
        environment['FACTORY_MOCK_CONTAINER_EXIT'] = '37'
        result = subprocess.run(['bash', str(helper), 'unit'], cwd=self.x.root, env=environment, capture_output=True)
        self.assertEqual(result.returncode, 37, result.stdout + result.stderr)
        shutil.rmtree(report.read_text())
