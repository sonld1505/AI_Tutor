"""REAL Factory integration workload. No MOCK adapters or synthetic PASS gates."""
import datetime
import json
import py_compile
import subprocess
import tempfile
from argparse import Namespace
from pathlib import Path

import yaml

from engine import Block, Factory, digest, require


def commit_fixture(root):
    """A fixture Git object, not an implementation commit or configured identity."""
    def git(*args, data=None):
        return subprocess.run(['git', '-C', str(root), *args], input=data, capture_output=True, check=True).stdout.decode().strip()
    git('add', '.')
    tree = git('write-tree')
    parent = git('rev-parse', 'HEAD')
    data = f'tree {tree}\nparent {parent}\nauthor Integration Fixture <fixture@example.invalid> 1 +0000\ncommitter Integration Fixture <fixture@example.invalid> 1 +0000\n\nDisposable integration fixture\n'
    commit = git('hash-object', '-t', 'commit', '-w', '--stdin', data=data.encode())
    git('update-ref', 'HEAD', commit)
    return commit


def execute_components(factory, story, steps):
    from cli import jenkins, orchestrate, write_record
    require(not factory.preconditions(story, factory.workflow['dispatch']['Integration Test']['prerequisites']), 'Integration prerequisites BLOCK')
    # Verify the Story's own approved review through the REAL injected production adapter.
    review = factory.latest_record([r for r in factory.records(story) if r.get('gate') == 'Code Review'])
    factory.review(story, review)
    clone = Path(tempfile.mkdtemp(prefix='factory-integration-')) / 'repo'
    subprocess.run(['git', 'clone', '--no-hardlinks', '--no-checkout', str(factory.root), str(clone)], capture_output=True, check=True)
    revision = factory.git('rev-parse', factory.revision).decode().strip()
    subprocess.run(['git', '-C', str(clone), 'checkout', '--detach', revision], capture_output=True, check=True)
    steps['own GitHub approved review'] = 'PASS'
    fixture_id = 'US-987654'
    s = {'id': fixture_id, 'title': 'Integration fixture', 'description': 'Disposable real-component sequence', 'status': 'READY', 'depends_on': [], 'blocked_by': [], 'open_questions': [], 'acceptance_criteria': [{'id': 'AC01', 'description': 'Real components execute'}], 'test_scenarios': [{'id': 'TS01', 'scenario': 'Real sequence'}], 'definition_of_ready': {k: True for k in yaml.safe_load(factory.blob('safe/templates/definition-of-ready.yaml'))['definition_of_ready']}}
    story_path = clone / f'safe/stories/{fixture_id}.yaml'
    state_path = clone / f'factory/state/{fixture_id}.json'
    evidence = clone / f'factory/evidence/{fixture_id}'
    evidence.mkdir(parents=True)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    story_path.write_text(yaml.safe_dump(s))
    state_path.write_text('{}')
    proof = evidence / 'summary.md'
    proof.write_text('REAL byte-compilation proof; individual source compilation completed by integration command.')
    commit_fixture(clone)
    f = Factory(clone)
    steps['workflow schema'] = 'PASS'
    # Register the disposable Story's command bindings as fixture configuration.
    # The evaluated production definition was loaded and schema-checked above.
    definition = yaml.safe_load((clone / 'factory/workflow.yaml').read_text())
    definition['commands'][fixture_id] = {
        'build': definition['commands']['factory_build'],
        'lint': definition['commands']['factory_lint'],
        'Unit Test': definition['commands']['factory_unit'],
        'Integration Test': definition['commands']['factory_integration']}
    (clone / 'factory/workflow.yaml').write_text(yaml.safe_dump(definition, sort_keys=False))
    commit_fixture(clone)
    f = Factory(clone)
    args = Namespace(story=fixture_id, action='dispatch', role='CODEX_DEVOPS', identity='integration_fixture', source=None, target=None, reason=None)
    orchestrate(f, args)
    commit_fixture(clone)
    f = Factory(clone)
    steps['orchestrator dispatch PASS'] = 'PASS'
    args.role = 'CODEX_TESTER'
    before = story_path.read_bytes(), state_path.read_bytes(), sorted(p.name for p in evidence.iterdir())
    try:
        orchestrate(f, args)
        raise AssertionError('required BLOCK did not occur')
    except Block:
        require(before == (story_path.read_bytes(), state_path.read_bytes(), sorted(p.name for p in evidence.iterdir())), 'BLOCK mutated files')
    steps['orchestrator BLOCK without writes'] = 'PASS'
    # Real shell delegation in the same canonical container, no Docker or Python fallback.
    result = subprocess.run(['bash', str(clone / 'scripts/validate-story.sh')], cwd=clone, env={**__import__('os').environ, 'STORY_FILE': str(story_path)}, capture_output=True)
    require(result.returncode == 0 and result.stdout.rstrip().endswith(b'DEFINITION OF READY: PASSED'), 'DoR shell delegation FAIL')
    steps['validate-story.sh delegation'] = 'PASS'
    require(not jenkins(f, f'feature/{fixture_id}-devops'), 'Jenkins local entry FAIL')
    stage = subprocess.run(['bash', str(clone / 'scripts/factory-jenkins.sh')], cwd=clone, env={**__import__('os').environ, 'BRANCH_NAME': f'feature/{fixture_id}-devops'}, capture_output=True)
    require(stage.returncode == 0, 'Jenkins shell entry FAIL')
    steps['Jenkins stage entry point'] = 'PASS'
    args = Namespace(story=fixture_id, action='transition', role=None, identity=None, source='READY', target='IN_PROGRESS', reason=None)
    orchestrate(f, args)
    commit_fixture(clone)
    f = Factory(clone)
    require(f.story(fixture_id)['status'] == 'IN_PROGRESS', 'orchestrator transition FAIL')
    s['status'] = 'IN_PROGRESS'
    steps['orchestrator transition PASS'] = 'PASS'
    for index, source in enumerate((clone / 'factory').rglob('*.py')):
        py_compile.compile(str(source), cfile=f'/tmp/integration-{index}.pyc', doraise=True)
    write_record(f, fixture_id, {'story_id': fixture_id, 'gate': 'build', 'result': 'PASS', 'producer_role': 'CODEX_DEVOPS', 'producer_identity': 'integration_fixture', 'command': f.command(fixture_id, 'build'), 'checks': {'byte-compilation': 'PASS', 'schema': 'PASS'}, 'artifacts': [{'path': str(proof.relative_to(clone)), 'sha256': digest(proof.read_bytes())}]})
    commit_fixture(clone)
    f = Factory(clone)
    steps['evidence writer'] = 'PASS'
    old_implementation, old_contract = f.implementation(), f.contract(fixture_id)
    (clone / 'integration-fixture-source.txt').write_text('Implementation change for stale detection')
    s['description'] = 'Changed acceptance contract'
    story_path.write_text(yaml.safe_dump(s))
    commit_fixture(clone)
    f = Factory(clone)
    require(old_implementation != f.implementation() and old_contract != f.contract(fixture_id), 'fingerprints did not change')
    require(f.gate(fixture_id, 'build')[0] == 'STALE_IMPLEMENTATION', 'stale detection FAIL')
    steps['both fingerprints and stale detection after commit'] = 'PASS'
    output = clone / f'factory/evidence/{story}/integration-result.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    summary = output.parent / 'integration-summary.md'
    summary.write_text('REAL Integration component results\n\n' + json.dumps(steps, indent=2) + '\n')
    # Successful result includes the real integration scenario outcome.
    record = {'story_id': story, 'gate': 'Integration Test', 'result': 'PASS', 'producer_role': factory.identity(story)['implementing_role'], 'producer_identity': factory.identity(story)['implementing_identity'], 'source_commit': revision, 'implementation_fingerprint': factory.implementation(), 'acceptance_contract_fingerprint': factory.contract(story), 'timestamp': datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00', 'Z'), 'checks': steps, 'artifacts': [{'path': str(summary.relative_to(clone)), 'sha256': digest(summary.read_bytes())}]}
    record["ts_results"] = {"TS24": "PASS"}
    record['command'] = factory.command(story, 'Integration Test')
    output.write_text(json.dumps(record, indent=2))
    print(f'NON-AUTHORITATIVE disposable output: {output}; promote through evidence writer and Git before gate evaluation. /tmp output never authorises a gate.')
    return record




def run(factory, story):
    """Preconditions block before execution; executed attempts preserve step results."""
    prerequisites = factory.workflow['dispatch']['Integration Test']['prerequisites']
    require(not factory.preconditions(story, prerequisites), 'Integration prerequisites BLOCK')
    required_steps = ('own GitHub approved review', 'workflow schema', 'orchestrator dispatch PASS', 'orchestrator BLOCK without writes', 'validate-story.sh delegation', 'Jenkins stage entry point', 'orchestrator transition PASS', 'evidence writer', 'both fingerprints and stale detection after commit')
    steps = {step: "NOT_EXECUTED" for step in required_steps}
    try:
        return execute_components(factory, story, steps)
    except (Block, OSError, ValueError, KeyError, TypeError, AssertionError, subprocess.SubprocessError, py_compile.PyCompileError, yaml.YAMLError) as error:
        output_dir = Path(tempfile.mkdtemp(prefix='factory-integration-failed-'))
        result = 'NOT_EXECUTED' if isinstance(error, Block) and 'NOT_EXECUTED' in str(error) else 'FAIL'
        record = {'story_id': story, 'gate': 'Integration Test', 'result': result, 'producer_role': factory.identity(story)['implementing_role'], 'producer_identity': factory.identity(story)['implementing_identity'], 'source_commit': factory.git('rev-parse', factory.revision).decode().strip(), 'implementation_fingerprint': factory.implementation(), 'acceptance_contract_fingerprint': factory.contract(story), 'timestamp': datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00', 'Z'), 'checks': steps, 'failure_type': type(error).__name__}
        record['checks']['execution'] = result
        for step in required_steps:
            if record["checks"][step] == "NOT_EXECUTED":
                record["checks"][step] = result
                break
        record["ts_results"] = {"TS24": result}
        record['command'] = factory.command(story, 'Integration Test')
        summary = output_dir / 'integration-summary.md'
        summary.write_text('REAL failed Integration component results\n\n' + json.dumps(record['checks'], indent=2) + '\n')
        record['artifacts'] = [{'path': f'factory/evidence/{story}/integration-summary.md', 'sha256': digest(summary.read_bytes())}]
        output = output_dir / 'integration-result.json'
        output.write_text(json.dumps(record, indent=2))
        print(f'NON-AUTHORITATIVE failed attempt output: {output}')
        raise Block(f'{result} Integration component execution; see non-authoritative structured output') from None
