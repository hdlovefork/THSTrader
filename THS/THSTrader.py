import hashlib
import threading
import time
import xml.etree.ElementTree as ET

import easyocr
import uiautomator2 as u2
from PIL import Image

from THS.__ini__ import calc_insert_stocks, calc_delete_stocks
from log import log
from main import env

PAGE_INDICATOR = {
    "模拟炒股": "com.hexin.plat.android:id/tab_mn",
    "A股": "com.hexin.plat.android:id/tab_a",
    "返回": "com.hexin.plat.android:id/title_bar_img",
    "股票多选": "com.hexin.plat.android:id/stockname_tv",
    "关闭按钮1": "com.hexin.plat.android:id/close_btn",
    "确定按钮": "com.hexin.plat.android:id/ok_btn",
    "刷新":'//*[@resource-id="com.hexin.plat.android:id/title_bar_right_container"]//*[@resource-id="com.hexin.plat.android:id/title_bar_img"]',
    "撤单": "com.hexin.plat.android:id/chedan_recycler_view"
}

MAX_COUNT = 1  # 最大可显示持仓数目，调试用


class THSTrader:
    def __init__(self, serial="emulator-5554") -> None:
        self.d = u2.connect_usb(serial)
        #self.reader = easyocr.Reader(['ch_sim', 'en'])

    def get_balance(self):
        """ 获取资产 """
        self.__back_to_moni_page()
        self.d(resourceId=f"com.hexin.plat.android:id/menu_holdings_image").click()
        time.sleep(1)
        self.d.swipe(340, 600, 340, 1000)
        time.sleep(1)
        return {
            "总资产": float(
                self.d(resourceId="com.hexin.plat.android:id/totalasset_value").get_text().replace(",", "")),
            "可用余额": float(self.d(resourceId="com.hexin.plat.android:id/canuse_value").get_text().replace(",", "")),
            "股票市值": float(
                self.d(resourceId="com.hexin.plat.android:id/totalworth_value").get_text().replace(",", "")),
        }

    def expect_node(self, xpath, timeout=1):
        return self.d.xpath(xpath).wait(timeout)

    def get_position(self):
        """ 获取当前持有股票 """
        self.__back_to_moni_page()
        self.d(resourceId=f"com.hexin.plat.android:id/menu_holdings_image").click()
        time.sleep(1)
        i = 0
        first = True
        while True:
            #             print(i)
            if i > MAX_COUNT:
                break
            try:
                self.d.xpath(
                    f'//*[@resource-id="com.hexin.plat.android:id/recyclerview_id"]/android.widget.RelativeLayout[{i + 1}]').screenshot().save(
                    f"tmp{i}.png")
                i += 1
                self.d.swipe(340, 1000, 340, 890)
            except:
                if first:
                    self.d.swipe(340, 1000, 340, 600)  # 滑动后还是找不到才退出
                    first = False
                else:
                    break

        count = i
        holdings = []
        for i in range(count):
            holdings.append(self.__ocr_parse_holding(f"tmp{i}.png"))

        return holdings

    def get_avail_withdrawals_ex(self, view_code=True):
        """ 获取可以撤单的列表 """
        if not self.enter_withdrawals_page():
            return []
        withdrawals = []
        root = lambda: self.d.xpath('@com.hexin.plat.android:id/chedan_recycler_view')
        # 点击完刷新后，等待列表出现
        root().wait()
        count = len(root().child('*').all())
        for i in range(count):
            # 如果有个元素它下面有文字是"其它",则说明是最后一行，不用再找了
            if root().child(f'*[{i + 1}]').child(
                    '*[@resource-id="com.hexin.plat.android:id/cannot_chedan_title_text"]').exists:
                break
            stock_code = None
            market_code = None
            if view_code:
                # 需要查看股票代码
                root().child(f'*[{i + 1}]').click()
                if self.d.xpath('@com.hexin.plat.android:id/stockcode_textview').wait():
                    stock_code = self.d.xpath('@com.hexin.plat.android:id/stockcode_textview').get_text()
                    self.d.xpath('@com.hexin.plat.android:id/option_cancel').click()
                    stock_code = stock_code.replace("代码", "")
                    stock_code = stock_code.replace(" ", "")
                    if len(stock_code) > 0:
                        market_code = 0 if int(stock_code[0]) == 0 else 1
            try:
                withdrawals.append({
                    "股票代码": stock_code,
                    "市场代码": market_code,
                    "股票名称": root().child(f'android.widget.LinearLayout[{i + 1}]').child(
                        '//*[@resource-id="com.hexin.plat.android:id/result0"]').get_text(),
                    "委托时间": root().child(f'android.widget.LinearLayout[{i + 1}]').child(
                        '//*[@resource-id="com.hexin.plat.android:id/result1"]').get_text(),
                    # "委托价格": float(root().child(f'android.widget.LinearLayout[{i + 1}]').child(
                    #     '//*[@resource-id="com.hexin.plat.android:id/result2"]').get_text()),
                    # "委托数量": int(root().child(f'android.widget.LinearLayout[{i + 1}]').child(
                    #     '//*[@resource-id="com.hexin.plat.android:id/first_tv"]').get_text()),
                    "委托方向": root().child(f'android.widget.LinearLayout[{i + 1}]').child(
                        '//*[@resource-id="com.hexin.plat.android:id/result6"]').get_text(),
                    # "委托状态": root().child(f'android.widget.LinearLayout[{i + 1}]').child(
                    #     '//*[@resource-id="com.hexin.plat.android:id/result7"]').get_text()
                })
            except:
                # 有可能页面已经改变，导致找不到元素
                break
        return withdrawals

    def withdraw(self, stock_name, t, amount, price):
        """ 撤单 """
        self.__back_to_moni_page()
        self.d(resourceId=f"com.hexin.plat.android:id/menu_withdrawal_image").click()
        success = False
        i = 0
        first = True
        while True:
            #             print(i)
            if i > MAX_COUNT:
                break
            try:
                self.d.xpath(
                    f'//*[@resource-id="com.hexin.plat.android:id/chedan_recycler_view"]/android.widget.LinearLayout[{i + 1}]').screenshot().save(
                    f"tmp{i}.png")
                info = self.__ocr_parse_withdrawal(f"tmp{i}.png")
                if (stock_name == info["股票名称"]) and int(amount) == int(info["委托数量"]) \
                        and (abs(float(price) - float(info["委托价格"])) < 0.01) and (t == info["委托类型"]):
                    self.d.xpath(
                        f'//*[@resource-id="com.hexin.plat.android:id/chedan_recycler_view"]/android.widget.LinearLayout[{i + 1}]').click()
                    time.sleep(1)
                    self.d(resourceId="com.hexin.plat.android:id/option_chedan").click()
                    time.sleep(1)
                    success = True
                    break

                i += 1
                self.d.swipe(340, 1000, 340, 890)
            except:
                if first:
                    self.d.swipe(340, 1000, 340, 600)  # 滑动后还是找不到才退出
                    first = False
                else:
                    break
        return {
            "success": success
        }

    def buy(self, stock_no, amount, price):
        return self.__imeaction(stock_no, amount, price, "menu_buy_image")

    def sell(self, stock_no, amount, price):
        return self.__imeaction(stock_no, amount, price, "menu_sale_image")

    def __imeaction(self, stock_no, amount, price, open_tag):
        """ 买入或者卖出通用 """
        stock_no = str(stock_no)
        amount = str(amount)
        price = str(price)
        success = False
        msg = ""
        stock_name = ""
        while True:
            self.__back_to_moni_page()
            self.d(resourceId=f"com.hexin.plat.android:id/{open_tag}").click()
            self.__input_stock_no(stock_no)
            self.__input_stock_price(price)
            self.__input_stock_buy_count(amount)
            self.d.xpath(
                '//*[@resource-id="com.hexin.plat.android:id/transaction_layout"]/android.widget.LinearLayout[1]').click()
            time.sleep(1)
            if self.__entrust_doubel_check(stock_no, amount, price):
                try:
                    stock_name = self.d(resourceId="com.hexin.plat.android:id/stock_name_value").get_text()
                    self.d(resourceId="com.hexin.plat.android:id/ok_btn").click()
                    time.sleep(1)
                    self.d(resourceId="com.hexin.plat.android:id/content_scroll").screenshot().save(f"tmp.png")
                    msg = self.__ocr_get_full_text()
                    self.d(resourceId="com.hexin.plat.android:id/ok_btn").click()
                    success = True
                    break
                except:
                    raise
            else:
                self.d(resourceId="com.hexin.plat.android:id/cancel_btn").click()
                time.sleep(2)

        if open_tag == "menu_buy_image":
            t = "买入"
        else:
            t = "卖出"
        return {
            "success": success,
            "msg": msg,
            "stock_name": stock_name.replace(" ", ""),
            "amount": amount,
            "price": price,
            "type": t
        }

    def __entrust_doubel_check(self, stock_no, amount, price):
        time.sleep(1)
        if self.d(resourceId="com.hexin.plat.android:id/stock_code_value").get_text().replace(" ", "") != stock_no:
            return False

        if self.d(resourceId="com.hexin.plat.android:id/number_value").get_text().replace(" ", "").replace(",",
                                                                                                           "") != amount:
            return False

        price = float(price)
        pnow = float(self.d(resourceId="com.hexin.plat.android:id/price_value").get_text())
        if abs(price - pnow) > 0.01:
            return False

        return True

    def click(self, path, wait=False):
        if wait:
            self.d.xpath(path).wait()
        self.d.xpath(path).click()

    def click_d(self, resource_id, wait=False):
        if wait:
            self.d(resourceId=resource_id).wait()
        if self.d(resourceId=resource_id).exists:
            self.d(resourceId=resource_id).click()

    def __back_to_moni_page(self):
        log.debug("退回到模拟页面")
        self.__util_close_other()
        self.d.app_start("com.hexin.plat.android")
        self.click('//*[@content-desc="交易"]/android.widget.ImageView[1]')
        self.click_d(PAGE_INDICATOR["返回"])
        self.click_d(PAGE_INDICATOR["模拟炒股"])
        return True

    def __input_stock_no(self, stock_no):
        """ 输入股票ID """
        self.__util_close_other()
        self.click_d("com.hexin.plat.android:id/content_stock")
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
        self.click_d("com.hexin.plat.android:id/stockprice")
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
        self.click_d(PAGE_INDICATOR["关闭按钮1"])
        self.click_d(PAGE_INDICATOR["确定按钮"])
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

    def __ocr_get_full_text(self):
        result = self.reader.readtext("tmp.png")
        text = ""
        for line in result:
            text += line[1]
        return text

    def __ocr_parse_holding(self, path):
        Image.open(path).crop((11, 11, 165, 55)).save("tmp.png")
        result = self.reader.readtext(f'tmp.png')
        stock_name = result[0][1]
        Image.open(path).crop((419, 11, 548, 55)).save("tmp.png")
        result = self.reader.readtext(f'tmp.png')
        stock_count = result[0][1]
        Image.open(path).crop((419, 60, 548, 102)).save("tmp.png")

        result = self.reader.readtext(f'tmp.png')
        try:
            stock_available = result[0][1]
        except:
            stock_available = "0"
        return {
            "股票名称": stock_name.replace(" ", ""),
            "股票余额": int(stock_count.replace(",", "")),
            "可用余额": int(stock_available.replace(",", ""))
        }

    def __ocr_parse_withdrawal(self, path):
        Image.open(path).crop((11, 11, 165, 55)).save("tmp.png")
        result = self.reader.readtext(f'tmp.png')
        stock_name = result[0][1]
        Image.open(path).crop((219, 11, 390, 55)).save("tmp.png")
        result = self.reader.readtext(f'tmp.png')
        stock_price = result[0][1]
        Image.open(path).crop((419, 11, 548, 55)).save("tmp.png")
        result = self.reader.readtext(f'tmp.png')
        stock_count = result[0][1]
        Image.open(path).crop((589, 11, 704, 55)).save("tmp.png")
        result = self.reader.readtext(f'tmp.png')
        t = result[0][1]
        return {
            "股票名称": stock_name.replace(" ", ""),
            "委托价格": float(stock_price.replace(",", "")),
            "委托数量": int(stock_count.replace(",", "")),
            "委托类型": t.replace(" ", "")
        }

    def enter_withdrawals_page(self):
        """ 进入撤单页面 """
        log.debug("进入撤单页面")
        if not self.__in_withdrawals_page():
            log.debug("不在撤单页面，尝试进入撤单页面")
            if env.appenv != "prod":
                self.__back_to_moni_page()
            else:
                self.__back_to_trade_page()
            r = self.__click_withdrawal()
            return r
        log.debug("已在撤单页面")
        return True

    def withdrawals_page_hierarchy(self):
        """ 获取撤单列表的xml内容 """
        log.debug("分析撤单列表是否有更新")
        # 刷新列表
        self.click(PAGE_INDICATOR["刷新"])
            # 等待刷新完成
        self.d(resourceId=PAGE_INDICATOR['撤单']).wait()
        if not self.d(resourceId=PAGE_INDICATOR['撤单']).exists:
            return None
        root = ET.fromstring(self.d.dump_hierarchy())
        # 找到撤单节点并获取xml内容
        node = root.find(f".//*[@resource-id='{PAGE_INDICATOR['撤单']}']")
        return ET.tostring(node, encoding='unicode')

    def __click_withdrawal(self):
        self.d(resourceId=f"com.hexin.plat.android:id/menu_withdrawal_image").wait()
        if self.d(resourceId=f"com.hexin.plat.android:id/menu_withdrawal_image").exists:
            self.d(resourceId=f"com.hexin.plat.android:id/menu_withdrawal_image").click()
            return True
        return False

    def __in_withdrawals_page(self):
        if not self.d(resourceId="com.hexin.plat.android:id/chedan_recycler_view").exists:
            return self.d.xpath('//*[@text="撤单"]').xpath('//*[@content-desc="撤单"]').exists
        return True

    def __back_to_trade_page(self):
        log.debug("退回到A股页面")
        self.__util_close_other()
        self.d.app_start("com.hexin.plat.android")
        self.click('//*[@content-desc="交易"]/android.widget.ImageView[1]')
        self.click_d(PAGE_INDICATOR["返回"])
        self.click_d(PAGE_INDICATOR["A股"])
        return True


