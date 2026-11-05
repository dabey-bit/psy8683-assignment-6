"""Check observable Q1-Q2 properties of PsychoPy output (Project 5).

Q3-Q10 are deferred to Project 6. PILOT means the output cannot establish
that part of the property, not that it has been verified by a person.
CSV headers are preserved, including duplicate participant columns.
"""
import argparse
from collections import Counter
import csv
from decimal import Decimal, InvalidOperation
from glob import glob
from pathlib import Path

COLUMNS = ('participant', 'phase', 'trial_index', 'item_id', 'target',
           'prime', 'relatedness', 'soa', 'correct_response', 'seed')
NUMERIC = {'participant', 'trial_index', 'soa', 'seed'}


def read_output(path):
    with Path(path).open(newline='', encoding='utf-8-sig') as stream:
        rows = list(csv.reader(stream))
    if not rows:
        raise ValueError('Empty output file.')
    headers = rows[0]
    positions = {}
    for index, name in enumerate(headers):
        positions.setdefault(name, []).append(index)
    records = []
    for line, values in enumerate(rows[1:], 2):
        if not any(values):
            continue
        if len(values) != len(headers):
            raise ValueError(f'CSV line {line}: {len(values)} fields for {len(headers)} headers.')
        records.append((line, values))
    return {'path': str(path), 'headers': headers, 'positions': positions, 'records': records}


def cells(output, values, name):
    return [values[index] for index in output['positions'].get(name, [])]


def normalize(name, value):
    if name in NUMERIC:
        try:
            number = Decimal(value)
            if number.is_finite() and number == number.to_integral_value():
                return str(int(number))
        except InvalidOperation:
            pass
    return value


def get_context(output, lists_dir):
    positions = output['positions']
    missing = [name for name in COLUMNS if name not in positions]
    if missing:
        raise ValueError('Missing trial-list columns: ' + ', '.join(missing))
    participants = set()
    trials = []
    for line, values in output['records']:
        # Retain every nonempty copy; a DictReader would silently discard one.
        for value in cells(output, values, 'participant'):
            if value:
                participants.add(normalize('participant', value))
        is_trial = any(any(cells(output, values, name)) for name in
                       ('phase', 'trial_index', 'item_id', 'prime', 'target',
                        'prime_onset', 'target_onset'))
        if not is_trial:
            continue
        row = []
        for name in COLUMNS:
            copies = cells(output, values, name)
            nonempty = {normalize(name, value) for value in copies if value != ''}
            if len(nonempty) > 1:
                raise ValueError(f'CSV line {line}: conflicting copies of {name}: {copies!r}')
            row.append(next(iter(nonempty), ''))
        trials.append((line, tuple(row)))
    if len(participants) != 1:
        raise ValueError(f'Expected one consistent participant; found {sorted(participants)!r}.')
    participant = next(iter(participants))
    if not participant.isdecimal() or int(participant) < 1:
        raise ValueError(f'Invalid participant value: {participant!r}.')
    path = Path(lists_dir) / f'trials_p{int(participant):02d}.csv'
    with path.open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError(f'{path}: expected the ten trial-list columns in order.')
        expected = [tuple(normalize(name, row[name]) for name in COLUMNS) for row in reader]
    if not expected or not trials:
        raise ValueError(f'No trial records: output={len(trials)}, reference={len(expected)}.')
    return participant, path, trials, expected


def check_q1(output, lists_dir):
    pilot = ('PILOT', 'Filename ldt.psyexp, dialog entry format, and actual relative-path loading cannot be established from output alone; inspect Builder and pilot.')
    try:
        participant, path, trials, expected = get_context(output, lists_dir)
        allowed = set(expected)
        wrong = [(line, row) for line, row in trials if row not in allowed]
        if wrong:
            line, row = wrong[0]
            result = ('FAIL', f'Participant {participant}: {len(wrong)}/{len(trials)} trial records do not match {path.name}; first at CSV line {line}, phase={row[1]!r}, index={row[2]!r}, item={row[3]!r}.')
        else:
            result = ('PASS', f'Participant {participant}: all {len(trials)} recorded trial records match {path.name} across the ten input columns (numeric formatting normalized). Completeness/order checked in Q2.')
    except (ValueError, OSError) as error:
        result = ('FAIL', str(error))
    return [result, pilot]


def check_q2(output, lists_dir):
    try:
        participant, path, trials, expected = get_context(output, lists_dir)
        actual = [row for line, row in trials]
        if actual == expected:
            return ('PASS', f'{len(actual)}/{len(expected)} trial records, each reference row once and in file order; {len(output["records"])-len(trials)} nontrial rows excluded. This verifies recorded rows, not independent screen observation.')
        missing = sum((Counter(expected) - Counter(actual)).values())
        extra = sum((Counter(actual) - Counter(expected)).values())
        mismatch = next((i+1 for i, pair in enumerate(zip(actual, expected)) if pair[0] != pair[1]), min(len(actual), len(expected))+1)
        return ('FAIL', f'{len(actual)}/{len(expected)} trial records; missing={missing}, extra/changed={extra}; first sequence mismatch at trial position {mismatch}.')
    except (ValueError, OSError) as error:
        return ('FAIL', str(error))


# Keep the template's function names, without reporting unimplemented checks
# as PASS or PILOT. Their implementation belongs to Project 6.
def deferred(output, lists_dir):
    raise NotImplementedError('Q3-Q10 are deferred to Project 6.')


check_q3 = check_q4 = check_q5 = check_q6 = deferred
check_q7 = check_q8 = check_q9 = check_q10 = deferred
CHECKS = [check_q1, check_q2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', help='CSV paths or wildcard patterns')
    parser.add_argument('--lists', default='trial_lists')
    args = parser.parse_args()
    paths = []
    for pattern in args.files:
        matches = sorted(glob(pattern))
        paths.extend(matches or [pattern])
    failed = False
    print('Scope: Q1-Q2 only. Q3-Q10 deferred to Project 6.')
    for path in dict.fromkeys(paths):
        print('\n' + path)
        try:
            output = read_output(path)
        except (ValueError, OSError, csv.Error) as error:
            print(f'Q1 FAIL {error}\nQ2 FAIL Cannot evaluate unreadable output.')
            failed = True
            continue
        for check in CHECKS:
            result = check(output, args.lists)
            if isinstance(result, tuple):
                result = [result]
            for verdict, evidence in result:
                print(f'{check.__name__[6:].upper()} {verdict} {evidence}')
                failed |= verdict == 'FAIL'
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
