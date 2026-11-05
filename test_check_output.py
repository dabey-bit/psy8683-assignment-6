"""Negative controls for the Q1-Q2 checker; no screen or participant run."""
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


if __name__ == '__main__':
    unittest.main()
