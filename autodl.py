"""
功能: 对AutoDL中即将释放的容器实例进行无卡模式开机 --> 重新计时
作者: qiyun71
时间: 2023-10-06

English:
Function: Turn on the cardless mode for the container instance to be released in AutoDL --> Restart the timer
Author: qiyun71
Time: 2023-10-06
"""

import argparse
from playwright.sync_api import sync_playwright, expect
import re

def start_wogpu_shutdown(page, remain_time):
    # 无卡模式开机
    button = page.locator(".el-table__row").filter(has_text=remain_time).get_by_role("button",name = "更多", exact=True).nth(0)
    aria_controls_value = button.get_attribute("aria-controls")
    button.hover(timeout=3000)
    # print(aria_controls_value)
    page.locator(f"#{aria_controls_value}").get_by_text("无卡模式开机").click()
    page.get_by_role("button",name = "确定", exact=True).click()
    page.wait_for_timeout(3000)
    
    # 关机
    locator_sd = page.locator(".el-table__row").filter(has_text="运行中")
    expect(locator_sd).to_be_visible(timeout=50000)	
    locator_sd.get_by_role("button",name = "关机", exact=True).click()
    page.get_by_role("button",name = "确定", exact=True).click()
    print(f"重启成功: {remain_time} \t aria_controls_value id为 {aria_controls_value}")

def main(account, pwd, headless = True, remain_thre=6):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless,slow_mo=50)
        page = browser.new_page()

        # 登录
        page.goto("https://www.autodl.com/")
        page.get_by_text("控制台").click()
        page.get_by_placeholder("请输入手机号").fill(account)
        page.get_by_placeholder("请输入密码").fill(pwd)
        page.wait_for_timeout(1000)
        # page.screenshot(path="AutoDL.png")
        page.get_by_role("button", name="登录", exact=True).click()
        
        # 进入容器实例
        page.get_by_role("menuitem", name="容器实例").locator("span").click()
        page.get_by_placeholder("请选择").click()
        page.get_by_text("100条/页").click()
        
        # 选中即将释放的实例
        table = page.locator(".el-table__row")
        text_table = table.all_text_contents()
        print(len(text_table))

        pattern = re.compile(r"\d+天\d+小时后释放")
        for i,string in enumerate(text_table):
            match = re.search(pattern, string)
            # print(i, match.group())
            remain_time = match.group()
            remain_day = int(remain_time.split("天")[0])
            # print(remain_day)
            if remain_day <= remain_thre:
                # print(i,  remain_time)
                start_wogpu_shutdown(page,remain_time)

        page.pause()
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--account', type=str, default="Phone number", help='AutoDL account')
    parser.add_argument('--pwd', type=str, default="Password", help='AutoDL password')
    parser.add_argument('--time', type=int, default=6, help='The threshold of remaining time')
    args, _ = parser.parse_known_args()

    main(args.account, args.pwd, headless = False, remain_thre=args.time)
