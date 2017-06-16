# coding=utf-8
import unittest

from dupin.organisation import filter_excluded_repos

class TestOrganisation(unittest.TestCase):
    excludes = ["organisation/foo", "organisation/bar", "org2/baz"]

    def test_does_not_filter_if_excludes_is_none(self):
        repos = ["https://github.com/guardian/dupin.git"]
        self.assertEqual(filter_excluded_repos(repos, None), repos)

    def test_does_not_filter_if_excludes_is_empty(self):
        repos = ["https://github.com/guardian/dupin.git"]
        self.assertEqual(filter_excluded_repos(repos, []), repos)

    def test_filter_repos_inlcudes_unfiltered_repo(self):
        repos = ["https://github.com/guardian/dupin.git"]
        self.assertEqual(filter_excluded_repos(repos, self.excludes), repos)

    def test_filter_excludes_matching_repo(self):
        repos = ["https://github.com/guardian/dupin.git", "https://github.com/organisation/foo.git"]
        self.assertEqual(filter_excluded_repos(repos, self.excludes), ["https://github.com/guardian/dupin.git"])

    def test_filters_multiple_excluded_repos(self):
        repos = ["https://github.com/organisation/foo.git", "git@github.com:org2/baz.git"]
        self.assertFalse(filter_excluded_repos(repos, self.excludes))

    def test_filters_exact_match(self):
        self.assertFalse(filter_excluded_repos(["https://github.com/guardian/dupin.git"], ["https://github.com/guardian/dupin.git"]))
