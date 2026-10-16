# HToolboxGuides

Practical, beginner-friendly guides to choosing and using web-security and network-analysis tools in authorized test environments.

## What's inside

- `blog/the-hackers-toolkit.md` — comparison of Burp Suite, OWASP ZAP, Fiddler, and Wireshark.
- `comparison_cheat_sheet.md` — quick decision matrix for speed, investigation depth, learning curve, and cost.
- `examples/local_http_demo.py` — safe local-only HTTP example using `127.0.0.1`.
- `payment-fraud-defense/` — educational, local-only fraud-prevention demo using synthetic transaction events; includes regression tests.
- `github-api-repo-audit/` — read-only Python example using GitHub REST API to inspect public repository metadata.
- `GITHUB_SETUP.md` — repository maintenance notes.
- `CONTRIBUTING.md` — contribution and test instructions.
- `SECURITY.md` — responsible security-reporting guidance.

## Tool quick-start links

- [Burp Suite Community Edition](https://portswigger.net/burp/communitydownload)
- [OWASP ZAP](https://www.zaproxy.org/download/)
- [Fiddler](https://www.telerik.com/fiddler)
- [Wireshark](https://www.wireshark.org/download.html)

Install tools only from their official sites and follow each project's licensing and installation instructions. For proxy-based testing, configure a browser to use the proxy and install a proxy CA certificate only in a dedicated test browser/profile when needed.

## Run the local HTTP demo

Python 3.9+ is recommended. The script uses only the Python standard library.

```bash
python3 examples/local_http_demo.py
```

It starts a temporary HTTP server on `127.0.0.1:8765`, sends a GET request to that local server, prints the status and response, and shuts the server down. It does not send requests to external hosts.

## Run the payment-risk regression tests

```bash
python3 -m unittest discover -s payment-fraud-defense -p 'test_*.py' -v
```

These tests exercise educational scoring rules and ensure sensitive card-data columns and non-synthetic input are rejected. The demo does not process real payment credentials.

## Run the GitHub API example

```bash
python3 github-api-repo-audit/main.py Dav1dushka HToolboxGuides
```

This performs a read-only request for public repository metadata. Unauthenticated GitHub API rate limits apply.

## Suggested learning path

1. Learn HTTP basics and browser developer tools.
2. Use ZAP's passive features against a local demo application.
3. Use Burp Suite Community to inspect and manually replay requests in a permitted lab.
4. Use Fiddler for HTTP(S) debugging and Wireshark for packet/protocol analysis.
5. Explore the local fraud-prevention and GitHub API examples.
6. Record findings, reproduce them safely, and focus reports on impact and remediation.

## Responsible use

Use these tools only against systems you own or are explicitly authorized to test. Do not intercept other people's traffic, bypass access controls, or run active scans against targets without permission. Never put real payment credentials, access tokens, passwords, or other secrets in sample files or commits.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidance and [SECURITY.md](SECURITY.md) for responsible security reporting.

## License

This educational repository is provided under the MIT License; see [LICENSE](LICENSE).
