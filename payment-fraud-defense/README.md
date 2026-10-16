# Payment Fraud Defense — synthetic-data demo

A small, local-only educational example of how a payment-risk review might combine several transaction signals. It is designed for fraud-prevention learning, not card testing.

## Safety and scope

- Uses **synthetic sample transaction events only**.
- Does not accept or process PAN/full card numbers, CVV/CVC values, track data, card dumps, or BIN lists.
- Makes no network requests and needs no API key.
- Produces a review queue, not an authorization or decline decision.
- Rules and thresholds are illustrative. They are not a production fraud model.

Do not put real customer data into this demo. Production systems should minimize and tokenize sensitive payment data, comply with PCI DSS and applicable privacy laws, and use a payment processor's approved risk APIs.

## Requirements

Python 3.9+; standard library only.

## Run

From this directory:

```bash
python3 main.py
```

Or provide an explicit synthetic CSV:

```bash
python3 main.py --input sample_transactions.csv --output risk_report.csv
```

The program checks that every row is marked `synthetic_data=true` and rejects files containing columns commonly used for sensitive card data, including `pan`, `card_number`, `cvv`, `cvc`, `track_data`, and `bin`.

## Example output

The script scores synthetic transaction events based on signals such as repeated attempts, account age, billing/IP country mismatch, AVS mismatch, and amount. The resulting `risk_report.csv` contains only a synthetic transaction ID, score, band, and explanatory reasons.

## Important limitations

A rule-based score can be wrong and can unfairly affect legitimate users. Never automatically reject a real payment based only on this example. Calibrate models on properly governed data, measure false-positive rates, provide review and appeal paths, and test for bias.

## Further reading

- [PCI Security Standards Council](https://www.pcisecuritystandards.org/)
- [OWASP Automated Threats to Web Applications](https://owasp.org/www-project-automated-threats-to-web-applications/)
