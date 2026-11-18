"""Check PsychoPy trial-list, presentation, response, and instrumentation evidence.

CSV headers are preserved, including duplicate participant columns.
"""
import argparse
from bisect import bisect_left, bisect_right
from collections import Counter
from itertools import accumulate
from math import isfinite
from functools import lru_cache
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


def is_trial_row(output, values):
    return any(any(cells(output, values, name)) for name in
               ('phase', 'trial_index', 'item_id', 'prime', 'target',
                'prime_onset', 'target_onset'))


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
        if not is_trial_row(output, values):
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
    manual = ('UNDETERMINED', 'Inspect the Builder file and test the dialog and relative-path loading to settle the remaining Q1 requirements.')
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
    return [result, manual]


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


# Builder names are arbitrary. Prefer known semantic names and require a unique
# match before using an unfamiliar component as evidence.
COMPONENTS = {
    'instructions': ('instructions_text', 'instr_text_stim', 'instruction_text', 'instr_text', 'instructions', 'instr'),
    'instructions_key': ('instructions_key', 'instruction_key', 'instr_key', 'instr_resp'),
    'fixation': ('fixation_text', 'fixation', 'fix', 'fix_text', 'fix_cross'),
    'prime': ('prime_text', 'prime', 'prime_stim'),
    'target': ('target_text', 'target', 'target_stim'),
    'keyboard': ('trial_key', 'response', 'resp', 'key_resp', 'response_key', 'trial_resp'),
    'feedback': ('feedback_text', 'feedback', 'fb_text', 'fb'),
    'iti': ('iti_blank', 'iti_text', 'blank_iti', 'blank', 'iti'),
    'break': ('break_text', 'break_screen_text', 'break_screen', 'break'),
    'break_key': ('break_key', 'break_resp', 'break_screen_key'),
    'end': ('end_text', 'end_screen_text', 'end_msg', 'end_screen', 'end'),
}


def resolve_column(output, role, suffix):
    names = COMPONENTS[role]
    for name in names:
        column = f'{name}.{suffix}'
        if column in output['positions']:
            return column
    # Match semantic names in camelCase or snake_case without choosing between
    # multiple candidates. Response families must actually have a keys column.
    keywords = {
        'instructions': ('instr',), 'instructions_key': ('instr',),
        'fixation': ('fix',), 'prime': ('prime',), 'target': ('target',),
        'keyboard': ('resp', 'trialkey', 'keyboard'), 'feedback': ('feedback', 'fb'),
        'iti': ('iti',), 'break': ('break',), 'break_key': ('break',), 'end': ('end', 'finish'),
    }
    keyboard = role in {'instructions_key', 'break_key', 'keyboard'}
    matches = []
    for column in output['positions']:
        name, _, ending = column.partition('.')
        compact = name.lower().replace('_', '')
        if ending != suffix or not any(word in compact for word in keywords[role]):
            continue
        if role == 'keyboard' and any(x in compact for x in ('instr', 'break', 'end')):
            continue
        if (name + '.keys' in output['positions']) == keyboard:
            matches.append(column)
    return matches[0] if len(matches) == 1 else ''


def finite_number(value):
    if value == '':
        return None
    try:
        result = float(value)
    except ValueError:
        return float('nan')
    return result if isfinite(result) else float('nan')


def event(output, values, role, suffix='started'):
    return finite_number(value_at(output, values, resolve_column(output, role, suffix)))


def field(output, values, name):
    return value_at(output, values, name).strip()


def key_value(value):
    return '' if value in {'', 'None', '[]'} else value


def record_verdict(label, rows, test, missing_evidence):
    """A test returns None for a match, a message for failure, or False for missing evidence."""
    errors, missing, matched = [], 0, 0
    for line, values in rows:
        detail = test(values)
        if detail is False:
            missing += 1
        elif detail is None:
            matched += 1
        else:
            errors.append((line, detail))
    if errors:
        line, detail = errors[0]
        return ('FAIL', f'{label}: {len(errors)} inconsistent rows, first at CSV line {line}: {detail}')
    if missing or not rows:
        return ('UNDETERMINED', f'{label}: {matched}/{len(rows)} assessable rows matched. {missing_evidence}')
    return ('PASS', f'{label}: all {matched} rows matched.')


