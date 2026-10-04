"""Disposable MOCK fixtures; no real management records are accessed."""
import copy
import datetime
import json
import subprocess
import tempfile
from pathlib import Path

import yaml

from engine import Factory, digest

STORY = 'US-999'


class Fixture:
    def __init__(self):
        self.temp = tempfile.TemporaryDirectory(prefix='factory-MOCK-')
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        source = Path(__file__).resolve().parents[1]
        (self.root / 'factory').mkdir()
        workflow = yaml.safe_load((source / 'workflow.yaml').read_text())
        workflow['commands'][STORY] = dict(workflow['commands']['US-FACTORY-003'])
        workflow['github_review']['approved_reviewers'] = ['MOCK_reviewer']
        (self.root / 'factory/workflow.yaml').write_text(yaml.safe_dump(workflow, sort_keys=False))
        for p in ('safe/stories', 'safe/templates', 'factory/state', f'factory/evidence/{STORY}'):
            (self.root / p).mkdir(parents=True, exist_ok=True)
        self.s = {'id': STORY, 'title': 'MOCK Fixture', 'description': 'MOCK contract', 'status': 'READY', 'depends_on': [], 'blocked_by': [], 'blocked_from': None, 'acceptance_criteria': [{'id': 'AC01', 'description': 'MOCK acceptance'}], 'test_scenarios': [{'id': 'TS01', 'scenario': 'MOCK scenario'}], 'open_questions': [], 'definition_of_ready': {k: True for k in ('business_value_defined', 'story_defined', 'acceptance_criteria_defined', 'dependencies_identified', 'architecture_reviewed', 'test_scenarios_defined', 'estimation_completed')}, 'definition_of_done': {'implementation_complete': True, 'evidence': {}}, 'components': {'infrastructure': True}}
        (self.root / 'safe/templates/definition-of-ready.yaml').write_text(yaml.safe_dump({'definition_of_ready': self.s['definition_of_ready']}))
        (self.root / 'safe/templates/definition-of-done.yaml').write_text('definition_of_done:\n  implementation_complete: true\n')
        (self.root / 'safe/raid.yaml').write_text('issues: []\n')
        (self.root / f'factory/state/{STORY}.json').write_text(json.dumps({'implementing_identity': 'MOCK_implementer', 'implementing_role': 'CODEX_DEVOPS', 'status': 'READY'}))
        (self.root / 'app.txt').write_text('implementation')
        (self.root / f'factory/evidence/{STORY}/summary.md').write_text('MOCK structured summary of checks; not a raw log')
        self.s['definition_of_done']['evidence'] = {'implementation_complete': {'path': f'factory/evidence/{STORY}/summary.md', 'sha256': digest(b'MOCK structured summary of checks; not a raw log')}}
        self.serial = 0
        self.save()
        self.f = Factory(self.root, github=self.mock_github, archive=self.mock_archive)

    def git(self, *args, data=None):
        return subprocess.run(['git', '-C', str(self.root), *args], input=data, capture_output=True, check=True).stdout

    def commit(self):
        """Write fixture Git objects without configuring or setting any Git identity."""
        self.git('add', '.')  # Only this disposable fixture index.
        tree = self.git('write-tree').decode().strip()
        parent = self.git('rev-parse', '--verify', 'HEAD').decode().strip() if (self.root / '.git/refs/heads/master').exists() else None
        content = f'tree {tree}\n' + (f'parent {parent}\n' if parent else '')
        content += 'author MOCK Fixture <mock@example.invalid> 1 +0000\ncommitter MOCK Fixture <mock@example.invalid> 1 +0000\n\nMOCK fixture object\n'
        sha = self.git('hash-object', '-t', 'commit', '-w', '--stdin', data=content.encode()).decode().strip()
        self.git('update-ref', 'refs/heads/master', sha)
        if hasattr(self, 'f'):
            # Production Factory instances pin a revision. The disposable test
            # driver explicitly advances its evaluated snapshot after each write.
            self.f.revision = sha
        return sha

    def save(self):
        (self.root / f'safe/stories/{STORY}.yaml').write_text(yaml.safe_dump(self.s, sort_keys=False))
        return self.commit()

    def mock_github(self, record):
        """MOCK GitHub: never real review evidence."""
        return ({'user': {'login': 'MOCK_author'}, 'commits': 1, 'base': {'repo': {'full_name': 'sonld1505/AI_Tutor'}}, 'head': {'ref': f'feature/{STORY}-devops'}}, [{'author': {'login': 'MOCK_author'}, 'committer': {'login': 'MOCK_author'}}], [{'id': 1, 'state': 'APPROVED', 'user': {'login': 'MOCK_reviewer'}, 'author_association': 'COLLABORATOR', 'submitted_at': '2026-10-03T00:00:00Z', 'commit_id': record['source_commit']}])

    def mock_archive(self, artifact):
        """MOCK Jenkins archive: never Jenkins evidence."""
        return b'MOCK archive'

    def record(self, gate, **updates):
        self.serial += 1
        role = {'Code Review': 'GITHUB', 'Tester': 'CODEX_TESTER', 'QA': 'CODEX_QA', 'Jenkins': 'JENKINS'}.get(gate, 'CODEX_DEVOPS')
        identity = 'MOCK_reviewer' if gate == 'Code Review' else ('MOCK_implementer' if role == 'CODEX_DEVOPS' else 'MOCK_' + role)
        timestamp = (datetime.datetime(2026, 10, 3, tzinfo=datetime.UTC) + datetime.timedelta(seconds=self.serial)).isoformat().replace('+00:00', 'Z')
        artifact = f'factory/evidence/{STORY}/summary.md'
        r = {'story_id': STORY, 'gate': gate, 'result': 'PASS', 'producer_role': role, 'producer_identity': identity, 'timestamp': timestamp, 'source_commit': self.git('rev-parse', 'HEAD').decode().strip(), 'implementation_fingerprint': self.f.implementation(), 'acceptance_contract_fingerprint': self.f.contract(STORY), 'checks': {'MOCK check': 'PASS'}, 'artifacts': [{'path': artifact, 'sha256': digest(self.f.blob(artifact))}], 'review_id': 1, 'ac_results': {'AC01': 'PASS'}, 'ts_results': {'TS01': 'PASS'}}
        if gate == 'Jenkins':
            r['checks']['Factory Validation'] = 'PASS'
        if gate == 'Code Review':
            r.update(repository='sonld1505/AI_Tutor', pull_request=1, review_submitted_at='2026-10-03T00:00:00Z')
        if role == 'CODEX_DEVOPS':
            r['command'] = self.f.command(STORY, gate)
        r.update(updates)
        path = self.root / f'factory/evidence/{STORY}/{self.serial:03}.json'
        path.write_text(json.dumps(r))
        self.commit()
        return copy.deepcopy(r), path

    def all_gates(self):
        for gate in self.f.workflow['gates']:
            self.record(gate)

    def close(self):
        self.temp.cleanup()
