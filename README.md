<h1><u>PAGE LOADER:</u></h1>

<h3>Hexlet tests and linter status:</h3>

[![Actions Status](https://github.com/Tragoedie/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/Tragoedie/python-project-lvl3/actions)
[![test_and_linter_check](https://github.com/Tragoedie/python-project-lvl3/actions/workflows/linter_test_check.yml/badge.svg)](https://github.com/Tragoedie/python-project-lvl3/actions/workflows/linter_test_check.yml)

<a href="https://codeclimate.com/github/Tragoedie/python-project-lvl3/maintainability"><img src="https://api.codeclimate.com/v1/badges/06b819f83205ba86dd05/maintainability" /></a>
<a href="https://codeclimate.com/github/Tragoedie/python-project-lvl3/test_coverage"><img src="https://api.codeclimate.com/v1/badges/06b819f83205ba86dd05/test_coverage" /></a>

<h1>Description:</h1>

Page loader downloads the web page to an existing folder allowing user to open it offline. 
This is achieved due to the fact that the program also downloads local resources of the web page to the computer.
Web page is downloaded to the directory chosen by user or by default to the current working directory.

<h2>Installation:</h2>

Use the package manager pip to install page loader:

```bash
  pip install --user git+https://github.com/Tragoedie/python-project-lvl3.git
```

<h3>Running:</h3>

Basic Page loader syntax looks like this:

```bash
page-loader --output url
```
output is an optional argument which means a folder where to download the page. 
By default it is to current working directory.

You can also recall about main features and syntax of a program using help command:
```bash
page-loader -h
```

<h2>Demo - asciinema demonstration:</h2>
How does it work:
<a href="https://asciinema.org/a/NlqofAb8BjvIOPUOJpJ1t7LM3" target="_blank"><img src="https://asciinema.org/a/NlqofAb8BjvIOPUOJpJ1t7LM3.svg" /></a>