def check_q3(output, lists_dir):
    trials = trial_values(output)
    phases = [field(output, v, 'phase') for _, v in trials]
    expected = ['practice'] * 8 + ['experimental'] * 96
    result = [('PASS' if phases == expected else 'FAIL',
               f'Phase sequence: {len(phases)} trials with {phases.count("practice")} practice and {phases.count("experimental")} experimental. Expected 8 practice followed by 96 experimental.')]
    for role, boundary in [('instructions', (None, trials[0][0] if trials else None)),
                           ('break', (trials[7][0], trials[8][0]) if len(trials) >= 9 else (None, None)),
                           ('end', (trials[-1][0] if trials else None, None))]:
        col = resolve_column(output, role, 'started')
        if not col:
            result.append(('UNDETERMINED', f'{role}: need a named start timestamp to establish placement.'))
            continue
        observed = [(line, values) for line, values in output['records'] if value_at(output, values, col)]
        low, high = boundary
        if len(observed) != 1 or not (low or 0) < observed[0][0] < (high or float('inf')) or not isfinite(event(output, observed[0][1], role)):
            result.append(('FAIL', f'{role}: expected exactly one screen in its proper place between phases. Found {len(observed)} starts.'))
            continue
        result.append(('PASS', f'{role}: {col} is recorded in the expected row (CSV line {observed[0][0]}).'))
        if role != 'end':
            key = field(output, observed[0][1], resolve_column(output, role + '_key', 'keys'))
            result.append(('UNDETERMINED' if not key else ('PASS' if key == 'space' else 'FAIL'),
                           f'{role}: recorded ending key {key!r}.' if key else f'{role}: need the ending key or an observed run to establish SPACE termination.'))

    def feedback(values):
        col = resolve_column(output, 'feedback', 'started')
        if not col:
            return False
        recorded = field(output, values, col)
        practice = field(output, values, 'phase') == 'practice'
        if bool(recorded) != practice or recorded and not isfinite(finite_number(recorded)):
            return 'expected a valid feedback onset only on practice rows'
        return None

    result.append(record_verdict('Feedback placement', trials, feedback, 'Need feedback component timestamps.'))
    feedback_trials = [(line, v) for line, v in trials if field(output, v, 'phase') == 'practice']
    end_rows = [(line, v) for line, v in output['records'] if event(output, v, 'end') is not None]
    result.append(duration_verdict(output, feedback_trials, 'Feedback', lambda v: display_duration(output, v, 'feedback', following='iti'), lambda _: 1000))
    result.append(duration_verdict(output, end_rows, 'End screen', lambda v: display_duration(output, v, 'end'), lambda _: 2000))
    result.append(('UNDETERMINED', 'Need the build or an observed run to establish the instruction and feedback wording and the actual screen transitions.'))
    return result


def display_duration(output, values, role, following=None):
    start = event(output, values, role)
    stop = event(output, values, role, 'stopped')
    if stop is None and following:
        stop = event(output, values, following)
    return None if start is None or stop is None else stop - start


def trial_flip_times(output):
    """Use aligned I1 intervals for events inside recorded trial windows."""
    if 'trial_flip_times' in output:
        return output['trial_flip_times']
    windows = {}
    try:
        trials = trial_values(output)
        intervals = frame_intervals(frame_log_path(output))
        frame = frame_duration(output, trials)
        aligned, _ = interval_windows(output, trials, intervals, frame)
        for line, start, end in aligned:
            windows[line] = list(accumulate(intervals[start:end], initial=0))
    except (OSError, ValueError):
        pass
    output['trial_flip_times'] = windows
    return windows


def logged_duration_frames(output, values, timestamps, label):
    roles = {'Fixation': ('fixation', 'started', 'fixation', 'stopped'),
             'Prime': ('prime', 'started', 'prime', 'stopped'),
             'SOA': ('prime', 'started', 'target', 'started')}
    if label not in roles or timestamps is None:
        return None
    a, sa, b, sb = roles[label]
    origin, start, stop = event(output, values, 'fixation'), event(output, values, a, sa), event(output, values, b, sb)
    if None in (origin, start, stop) or not all(map(isfinite, (origin, start, stop))):
        return None
    a_idx, b_idx = (nearest_flip(timestamps, value - origin) for value in (start, stop))
    if max(abs(timestamps[i] - (t - origin)) for i, t in [(a_idx, start), (b_idx, stop)]) > .001:
        return None
    return b_idx - a_idx


