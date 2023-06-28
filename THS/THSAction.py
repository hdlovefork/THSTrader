import hashlib
import os
import threading
import time
import xml.etree.ElementTree as ET

import uiautomator2 as u2

from THS.__ini__ import calc_insert_stocks, calc_delete_stocks
from log import log

PAGE_INDICATOR = {
    "模拟炒股": "@com.hexin.plat.android:id/tab_mn",
    "A股": "@com.hexin.plat.android:id/tab_a",
    "返回": '//*[@resource-id="com.hexin.plat.android:id/title_bar_left_container"]//*[@resource-id="com.hexin.plat.android:id/title_bar_img"]',
    "股票多选": "com.hexin.plat.android:id/stockname_tv",
    "关闭按钮1": "com.hexin.plat.android:id/close_btn",
    "确定按钮": "com.hexin.plat.android:id/ok_btn",
    "刷新": '//*[@resource-id="com.hexin.plat.android:id/title_bar_right_container"]//*[@resource-id="com.hexin.plat.android:id/title_bar_img"]',
    "撤单列表": "com.hexin.plat.android:id/chedan_recycler_view",
    "取消": "com.hexin.plat.android:id/cancel_btn",
    "撤单取消": "@com.hexin.plat.android:id/option_cancel",
    "撤单确定": "@com.hexin.plat.android:id/option_chedan",
    "导航栏交易": '//*[@content-desc="交易"]/android.widget.ImageView[1]',
    '交易面板撤单按钮': '@com.hexin.plat.android:id/menu_withdrawal_image'
}

MAX_COUNT = 1  # 最大可显示持仓数目，调试用

BTN_CLOSE = {
    # 关闭按钮
    "关闭按钮": "@com.hexin.plat.android:id/close_btn",
    "悬浮广告关闭按钮": "@com.hexin.plat.android:id/close_button",
    # 取消
    "取消": "@com.hexin.plat.android:id/cancel_btn",
    # 返回
    # "返回": "@com.hexin.plat.android:id/backButton",
    # 撤单对话框取消
    "撤单对话框取消": "@com.hexin.plat.android:id/option_cancel",
    # 确定
    "确定": "@com.hexin.plat.android:id/ok_btn",
}


