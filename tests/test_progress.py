from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.update_progress import archive_ids, chart_svg, attempt_ids, completed_ids, progress_block, game_results, result_counts


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

    def test_completed_solution_replaces_broken_attempt(self):
        with TemporaryDirectory() as directory:
            for name in ['#1 Working.py', '#1 Working (broken).py', '#2 Mug (broken).py']:
                Path(directory, name).touch()
            self.assertEqual(attempt_ids(Path(directory)), ({1}, {2}))

    def test_best_saved_attempt_and_strict_limits(self):
        with TemporaryDirectory() as directory:
            files = {
                '#1 Multiple.py': '#First solution 180/250\npydle()\n#Final solution 124/250\npydle()\n',
                '#2 Boundary.py': '#Solution 125/250\npydle()\n#Final 111/250\n',
                '#3 Boundary.py': '#Solution 250/250\npydle()\n',
                '#4 Broken (broken).py': '#Solution 80/250\npydle()\n',
                '#5 Missing score.py': 'pydle()\n',
                '#1 Duplicate.py': '#Solution 200/250\npydle()\n',
                '#6 Easy.py': '#Solution 249/250\npydle()\n',
            }
            for name, code in files.items():
                Path(directory, name).write_text(code)
            results = game_results(Path(directory))
            self.assertEqual(results[1]['best'], 124)
            self.assertEqual(results[2]['best'], 125)
            self.assertEqual([results[i]['status'] for i in range(1, 7)],
                             ['Hard', 'Easy only', 'Incomplete', 'Incomplete', 'Incomplete', 'Easy only'])
            counts = result_counts(results, set(range(1, 8)))
            self.assertEqual(counts, {'Hard': 1, 'Easy only': 2, 'Incomplete': 3, 'Unattempted': 1})
            block = progress_block(results, set(range(1, 8)))
            self.assertIn('**3 / 7 games completed**', block)
            self.assertIn('**6 attempted**', block)
            self.assertIn('(1 broken)', block)
            import xml.etree.ElementTree as ET
            chart = chart_svg(counts)
            ET.fromstring(chart)
            self.assertIn('Hard: 1, Easy only: 2, Incomplete: 3, Unattempted: 1', chart)


if __name__ == '__main__':
    unittest.main()