def duration_verdict(output, rows, label, elapsed, milliseconds):
    try:
        nominal_frame = frame_duration(output, trial_values(output))
        measured_frame = 1 / float(field(output, trial_values(output)[0][1], 'frameRate'))
    except (ValueError, IndexError):
        return ('UNDETERMINED', f'{label}: need a consistent measured frameRate to check rounded frame timing.')
    mismatches, missing, matched = [], 0, 0
    aligned_flips, elapsed_anomalies = 0, 0
    for line, values in rows:
        actual = elapsed(values)
        ms = milliseconds(values)
        if actual is None or ms is None:
            missing += 1
            continue
        if not isfinite(actual) or not isfinite(ms) or actual <= 0 or ms < 0:
            mismatches.append((line, 0, True, 'invalid duration or SOA'))
            continue
        frames = round(ms * round(1 / nominal_frame) / 1000)
        elapsed_periods = round(actual / measured_frame)
        exact = logged_duration_frames(output, values, trial_flip_times(output).get(line), label)
        if exact is not None:
            aligned_flips += 1
        observed = elapsed_periods if exact is None else exact
        if observed == frames:
            matched += 1
            elapsed_anomalies += elapsed_periods != frames
        else:
            method = 'recorded flips' if exact is not None else 'elapsed frame periods'
            mismatches.append((line, observed - frames, exact is not None,
                               f'{observed} {method} ({actual * 1000:.3f} ms), expected {frames}'))
    # A persistent shift is evidence against the planned duration. Isolated
    # discrepancies without flip counts may be scheduling or refresh delays.
    expected_groups = Counter(milliseconds(values) for _, values in rows)
    by_line = {line: milliseconds(values) for line, values in rows}
    counts = Counter((by_line[line], offset) for line, offset, _, _ in mismatches)
    failures = [(line, detail) for line, offset, exact, detail in mismatches
                if exact or (expected_groups[by_line[line]] > 1
                             and counts[by_line[line], offset] > expected_groups[by_line[line]] / 2)]
    if failures:
        line, detail = failures[0]
        return ('FAIL', f'{label}: {len(failures)}/{len(rows)} definite or systematic mismatches, first at CSV line {line}: {detail}.')
    if mismatches or missing or not rows:
        detail = f' First at CSV line {mismatches[0][0]}: {mismatches[0][3]}.' if mismatches else ''
        return ('UNDETERMINED', f'{label}: {matched}/{len(rows)} matched, {missing} lack timestamps, {len(mismatches)} have unexplained elapsed-time deviations.{detail} Need the actual flip counts to distinguish delays from a frame setting error.')
    detail = f' {aligned_flips} checked against logged flips; {elapsed_anomalies} had elapsed-time deviations despite the correct count.' if aligned_flips else ''
    return ('PASS', f'{label}: {matched} durations agree with the rounded frame counts in the software evidence.{detail}')


def timing_delta(output, values, first, second):
    start, stop = (event(output, values, role, suffix) for role, suffix in (first, second))
    return None if start is None or stop is None else stop - start


def trial_timing(output):
    trials = trial_values(output)
    trial_specs = [
        ('Fixation', lambda v: display_duration(output, v, 'fixation', following='prime'), lambda _: 500),
        ('Prime', lambda v: display_duration(output, v, 'prime'), lambda _: 150),
        ('SOA', lambda v: timing_delta(output, v, ('prime', 'started'), ('target', 'started')), lambda v: finite_number(field(output, v, 'soa'))),
        ('ITI', lambda v: display_duration(output, v, 'iti'), lambda _: 500),
    ]
    return [duration_verdict(output, trials, label, elapsed, ms) for label, elapsed, ms in trial_specs]


def target_offset(output, values):
    stop = event(output, values, 'target', 'stopped')
    if stop is not None:
        return stop
    role = 'feedback' if field(output, values, 'phase') == 'practice' else 'iti'
    return event(output, values, role)


