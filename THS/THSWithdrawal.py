from log import log
from THS.__ini__ import voice

class THSWithdrawal:
    DIRECT_SENSITIVE = 1
    DIRECT_INSENSITIVE = 0

    def __init__(self, action, env):
        self.action = action
        # 上一次股票行情数据 {'000001': {bid_vol1: 0, ask_vol1: 0,...}}
        self.last_tick = {}
        self.env = env

    def resolve(self, quot_stocks):
        log.debug("撤单分析开始...")
        satisfy_stocks = []
        for s in quot_stocks:
            cur_stock = dict(s)
            log.debug("当前股票：{}".format(cur_stock))
            '''
            cur_stock数据结构：
            {'market': 0, 'code': '000010', 'active1': 0, 'price': 0.0, 'last_close': 2.08, 'open': 0.0, 
            'high': 0.0, 'low': 0.0, 'servertime': '9:15:05.406', 'reversed_bytes0': 9150901, 'reversed_bytes1': 0, 
            'vol': 0, 'cur_vol': 0, 'amount': 5.877471754111438e-39, 's_vol': 0, 'b_vol': 0, 'reversed_bytes2': 1700, 
            'reversed_bytes3': 17, 'bid1': 2.08, 'ask1': 2.08, 'bid_vol1': 8, 'ask_vol1': 8, 'bid2': 0.0, 
            'ask2': 0.0, 'bid_vol2': 17, 'ask_vol2': 0, 'bid3': 0.0, 'ask3': 0.0, 'bid_vol3': 0, 'ask_vol3': 0, 
            'bid4': 0.0, 'ask4': 0.0, 'bid_vol4': 0, 'ask_vol4': 0, 'bid5': 0.0, 'ask5': 0.0, 'bid_vol5': 0, 
            'ask_vol5': 0, 'reversed_bytes4': (8,), 'reversed_bytes5': 0, 'reversed_bytes6': 0, 'reversed_bytes7': 0, 
            'reversed_bytes8': 0, 'reversed_bytes9': 0.0, 'active2': 0}
            '''
            # 当前买1数
            cur_bid_vol1 = cur_stock['bid_vol1']
            # 判断是否需要撤单
            is_withdrawal = False
            # 如果撤单规则的bid_vol1大于0，同时当前买1数大于当前行情的买1数，则撤单
            top_bid_vol1 = self.env('withdrawal.top.bid_vol1', 0)
            if top_bid_vol1 > 1 and top_bid_vol1 > cur_bid_vol1:
                log.info("撤单：由于当前买1数(%d) < 配置买1数(%d)" % (cur_bid_vol1, top_bid_vol1))
                satisfy_stocks.extend(self.do_withdraw(cur_stock))
                continue
            # 如果self.withdrawal_stocks中没有该stock.code，则添加
            if cur_stock['code'] not in self.last_tick:
                self.last_tick[cur_stock['code']] = cur_stock
                log.debug("添加股票行情：%s,%s" % (cur_stock['code'], cur_stock['name']))
                continue
            # 如果self.withdrawal_stocks中有该stock.code，则更新
            else:
                last_bid_vol1 = self.last_tick[cur_stock['code']]['bid_vol1']
                top_bid_vol1 = self.env('withdrawal.top.bid_vol1', 0)
                # 如果撤单规则的买1数小于0，同时当前行情的买1数小于上次的买1数
                if 1 > top_bid_vol1 > 0 and cur_bid_vol1 < last_bid_vol1:
                    # 如果bid_vol1减小的比例大于撤单规则的bid_vol1，则撤单
                    rate = (last_bid_vol1 - cur_bid_vol1) / last_bid_vol1
                    if rate > top_bid_vol1:
                        log.info("撤单：(上次买1数[%d] - 当前买1数[%d]) / 上次买1数[%d] = %.3f > 配置买1数[%.2f]"
                                 % (last_bid_vol1, cur_bid_vol1, last_bid_vol1, rate, top_bid_vol1))
                        is_withdrawal = True
            # 需要撤单
            if is_withdrawal:
                satisfy_stocks.extend(self.do_withdraw(cur_stock))
            else:
                log.debug("更新股票行情：%s,%s" % (cur_stock['code'], cur_stock['name']))
                self.last_tick[cur_stock['code']].update(cur_stock)
        log.debug("撤单处理结束，满足条件的股票：%s" % satisfy_stocks)
        return satisfy_stocks

    def do_withdraw(self, cur_stock):
        log.info("执行撤单操作：%s,%s" % (cur_stock['code'], cur_stock['name']))
        top_direct_sensitive = self.env('withdrawal.top.direct_sensitive', THSWithdrawal.DIRECT_INSENSITIVE)
        withdrew_stocks = self.action.withdraw(cur_stock['name'], lambda s: s['withdraw_direct'] == '买入',
                                               top_direct_sensitive == THSWithdrawal.DIRECT_SENSITIVE)
        # 撤单后，从行情tick记录中删除该股票
        if cur_stock['code'] in self.last_tick:
            self.last_tick.pop(cur_stock['code'])
        log.debug("已撤单股票：%s" % withdrew_stocks)
        self.play_sound(cur_stock)
        return withdrew_stocks

    def play_sound(self,cur_stock):
        """播放语音"""
        msg = self.env.withdrawal.top.voice_msg
        # 如果消息的长度大于0，则播放语音
        if msg and len(msg) > 0:
            # 将%s替换为股票名称
            msg = msg.replace('%s', cur_stock['name'])
            voice.say(msg)
