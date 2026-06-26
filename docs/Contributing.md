# Contributing to Grant Research Website

Thank you for your interest in contributing to the Grant Research Website project! We welcome contributions from everyone—whether you're fixing bugs, adding features, improving documentation, or sharing ideas.

This document provides guidelines and instructions for contributing to the project.


# Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful, constructive, and professional in all interactions.

Expected Behavior:

•
Be respectful and inclusive

•
Welcome diverse perspectives

•
Provide constructive feedback

•
Focus on what is best for the community

Unacceptable Behavior:

•
Harassment, discrimination, or offensive language

•
Trolling or intentional disruption

•
Unwelcome sexual attention or advances

•
Publishing private information without consent

Reporting Issues:
If you witness or experience unacceptable behavior, please report it by emailing [28886668+slee5777@users.noreply.github.com].




Getting Started

Prerequisites

•
Python 3.11+ – Required for running the project

•
Git – For version control

•
pip/pnpm – For dependency management

•
GitHub Account – For forking and submitting pull requests

# Setting Up Your Development Environment

1. Fork the Repository

```Bash
# Visit https://github.com/slee5777/grant-research-website
# Click "Fork" in the top-right corner
```

2. Clone Your Fork

```Bash
git clone https://github.com/YOUR-USERNAME/grant-research-website.git
cd grant-research-website
```

3. Add Upstream Remote

```Bash
git remote add upstream https://github.com/slee5777/grant-research-website.git
```

4. Create a Virtual Environment

```Bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

5. Install Dependencies

```Bash
pip install -r requirements.txt
```

6. Run Tests

```Bash
python -m pytest tests/
```

# Types of Contributions

🐛 Bug Reports

Found a bug? Please report it by opening a GitHub issue.

Before submitting:

•
Check existing issues to avoid duplicates

•
Test on the latest version

•
Include steps to reproduce the issue

•
Provide expected vs. actual behavior

Issue Template:

```Markdown
## Description
Brief description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version: 3.11.x
- OS: Windows/Mac/Linux
- Project version: [commit hash or version]

## Screenshots/Logs
[If applicable]
```


✨ Feature Requests

Have an idea for a new feature? We'd love to hear it!

Before submitting:

•
Check existing issues and discussions

•
Describe the use case and benefits

•
Provide examples if possible

Feature Request Template:

```Markdown
## Description
Clear description of the feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should this feature work?

## Alternative Solutions
Any alternatives you've considered?

## Additional Context
[Screenshots, examples, or other context]
```


📚 Documentation Improvements

Documentation is crucial! We welcome improvements to:

•
README.md

•
Docstrings in code

•
Configuration guides

•
Troubleshooting guides

•
Examples and tutorials

🔧 Code Contributions

Want to fix a bug or add a feature? Follow the workflow below.




# Development Workflow

1. Create a Feature Branch
```Bash


# Update your fork with latest changes
git fetch upstream
git rebase upstream/main

# Create a feature branch
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b fix/bug-description
```


Branch Naming Conventions:

•
feature/ – New features

•
fix/ – Bug fixes

•
docs/ – Documentation improvements

•
test/ – Test additions or improvements

•
refactor/ – Code refactoring

•
chore/ – Maintenance tasks

2. Make Your Changes

Code Style Guidelines:

•
Python: Follow PEP 8

•
Naming: Use descriptive names (e.g., parse_grant_deadline() not parse())

•
Comments: Write clear comments explaining why, not what

•
Type Hints: Use type hints for all function parameters and returns

•
Docstrings: Write comprehensive docstrings using Google style

Example:

```Python
def extract_grant_amount(text: str) -> Optional[float]:
    """
    Extract the grant amount from text.
    
    Handles various formats like "$50,000", "50000", "50k", etc.
    
    Args:
        text: The text to parse for grant amount
        
    Returns:
        The grant amount as a float, or None if not found
        
    Raises:
        ValueError: If the text contains an invalid amount format
        
    Example:
        >>> extract_grant_amount("Grant: $50,000")
        50000.0
    """
    # Implementation here
    pass
```


3. Write Tests

All new features and bug fixes must include tests.

```Bash
# Run existing tests
python -m pytest tests/

# Run tests with coverage
python -m pytest tests/ --cov=scripts --cov-report=html
```


Test Guidelines:

•
Write tests in tests/test_*.py files

•
Use descriptive test names: test_parse_grant_amount_with_comma_separator()

•
Test both success and failure cases

•
Aim for >80% code coverage

Example Test:

```Python
import pytest
from scripts.utils.amount_parser import extract_grant_amount

def test_extract_grant_amount_with_comma():
    """Test parsing amounts with comma separators."""
    assert extract_grant_amount("$50,000") == 50000.0