class THSWithdrawWatcher:
    def __init__(self, trader, insert_stock_callback=None, delete_stock_callback=None):
        self.worker_thread = None
        self.thread_lock = threading.Lock()
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
        if self.worker_thread.is_alive():
            self.worker_thread.join()
        self.worker_thread = None

    def __worker(self):
        log.debug("正在监控撤单页面变化...")
        last = None
        last_stocks = []
        while not self.stop_event.is_set():
            with self.thread_lock:
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
                        stocks = self.trader.get_avail_withdrawals_ex(False)
                        # 获取当前持仓股票与上一次持仓股票的差集
                        if self.insert_stock_callback is not None:
                            insert_stocks = calc_insert_stocks(last_stocks, stocks)
                            if len(insert_stocks) > 0:
                                log.debug(f"发现新增股票：{insert_stocks}")
                                self.insert_stock_callback(insert_stocks)
                        if self.delete_stock_callback is not None:
                            delete_stocks = calc_delete_stocks(last_stocks, stocks)
                            if len(delete_stocks) > 0:
                                log.debug(f"发现删除股票：{delete_stocks}")
                                self.delete_stock_callback(delete_stocks)
                        last_stocks = stocks
            self.stop_event.wait(self.wait_interval)

    def __calc_md5(self, content):
        log.debug("计算页面的md5")
        return hashlib.md5(content.encode()).hexdigest()
