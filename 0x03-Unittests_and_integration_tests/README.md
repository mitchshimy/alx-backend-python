# Python Unit Testing Project

## Project Overview

This project contains unit and integration tests for utility functions and the `GithubOrgClient` class, following best practices in Python testing using `unittest`, `unittest.mock`, and `parameterized`. 

The tests are designed to:

- Validate functionality of nested data access utilities.
- Mock and patch HTTP requests to avoid external dependencies.
- Test memoization decorators for caching behavior.
- Verify client interactions with the GitHub API using mocked data.
- Provide integration testing with fixtures for external API responses.

## Project Structure

- `test_utils.py`  
  Contains tests for utility functions such as `access_nested_map`, `get_json`, and the `memoize` decorator.  
  - Parameterized tests for different inputs and exceptions  
  - Mocked HTTP calls  
  - Memoization behavior testing

- `test_client.py`  
  Contains tests for the `GithubOrgClient` class methods.  
  - Tests for the `org` property with mocked JSON responses  
  - Tests for memoized properties and repository listing  
  - License checking method tests with parameterized inputs

- `fixtures.py`  
  Provides fixture data used for integration tests in `TestIntegrationGithubOrgClient`.

- `test_integration.py`  
  Contains integration tests for `GithubOrgClient.public_repos` with external API calls mocked to use fixture data.

## Testing Requirements

- Python 3.7+  
- `unittest` (built-in)  
- `parameterized` (install via `pip install parameterized`)  
- All tests follow PEP8 style guidelines using `pycodestyle` 2.5  
- All source files are executable and include documentation for modules, classes, and methods.

