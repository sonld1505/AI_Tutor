"""Round 4 regression tests (MOCK remotes, disposable real-Git fixtures only)."""
import contextlib
import io
import subprocess
import sys
import unittest
from pathlib import Path

from cli import jenkins
from engine import Block, Factory, digest
from fixtures import STORY
from test_git_graph import GitGraphFixture

FEATURE = f'feature/{STORY}-devops'


class Round4(unittest.TestCase):
    def setUp(self):
        self.x = GitGraphFixture()
        self.base = self.x.git('rev-parse', 'HEAD').decode().strip()
        self.x.git('branch', '-m', FEATURE)
        print('REAL Git graph / MOCK remote round-4 ' + self.id())

    def tearDown(self):
        self.x.close()

    def status(self, status, **extra):
        self.x.s['status'] = status
        self.x.s.update(extra)
        return self.x.save()

    def develop(self, implementation):
        self.x.git('checkout', '-q', '-b', 'develop', self.base)
        name = 'other_story_code.txt' if implementation else 'docs/unrelated.md'
        (self.x.root / 'docs').mkdir(exist_ok=True)
        (self.x.root / name).write_text('MOCK change from another Story')
        self.x.commit()

    def merge_feature(self):
        self.x.git('merge', '-q', '--no-ff', FEATURE, '-m', 'MOCK Merge pull request')
        self.x.refresh()

    def cli(self, branch, expected):
        cli = Path(__file__).resolve().parents[1] / 'cli.py'
        r = subprocess.run([sys.executable, str(cli), 'jenkins', '--root', str(self.x.root), '--branch', branch], capture_output=True, text=True)
        self.assertEqual(r.returncode, expected, r.stdout + r.stderr)
        return r.stdout

    def notices(self, branch):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            errors = jenkins(self.x.f, branch)
        return errors, out.getvalue()

    def done_feature(self):
        self.x.all_gates()
        self.status('QA')
        self.assertEqual(self.x.f.transition(STORY, 'QA', 'DONE'), [])
        self.status('DONE')

    # R3-02 (defect): fails at 233b1e9 with STALE_IMPLEMENTATION errors.
    def test_TS21_MOCK_develop_done_survives_later_implementation(self):
        self.done_feature()
        self.assertEqual(jenkins(self.x.f, FEATURE), [])
        self.develop(implementation=True)
        self.merge_feature()
        self.assertEqual(jenkins(self.x.f, 'develop'), [])
        (self.x.root / 'later_story_code.txt').write_text('MOCK later Story')
        self.x.commit()
        self.assertEqual(jenkins(self.x.f, 'develop'), [])
        self.assertEqual(self.x.f.gate(STORY, 'Validation')[0], 'STALE_IMPLEMENTATION')  # status report stays truthful

    # R3-02 (defect): AC06 must hold AT the completion snapshot; 233b1e9 passes on develop.
    def test_TS21_MOCK_done_without_ac06_at_completion_fails(self):
        for gate in ('build', 'lint', 'Unit Test', 'Validation'):
            self.x.record(gate)
        self.status('QA')
        self.status('DONE')
        self.x.record('Jenkins')  # evidence completed only after DONE
        errors = jenkins(self.x.f, FEATURE)
        self.assertTrue(any(e.startswith('DONE completion snapshot ') and 'Jenkins: MISSING' in e for e in errors), errors)
        self.develop(implementation=False)
        self.merge_feature()
        self.assertTrue(any(e.startswith('DONE completion snapshot ') for e in jenkins(self.x.f, 'develop')))
        self.assertIn('DONE completion snapshot', self.cli('develop', 1))

    def test_TS21_MOCK_done_not_entered_from_qa_fails(self):
        self.x.all_gates()
        self.status('DONE')  # READY -> DONE by hand
        self.assertIn('INVALID DONE completion snapshot: not entered from QA (AC04)', jenkins(self.x.f, FEATURE))
        self.assertIn('INVALID DONE completion snapshot: not entered from QA (AC04)', jenkins(self.x.f, 'develop'))

    def test_TS21_MOCK_done_removed_or_ambiguous_fails(self):
        self.done_feature()
        self.status('QA')
        self.status('DONE')
        self.assertTrue(any('DONE removed in history' in e for e in jenkins(self.x.f, 'develop')))
        # Two independent introductions on two branches, then merged.
        self.x.close()
        self.setUp()
        self.x.all_gates()
        qa = self.status('QA')
        self.status('DONE')
        self.x.git('checkout', '-q', '-b', 'second', qa)
        (self.x.root / 'docs').mkdir(exist_ok=True)
        (self.x.root / 'docs/second.md').write_text('MOCK second branch')
        self.x.commit()
        self.status('DONE')
        self.x.git('checkout', '-q', FEATURE)
        self.x.git('merge', '-q', '--no-ff', 'second', '-m', 'MOCK merge second DONE')
        self.x.refresh()
        self.assertTrue(any('ambiguous (2 introductions)' in e for e in jenkins(self.x.f, 'develop')))

    def test_TS21_MOCK_done_introduced_by_merge_fails(self):
        self.x.all_gates()
        self.status('QA')
        self.develop(implementation=False)
        self.x.git('checkout', '-q', FEATURE)
        self.x.git('merge', '-q', '--no-ff', '--no-commit', 'develop')
        self.status('DONE')  # commits the merge with DONE introduced in it
        self.assertEqual(len(self.x.git('rev-list', '--parents', '-1', 'HEAD').split()), 3)
        self.assertTrue(any('merge or root introduction' in e for e in jenkins(self.x.f, 'develop')))

    def test_TS21_MOCK_done_squash_merge_names_policy(self):
        self.done_feature()
        tip = self.x.git('rev-parse', 'HEAD').decode().strip()
        self.develop(implementation=False)
        self.x.git('merge', '--squash', tip)
        self.x.commit()
        self.assertIn('merge-commit-only policy', self.cli('develop', 1))

    # R3-01 (defect): fails at 233b1e9 with 'INVALID Tester/QA: out-of-order historical record'.
    def test_TS11_MOCK_documented_out_of_order_recovery_reaches_done(self):
        self.status('QA')
        for gate in ('build', 'lint', 'Unit Test', 'Jenkins', 'Code Review', 'Integration Test'):
            self.x.record(gate)
        stale = {p: p.read_bytes() for p in (self.x.root / f'factory/evidence/{STORY}').glob('*.json')}
        self.assertEqual(self.x.f.transition(STORY, 'QA', 'TESTING', 'DoD FAIL: MOCK review before validation'), [])
        self.status('TESTING')
        errors, out = self.notices(FEATURE)
        self.assertEqual(errors, [])
        self.assertIn('HISTORY Code Review: out-of-order record', out)
        self.x.record('Validation')
        self.assertEqual(self.x.f.transition(STORY, 'TESTING', 'QA'), [])
        self.status('QA')
        self.assertEqual(self.notices(FEATURE)[0], [])
        for gate in ('Code Review', 'Integration Test'):
            self.x.record(gate)
            self.assertEqual(self.notices(FEATURE)[0], [])
        self.assertEqual(self.x.f.transition(STORY, 'QA', 'DONE'), [])
        self.status('DONE')
        self.assertEqual(self.notices(FEATURE)[0], [])
        self.assertEqual({p: p.read_bytes() for p in stale}, stale)
        self.develop(implementation=True)
        self.merge_feature()
        self.assertEqual(jenkins(self.x.f, 'develop'), [])

    def test_TS11_MOCK_required_out_of_order_latest_still_fails(self):
        for gate in ('build', 'lint', 'Validation', 'Unit Test'):
            self.x.record(gate)
        self.status('QA')
        self.assertTrue(any(e.startswith('Validation: INVALID') and 'out-of-order record' in e for e in jenkins(self.x.f, FEATURE)))

    # R3-03 (defect): fails at 233b1e9 with 'PASS WITH BLOCKERS result not PASS' on develop.
    def test_TS21_MOCK_superseded_nonpass_history_same_in_both_modes(self):
        for gate in ('build', 'lint', 'Unit Test'):
            self.x.record(gate)
        self.x.record('Validation', result='PASS WITH BLOCKERS', checks={'MOCK': 'PARTIAL'})
        self.x.record('Validation', result='PARTIAL', checks={'MOCK': 'PARTIAL'})
        for gate in ('Validation', 'Jenkins', 'Code Review', 'Integration Test'):
            self.x.record(gate)
        self.status('QA')
        self.status('DONE')
        self.assertEqual(jenkins(self.x.f, FEATURE), [])
        self.develop(implementation=False)
        self.merge_feature()
        self.assertEqual(jenkins(self.x.f, 'develop'), [])
        self.x.record('Validation', result='MAYBE', checks={'MOCK': 'MAYBE'})
        self.assertIn('MAYBE result not PASS', jenkins(self.x.f, 'develop'))

    # R3-04 guards (pass at 233b1e9; each kills one surviving mutant).
    def test_TS11_MOCK_real_git_evil_merge_record_introduction_invalid(self):
        for gate in ('build', 'lint', 'Unit Test'):
            self.x.record(gate)
        self.develop(implementation=False)
        self.x.git('checkout', '-q', FEATURE)
        self.x.git('merge', '-q', '--no-ff', '--no-commit', 'develop')
        self.x.record('Code Review')  # new record introduced only by the merge commit
        self.assertEqual(len(self.x.git('rev-list', '--parents', '-1', 'HEAD').split()), 3)
        with self.assertRaisesRegex(Block, 'ambiguous merge introduction'):
            self.x.f.records(STORY)

    def test_TS11_MOCK_real_git_history_record_provenance_invalid(self):
        self.status('IN_PROGRESS')
        for gate in ('build', 'lint', 'Unit Test'):
            self.x.record(gate)
        here = self.x.git('rev-parse', 'HEAD').decode().strip()
        self.x.git('checkout', '-q', '-b', 'side')
        (self.x.root / 'docs').mkdir(exist_ok=True)
        (self.x.root / 'docs/side.md').write_text('MOCK side')
        side = self.x.commit()
        self.x.git('checkout', '-q', FEATURE)
        self.x.refresh()
        self.assertEqual(self.x.git('rev-parse', 'HEAD').decode().strip(), here)
        self.x.record('Validation', source_commit=side)  # not an ancestor of its introduction
        self.assertTrue(any('execution snapshot provenance' in e for e in jenkins(self.x.f, FEATURE)))

    def test_TS11_MOCK_real_git_history_stale_prerequisite_is_reported(self):
        self.status('IN_PROGRESS')
        for gate in ('build', 'lint', 'Unit Test', 'Validation', 'Jenkins', 'Code Review', 'Integration Test'):
            self.x.record(gate)
        (self.x.root / 'app.txt').write_text('MOCK implementation after Integration')
        self.x.commit()
        self.x.record('Validation')
        out = self.cli(FEATURE, 0)
        self.assertIn('HISTORY Validation: out-of-order record', out)

    # R2-05a (defect): 233b1e9 accepts blocked_from DONE and BLOCKED->DONE.
    def test_TS15_MOCK_blocked_from_must_precede_done(self):
        for gate in ('build', 'lint', 'Unit Test'):
            self.x.record(gate)
        self.status('BLOCKED', blocked_from='DONE', blocked_by=['MOCK-R1'])
        self.assertIn('INVALID blocked_from must be a state before DONE', jenkins(self.x.f, FEATURE))
        with self.assertRaisesRegex(Block, 'blocked_from must be a state before DONE'):
            self.x.f.transition(STORY, 'BLOCKED', 'DONE')
        self.status('BLOCKED', blocked_from='BLOCKED')
        with self.assertRaises(Block):
            self.x.f.transition(STORY, 'BLOCKED', 'BLOCKED')
        self.status('BLOCKED', blocked_from='READY', blocked_by=[])
        self.assertEqual(jenkins(self.x.f, FEATURE), [])  # cleared blocker awaiting return stays green
        self.assertEqual(self.x.f.transition(STORY, 'BLOCKED', 'READY'), [])

    def test_TS13_MOCK_integrity_invalid_superseded_record_still_fails(self):
        self.status('IN_PROGRESS')
        self.x.review_ready()
        self.x.record('Validation', producer_role='CODEX_DEVOPS')
        self.x.record('Validation')
        self.assertIn('wrong producer', jenkins(self.x.f, FEATURE))