class THSAction:
    def __init__(self, serial="emulator-5554") -> None:
        self.d = u2.connect_usb(serial)
        # 操作间等待某元素出现时的最长秒数
        self.d.settings['wait_timeout'] = 1
        # 撤单页面刷新与撤单操作不能同时进行
        self.withdraw_lock = threading.Lock()
        self.last_withdrawal_stocks = None

    def get_avail_withdrawals_ex(self, view_code=True):
        """ 获取可以撤单的列表 """
        log.debug("获取可以撤单的列表")
        if not self.enter_withdrawals_page():
            return []
        withdrawals = []
        root = lambda: self.d.xpath('@com.hexin.plat.android:id/chedan_recycler_view')
        # 点击完刷新后，等待列表出现
        log.debug("等待撤单列表出现")
        root().wait()
        count = len(root().child('*').all())
        log.debug(f"撤单列表有{count}个元素")
        for i in range(count):
            # 空列表，则说明是最后一行，不用再找了
            if root().child(f'*[{i + 1}]').child(
                    '*[@resource-id="com.hexin.plat.android:id/chedan_empty_layout"]').exists:
                log.debug("当前没有可撤委托单")
                break
            # 如果有个元素它下面有文字是"其它",则说明是最后一行，不用再找了
            if root().child(f'*[{i + 1}]').child(
                    '*[@resource-id="com.hexin.plat.android:id/cannot_chedan_title_text"]').exists:
                log.debug("到其它了，不用再找了")
                break
            # 全撤、撤买、撤卖按钮组，则说明是最后一行，不用再找了
            if root().child(f'*[{i + 1}]').xpath('@com.hexin.plat.android:id/gdqc_layout').exists:
                log.debug("到全撤、撤买、撤卖按钮组了，不用再找了")
                break
            stock_code = None
            market_code = None
            if view_code:
                # 需要查看股票代码
                log.debug(f"查看第{i + 1}个元素的股票代码")
                stock = self.withdraw_dialog_cancel_when(i, lambda stock: True)
                stock_code = stock["stock_code"]
                market_code = stock["market_code"]
            try:
                withdrawals.append({
                    "stock_code": stock_code,
                    "market_code": market_code,
                    "stock_name": root().child(f'android.widget.LinearLayout[{i + 1}]').child(
                        '//*[@resource-id="com.hexin.plat.android:id/result0"]').get_text(),
                    "withdraw_time": root().child(f'android.widget.LinearLayout[{i + 1}]').child(
                        '//*[@resource-id="com.hexin.plat.android:id/result1"]').get_text(),
                    # "withdraw_price": float(root().child(f'android.widget.LinearLayout[{i + 1}]').child(
                    #     '//*[@resource-id="com.hexin.plat.android:id/result2"]').get_text()),
                    # "withdraw_count": int(root().child(f'android.widget.LinearLayout[{i + 1}]').child(
                    #     '//*[@resource-id="com.hexin.plat.android:id/first_tv"]').get_text()),
                    "withdraw_direct": root().child(f'android.widget.LinearLayout[{i + 1}]').child(
                        '//*[@resource-id="com.hexin.plat.android:id/result6"]').get_text(),
                    # "withdraw_status": root().child(f'android.widget.LinearLayout[{i + 1}]').child(
                    #     '//*[@resource-id="com.hexin.plat.android:id/result7"]').get_text()
                })
            except:
                # 有可能页面已经改变，导致找不到元素
                break
        self.last_withdrawal_stocks = withdrawals
        return withdrawals

    def withdraw_dialog(self, i):
        root = self.__withdrawal_page_root
        try:
            log.debug("点击撤单列表第{}个元素".format(i + 1))
            root().child(f'*[{i + 1}]').click()
            time.sleep(.1)
            if self.d.xpath('@com.hexin.plat.android:id/title_view').wait():
                stock = {}
                log.debug("——股票撤单对话框出现")
                stock['stock_name'] = self.d.xpath('@com.hexin.plat.android:id/stockname_textview').get_text()
                stock['stock_code'] = self.d.xpath('@com.hexin.plat.android:id/stockcode_textview').get_text()
                stock['stock_name'] = stock['stock_name'].replace('名称', '').replace(' ', '')
                stock['stock_code'] = stock['stock_code'].replace('代码', '').replace(' ', '')
                stock['market_code'] = 0 if int(stock['stock_code'][0]) == 0 else 1
                log.debug("——股票代码：{} 股票名称：{}".format(stock['stock_code'], stock['stock_name']))
                return stock
        except:
            pass
        log.debug("——股票撤单对话框未出现")
        return None

    def withdraw_dialog_when(self, i, when, then):
        stock = self.withdraw_dialog(i)
        if stock is not None:
            if when(stock):
                then(stock)
                return stock
        return None

    def withdraw_dialog_chedan_when(self, i, when):
        r = self.withdraw_dialog_when(i, when, lambda stock: self.click('撤单确定'))
        if r is not None:
            # 点击确定后，等待撤单列表刷新
            self.__withdrawal_page_root().wait()
        return r

    def withdraw_dialog_cancel_when(self, i, when):
        return self.withdraw_dialog_when(i, when, lambda stock: self.click('撤单取消'))

    def withdraw(self, stock_name):
        """ 撤单 """
        # 重试3次
        completed = False
        for i in range(3):
            # 如果已经完成，则不再重试
            if completed:
                break
            with self.withdraw_lock:
                if not self.enter_withdrawals_page():
                    continue
                if self.last_withdrawal_stocks is None:
                    self.last_withdrawal_stocks = self.get_avail_withdrawals_ex(False)
                i = 0
                while i < len(self.last_withdrawal_stocks):
                    stock = self.last_withdrawal_stocks[i]
                    if stock['stock_name'] != stock_name:
                        # 不是要撤单的股票，继续下一个
                        i += 1
                        continue
                    if self.withdraw_dialog_chedan_when(i, lambda s: s['stock_name'] == stock_name) is None:
                        # 未删除成功，继续下一个
                        i += 1
                        continue
                    # 从撤单列表中删除
                    self.last_withdrawal_stocks.pop(i)
                    # 不需要重试
                    completed = True
                    # 撤单成功后，从i开始继续检索，因为可能同一股票名称有2笔买入订单
                    # i位置的元素已经被删除了，所以不需要i+1
        return completed

    def click(self, name, wait=False, set=None):
        set = PAGE_INDICATOR if set is None else set
        if name not in set:
            return
        path = set[name]
        log.debug(f"点击{name} {path}")
        if wait:
            # 等到元素出现则直接点击，等不到则退出
            if self.d.xpath(path).wait() is not None:
                try:
                    self.d.xpath(path).click()
                except:
                    pass
            return
        # 不等待直接点击
        try:
            self.d.xpath(path).click()
        except:
            pass

    def __back_to_trade_page(self, app_env, when=None):
        log.debug("退回到交易页面")
        self.click('导航栏交易', True)
        if callable(when) and when():
            return True
        self.click('返回', True)
        if app_env != 'prod':
            self.click('模拟炒股', True)
        else:
            self.click('A股', True)
        return True

    def __input_stock_no(self, stock_no):
        """ 输入股票ID """
        self.__util_close_other()
        self.click("@com.hexin.plat.android:id/content_stock")
        time.sleep(2)
        self.__util_input_text(stock_no)
        time.sleep(2)
        if self.__util_check_app_page(PAGE_INDICATOR["股票多选"]):
            try:
                self.d.xpath(
                    '//*[@resource-id="com.hexin.plat.android:id/recyclerView"]/android.widget.RelativeLayout[1]').click()
            except:
                pass

    def __input_stock_price(self, price):
        """ 输入股票价格 """
        self.__util_close_other()
        self.click("@com.hexin.plat.android:id/stockprice")
        self.__util_input_text(price)

    def __input_stock_buy_count(self, buy_count):
        """ 输入股票购买量 """
        self.__util_close_other()
        self.d(resourceId="com.hexin.plat.android:id/stockvolume").click()
        time.sleep(2)
        self.__util_input_text(buy_count)

    def __util_close_other(self):
        """ 关闭其他弹窗 """
        log.debug("关闭其他弹窗")
        for key in BTN_CLOSE:
            self.click(key,set=BTN_CLOSE)
        return True

    def __util_input_text(self, text):
        """ 输入工具，uiautomator2的clear_text和send_keys速度好像有点儿慢，所以用了这种方法 """
        self.d.shell("input keyevent 123")
        for _ in range(20):
            self.d.shell("input keyevent 67")
        self.d.shell(f"input text {text}")

    def __util_check_app_page(self, indicator):
        """ 工具，检查页面是否包含某特征 """
        hierachy = self.d.dump_hierarchy()
        if indicator in hierachy:
            return True
        return False

    def enter_withdrawals_page(self):
        """ 进入撤单页面 """
        log.debug("进入撤单页面")
        if not self.in_withdrawals_page():
            log.debug("——不在撤单页面，尝试进入撤单页面")
            self.__back_to_trade_page(os.getenv("APPENV"), lambda:self.in_withdrawals_page())
            if not self.in_withdrawals_page():
                return self.click("交易面板撤单按钮", True)
        log.debug("——已在撤单页面")
        return True

    def withdrawals_page_hierarchy(self):
        """ 获取撤单列表的xml内容 """
        log.debug("分析撤单列表是否有更新")
        # 刷新列表
        self.click("刷新")
        # 等待刷新完成
        self.__withdrawal_page_root().wait()
        if not self.__withdrawal_page_root().exists:
            return None
        root = ET.fromstring(self.d.dump_hierarchy())
        # 找到撤单节点并获取xml内容
        node = root.find(f".//*[@resource-id='{PAGE_INDICATOR['撤单列表']}']")
        if node is not None:
            return ET.tostring(node, encoding='unicode')
        return None

    def in_withdrawals_page(self):
        return self.__withdrawal_page_root().wait() is not None

    def __withdrawal_page_root(self):
        return self.d.xpath(f"//*[@resource-id='{PAGE_INDICATOR['撤单列表']}']")


