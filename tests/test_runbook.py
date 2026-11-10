from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock
from runbook import Chunk, Index, answer, load_chunks


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.index = Index(load_chunks(Path(__file__).resolve().parents[1] / 'runbooks'))

    def test_relevant_section_first(self):
        self.assertEqual(self.index.search('S3 AccessDenied')[0]['section'], 'S3 AccessDenied')

    def test_unknown_query_abstains(self):
        matches = self.index.search('zyxwvu')
        self.assertEqual(matches, [])
        client = Mock()
        self.assertIn('No matching', answer('zyxwvu', matches, client, 'model'))
        client.converse.assert_not_called()

    def test_empty_and_stopword_queries(self):
        for query in ('', 'the and of'):
            self.assertEqual(self.index.search(query), [])

    def test_limit_validated(self):
        with self.assertRaises(ValueError):
            self.index.search('S3', 0)

    def test_chunks_are_bounded_and_sources_relative(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'large.md').write_text('# Title\n' + 'word ' * 400)
            chunks = load_chunks(directory)
            self.assertEqual(len(chunks), 3)
            self.assertTrue(all(len(c.text.split()) <= 180 for c in chunks))
            self.assertEqual(chunks[0].source, 'large.md')

    def test_empty_docs_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                load_chunks(directory)

    def test_bedrock_uses_grounding_and_citations(self):
        client = Mock()
        client.converse.return_value = {'output': {'message': {'content': [{'text': 'Check policy [1].'}]}}}
        result = answer('S3', self.index.search('S3'), client, 'example-model')
        self.assertEqual(result, 'Check policy [1].')
        request = client.converse.call_args.kwargs
        self.assertEqual(request['modelId'], 'example-model')
        self.assertIn('untrusted', request['system'][0]['text'])

    def test_zero_token_chunk_is_safe(self):
        self.assertEqual(Index([Chunk('x', '', '')]).search('hello'), [])


if __name__ == '__main__':
    unittest.main()
