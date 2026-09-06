# Python Automation

[![E2E Tests](https://github.com/Arshdeepdubey/Python-Automation/actions/workflows/e2e-tests.yml/badge.svg)](https://github.com/Arshdeepdubey/Python-Automation/actions/workflows/e2e-tests.yml)

End-to-end UI test automation, written in Python with Selenium and pytest, against
[Practice Software Testing (Toolshop)](https://practicesoftwaretesting.com) — an
open-source e-commerce demo app ([testsmith-io/practice-software-testing](https://github.com/testsmith-io/practice-software-testing))
built specifically for automation practice.

## Contents

- [`shopping-e2e-tests/`](shopping-e2e-tests) — the Selenium + pytest test suite. See its
  [README](shopping-e2e-tests/README.md) for setup and usage.

## CI/CD

A GitHub Actions workflow ([`.github/workflows/e2e-tests.yml`](.github/workflows/e2e-tests.yml))
runs the full suite headlessly on every push to any branch, every pull request, and on
demand. It installs dependencies, runs `pytest` against the live site, and uploads the
HTML report (and failure screenshots, if any) as workflow artifacts.

## Why this site

`demo.opencart.com` was considered but sits behind Cloudflare bot-verification, which
blocks Selenium the same way it blocks any other bot — so it was ruled out in favor of a
site built for this purpose, with stable `data-test` locators throughout.
