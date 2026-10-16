# HToolboxGuides

Practical, beginner-friendly guides to choosing and using web-security and network-analysis tools in authorized test environments.

## What's inside

- `blog/the-hackers-toolkit.md` — an article comparing Burp Suite, OWASP ZAP, Fiddler, and Wireshark.
- `comparison_cheat_sheet.md` — a quick decision matrix for speed, depth, learning curve, and cost.
- `examples/local_http_demo.py` — a safe local-only HTTP example that starts a server on 127.0.0.1 and sends a sample GET request.
- `GITHUB_SETUP.md` — notes for maintaining this repository.

## Tool quick-start links

- [Burp Suite Community Edition](https://portswigger.net/burp/communitydownload)
- [OWASP ZAP](https://www.zaproxy.org/download/)
- [Fiddler](https://www.telerik.com/fiddler)
- [Wireshark](https://www.wireshark.org/download.html)

Install tools only from their official sites and follow each project's licensing and installation instructions. For proxy-based testing, configure a browser to use the proxy and install a proxy CA certificate only in a dedicated test browser/profile when needed.

## Run the local demo

Python 3.9+ is recommended. The script uses only the Python standard library.

```bash
python3 examples/local_http_demo.py
```

It starts a temporary HTTP server on `127.0.0.1:8765`, sends a GET request to that local server, prints the status and response, and shuts the server down. It does not send requests to external hosts.

## Suggested learning path

1. Learn HTTP basics and browser developer tools.
2. Use ZAP's passive features against a local demo application.
3. Use Burp Suite Community to inspect and manually replay requests in a permitted lab.
4. Use Fiddler for HTTP(S) debugging and Wireshark for packet/protocol analysis.
5. Record findings, reproduce them safely, and focus reports on impact and remediation.

## Responsible use

Use these tools only against systems you own or are explicitly authorized to test. Do not intercept other people's traffic, bypass access controls, or run active scans against targets without permission.

## License

This educational repository is provided under the MIT License; see [LICENSE](LICENSE).