def presentation_order(output, values):
    placement = [('fixation', 'started'), ('prime', 'started'), ('prime', 'stopped'), ('target', 'started')]
    stamps = [event(output, values, role, suffix) for role, suffix in placement]
    stamps.append(target_offset(output, values))
    if field(output, values, 'phase') == 'practice':
        stamps.append(event(output, values, 'feedback'))
    stamps.append(event(output, values, 'iti'))
    present = [stamp for stamp in stamps if stamp is not None]
    if any(not isfinite(stamp) for stamp in present) or any(b + .001 < a for a, b in zip(present, present[1:])):
        return 'fixation, prime, target, feedback or ITI timestamps are out of order'
    return False if len(present) != len(stamps) else None


def check_q4(output, lists_dir):
    trials = trial_values(output)
    result = trial_timing(output)
    result.append(record_verdict('Presentation order', trials, lambda v: presentation_order(output, v),
                                 'Need fixation, prime onset and offset, target onset and offset, and following screen flips.'))
    def target_window(values):
        start = event(output, values, 'target')
        stop = target_offset(output, values)
        listening = event(output, values, 'keyboard')
        if None in (start, stop):
            return False
        if not (isfinite(start) and isfinite(stop) and start < stop):
            return 'invalid or nonpositive target display interval'
        try:
            frame = frame_duration(output, trials)
        except ValueError:
            return False
        if listening is not None and (not isfinite(listening) or abs(listening - start) > .001):
            return 'response window is not synchronized to target onset'
        timeout = field(output, values, 'timeout')
        rt = finite_number(field(output, values, 'rt'))
        actual = stop - start
        if timeout == '1' and abs(actual - (round(2 / frame) / float(field(output, values, 'frameRate')))) <= .5 * frame:
            return None
        if timeout == '1' and actual > 2 and field(output, values, 'dropped_frames').isdecimal() and int(field(output, values, 'dropped_frames')):
            return False
        if timeout == '1':
            return f'timeout target duration was {actual:.6f} s (expected approximately 2 s)'
        if timeout != '0' or rt is None:
            return False
        if not isfinite(rt) or actual + .001 < rt:
            return 'target ended before the recorded response'
        if actual > rt + 2 * frame + .001:
            if field(output, values, 'dropped_frames').isdecimal() and int(field(output, values, 'dropped_frames')):
                return False
            return False  # The post-target flip is outside I1; a delay here cannot be attributed from the CSV.
        return None

    result.append(record_verdict('Target through response or timeout', trials, target_window,
                                 'Need the target offset, response time or event-level interval evidence.'))
    result.append(('UNDETERMINED', 'Inspect the build or watch a run to confirm the fixation cross, stimulus case, and blank SOA and ITI screens. Physical timing requires a photodiode.'))
    return result


def check_q5(output, lists_dir):
    result = trial_timing(output)
    trials = trial_values(output)
    timeouts = [(line, values) for line, values in trials if field(output, values, 'timeout') == '1']
    if timeouts:
        def timeout_duration(values):
            start, stop = event(output, values, 'target'), target_offset(output, values)
            return None if start is None or stop is None else stop - start
        result.append(duration_verdict(output, timeouts, 'Timeout target', timeout_duration, lambda _: 2000))
    else:
        result.append(('UNDETERMINED', 'Timeout target: no timeout trials; need a run that reaches the deadline.'))
    result.extend(r for r in check_q3(output, lists_dir) if r[1].startswith(('Feedback:', 'End screen:')))
    result.append(('UNDETERMINED', 'One recorded refresh rate cannot establish the Builder conversion rule at other rates. Inspect the frame expressions and refresh-rate source.'))
    return result


def expected_key(output, values):
    pids = {normalize('participant', p) for p in cells(output, values, 'participant') if p}
    category = field(output, values, 'correct_response')
    if len(pids) != 1 or not next(iter(pids)).isdecimal() or category not in {'word', 'nonword'}:
        return None
    odd = int(pids.pop()) % 2 == 1
    return 'f' if odd == (category == 'word') else 'j'


def check_q6(output, lists_dir):
    def mapping(values):
        observed = key_value(field(output, values, 'key'))
        automatic = key_value(field(output, values, resolve_column(output, 'keyboard', 'keys')))
        invalid = [key for key in (observed, automatic) if key and key not in {'f', 'j'}]
        if invalid:
            return f'unexpected accepted key {invalid[0]!r}'
        return None

    trials = trial_values(output)
    auto = resolve_column(output, 'keyboard', 'keys')
    responses = [(l, v) for l, v in trials if any(key_value(field(output, v, c)) for c in ('key', auto))]
    return [record_verdict('Accepted response keys', responses, mapping, 'Need recorded response keys.'),
            ('UNDETERMINED', 'Need the instructions and keyboard configuration or a controlled run to confirm displayed mapping, ignored keys and Escape.')]


