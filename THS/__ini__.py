from THS.Voice import Voice

voice = Voice()

def calc_insert_stocks(last_stocks, current_stocks):
    # 转换元组，放入set对象
    set1 = {tuple(sorted(d.items())) for d in last_stocks}
    set2 = {tuple(sorted(d.items())) for d in current_stocks}

    # 求差集，结果是元组的set对象
    diff_set = set2 - set1

    # 转换回dict列表
    return [dict(t) for t in diff_set]


def calc_delete_stocks(last_stocks, current_stocks):
    # 转换元组，放入set对象
    set1 = {tuple(sorted(d.items())) for d in last_stocks}
    set2 = {tuple(sorted(d.items())) for d in current_stocks}

    # 求差集，结果是元组的set对象
    diff_set = set1 - set2

    # 转换回dict列表
    return [dict(t) for t in diff_set]
