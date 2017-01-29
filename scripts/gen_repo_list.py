#!/usr/bin/env python

import re
import github
global g


def make_github_agent(user=None, password=None):
    """ Create github agent to auth """
    if not user:
        return github.Github()
    else:
        return github.Github(user, password)


def get_org_repos(org_name):
    org = g.get_organization(org_name)
    for repo in org.get_repos():
        yield repo.name


def print_repo_config(org, repo):
    formula_name = re.match('^salt-formula-(.*)?', repo).group(1)
    print "[%s/%s]" % (org, formula_name)
    print "checkout = git_checkout %s" % (org, formula_name)
    print "skip = lazy"
    print ""

g = make_github_agent()

repos = []
for repo in get_org_repos("salt-formulas"):
    if not repo.startswith('salt-formula-'):
        continue
    if repo not in repos:
        repos.append(repo)
        print_repo_config("salt-formulas", repo)
    else:
        print "Repository %s present in different organization" % repo