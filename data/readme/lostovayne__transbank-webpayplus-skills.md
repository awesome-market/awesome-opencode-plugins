# Transbank WebpayPlus Skills

Professional integration skill for **Transbank WebpayPlus REST API** — the leading payment gateway in Chile.

[![Skills](https://img.shields.io/badge/skills.sh-install-blue)](https://skills.sh/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

## What's Inside

Complete, production-ready skill for integrating WebpayPlus with any AI coding agent:

- **Full transaction flow** — create, redirect, commit, status, refund, capture
- **WebpayPlus Mall** — multi-store transactions with child commerce codes
- **6 SDK languages** — Node.js, Python, PHP, Java, .NET, Ruby
- **REST API reference** — every endpoint with curl examples and schemas
- **Test cards** — all integration environment cards with expected results
- **Error codes** — VCI, response_code, HTTP errors, refund/capture specific codes
- **Security guide** — TLS 1.2, PCI compliance, OWASP, credential management
- **Production checklist** — step-by-step go-live validation with Transbank

## Install

```bash
npx skills add lostoVayne/transbank-webpayplus-skills@transbank-webpayplus
```

Or browse: <https://skills.sh/lostoVayne/transbank-webpayplus-skills/transbank-webpayplus>

## Structure

```
transbank-webpayplus/
├── SKILL.md                        # Core skill contract (triggers, rules, quick reference)
├── assets/
│   └── env-template.env            # Environment variables template
└── references/
    ├── api-endpoints.md            # Full REST API specs with curl examples
    ├── mall-transactions.md        # Multi-store Mall integration
    ├── error-codes.md              # VCI, response_code, HTTP, refund/capture errors
    └── production-checklist.md     # Validation and go-live steps
```

## Usage Examples

Once installed, any AI agent can help you:

```
"Integrate WebpayPlus in my Next.js app"
"Create a payment flow with Python Django"
"Why is my transaction returning response_code -5?"
"How do I refund a WebpayPlus Mall transaction?"
"Set up WebpayPlus for production"
```

## Supported Languages

| Language | Package | Install |
| --- | --- | --- |
| Node.js | `transbank-sdk` | `npm install transbank-sdk` |
| Python | `transbank-sdk` | `pip install transbank-sdk` |
| PHP | `transbank/transbank-sdk` | `composer require transbank/transbank-sdk:^5.0` |
| Java | `transbank-sdk-java` | Maven dependency |
| .NET | `TransbankSDK` | `Install-Package TransbankSDK` |
| Ruby | `transbank-sdk` | `gem install transbank-sdk` |

## Official Resources

- [Transbank Developers](https://www.transbankdevelopers.cl)
- [WebpayPlus API Reference](https://www.transbankdevelopers.cl/referencia/webpay)
- [SDK GitHub Repos](https://github.com/TransbankDevelopers)
- [Postman Collection](https://documenter.getpostman.com/view/12687204/TVRoYmUj)
- [Integration Examples](https://proyectos-ejemplo.transbankdevelopers.cl/)

## License

Apache-2.0
