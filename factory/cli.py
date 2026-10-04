"""Canonical-runtime entry point; supervised operations only."""
import argparse
import datetime
import json
import os
import py_compile
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from engine import Block, Factory, require
from remotes import GitHub, JenkinsArchive


def write_record(factory, story, record):
    """Append only; validate artifacts before creating anything."""
    require(record.get('story_id') == story, 'INVALID writer Story')
    require(record.get('gate') in factory.workflow['gates'], 'unknown writer gate')
    # The producer cannot supply a forged fingerprint.
    record['source_commit'] = factory.git('rev-parse', factory.revision).decode().strip()
    record['implementation_fingerprint'] = factory.implementation()
    record['acceptance_contract_fingerprint'] = factory.contract(story)
    for artifact in record.get('artifacts', []):
        factory.artifact(artifact)
    record['timestamp'] = datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00', 'Z')
    require(record['gate'] != 'Code Review', 'implementer cannot write Code Review evidence')
    factory.record(story, record['gate'], record, allow_nonpass=True)
    for parent in factory.workflow['gates'][record['gate']]['prerequisites']:
        state, _ = factory.gate(story, parent)
        require(state in ('PASS', 'N/A-APPROVED'), f'{parent} prerequisite BLOCK')
    directory = factory.path(f'factory/evidence/{story}')
    require(directory.is_dir(), 'evidence directory must exist')
    target = directory / (record['timestamp'].replace(':', '-') + '.json')
    with target.open('x') as f:
        json.dump(record, f, sort_keys=True, indent=2)


