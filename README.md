# Abstract
**Web operation automation script**

This is a simple script to turn on the cardless mode for the container instance to be released in [AutoDL](https://www.autodl.com)

## Python environment

> [playwright docs](https://playwright.dev/python/docs/intro)

`pip install pytest-playwright`
`playwright install`

## Run

`python autodl.py --account <account> --password <password> --time <time>`
- time: the time(hours) to release the container instance

eg: `python autodl.py --account 123456789 --password 123456 --time 3` is to turn on the cardless mode for the container instance that will be released in 3 hours. Then shut down the container immediately.