def test_extract_grant_amount_invalid():
    """Test that invalid amounts raise ValueError."""
    with pytest.raises(ValueError):
        extract_grant_amount("invalid amount")
```


4. Commit Your Changes

Commit Message Guidelines:

•
Use clear, descriptive messages

•
Start with a verb (Add, Fix, Update, Remove, etc.)

•
Keep the first line under 50 characters

•
Add a blank line, then detailed explanation if needed

•
Reference issue numbers: Fixes #123

Good Examples:

```Plain Text
Fix date parsing for invalid deadline formats

- Handle "TBD" and "TBA" as special cases
- Add unit tests for edge cases
- Fixes #45
```


```Plain Text
Add support for multiple funding sources

- Load funding sources from config/grants_sources.json
- Implement deduplication logic
- Update documentation
```


Bad Examples:

```Plain Text
fixed bug
updated code
changes
```


5. Push and Create a Pull Request

```Bash
# Push your branch
git push origin feature/your-feature-name

# Visit GitHub and create a Pull Request
```


Pull Request Template:

```Markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation improvement
- [ ] Code refactoring

## Related Issues
Fixes #[issue number]

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Added/updated tests
- [ ] All tests pass
- [ ] Tested locally

## Screenshots/Examples
[If applicable]

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```





## Code Review Process

What to Expect

1.
Automated Checks

•
GitHub Actions runs tests and linting

•
Coverage must be >80%

•
All tests must pass



2.
Maintainer Review

•
Code quality and style

•
Alignment with project goals

•
Documentation completeness

•
Test coverage



3.
Feedback & Iteration

•
Maintainers may request changes

•
Respond to feedback promptly

•
Update your PR accordingly



4.
Approval & Merge

•
Once approved, your PR will be merged

•
Your contribution will be credited



Tips for Getting Your PR Merged

•
✅ Keep PRs focused and reasonably sized

•
✅ Write clear commit messages

•
✅ Include comprehensive tests

•
✅ Update documentation

•
✅ Respond to feedback constructively

•
✅ Be patient—reviews take time




## Project Structure

See `Grant Research Website.md`

## Common Contribution Scenarios

Adding a New Grant Source

1. Update Configuration

```JSON
// config/grants_sources.json
{
  "new_source": {
    "name": "New Funding Source",
    "url": "https://example.com",
    "grants": [...]
  }
}
```




2. Create/Update Parser

• Add logic to `scripts/utils/` if needed

• Write tests for the parser



3. Update Documentation

•
Document the new source in README.md

•
Add examples to CONTRIBUTING.md



Fixing a Bug

1. Create an Issue (if not already created )

2. Create a Feature Branch from the issue

3. Write a Test that reproduces the bug

4. Fix the Bug

5. Verify Tests Pass

6. Submit a Pull Request

Improving Documentation

1. Identify the Gap

2. Create a Branch: docs/description

3. Make Changes to relevant files

4. Preview Locally if possible

5. Submit a Pull Request




## Testing Guidelines

Running Tests

```Bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_utilities.py

# Run with verbose output
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=scripts --cov-report=html
```


Writing Tests

•
Use pytest framework

•
Test file names: test_*.py

•
Test function names: test_*

•
One assertion per test when possible

•
Test both success and failure cases




## Documentation Guidelines

Docstring Format

Use Google-style docstrings:

```Python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief one-line description.
    
    Longer description explaining what the function does,
    including any important details or caveats.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When this error occurs
        TypeError: When this error occurs
        
    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```


README Sections

•
Project description

•
Installation instructions

•
Quick start guide

•
Configuration options

•
Usage examples

•
Contributing guidelines

•
License information




Getting Help

Resources

•
Documentation: See README.md

•
Issues: Check GitHub Issues

•
Discussions: Use GitHub Discussions

•
Email: [28886668+slee5777@users.noreply.github.com]

Questions?

•
Ask in GitHub Discussions

•
Comment on relevant issues

•
Email the maintainers

•
Don't hesitate to ask for help!




Recognition

We appreciate all contributions! Contributors will be:

•
✅ Listed in CONTRIBUTORS.md

•
✅ Credited in release notes

•
✅ Recognized in commit history

•
✅ Thanked publicly




License

By contributing to this project, you agree that your contributions will be licensed under the same dual license as the project (MIT License for community use, Commercial License for commercial use).

If you're contributing code that you own, you can choose which license applies. If you're contributing code from another project, ensure it's compatible with our licenses.




Thank You! 🙏

Thank you for contributing to the Grant Research Website project! Your efforts help make this project better for everyone in the community.




Additional Resources

•
GitHub Flow Guide

•
How to Write Good Commit Messages

•
PEP 8 Style Guide

•
Google Python Style Guide

•
Pytest Documentation

Last Updated: June 26, 2026
Maintained By: [Assisted Evolution]
Questions? Open an issue or start a discussion!