def orchestrate(factory, args):
    require(factory.git('rev-parse', factory.revision) == factory.git('rev-parse', 'HEAD'), 'BLOCK orchestrate revision must equal HEAD')
    errors = factory.transition(args.story, args.source, args.target, args.reason) if args.action == 'transition' else factory.dispatch(args.story, args.role)
    require(not errors, '; '.join(errors))
    s = factory.story(args.story)
    state_path = factory.path(f'factory/state/{args.story}.json')
    require(state_path.is_file(), 'state target must exist')
    require(state_path.read_bytes() == factory.blob(f'factory/state/{args.story}.json'), 'BLOCK uncommitted state changes')
    state = json.loads(state_path.read_text())
    if args.action == 'dispatch' and args.role in factory.workflow['implementing_roles']:
        require(args.identity, 'implementing identity required')
        state.update(implementing_identity=args.identity, implementing_role=args.role)
    event = {'story_id': args.story, 'action': args.action, 'source_commit': factory.git('rev-parse', factory.revision).decode().strip(), 'implementation_fingerprint': factory.implementation(), 'acceptance_contract_fingerprint': factory.contract(args.story), 'timestamp': datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00', 'Z'), 'role': args.role, 'implementing_identity': args.identity, 'from': args.source, 'to': args.target, 'reason': args.reason}
    directory = factory.path(f'factory/evidence/{args.story}')
    require(directory.is_dir(), 'evidence target must exist')
    target = directory / ('event-' + event['timestamp'].replace(':', '-') + '.json')
    invocation = None
    if args.action == 'dispatch':
        if args.role == 'Code Review':
            invocation = f'Request the PO GitHub PR approval for {args.story} after Validation and Jenkins PASS; a human requests the review. No reviewer agent role is created.'
        elif args.role == 'Integration Test':
            actor = factory.identity(args.story)['implementing_role']
            invocation = f'Act as {actor} for {args.story}; run the workflow Integration Test command after the PO PR approval (Code Review PASS). Human starts the agent.'
        else:
            invocation = f'Act as {args.role} for {args.story}; read AGENTS.md, role file and Story. Human starts the agent.'
    require(state.get("status", s["status"]) == s["status"], "INVALID state/Story mismatch")
    require(factory.path(f"safe/stories/{args.story}.yaml").read_bytes() == factory.blob(f"safe/stories/{args.story}.yaml"), "BLOCK uncommitted Story changes")
    for path in (state_path, factory.path(f"safe/stories/{args.story}.yaml")):
        with path.open("r+"):
            pass
    require(os.access(directory, os.W_OK), "BLOCK evidence target read-only")
    story_text = None
    if args.action == 'transition':
        original = factory.blob(f'safe/stories/{args.story}.yaml').decode()
        matches = list(re.finditer(r'^(status:[ \t]*)([^#\r\n]*?)([ \t]*(?:#[^\r\n]*)?)$', original, re.MULTILINE))
        require(len(matches) == 1, 'INVALID single top-level status line required')
        match = matches[0]
        require(yaml.safe_load(match[2]) == s['status'], 'INVALID status value')
        story_text = original[:match.start(2)] + args.target + original[match.end(2):]
        expected = dict(s, status=args.target)
        require(yaml.safe_load(story_text) == expected, 'INVALID status edit changed other Story content')
    # All validation has completed before the first write.
    require(factory.git('rev-parse', factory.revision) == factory.git('rev-parse', 'HEAD'), 'BLOCK HEAD changed during orchestration')
    with target.open('x') as f:
        json.dump(event, f, indent=2)
    if args.action == 'transition':
        factory.path(f'safe/stories/{args.story}.yaml').write_text(story_text)
        state['status'] = args.target
    state_path.write_text(json.dumps(state, indent=2))
    if args.action == 'dispatch':
        print(invocation)


def jenkins(factory, branch):
    match = re.fullmatch(r'feature/(US-(?:FACTORY-)?[0-9]+)-[a-z]+', branch)
    stories = [match[1]] if match else [Path(p.decode()).stem for p in factory.git('ls-tree', '-r', '--name-only', factory.revision, '--', 'safe/stories/').splitlines() if p.endswith(b'.yaml')]
    errors = []
    notices = []
    for story in stories:
        s = factory.story(story)
        if not match and s['status'] != 'DONE':
            continue
        f = factory
        if not match:
            try:
                fresh = factory.arrived(story)
            except Block:
                fresh = True  # completion_errors reports the reason
            if not fresh:
                # Integrated by an earlier first-parent commit: AC06 at completion and record
                # integrity are re-checked offline; remote review/archive verification ran on arrival.
                f = Factory(factory.root, factory.revision, github=None, archive=None, verify_review=False)
        target = s['status']
        if match:
            # Feature branch: the recorded status must be supported at the tip.
            incoming = [edge for edge in factory.workflow['transitions'] if edge.endswith('->' + target)]
            require(incoming or target in ('DRAFT', 'BLOCKED'), 'unsupported Story status')
            if target == 'BLOCKED' and s.get('blocked_from') not in factory.pre_done():
                errors.append('INVALID blocked_from must be a state before DONE')
            for edge in incoming:
                names = factory.workflow['transitions'][edge]
                # Entry readiness remains valid after starting; DoR's admission status
                # check applies only to requests to enter development.
                if 'DoR' in names and target == 'IN_PROGRESS':
                    errors.extend(factory.dor(s, check_status=False))
                    names = [name for name in names if name != 'DoR']
                errors.extend(factory.preconditions(story, names))
        if target == 'DONE':
            # Both modes: AC06 held at the unique commit that introduced DONE.
            errors.extend(f.completion_errors(story))
        # Both modes: integrity of every record at the evaluated revision.
        errors.extend(f.history_errors(story, notices))
        external = [a for r in factory.records(story) for a in r.get('artifacts', []) if 'system' in a]
        require(not external or (not match and not fresh) or factory.archive is not None, 'NOT_EXECUTED Jenkins archive verification unavailable')
    for notice in notices:
        print(notice)
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['build', 'lint', 'unit', 'integration', 'dor', 'status', 'validate-gate', 'can-transition', 'can-dispatch', 'orchestrate', 'write-evidence', 'jenkins'])
    parser.add_argument('--root', default=os.getcwd())
    parser.add_argument('--revision', default='HEAD')
    parser.add_argument('--story')
    parser.add_argument('--gate')
    parser.add_argument('--role')
    parser.add_argument('--identity')
    parser.add_argument('--from', dest='source')
    parser.add_argument('--to', dest='target')
    parser.add_argument('--reason')
    parser.add_argument('--story-file')
    parser.add_argument('--record-file')
    parser.add_argument('--action', choices=['transition', 'dispatch'])
    parser.add_argument('--branch', default=os.environ.get('BRANCH_NAME', ''))
    args = parser.parse_args()
    try:
        factory = Factory(args.root, args.revision, github=GitHub(os.environ.get("FACTORY_GITHUB_TOKEN")), archive=JenkinsArchive() if args.command == "jenkins" else None)
        errors = []
        if args.command == 'build':
            sources = list((factory.root / 'factory').rglob('*.py'))
            require(sources, 'zero Factory sources')
            with tempfile.TemporaryDirectory(prefix='factory-build-') as compiled:
                for i, source in enumerate(sources):
                    py_compile.compile(str(source), cfile=str(Path(compiled) / f'{i}.pyc'), doraise=True)
        elif args.command == 'lint':
            return subprocess.run(['ruff', 'check', '--no-cache', str(factory.root / 'factory')]).returncode
        elif args.command == 'unit':
            suite = unittest.defaultTestLoader.discover(str(factory.root / 'factory/tests'))
            def flatten(tests):
                for test in tests:
                    if isinstance(test, unittest.TestSuite):
                        yield from flatten(test)
                    else:
                        yield test
            collected = list(flatten(suite))
            result = unittest.TextTestRunner(verbosity=2).run(suite)
            failed_ids = {t.id() for t, _ in result.failures + result.errors}
            skipped_ids = {t.id() for t, _ in result.skipped}
            for scenario in factory.workflow["unit_scenarios"]:
                ids = {t.id() for t in collected if f"_{scenario}_" in t.id()}
                print(f"{scenario}: collected={len(ids)} passed={len(ids - failed_ids - skipped_ids)} failed={len(ids & failed_ids)} not-executed={len(ids & skipped_ids)}")
                require(ids, f"zero collected tests for {scenario}")
            require(result.testsRun > 0 and result.wasSuccessful() and not result.skipped, 'Unit Test NOT PASS (failures, pending/not-executed, or zero tests)')
        elif args.command == 'dor':
            s = yaml.safe_load(Path(args.story_file).read_text())
            errors = factory.dor(s)
        elif args.command == 'status':
            for gate in factory.workflow['gates']:
                state, reasons = factory.gate(args.story, gate)
                print(f'{gate}: {state} {"; ".join(reasons)}')
                if state not in ('PASS', 'N/A-APPROVED'):
                    errors.append(gate)
            print('Rerun in workflow prerequisite order: ' + ', '.join(factory.rerun_order(args.story)))
        elif args.command == 'validate-gate':
            state, errors = factory.gate(args.story, args.gate)
            require(state in ('PASS', 'N/A-APPROVED'), f'{args.gate}: {state}; {errors}')
        elif args.command == 'can-transition':
            errors = factory.transition(args.story, args.source, args.target, args.reason)
        elif args.command == 'can-dispatch':
            errors = factory.dispatch(args.story, args.role)
        elif args.command == 'orchestrate':
            orchestrate(factory, args)
        elif args.command == 'write-evidence':
            write_record(factory, args.story, json.loads(Path(args.record_file).read_text()))
        elif args.command == 'jenkins':
            errors = jenkins(factory, args.branch)
        elif args.command == 'integration':
            errors = factory.preconditions(args.story, factory.workflow['dispatch']['Integration Test']['prerequisites'])
            require(not errors, '; '.join(errors))
            from integration import run
            run(factory, args.story)
        require(not errors, '; '.join(errors))
        print('DEFINITION OF READY: PASSED' if args.command == 'dor' else 'PASS')
        return 0
    except (Block, OSError, ValueError, TypeError, KeyError, yaml.YAMLError, py_compile.PyCompileError) as e:
        print(f'BLOCK: {type(e).__name__}: {e}')
        if args.command == 'dor':
            print('DEFINITION OF READY: FAILED')
        return 1


if __name__ == '__main__':
    sys.exit(main())
