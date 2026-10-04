"""Real Git graphs with MOCK remote responses; disposable repositories only."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from cli import jenkins
from engine import Block, Factory
from fixtures import STORY, Fixture


class GitGraphFixture(Fixture):
    """Use porcelain commits and merges, with per-command identity, no config."""
    def git(self, *args, data=None):
        environment = dict(os.environ, GIT_AUTHOR_NAME='MOCK Fixture',
                           GIT_AUTHOR_EMAIL='mock@example.invalid',
                           GIT_COMMITTER_NAME='MOCK Fixture',
                           GIT_COMMITTER_EMAIL='mock@example.invalid',
                           GIT_EDITOR='true', GIT_MERGE_AUTOEDIT='no')
        return subprocess.run(['git', '-C', str(self.root), *args], input=data,
                              env=environment, capture_output=True, check=True).stdout

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-q', '--allow-empty', '-m', 'MOCK real Git fixture commit')
        return self.refresh()

    def refresh(self):
        sha = self.git('rev-parse', 'HEAD').decode().strip()
        if hasattr(self, 'f'):
            self.f = Factory(self.root, github=self.mock_github, archive=self.mock_archive)
        return sha


class GitGraphTests(unittest.TestCase):
    def setUp(self):
        self.x = GitGraphFixture()
        self.base = self.x.git('rev-parse', 'HEAD').decode().strip()
        self.x.git('branch', '-m', f'feature/{STORY}-devops')
        print('REAL Git graph / MOCK remote regression ' + self.id())

    def tearDown(self):
        self.x.close()

    def status(self, status):
        self.x.s['status'] = status
        self.x.save()

    def unit_gates(self):
        for gate in ('build', 'lint', 'Unit Test'):
            self.x.record(gate)

    def advance_develop(self):
        self.x.git('checkout', '-q', '-b', 'develop', self.base)
        (self.x.root / 'docs').mkdir(exist_ok=True)
        (self.x.root / 'docs/unrelated.md').write_text('MOCK unrelated develop change')
        self.x.commit()

    def cli_jenkins(self, expected):
        cli = Path(__file__).resolve().parents[1] / 'cli.py'
        result = subprocess.run([sys.executable, str(cli), 'jenkins', '--root',
                                 str(self.x.root), '--branch', f'feature/{STORY}-devops'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def test_TS12_MOCK_real_git_merge_develop_preserves_introduction(self):
        self.x.all_gates()
        self.status('DEV_COMPLETE')
        before = self.x.f.records(STORY)
        fingerprint = self.x.f.implementation()
        self.advance_develop()
        self.x.git('checkout', '-q', f'feature/{STORY}-devops')
        self.x.git('merge', '-q', '--no-ff', 'develop', '-m', 'MOCK merge develop into feature')
        self.x.refresh()
        self.assertEqual(len(self.x.git('rev-list', '--parents', '-1', 'HEAD').split()), 3)
        self.assertEqual(self.x.f.implementation(), fingerprint)
        self.assertEqual(self.x.f.records(STORY), before)
        for gate in self.x.f.workflow['gates']:
            self.assertEqual(self.x.f.gate(STORY, gate), ('PASS', []), gate)
        self.assertEqual(self.x.f.transition(STORY, 'DEV_COMPLETE', 'TESTING'), [])
        self.assertEqual(jenkins(self.x.f, f'feature/{STORY}-devops'), [])
        self.cli_jenkins(0)

    def test_TS21_MOCK_real_git_done_pr_merge_develop_passes(self):
        self.x.all_gates()
        self.status('QA')
        self.status('DONE')
        self.assertEqual(jenkins(self.x.f, 'develop'), [])
        before = self.x.f.records(STORY)
        self.advance_develop()
        self.x.git('merge', '-q', '--no-ff', f'feature/{STORY}-devops',
                   '-m', 'MOCK Merge pull request')
        self.x.refresh()
        self.assertEqual(len(self.x.git('rev-list', '--parents', '-1', 'HEAD').split()), 3)
        self.assertEqual(self.x.f.records(STORY), before)
        self.assertEqual(jenkins(self.x.f, 'develop'), [])

    def test_TS11_MOCK_real_git_merge_resolution_rewrites_record_invalid(self):
        self.x.review_ready()
        _, path = self.x.record('Code Review')
        original = path.read_bytes()
        relative = path.relative_to(self.x.root).as_posix()
        (self.x.root / 'docs').mkdir()
        conflict = self.x.root / 'docs/conflict.md'
        conflict.write_text('MOCK common document\n')
        self.x.commit()
        common = self.x.git('rev-parse', 'HEAD').decode().strip()
        self.x.git('checkout', '-q', '-b', 'other', common)
        conflict.write_text('MOCK other document\n')
        (self.x.root / 'docs/other.md').write_text('MOCK other side')
        self.x.commit()
        self.x.git('checkout', '-q', f'feature/{STORY}-devops')
        conflict.write_text('MOCK feature document\n')
        (self.x.root / 'docs/feature.md').write_text('MOCK feature side')
        self.x.commit()
        with self.assertRaises(subprocess.CalledProcessError) as failed_merge:
            self.x.git('merge', '--no-ff', '--no-commit', 'other')
        self.assertEqual(failed_merge.exception.returncode, 1)
        self.assertIn(b'CONFLICT', failed_merge.exception.stdout)
        self.assertEqual(self.x.git('diff', '--name-only', '--diff-filter=U').strip(), b'docs/conflict.md')
        self.assertEqual(path.read_bytes(), original)
        conflict.write_text('MOCK resolved document\n')
        record = json.loads(path.read_text())
        record['timestamp'] = '2099-01-01T00:00:00Z'
        path.write_text(json.dumps(record))
        self.x.commit()
        self.assertEqual(len(self.x.git('rev-list', '--parents', '-1', 'HEAD').split()), 3)
        for parent in ('HEAD^1', 'HEAD^2'):
            self.assertEqual(self.x.git('show', f'{parent}:{relative}'), original)
        self.assertNotEqual(self.x.git('show', f'HEAD:{relative}'), original)
        with self.assertRaisesRegex(Block, 'history rewritten'):
            self.x.f.records(STORY)
        self.assertIn('history rewritten', self.cli_jenkins(1))

    def test_TS11_MOCK_real_git_squash_cherry_pick_loses_provenance(self):
        self.unit_gates()
        self.status('DEV_COMPLETE')
        tip = self.x.git('rev-parse', 'HEAD').decode().strip()
        self.x.git('checkout', '-q', '-b', 'squashed', self.base)
        self.x.git('merge', '--squash', tip)
        self.x.commit()
        self.assertIn('merge-commit-only policy', self.cli_jenkins(1))
        self.assertTrue(self.x.f.preconditions(STORY, ['Unit Test']))
        # Cherry-picking all three record introductions onto an unrelated
        # documentation commit likewise preserves bytes but loses source ancestry.
        self.advance_develop()
        for commit in self.x.git('rev-list', '--reverse', f'{self.base}..{tip}').decode().splitlines():
            self.x.git('cherry-pick', commit)
        self.x.refresh()
        self.assertIn('merge-commit-only policy', self.cli_jenkins(1))

    def test_TS11_MOCK_real_git_rebase_loses_provenance(self):
        self.unit_gates()
        self.status('DEV_COMPLETE')
        self.advance_develop()
        self.x.git('checkout', '-q', f'feature/{STORY}-devops')
        self.x.git('rebase', '--onto', 'develop', self.base)
        self.x.refresh()
        self.assertIn('merge-commit-only policy', self.cli_jenkins(1))

    def test_TS11_MOCK_real_git_shallow_clone_fails_closed(self):
        self.unit_gates()
        self.status('DEV_COMPLETE')
        with tempfile.TemporaryDirectory(prefix='factory-MOCK-shallow-') as directory:
            clone = Path(directory) / 'clone'
            self.x.git('clone', '-q', '--depth=1', self.x.root.as_uri(), str(clone))
            factory = Factory(clone)
            with self.assertRaisesRegex(Block, 'merge-commit-only policy.*shallow'):
                factory.records(STORY)

    def test_TS07_MOCK_real_git_in_progress_stale_and_nonpass_history_passes(self):
        self.status('IN_PROGRESS')
        self.unit_gates()
        history = self.x.f.records(STORY)
        (self.x.root / 'app.txt').write_text('MOCK further implementation')
        self.x.commit()
        self.assertEqual(self.x.f.gate(STORY, 'Unit Test')[0], 'STALE_IMPLEMENTATION')
        self.assertEqual(self.x.f.records(STORY), history)
        self.assertEqual(jenkins(self.x.f, f'feature/{STORY}-devops'), [])
        self.cli_jenkins(0)
        for result in ('FAIL', 'UNKNOWN', 'NOT_EXECUTED', 'PARTIAL', 'PASS WITH BLOCKERS'):
            self.x.record('build', result=result, checks={'MOCK compilation': result})
            self.cli_jenkins(0)
        self.unit_gates()
        self.cli_jenkins(0)  # Superseded non-PASS record remains well-formed.

    def test_TS21_MOCK_real_git_recovery_stale_downstream_history_passes(self):
        self.x.all_gates()
        self.status('QA')
        self.assertEqual(self.x.f.transition(STORY, 'QA', 'IN_PROGRESS', 'QA FAIL: MOCK fix'), [])
        self.status('IN_PROGRESS')
        (self.x.root / 'app.txt').write_text('MOCK fix after QA')
        self.x.commit()
        self.unit_gates()
        self.assertEqual(self.x.f.transition(STORY, 'IN_PROGRESS', 'DEV_COMPLETE'), [])
        self.status('DEV_COMPLETE')
        for gate in ('Code Review', 'Integration Test', 'Validation', 'Jenkins'):
            self.assertEqual(self.x.f.gate(STORY, gate)[0], 'STALE_IMPLEMENTATION', gate)
        self.assertEqual(jenkins(self.x.f, f'feature/{STORY}-devops'), [])
        self.cli_jenkins(0)

    def test_TS21_MOCK_real_git_invalid_record_and_unsupported_status_fail(self):
        self.status('DEV_COMPLETE')
        self.assertIn('missing evidence', self.cli_jenkins(1))
        self.unit_gates()
        self.cli_jenkins(0)
        self.x.record('Validation', producer_role='CODEX_DEVOPS')
        self.assertEqual(jenkins(self.x.f, f'feature/{STORY}-devops'), ['wrong producer'])
        self.assertIn('wrong producer', self.cli_jenkins(1))

    def test_TS12_MOCK_real_git_stale_contract_history_is_valid(self):
        self.x.all_gates()
        self.status('DEV_COMPLETE')
        self.x.s['acceptance_criteria'].append({'id': 'AC02', 'description': 'MOCK new contract'})
        self.x.save()
        self.assertEqual(self.x.f.gate(STORY, 'Validation')[0], 'STALE_CONTRACT')
        self.assertEqual(jenkins(self.x.f, f'feature/{STORY}-devops'), [])
        self.cli_jenkins(0)

    def test_TS11_MOCK_real_git_optional_out_of_order_pass_is_history(self):
        self.status('IN_PROGRESS')
        for gate in ('build', 'lint'):
            self.x.record(gate)
        self.x.record('Validation', timestamp='2099-01-01T00:00:00Z')
        self.x.record('Unit Test')
        self.assertEqual(jenkins(self.x.f, f'feature/{STORY}-devops'), [])
        self.assertIn('HISTORY Validation: out-of-order record', self.cli_jenkins(0))
        self.status('TESTING')
        self.assertTrue(self.x.f.transition(STORY, 'TESTING', 'QA'))

    def test_TS11_MOCK_real_git_multiple_introductions_are_invalid(self):
        _, path = self.x.record('build')
        content = path.read_bytes()
        self.advance_develop()
        path.write_bytes(content)
        self.x.commit()
        self.x.git('merge', '-q', '--no-ff', f'feature/{STORY}-devops', '-m', 'MOCK duplicate introductions')
        self.x.refresh()
        with self.assertRaisesRegex(Block, 'ambiguous evidence introduction.*merge-commit-only policy'):
            self.x.f.records(STORY)

    def test_TS11_MOCK_real_git_rewrite_then_restore_is_invalid(self):
        _, path = self.x.record('build')
        content = path.read_bytes()
        path.write_bytes(content + b'\n')
        self.x.commit()
        path.write_bytes(content)
        self.x.commit()
        with self.assertRaisesRegex(Block, 'history rewritten'):
            self.x.f.records(STORY)
