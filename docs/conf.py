# -*- coding: utf-8 -*-
import os
import sys
import sphinx_rtd_theme


project = u"restible"
copyright = u"2016-2017, Mateusz 'novo' Klos"
author = u"Mateusz 'novo' Klos"


def repo_path(path):
    ret = os.path.join(os.path.dirname(__file__), '..', path)
    return os.path.normpath(ret)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

sys.path.insert(0, repo_path('src'))
sys.path.insert(1, repo_path('.'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
]
import restible
version = restible.__version__
release = restible.__version__
doctest_test_doctest_blocks='default'
templates_path = [repo_path('docs/_templates')]
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = [
    '_build',
    'env',
    'tmp',
    '.tox',
    'Thumbs.db',
    '.DS_Store'
]
todo_include_todos = False
intersphinx_mapping = {'https://docs.python.org/': None}

default_role = 'any'
pygments_style = 'monokai'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme = "sphinx_rtd_theme"
html_static_path = [repo_path('docs/assets')]
htmlhelp_basename = 'restible'

latex_elements = {}
latex_documents = [
    (master_doc, 'restible.tex', 'restible Documentation',
     'Mateusz \'novo\' Klos', 'manual'),
]
man_pages = [
    (master_doc, 'restible', 'restible Documentation', [author], 1)
]
texinfo_documents = [
    (master_doc, 'restible', 'restible Documentation',
     author, 'restible', 'One line description of project.',
     'Miscellaneous'),
]
