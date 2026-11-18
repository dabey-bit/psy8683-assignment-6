"""Negative controls for the checker using temporary CSVs and logs."""
import csv
from pathlib import Path
import tempfile
import unittest
import check_output as checker


class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / 'output.csv'
        with Path('trial_lists/trials_p03.csv').open(newline='') as stream:
            self.source = list(csv.reader(stream))
        self.headers = self.source[0] + ['participant']
        self.rows = [row + ['3'] for row in self.source[1:]]

    def output(self):
        with self.path.open('w', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(self.headers)
            writer.writerows(self.rows)
        return checker.read_output(self.path)

    def verdict(self, number):
        result = getattr(checker, f'check_q{number}')(self.output(), 'trial_lists')
        return result[0][0] if isinstance(result, list) else result[0]

    def test_correct_with_duplicate_header_and_nontrial_row(self):
        self.rows.insert(0, [''] * 10 + ['3'])
        self.assertEqual(self.verdict(1), 'PASS')
        self.assertEqual(self.verdict(2), 'PASS')

    def test_omitted_trial(self):
        self.rows.pop()
        self.assertEqual(self.verdict(2), 'FAIL')

    def test_duplicate_trial(self):
        self.rows.append(self.rows[-1])
        self.assertEqual(self.verdict(2), 'FAIL')

    def test_reordered_trials(self):
        self.rows[0], self.rows[1] = self.rows[1], self.rows[0]
        self.assertEqual(self.verdict(1), 'PASS')
        self.assertEqual(self.verdict(2), 'FAIL')

    def test_wrong_list_with_consistent_participant_label(self):
        for row in self.rows:
            row[0] = row[-1] = '6'
        self.assertEqual(self.verdict(1), 'FAIL')
        self.assertEqual(self.verdict(2), 'FAIL')

    def test_conflicting_participant_copies(self):
        self.rows[0][-1] = '6'
        self.assertEqual(self.verdict(1), 'FAIL')

    def test_changed_item(self):
        self.rows[0][3] = 'missing_item'
        self.assertEqual(self.verdict(1), 'FAIL')
        self.assertEqual(self.verdict(2), 'FAIL')

    def test_no_trials(self):
        self.rows = [[''] * 10 + ['3']]
        self.assertEqual(self.verdict(1), 'FAIL')
        self.assertEqual(self.verdict(2), 'FAIL')

    def test_equivalent_numeric_csv_formatting(self):
        self.rows[0][2] += '.0'
        self.assertEqual(self.verdict(2), 'PASS')


class A6CheckerTests(unittest.TestCase):
    frame = 1 / 60

    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / 'test.csv'
        self.log = self.path.with_name('test_frameIntervals.log')

    def trial(self, origin=10, dropped=True, prime_frames=9):
        fixation = [self.frame] * 30
        if dropped:
            fixation[5] *= 2
        prime = origin + sum(fixation)
        prime_to_target = [self.frame] * prime_frames
        target = prime + sum(prime_to_target)
        intervals = fixation + prime_to_target + [self.frame] * 30
        offset = origin + sum(intervals) + self.frame
        return ({'participant': '3', 'phase': 'experimental', 'trial_index': 1,
                 'frameRate': 60, 'fixation.started': origin, 'fixation.stopped': prime,
                 'prime_text.started': prime, 'prime_onset': prime, 'prime_text.stopped': target,
                 'target_text.started': target, 'target_onset': target, 'key_resp.started': target,
                 'blank.started': offset, 'blank.stopped': offset + 0.5,
                 'key_resp.keys': 'f', 'key_resp.rt': 0.5,
                 'key': 'f', 'timeout': 0, 'accuracy': 1, 'rt': 0.5,
                 'correct_response': 'word', 'prime': 'cue', 'target': 'word',
                 'prime_shown': 'cue', 'target_shown': 'WORD', 'soa': 150,
                 'dropped_frames': int(dropped)}, intervals)

    def output(self, rows, intervals=None):
        with self.path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        if intervals is not None:
            self.log.write_text(''.join(f'{x}\n' for x in intervals), encoding='utf-8')
        return checker.read_output(self.path)

    def test_logged_drop_changes_elapsed_time_but_not_flip_count(self):
        trial, intervals = self.trial()
        output = self.output([trial], intervals)
        fixation = checker.check_q5(output, 'trial_lists')[0]
        self.assertEqual(fixation[0], 'PASS')
        self.assertIn('1 had elapsed-time deviations', fixation[1])
        self.assertEqual(checker.check_i1(output, '')[-1][0], 'PASS')
        self.assertEqual(checker.check_i2(output, '')[-1][0], 'PASS')

    def test_wrong_prime_flip_count_fails_even_with_drop(self):
        trial, intervals = self.trial(prime_frames=10)
        self.assertEqual(checker.check_q5(self.output([trial], intervals), '')[1][0], 'FAIL')

    def test_same_total_with_wrong_per_trial_counts_fails(self):
        a, first = self.trial()
        b, second = self.trial(origin=13, dropped=False)
        a['dropped_frames'], b['dropped_frames'] = 0, 1
        result = checker.check_i2(self.output([a, b], first + second), '')
        self.assertEqual([verdict for verdict, _ in result], ['PASS', 'FAIL'])

    def test_dropped_frame_total_mismatch_fails(self):
        trial, intervals = self.trial()
        trial['dropped_frames'] = 0
        self.assertEqual(checker.check_i2(self.output([trial], intervals), '')[0], 'FAIL')

    def test_comma_separated_and_excess_interval_logs_fail(self):
        trial, intervals = self.trial()
        output = self.output([trial])
        self.log.write_text('0.016, 0.017', encoding='utf-8')
        self.assertEqual(checker.check_i1(output, '')[0], 'FAIL')
        output = self.output([trial], intervals + [0.5])
        self.assertEqual(checker.check_i1(output, '')[-1][0], 'FAIL')

    def test_corrupted_text_onset_and_keyboard_are_detected(self):
        trial, _ = self.trial()
        trial['prime_shown'] = 'prime'
        trial['prime_onset'] += 0.02
        trial['key_resp.started'] -= 0.65
        output = self.output([trial])
        for check in (checker.check_q7, checker.check_q8, checker.check_q9):
            with self.subTest(check=check.__name__):
                self.assertEqual(check(output, '')[0][0], 'FAIL')

    def test_invalid_response_and_wrong_accuracy_fail(self):
        trial, _ = self.trial()
        reference_row = [3, 'experimental', 1, 'ID1', 'word', 'cue', 'related', 150, 'word', 1]
        trial.update(dict(zip(checker.COLUMNS, reference_row)))
        for changes in ({'accuracy': 0}, {'rt': 2.01}, {'key': 'space'}, {'timeout': 1}):
            with self.subTest(changes=changes):
                output = self.output([{**trial, **changes}])
                self.assertEqual(checker.check_q10(output, self.path.parent)[0][0], 'FAIL')

    def test_missing_log_and_manual_evidence_are_undetermined(self):
        trial, _ = self.trial()
        trial.pop('dropped_frames')
        output = self.output([trial])
        self.assertEqual(checker.check_i1(output, '')[0], 'UNDETERMINED')
        self.assertEqual(checker.check_i2(output, '')[0], 'UNDETERMINED')
        self.assertEqual(checker.source_evidence(output, None), [])


if __name__ == '__main__':
    unittest.main()
