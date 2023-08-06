# Copyright 2021-2023 Henix, henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, Iterable, List, Union

import sys

from opentf.tools.ctlcommons import (
    _ensure_options,
    _is_command,
    _get_arg,
    _emit_csv,
    _ensure_uuid,
    _error,
    _warning,
    _debug,
)
from opentf.tools.ctlworkflows import _retrieve_columns_to_display, _file_not_found
from opentf.tools.ctlconfig import read_configuration
from opentf.tools.ctlnetworking import (
    _qualitygate,
    _get_json,
    _post,
)

########################################################################
# Help messages

GET_QUALITYGATE_HELP = '''Get qualitygate status for a workflow

Examples:
  # Get the quality gate status of a workflow applying the specific quality gate from the definition file
  opentf-ctl get qualitygate 9ea3be45-ee90-4135-b47f-e66e4f793383 --using=my.qualitygate.yaml --mode=my.quality.gate

  # Get the qualitygate status of a workflow applying the default strict quality gate (threshold=100%)
  opentf-ctl get qualitygate 9ea3be45-ee90-4135-b47f-e66e4f793383

Options:
  --mode=my.quality.gate|strict|passing|... or -m=...: use the specific qualitygate from the definition file
  or one of the default quality gates (strict with 100% threshold and passing with 0% threshold)
  --using=/path/to/definition.yaml: use the specific quality gate definition file.

Usage:
  opentf-ctl get qualitygate WORKFLOW_ID [--mode=mode] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

DESCRIBE_QUALITYGATE_HELP = '''Get qualitygate status description for a workflow

Examples:
  # Get the quality gate status description of a workflow applying the specific quality gate from the definition file
  opentf-ctl describe qualitygate 9ea3be45-ee90-4135-b47f-e66e4f793383 --using=my.qualitygate.yaml --mode=my.quality.gate

  # Get the qualitygate status description of a workflow applying the default strict quality gate (threshold=100%)
  opentf-ctl describe qualitygate 9ea3be45-ee90-4135-b47f-e66e4f793383

Options:
  --mode=my.quality.gate|strict|passing|... or -m=...: use the specific qualitygate from the definition file
  or one of the default quality gates (strict with 100% threshold and passing with 0% threshold)
  --using=/path/to/definition.yaml: use the specific quality gate definition file.

Usage:
  opentf-ctl describe qualitygate WORKFLOW_ID [--mode=mode] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

########################################################################
# Quality gate

DEFAULT_COLUMNS = (
    'RULE:rule',
    'RESULT:rule.result',
    'TESTS_IN_SCOPE:rule.tests_in_scope',
    'TESTS_FAILED:rule.tests_failed',
    'TESTS_PASSED:rule.tests_passed',
    'SUCCESS_RATIO:rule.success_ratio',
)
WIDE_COLUMNS = (
    'RULE:rule',
    'RESULT:rule.result',
    'TESTS_IN_SCOPE:rule.tests_in_scope',
    'TESTS_FAILED:rule.tests_failed',
    'TESTS_PASSED:rule.tests_passed',
    'SUCCESS_RATIO:rule.success_ratio',
    'SCOPE:rule.scope',
)

STATUS_TEMPLATES = {
    'SUCCESS': 'Workflow {workflow_id} successfully passed the quality gate `{mode}` applying the rule `{rule}`.',
    'FAILURE': 'Workflow {workflow_id} failed the quality gate `{mode}` applying the rule `{rule}`.',
    'NOTEST': 'Workflow {workflow_id} contains no tests matching the quality gate `{mode}` rule `{rule}`.',
}


def _describe_qualitygate(workflow_id: str, mode: str, status: Dict[str, Any]) -> None:
    """Get quality gate results for a workflow in a pretty form."""
    for rule, data in status.items():
        if data['result'] not in ('SUCCESS', 'NOTEST', 'FAILURE'):
            _error(
                f'Unexpected quality gate result when applying rule `{rule}`: {data["result"]} (was expecting SUCCESS, FAILURE or NOTEST).'
            )
            continue
        print(f'\n--------RESULTS: {mode}, {rule}--------\n')
        print(_make_qualitygate_status_message(data['result'], workflow_id, mode, rule))
        if data['result'] in ('SUCCESS', 'FAILURE'):
            print('\n    --------STATISTICS--------\n')
            print(f'    Tests in scope: {data["tests_in_scope"]}')
            print(f'    Tests failed:   {data["tests_failed"]}')
            print(f'    Tests passed:   {data["tests_passed"]}')
            print(f'    Success ratio:  {data["success_ratio"]}')


def _make_qualitygate_status_message(
    status: str, workflow_id: str, mode: str, rule: str
) -> str:
    return STATUS_TEMPLATES[status].format(
        workflow_id=workflow_id, mode=mode, rule=rule
    )


def _make_rule_row(name: str, definition, fields: List[str]) -> List[str]:
    if definition['result'] not in ('SUCCESS', 'NOTEST', 'FAILURE'):
        _error(
            f'Unexpected quality gate result when applying rule `{name}`: {definition["result"]} (was expecting SUCCESS, FAILURE or NOTEST).'
        )
        sys.exit(2)
    row = []
    for field in fields:
        if field == 'rule':
            row.append(name)
        elif field.startswith('rule.') and definition:
            row.append(definition.get(field.split('.')[1], ''))
        else:
            row.append('')
    return row


