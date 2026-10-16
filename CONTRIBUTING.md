# Contributing

Thanks for helping improve HToolboxGuides. Contributions should make the examples clearer, safer, more accurate, or easier to reproduce.

## Before opening a pull request

1. Describe the user problem and proposed change.
2. Keep examples scoped to systems you own or have explicit permission to test.
3. Use fictional/synthetic values; never commit credentials, tokens, full payment-card data, CVV/CVC, private logs, or customer information.
4. Run relevant checks locally:
   - `python3 -m unittest discover -s payment-fraud-defense -p 'test_*.py' -v`
   - `python3 examples/local_http_demo.py`
5. Explain what changed, how it was tested, and any limitations.

## Pull request checklist

- [ ] The change has a clear, focused purpose.
- [ ] Documentation and examples match the behavior.
- [ ] Tests pass or a reason for missing tests is included.
- [ ] No secrets or personal data are included.
- [ ] Security-sensitive examples remain confined to authorized labs.

## Tone and collaboration

Be respectful, describe issues clearly, and prefer constructive suggestions. Please do not open pull requests just to manipulate achievement counters; each PR should make a useful contribution.
