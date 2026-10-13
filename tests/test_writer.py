import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills' / 'distilly-qq' / 'tools'))
from qq_writer import build
from package import package


class WriterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.evidence = {'group_id': 123, 'user_id': 8, 'period': {'start': '2026-10-01', 'end': '2026-10-13'},
                         'sample_count': 1, 'seed': 'test', 'claims': [
                             {'claim': 'Likes examples', 'kind': 'inference', 'message_ids': ['snowluma:1']}],
                         'limitations': ['One recorded message only']}
        self.source = [{'record_type': 'metadata', 'group_id': 123},
                       {'record_type': 'message', 'role': 'selected', 'sender_id': 8,
                        'message_id': 'snowluma:1', 'time': '2026-10-01T12:00:00+08:00'},
                       {'record_type': 'message', 'role': 'context', 'sender_id': 9,
                        'message_id': 'snowluma:2', 'time': '2026-10-01T12:00:01+08:00'}]

    def tearDown(self):
        self.tmp.cleanup()

    def create(self, output='profile'):
        return build(123, 8, '小明: "样例"', '## Interests\nExamples.', '## Tone\nBrief.',
                     self.evidence, self.source, self.root / output)

    def test_generated_artifacts_and_no_overwrite(self):
        result = self.create()
        self.assertFalse(result['installed'])
        self.assertEqual(result['skill_name'], 'qq-persona-123-8')
        skill = Path(result['skill_file']).read_text()
        self.assertIn('snowluma:1', skill)
        self.assertNotIn('snowluma:2', skill)
        self.assertIn('name: qq-persona-123-8', skill)
        self.assertIn('explicit request', skill)
        self.assertNotIn('always take priority', skill)
        for name in ('SKILL.md', 'work_skill.md', 'persona_skill.md'):
            self.assertIn('Host instructions', (self.root / 'profile' / name).read_text())
        self.assertEqual(json.loads((self.root / 'profile/evidence.json').read_text())['sample_count'], 1)
        with self.assertRaises(ValueError):
            self.create()

    def test_evidence_checks_target_scope_counts_and_dates(self):
        changes = [lambda: self.evidence.update(group_id=999),
                   lambda: self.evidence.update(sample_count=2),
                   lambda: self.evidence['claims'][0].update(message_ids=['snowluma:2']),
                   lambda: self.source[1].update(sender_id=9),
                   lambda: self.source[1].update(time='2026-09-01T12:00:00+08:00')]
        original_evidence, original_source = json.dumps(self.evidence), json.dumps(self.source)
        for change in changes:
            self.evidence, self.source = json.loads(original_evidence), json.loads(original_source)
            change()
            with self.assertRaises(ValueError):
                self.create()
            self.assertFalse((self.root / 'profile').exists())

    def test_clean_single_skill_archive(self):
        destination = self.root / 'bundle.zip'
        count = package(destination)
        with zipfile.ZipFile(destination) as archive:
            names = archive.namelist()
            self.assertEqual(len(names), count)
            self.assertEqual(sum(n.endswith('/SKILL.md') for n in names), 1)
            self.assertIn('distilly-qq/tools/upstream/skill_writer.py', names)
            self.assertIn('distilly-qq/LICENSE', names)
            self.assertFalse(any('.git' in n or '__pycache__' in n or '/tests/' in n for n in names))
            self.assertLess(count, 100)


if __name__ == '__main__':
    unittest.main()
