# coding=utf-8
import unittest
from textwrap import dedent

from dupin.trufflehog.trufflehog import focus_diff, bcolors


class TestTruffleHog(unittest.TestCase):
    search = "!"

    def test_returns_empty_string_if_search_not_found(self):
        text = dedent("""\
        Test text
        No line matches""")
        self.assertEqual(focus_diff(text, self.search), "")

    def test_can_search_for_ctrl_char(self):
        text = bcolors.WARNING + " Should match"
        self.assertEqual(focus_diff(text, bcolors.WARNING), text)

    def test_returns_context_for_matching_line(self):
        text = dedent("""\
        Line 1
        Line 2
        Line 3
        This line matches!
        Additional context
        Still printed
        Not this""")
        expected = dedent("""\
        Line 2
        Line 3
        This line matches!
        Additional context
        Still printed""")
        self.assertEqual(focus_diff(text, self.search), expected)

    def test_does_not_overlap_context(self):
        text = dedent("""\
        Line 1
        Line 2
        This line matches!
        Another match!
        Additional context
        Still printed
        Not this""")
        expected = dedent("""\
        Line 1
        Line 2
        This line matches!
        Another match!
        Additional context
        Still printed""")
        self.assertEqual(focus_diff(text, self.search), expected)

    def test_does_not_overlap_multiple_contexts(self):
        text = dedent("""\
            not printed
            context 1
            context 2
            This line matches!
            context 3
            context 4
            not printed
            context 5
            context 6
            Another match!
            Match again!
            context 7
            context 8
            not printed""")
        expected = dedent("""\
            context 1
            context 2
            This line matches!
            context 3
            context 4
            context 5
            context 6
            Another match!
            Match again!
            context 7
            context 8""")
        self.assertEqual(focus_diff(text, self.search), expected)