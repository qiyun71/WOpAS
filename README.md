# Abstract
**Web operation automation script**

对[AutoDL](https://www.autodl.com)中即将释放的实例进行重启

*当[AutoDL](https://www.autodl.com)中实例即将释放但想要将其保留时，需要对实例进行重启操作。如果实例太多逐个手动重启过于繁琐，可以通过该脚本进行自动化重启操作*

## 环境配置

> [playwright docs](https://playwright.dev/python/docs/intro)

`pip install pytest-playwright`
`playwright install`

## 运行

`python autodl.py --account <account> --pwd <password>`