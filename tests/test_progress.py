from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import AsyncMock, Mock, patch

from scripts.update_progress import archive_ids, chart_svg, progress_block, game_results, result_counts
from scripts.update_progress import read_archive


class ProgressTests(unittest.TestCase):
    def test_archive_gaps_and_duplicates(self):
        self.assertEqual(archive_ids('Archive #1 Cherry #73 Frog #73 Frog #233 Stone'), {1, 73, 233})

    def test_empty_archive_fails(self):
        with self.assertRaises(ValueError):
            archive_ids('Loading…')

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
                             ['Hard', 'Easy only', 'Incomplete', 'Broken', 'Incomplete', 'Easy only'])
            counts = result_counts(results, 7)
            self.assertEqual(counts, {'Hard': 1, 'Easy only': 2, 'Broken': 1, 'Incomplete': 3})
            block = progress_block(results, 7)
            self.assertIn('**3 / 7 games completed**', block)
            self.assertIn('**6 attempted**', block)
            self.assertIn('**1 broken**', block)
            self.assertIn('Average best score: 166.0 characters', block)
            self.assertNotIn('| Game |', block)
            import xml.etree.ElementTree as ET
            chart = chart_svg(counts)
            ET.fromstring(chart)
            self.assertIn('Hard: 1, Easy only: 2, Broken: 1, Incomplete: 3', chart)

    def test_repo_ids_do_not_depend_on_archive_ids(self):
        results = {9999: {"best": 100, "status": "Hard", "broken": False}}
        counts = result_counts(results, 234)
        self.assertEqual(counts, {"Hard": 1, "Easy only": 0, "Broken": 0, "Incomplete": 233})
        self.assertIn('**1 attempted**', progress_block(results, 234))
        for color in ['#3b82f6', '#22c55e', '#eab308', '#ef4444']:
            self.assertIn(color, chart_svg(counts))



class ArchiveReadTests(unittest.IsolatedAsyncioTestCase):
    async def test_reads_until_scroll_position_and_entries_stabilize(self):
        entries = Mock()
        entries.first.wait_for = AsyncMock()
        labels = Mock()
        entries.get_by_text.return_value = labels
        labels.all_text_contents = AsyncMock(side_effect=[
            ['Pydle #1'], ['Pydle #1', 'Pydle #2'],
            ['Pydle #1', 'Pydle #2'], ['Pydle #1', 'Pydle #2'],
            ['Pydle #1', 'Pydle #2'],
        ])
        archive = Mock()
        archive.get_by_role.return_value.filter.return_value = entries
        archive.evaluate = AsyncMock(side_effect=[
            [[50, 200, 100]], [[100, 200, 100]], [[100, 200, 100]],
            [[100, 200, 100]], [[100, 200, 100]],
        ])
        with patch('scripts.update_progress.asyncio.sleep', new_callable=AsyncMock):
            self.assertEqual(await read_archive(archive), {1, 2})
        self.assertEqual(archive.evaluate.await_count, 5)


if __name__ == '__main__':
    unittest.main()