def check_q7(output, lists_dir):
    trials = trial_values(output)

    def synchronization(values):
        target, keyboard = event(output, values, 'target'), event(output, values, 'keyboard')
        if target is None or keyboard is None:
            return False
        if not (isfinite(target) and isfinite(keyboard)) or abs(target - keyboard) > .001:
            return f'keyboard minus target onset is {1000 * (keyboard - target):.3f} ms'
        return None

    def reaction(values):
        rt = finite_number(field(output, values, 'rt'))
        if rt is None:
            return False
        if not isfinite(rt) or not 0 <= rt < 2:
            return f'invalid target-relative RT {rt!r}'
        col = resolve_column(output, 'keyboard', 'rt')
        auto = finite_number(field(output, values, col))
        if auto is None or synchronization(values) is False:
            return False
        if not isfinite(auto) or abs(rt - auto) > .001:
            return f'saved RT {rt} differs from keyboard RT {auto}'
        return synchronization(values)

    responses = [(l, v) for l, v in trials if key_value(field(output, v, 'key'))]
    return [record_verdict('Keyboard synchronization', trials, synchronization, 'Need separate target and keyboard start timestamps.'),
            record_verdict('Recorded RT reference', responses, reaction, 'Need the automatic keyboard RT and its start relative to the target.'),
            ('UNDETERMINED', 'Need Builder or a controlled run to verify buffer clearing and first-key storage. Physical stimulus-to-key latency needs external measurement.')]


def check_q8(output, lists_dir):
    trials = trial_values(output)
    result = []
    for role in ('prime', 'target'):
        def text_matches(values):
            shown = value_at(output, values, role + '_shown')
            source = value_at(output, values, role)
            if not source or not shown:
                return 'required source or shown text is empty or missing'
            expected = source.lower() if role == 'prime' else source.upper()
            return None if shown == expected else f'saved {shown!r}, expected {expected!r}'
        result.append(record_verdict(f'{role} text', trials, text_matches, 'Need trial rows.'))
    result.append(('UNDETERMINED', 'Need Builder code to confirm the saved strings came from the stimulus objects at trial end.'))
    return result


def check_q9(output, lists_dir):
    trials = trial_values(output)

    def onsets(values):
        prime, target = (finite_number(field(output, values, role + '_onset')) for role in ('prime', 'target'))
        if prime is None or target is None or not (isfinite(prime) and isfinite(target) and 0 <= prime < target):
            return 'required onsets must be finite seconds in prime-then-target order'
        for role, custom in [('prime', prime), ('target', target)]:
            auto = event(output, values, role)
            if auto is None:
                return False
            if not isfinite(auto) or abs(auto - custom) > .001:
                return f'{role}_onset ({custom}) differs from the automatic started timestamp ({auto})'
        return None

    return [record_verdict('Custom onsets versus automatic flip stamps', trials, onsets, 'Need both automatic started columns to compare their clock and values.'),
            ('UNDETERMINED', 'Need build code to establish how the timestamps were captured. Measuring physical light onset requires hardware.')]