def _generate_qualitygate_rows(
    status: Dict[str, Any], columns: Iterable[str]
) -> List[List[Any]]:
    """Generate rows with quality gate results."""
    fields = [column.split(':')[1] for column in columns]
    return [
        _make_rule_row(name, definition, fields) for name, definition in status.items()
    ]


def _get_qualitygate_status(workflow_id: str, mode: str) -> Union[str, Dict[str, Any]]:
    _ensure_uuid(workflow_id)
    result = _get_json(
        _qualitygate(),
        f'/workflows/{workflow_id}/qualitygate?mode={mode}',
        statuses=(200, 404, 422),
    )
    return _process_qualitygate_result(result, workflow_id)


def _process_qualitygate_result(result, workflow_id):
    if result.get('code') == 404:
        _error(
            'Unknown workflow %s.  It is either too new, too old, or the provided '
            + 'workflow ID is incorrect.  You can use "opentf-ctl get workflows" to list '
            + 'the known workflow IDs.',
            workflow_id,
        )
        sys.exit(2)
    if result.get('code') == 422:
        _error(result.get('message'))
        sys.exit(2)
    if 'details' not in result or 'status' not in result.get('details', {}):
        _error(
            'Unexpected response from qualitygate.  Was expecting a JSON object'
            + ' with a .details.status entry, got: %s.',
            str(result),
        )
        sys.exit(2)

    return result['details']


def _post_qualitygate_definition(workflow_id, using, mode):
    _ensure_uuid(workflow_id)
    try:
        files = {'qualitygates': open(using, 'rb')}
        result = _post(
            _qualitygate(),
            f'/workflows/{workflow_id}/qualitygate?mode={mode}',
            statuses=(200,),
            files=files,
        )
        return _process_qualitygate_result(result, workflow_id)
    except FileNotFoundError as err:
        _file_not_found(using, err)
    except Exception as err:
        _error(f'Exception while handling quality gate definition file: {err}')
        sys.exit(2)


def get_qualitygate(workflow_id: str, mode: str, describe=False, using='') -> None:
    """Get qualitygate status.

    # Required parameter

    - workflow_id: a non-empty string (an UUID)
    - mode: a string

    # Raised exceptions

    Abort with an error code of 2 if the specified `workflow_id` is
    invalid or if an error occurred while contacting the orchestrator.

    Abort with an error code of 101 if the workflow is still running.

    Abort with an error code of 102 if the qualitygate failed.
    """
    if using:
        details = _post_qualitygate_definition(workflow_id, using, mode)
    else:
        details = _get_qualitygate_status(workflow_id, mode)

    status = details['status']
    if status not in ('NOTEST', 'FAILURE', 'RUNNING', 'SUCCESS'):
        _error(
            'Unexpected workflow status from qualitygate service: %s (was expecting NOTEST,'
            + ' SUCCESS, FAILURE, or RUNNING).',
            status,
        )
        sys.exit(2)
    if status == 'RUNNING':
        print(
            f'Workflow {workflow_id} is still running.  Please retry after workflow completion.'
        )
        sys.exit(101)

    if (rules := details.get('rules')) is not None:
        if describe:
            _describe_qualitygate(workflow_id, mode, rules)
        else:
            columns = _retrieve_columns_to_display(WIDE_COLUMNS, DEFAULT_COLUMNS)
            _emit_csv(_generate_qualitygate_rows(rules, columns), columns)

    if status == 'FAILURE':
        print(f'Workflow {workflow_id} failed the qualitygate using mode {mode}.')
        sys.exit(102)
    if status == 'NOTEST':
        print(f'Workflow {workflow_id} contains no test matching quality gate scopes.')


########################################################################
# Helpers


def print_qualitygate_help(args: List[str]):
    """Display help."""
    if _is_command('get qualitygate', args):
        print(GET_QUALITYGATE_HELP)
    elif _is_command('describe qualitygate', args):
        print(DESCRIBE_QUALITYGATE_HELP)
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


def qualitygate_cmd():
    """Interact with qualitygate."""
    if _is_command('get qualitygate _', sys.argv):
        _ensure_options(
            sys.argv[4:], [('--mode', '-m'), ('--output', '-o'), ('--using', '-u')]
        )
        read_configuration()
        get_qualitygate(
            sys.argv[3],
            _get_arg('--mode=') or _get_arg('-m=') or 'strict',
            False,
            _get_arg('--using=') or _get_arg('-u='),
        )
    elif _is_command('describe qualitygate _', sys.argv):
        _ensure_options(sys.argv[4:], [('--mode', '-m'), ('--using', '-u')])
        read_configuration()
        get_qualitygate(
            sys.argv[3],
            _get_arg('--mode=') or _get_arg('-m=') or 'strict',
            True,
            _get_arg('--using=') or _get_arg('-u='),
        )
    else:
        _error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)
