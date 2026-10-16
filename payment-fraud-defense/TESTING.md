# Testing

From the repository root, run:

```bash
python3 -m unittest discover -s payment-fraud-defense -p 'test_*.py' -v
```

The tests cover illustrative score rules, score-band boundaries, synthetic-data enforcement, and rejection of sensitive card-data columns. The fixtures are fictional; no network requests are made.
