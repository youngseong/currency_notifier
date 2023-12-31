# Currency Notifier

It alerts the currency exchange rate via a messaging app (only Telegram Bot is supported currently.)

<img src="images/output.png" width=300/>

## Workflow

It is automated to check a currency exchange rate at a planned schedule (e.g., every hour.) It is compatible with AWS and GitHub Workflow. Though AWS runs the system more punctually, I prefer GitHub Workflow as it's free of charge.

### AWS Workflow Diagram

<img src="images/diagram.png" width=400/>

## Prerequisites

- Python 3.8+
  - [requests](https://pypi.org/project/requests/)
  - [python-telegram-bot](https://pypi.org/project/python-telegram-bot/)
- Telegram Bot
- API Credentials
  - [Geo API Key](https://currency.getgeoapi.com/) for checking the currency rate
  - Telegram Access Token for notification
