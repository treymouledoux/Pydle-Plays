from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.update_progress import archive_ids, chart_svg, attempt_ids, completed_ids, progress_block


class ProgressTests(unittest.TestCase):
    def test_archive_gaps_and_duplicates(self):
        self.assertEqual(archive_ids('Archive #1 Cherry #73 Frog #73 Frog #233 Stone'), {1, 73, 233})

    def test_empty_archive_fails(self):
        with self.assertRaises(ValueError):
            archive_ids('Loading…')

    def test_attempts_deduplicate_and_exclude_broken(self):
        with TemporaryDirectory() as directory:
            for name in ['#1 Cherry.py', '#1 Other.py', '#2 Mug (broken).py', 'helper.py', '#3.txt']:
                Path(directory, name).touch()
            self.assertEqual(completed_ids(Path(directory)), {1})

    def test_percentage_uses_intersection(self):
        block = progress_block({1, 99}, {1, 2, 4, 8})
        self.assertIn('**25.0%**', block)
        self.assertIn('**1 / 4 games completed**', block)

    def test_completed_solution_replaces_broken_attempt(self):
        with TemporaryDirectory() as directory:
            for name in ['#1 Working.py', '#1 Working (broken).py', '#2 Mug (broken).py']:
                Path(directory, name).touch()
            self.assertEqual(attempt_ids(Path(directory)), ({1}, {2}))

    def test_pie_slices_and_attempt_total(self):
        block = progress_block({1, 99}, {1, 2, 3, 4}, {1, 2, 98})
        self.assertIn('**2 attempted** · **1 broken**', block)
        self.assertIn('assets/pydle-progress.svg', block)
        import xml.etree.ElementTree as ET
        chart = chart_svg(1, 1, 2)
        ET.fromstring(chart)
        self.assertIn('Completed: 1, Broken attempts: 1, Unattempted: 2', chart)
        self.assertIn('25.0% completed', chart)


if __name__ == '__main__':
    unittest.main()