def check_q10(output, lists_dir):
    def response(values):
        key = field(output, values, 'key')
        rt = field(output, values, 'rt')
        accuracy = field(output, values, 'accuracy')
        timeout = field(output, values, 'timeout')
        if key not in {'', 'f', 'j'} or accuracy not in {'0', '1'} or timeout not in {'0', '1'}:
            return f'invalid key, accuracy or timeout: {(key, accuracy, timeout)!r}'
        if timeout == '1' and (key or rt or accuracy != '0'):
            return 'timeout must have blank key and RT and zero accuracy'
        if timeout == '0':
            seconds = finite_number(rt)
            if not key or seconds is None or not isfinite(seconds) or not 0 <= seconds < 2:
                return f'response needs f/j and an RT in [0, 2) seconds; got {key!r}, {rt!r}'
            correct = expected_key(output, values)
            if correct is None:
                return False
            if int(accuracy) != int(key == correct):
                return f'accuracy {accuracy} for {key!r}; correct key is {correct!r}'
        auto_col = resolve_column(output, 'keyboard', 'keys')
        auto = key_value(field(output, values, auto_col))
        auto_rt = finite_number(field(output, values, resolve_column(output, 'keyboard', 'rt')))
        if auto_col and auto != key:
            # The automatic component can report a late press the custom fields correctly discard.
            if not (timeout == '1' and auto in {'f', 'j'} and auto_rt is not None
                    and isfinite(auto_rt) and auto_rt >= 2):
                return f'custom key {key!r} disagrees with keyboard key {auto!r}'
        if key and auto_rt is not None and (not isfinite(auto_rt) or abs(float(rt) - auto_rt) > .001):
            return f'custom RT {rt} disagrees with keyboard RT {auto_rt}'
        start, keyboard = event(output, values, 'target'), event(output, values, 'keyboard')
        if start is not None and keyboard is not None and abs(start - keyboard) > .001:
            return 'keyboard times are referenced to a different onset, so the saved RT or timeout is not target-relative'
        return None

    trials = trial_values(output)
    missing = set(COLUMNS + ('key', 'rt', 'accuracy', 'timeout')) - output['positions'].keys()
    if missing:
        return ('FAIL', f'Missing required Q10 columns: {", ".join(sorted(missing))}.')
    result = [record_verdict('Recorded response and timeout coding', trials, response, 'Need participant parity and lexical category to recompute accuracy.')]
    try:
        _, path, actual, expected = get_context(output, lists_dir)
        allowed = set(expected)
        wrong = [line for line, row in actual if row not in allowed]
        result.append(('FAIL', f'{len(wrong)} trial rows differ from {path.name}, first at CSV line {wrong[0]}.') if wrong else
                      ('PASS', f'All ten recorded trial-list values match a row in {path.name}.'))
    except (ValueError, OSError) as error:
        result.append(('FAIL', str(error)))
    result.append(('UNDETERMINED', 'Saved response codes cannot show unrecorded presses or establish the physical two-second deadline without reference timing evidence.'))
    return result




def frame_log_path(output):
    path = Path(output['path'])
    return path.with_name(path.stem + '_frameIntervals.log')


@lru_cache(maxsize=16)
def _read_frame_intervals(path, modified_ns, size):
    with path.open(encoding='utf-8-sig') as stream:
        intervals = []
        for line_number, line in enumerate(stream, 1):
            try:
                value = float(line)
                if not isfinite(value) or value <= 0:
                    raise ValueError
            except ValueError:
                raise ValueError(f'{path.name} line {line_number}: expected one positive, finite interval in seconds.') from None
            intervals.append(value)
    if not intervals:
        raise ValueError(f'{path.name} has no intervals.')
    return tuple(intervals)


def frame_intervals(path):
    stat = path.stat()
    return _read_frame_intervals(path, stat.st_mtime_ns, stat.st_size)


def trial_values(output):
    return [(line, values) for line, values in output['records']
            if is_trial_row(output, values)]


def value_at(output, values, name):
    values = cells(output, values, name)
    return values[0] if len(values) == 1 else ''


def frame_duration(output, trials):
    rates = {float(value_at(output, values, 'frameRate')) for _, values in trials}
    if len(rates) != 1:
        raise ValueError('Expected a consistent frameRate on the trial rows.')
    rate = rates.pop()
    if not isfinite(rate) or round(rate) < 1:
        raise ValueError('Expected a positive, finite frameRate that rounds to at least 1 Hz.')
    return 1 / round(rate)


def nearest_flip(timestamps, target, start=0):
    pos = bisect_left(timestamps, target, lo=start)
    candidates = [i for i in (pos - 1, pos) if start <= i < len(timestamps)]
    return min(candidates, key=lambda i: abs(timestamps[i] - target)) if candidates else None


