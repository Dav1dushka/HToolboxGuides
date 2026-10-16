# HToolboxGuides — comparison cheat sheet

> The right tool depends on the question being asked. This table is a practical rule of thumb, not a benchmark; performance varies with project size, configuration, and user experience.

| Tool | Main role | Speed for initial overview | Investigation depth | Learning curve | Cost model | Best fit |
|---|---|---:|---:|---|---|---|
| Burp Suite Community / Professional | Intercepting proxy and hands-on web application testing | Medium | High for manual testing; automated capabilities vary by edition | Medium–high | Community edition free; Professional paid | Manually examining HTTP requests, parameters, sessions, and API behavior |
| OWASP ZAP | Web application proxy and security scanner | High for an initial baseline | Medium; deeper results require manual validation and configuration | Medium | Free and open source | Repeatable baseline scans and automation in a test pipeline |
| Fiddler | HTTP(S) debugging proxy | High for HTTP-focused debugging | High for request/response troubleshooting; not a general packet analyzer | Low–medium | Product/edition dependent | Debugging application traffic, headers, bodies, and client-server behavior |
| Wireshark | Packet capture and protocol analysis | Medium; captures may need filtering | Very high at the packet and protocol level | Medium–high | Free and open source | Understanding DNS, TCP/TLS handshakes, retransmissions, and traffic flow |

## Practical distinctions

- **Burp Suite** is useful when a person needs to understand and manipulate web requests manually. Features differ between Community and Professional editions.
- **OWASP ZAP** is a good first choice for repeatable automated baselines. Automated scanners can produce false positives and miss logic flaws; verify results manually.
- **Fiddler and Wireshark are not interchangeable.** Fiddler is aimed at HTTP(S) debugging through a proxy; Wireshark analyzes captured network packets and many protocols.
- HTTPS packet captures usually do not reveal application content without appropriate, authorized decryption setup. Wireshark alone does not magically decrypt TLS.
- None of these tools proves an application is secure simply because a scan completes without findings.

## Choose by objective

- **Need a fast first pass?** Start with ZAP's baseline/automated features on an authorized target.
- **Need to understand a web request deeply?** Use Burp Suite or ZAP as an intercepting proxy.
- **Need to debug an HTTP(S) client?** Use Fiddler.
- **Need to inspect DNS, TCP, TLS negotiation, or retransmissions?** Use Wireshark.

## Safe starting checklist

1. Use a local lab or a target you are explicitly authorized to test.
2. Start with passive observation and low-impact settings.
3. Keep test data fictional; never capture real credentials or payment data.
4. Reproduce each finding and document remediation.
5. Remove temporary proxy certificates and test configurations when finished.

## Official documentation

- [Burp Suite documentation](https://portswigger.net/burp/documentation)
- [OWASP ZAP documentation](https://www.zaproxy.org/docs/)
- [Fiddler documentation](https://docs.telerik.com/fiddler)
- [Wireshark documentation](https://www.wireshark.org/docs/)