class Lean(unittest.TestCase):
    def setUp(self):
        self.x = GitGraphFixture()
        self.base = self.x.git('rev-parse', 'HEAD').decode().strip()
        self.x.git('branch', '-m', FEATURE)
        print('REAL Git graph / MOCK remote lean ' + self.id())

    def tearDown(self):
        self.x.close()

    def status(self, status):
        self.x.s['status'] = status
        return self.x.save()

    def offline(self):
        return Factory(self.x.root, github=None, archive=None)

    def test_TS01_MOCK_lean_flow_to_done_and_develop(self):
        def f():
            return self.x.f
        self.status('IN_PROGRESS')
        for g in ('build', 'lint', 'Unit Test'):
            self.x.record(g)
        self.assertEqual(f().transition(STORY, 'IN_PROGRESS', 'DEV_COMPLETE'), [])
        self.status('DEV_COMPLETE')
        self.assertEqual(f().transition(STORY, 'DEV_COMPLETE', 'TESTING'), [])
        self.status('TESTING')
        self.assertEqual(f().dispatch(STORY, 'CODEX_QA'), [])
        self.assertTrue(f().transition(STORY, 'TESTING', 'QA'))  # Validation MISSING
        with self.assertRaises(Block):
            f().dispatch(STORY, 'CODEX_TESTER')  # Tester gate retired
        self.x.record('Validation')
        self.assertEqual(f().transition(STORY, 'TESTING', 'QA'), [])
        self.status('QA')
        self.assertTrue(any('Jenkins: MISSING' in e for e in f().dispatch(STORY, 'Code Review')))
        self.assertEqual(jenkins(f(), FEATURE), [])
        self.x.record('Jenkins', artifacts=[{'system': 'jenkins', 'job': 'MOCK-job', 'build': 1, 'path': 'MOCK-report.txt', 'sha256': digest(b'MOCK archive')}])
        self.assertEqual(f().dispatch(STORY, 'Code Review'), [])
        self.assertTrue(any('Code Review: MISSING' in e for e in f().dispatch(STORY, 'Integration Test')))
        self.x.record('Code Review')
        self.assertEqual(f().dispatch(STORY, 'Integration Test'), [])
        self.assertTrue(f().transition(STORY, 'QA', 'DONE'))  # Integration MISSING
        self.x.record('Integration Test')
        self.assertEqual(f().transition(STORY, 'QA', 'DONE'), [])
        self.status('DONE')
        self.assertEqual(jenkins(f(), FEATURE), [])
        with self.assertRaisesRegex(Block, 'NOT_EXECUTED Jenkins archive verification unavailable'):
            jenkins(self.offline(), FEATURE)  # feature always verifies
        # develop: another Story's implementation first, then merge, then a later implementation.
        self.x.git('checkout', '-q', '-b', 'develop', self.base)
        (self.x.root / 'other_story_code.txt').write_text('MOCK other Story')
        self.x.commit()
        self.x.git('merge', '-q', '--no-ff', FEATURE, '-m', 'MOCK Merge pull request')
        self.x.refresh()
        self.assertEqual(jenkins(f(), 'develop'), [])
        with self.assertRaisesRegex(Block, 'NOT_EXECUTED Jenkins archive verification unavailable'):
            jenkins(self.offline(), 'develop')  # arrival verifies
        (self.x.root / 'later_story_code.txt').write_text('MOCK later Story')
        self.x.commit()
        self.assertEqual(jenkins(self.offline(), 'develop'), [])  # integrated earlier: no remote re-verification
        self.assertEqual(f().gate(STORY, 'Validation')[0], 'STALE_IMPLEMENTATION')

    def test_TS13_MOCK_validation_independence_and_verdict(self):
        for g in ('build', 'lint', 'Unit Test'):
            self.x.record(g)
        self.x.record('Validation', findings={'critical': 0, 'major': 1})
        self.assertIn('Critical and Major', ' '.join(self.x.f.gate(STORY, 'Validation')[1]))
        self.x.record('Validation', findings={'critical': 0, 'major': True})
        self.assertIn('Critical and Major', ' '.join(self.x.f.gate(STORY, 'Validation')[1]))
        self.x.record('Validation', producer_identity='MOCK_implementer')
        self.assertIn('independent identity', ' '.join(self.x.f.gate(STORY, 'Validation')[1]))
        self.x.record('Validation', producer_role='CODEX_TESTER')
        self.assertIn('wrong producer', ' '.join(self.x.f.gate(STORY, 'Validation')[1]))
        self.x.record('Validation', ac_results={})
        self.assertIn('per-AC', ' '.join(self.x.f.gate(STORY, 'Validation')[1]))
        self.x.record('Validation')
        self.assertEqual(self.x.f.gate(STORY, 'Validation'), ('PASS', []))