def interval_windows(output, trials, intervals, duration, dropped_counts=None):
    """Find alignments using the timestamps available in this build's CSV."""
    cumulative = list(accumulate(intervals, initial=0))
    starts = {0: ()}
    dropped = list(accumulate((x > 1.5 * duration for x in intervals), initial=0))
    # Allow sub-frame timestamp noise while requiring both internal flip anchors.
    tolerance = min(0.001, duration / 8)
    for index, (line, values) in enumerate(trials):
        def timestamp(name):
            return value_at(output, values, name)

        fields = (timestamp(resolve_column(output, 'fixation', 'started')), timestamp('prime_onset'),
                  timestamp('target_onset'),
                  timestamp(resolve_column(output, 'feedback', 'started'))
                  or timestamp(resolve_column(output, 'iti', 'started')))
        if not all(fields):
            raise ValueError(f'CSV line {line} lacks a fixation, prime, target, or post-trial flip timestamp.')
        fixation, prime, target, after = map(float, fields)
        if not all(map(isfinite, (fixation, prime, target, after))) or not fixation < prime < target < after:
            raise ValueError(f'CSV line {line} has invalid or out-of-order trial timestamps.')
        ends = {}
        for start, prior in starts.items():
            zero = cumulative[start]
            prime_flip = nearest_flip(cumulative, zero + prime - fixation, start + 1)
            if prime_flip is None or abs(cumulative[prime_flip] - zero - (prime - fixation)) > tolerance:
                continue
            target_flip = nearest_flip(cumulative, zero + target - fixation, prime_flip + 1)
            if target_flip is None or abs(cumulative[target_flip] - zero - (target - fixation)) > tolerance:
                continue
            # The next routine starts about one frame after the last logged target flip.
            post_trial = zero + after - fixation
            low = bisect_left(cumulative, post_trial - 1.5 * duration, lo=target_flip)
            high = bisect_right(cumulative, post_trial - 0.5 * duration, lo=low)
            for end in range(low, high):
                if dropped_counts is None or dropped[end] - dropped[start] == dropped_counts[index]:
                    ends[end] = prior + ((line, start, end),)
        if not ends:
            return (), line
        starts = ends
    return starts.get(len(intervals), ()), None


def check_i1(output, lists_dir):
    path = frame_log_path(output)
    if not path.is_file() and 'dropped_frames' not in output['positions']:
        return ('UNDETERMINED', 'No instrumentation log or column. Run the instrumented build and retain its matching log.')
    try:
        intervals = frame_intervals(path)
    except (OSError, ValueError) as error:
        return ('FAIL', str(error))
    trials = trial_values(output)
    fmt = ('PASS', f'{len(intervals)} positive, finite intervals, one per line in {path.name}.')
    try:
        if not trials:
            raise ValueError('No trial rows available for alignment.')
        duration = frame_duration(output, trials)
        aligned, line = interval_windows(output, trials, intervals, duration)
    except ValueError as error:
        return [fmt, ('UNDETERMINED', f'{error} Need the fixation, prime, target and following flip timestamps and frameRate.')]
    if not aligned:
        spans = []
        for _, values in trials:
            start = event(output, values, 'fixation')
            following = event(output, values, 'feedback') or event(output, values, 'iti')
            spans.append(following - start)
        if sum(intervals) > sum(spans) + 0.001:
            return [fmt, ('FAIL', f'The log covers {sum(intervals):.3f} s, longer than the {sum(spans):.3f} s from all fixation flips through their following routine flips.')]
        where = f' at CSV line {line}' if line else ' through the end of the log'
        return [fmt, ('UNDETERMINED', f'Could not align all intervals{where} with one flip between the last target flip and the next routine. Check the actual offset flip and any delay at that boundary.')]
    return [fmt, ('PASS', f'All intervals align with the fixation, prime and target timestamps for {len(trials)} trials and end about one flip before feedback or ITI. No extra intervals outside those windows.')]