class THSWithdrawWatcher:
    def __init__(self, trader, insert_stock_callback=None, delete_stock_callback=None):
        self.worker_thread = None
        self.withdraw_lock = trader.withdraw_lock
        self.stop_event = threading.Event()
        self.wait_interval = 0.1
        self.trader = trader
        self.insert_stock_callback = insert_stock_callback
        self.delete_stock_callback = delete_stock_callback

    # 析构函数
    def __del__(self):
        self.stop()

    def start(self):
        self.worker_thread = threading.Thread(target=self.__worker)
        self.worker_thread.start()

    def stop(self):
        self.stop_event.set()
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join()
        self.worker_thread = None

    def __worker(self):
        log.info("正在监控撤单页面变化...")
        last = None
        last_stocks = []
        while not self.stop_event.is_set():
            with self.withdraw_lock:
                if self.trader.enter_withdrawals_page():
                    content = self.trader.withdrawals_page_hierarchy()
                    if content is None:
                        continue
                    current = self.__calc_md5(content)
                    if last != current:
                        log.debug(f'last: {last}, current: {current}\n{content}')
                        last = current
                        log.debug("撤单页面发生变化")
                        # 获取变化的股票
                        stocks = self.trader.get_avail_withdrawals_ex()
                        # 获取当前持仓股票与上一次持仓股票的差集
                        if self.insert_stock_callback is not None:
                            insert_stocks = calc_insert_stocks(last_stocks, stocks)
                            if len(insert_stocks) > 0:
                                log.info(f"发现新增股票：{insert_stocks}")
                                self.insert_stock_callback(insert_stocks)
                        if self.delete_stock_callback is not None:
                            delete_stocks = calc_delete_stocks(last_stocks, stocks)
                            if len(delete_stocks) > 0:
                                log.info(f"发现删除股票：{delete_stocks}")
                                self.delete_stock_callback(delete_stocks)
                        last_stocks = stocks
                        self.trader.last_withdrawal_stocks = stocks
            self.stop_event.wait(self.wait_interval)

    def __calc_md5(self, content):
        log.debug("计算页面的md5")
        return hashlib.md5(content.encode()).hexdigest()