def check_i2(output, lists_dir):
    path = frame_log_path(output)
    if 'dropped_frames' not in output['positions']:
        if path.is_file():
            return ('FAIL', 'Frame interval log is present but the CSV has no dropped_frames column.')
        return ('UNDETERMINED', 'No dropped_frames column or matching log. Run the instrumented build and retain both outputs.')
    trials = trial_values(output)
    if not trials:
        return ('FAIL', 'No trial rows carry dropped-frame counts.')
    counts = []
    for line, values in trials:
        count = value_at(output, values, 'dropped_frames')
        if not count.isascii() or not count.isdecimal():
            return ('FAIL', f'CSV line {line}: dropped_frames must be a nonnegative integer, got {count!r}.')
        counts.append(int(count))
    total = sum(counts)
    try:
        intervals = frame_intervals(path)
    except (OSError, ValueError) as error:
        return ('FAIL', f'Cannot reconcile dropped_frames with the matching interval log: {error}')
    try:
        duration = frame_duration(output, trials)
        threshold = 1.5 * duration
    except ValueError as error:
        return ('UNDETERMINED', f'Cannot compute the threshold. Need a consistent measured frameRate on the trial rows: {error}')
    observed = sum(value > threshold for value in intervals)
    evidence = (f'{len(trials)} trial counts sum to {total}; the log has {observed} '
                f'intervals strictly above {threshold * 1000:.6g} ms.')
    if total != observed:
        return ('FAIL', evidence)
    result = [('PASS', evidence)]
    try:
        aligned, _ = interval_windows(output, trials, intervals, duration)
    except ValueError:
        aligned = False
    if not aligned:
        return result + [('UNDETERMINED', 'Per-trial counts need trial boundary timestamps that align with the interval log.')]
    matching, _ = interval_windows(output, trials, intervals, duration, counts)
    if not matching:
        return result + [('FAIL', 'No timestamp-aligned partition of the log matches the per-trial dropped_frames values.')]
    return result + [('PASS', 'Per-trial dropped_frames values agree with a timestamp-aligned partition of the log.')]


CHECKS = [check_q1, check_q2, check_q3, check_q4, check_q5, check_q6,
          check_q7, check_q8, check_q9, check_q10, check_i1, check_i2]


# These source inspections are tied to the exact experiment commits used for
# the author's runs. They are opt-in and never inferred from column names.
REVIEWED_BUILDS = {
    'a5-baseline': ('ef6c471', {'3', '6'}),
    'a6-instrumented': ('9b1a2a0', {'7', '8'}),
}

SOURCE_EVIDENCE = {
    'Q1': 'ldt.psyexp setup validates a plain positive integer, formats trial_lists/trials_p%02d.csv, and both loops use trialListFile.',
    'Q3': 'SPACE ends the instructions and break routines. Practice alone includes feedback, set to Correct, Incorrect or Too slow from the recorded outcome.',
    'Q4': 'Builder defines +, the prime and uppercase target, leaves the long SOA gap undrawn, and uses a blank ITI after feedback in practice.',
    'Q5': 'Setup measures the refresh rate and rounds it to whole Hz; msToFrames rounds to whole frames and targetStartFrame uses that conversion for SOA.',
    'Q6': 'The displayed and scoring mappings both use wordKey/nonwordKey from participant parity. Trial keyboard accepts f/j and Enable Escape is on.',
    'Q7': 'Target and keyboard share targetStartFrame. The keyboard is refresh-synchronized, discards previous events and stores the first key.',
    'Q8': 'trial_record End Routine reads prime_text.text and target_text.text directly from the stimulus objects.',
    'Q9': 'trial_record End Routine saves prime_text.tStartRefresh and target_text.tStartRefresh.',
    'Q10': 'trial_record treats RT >= 2 s as late and computes accuracy against the expected key for the recorded category.',
}


def source_evidence(output, reviewed):
    if not reviewed:
        return []
    commit, participants = REVIEWED_BUILDS[reviewed]
    observed = {normalize('participant', pid) for _, vals in trial_values(output)
                for pid in cells(output, vals, 'participant') if pid}
    if Path(output['path']).resolve().parent != Path('data').resolve() or len(observed) != 1 or not observed <= participants:
        return []
    return [(prop, f'Source at {commit}: {detail}') for prop, detail in SOURCE_EVIDENCE.items()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', help='CSV paths or wildcard patterns')
    parser.add_argument('--lists', default='trial_lists')
    parser.add_argument('--reviewed-build', choices=REVIEWED_BUILDS,
                        help='include source inspection evidence for these runs, if they came from this reviewed build')
    args = parser.parse_args()
    paths = []
    for pattern in args.files:
        matches = sorted(glob(pattern))
        paths.extend(matches or [pattern])
    failed = False
    print('Scope: software evidence for Q1-Q10 and I1-I2.')
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
        reviewed = source_evidence(output, args.reviewed_build)
        for prop, evidence in reviewed:
            print(f'{prop} PILOT {evidence}')
        if reviewed:
            print('Q3 NOTE The break text stops after 1 s while the routine continues waiting for SPACE.')
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
