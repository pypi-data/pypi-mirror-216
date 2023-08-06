from json import load as json_load
import importlib.resources

原始数据 = None
拆字 = None

def 初始化():
    global 拆字
    global 原始数据
    with importlib.resources.open_text('chinese_characters_words.数据', 'IDS-UCS-Basic.txt') as f:
        所有行 = f.read().split('\n')
        拆字 = {}
        for 行 in 所有行:
            字段 = 行.split('\t')
            if (len(字段) != 3):
                continue
            字 = 字段[1]
            信息 = 字段[2]
            if (字 != 信息):
                字型 = 信息[0]
                部分 = []
                for i in range(1, len(信息)):
                    部分.append(信息[i])
                拆字[字] = {'字型': 字型, '部分': 部分}

    with importlib.resources.open_text("chinese_characters_words.数据", "字典.json") as 文件:
        原始数据 = json_load(文件)


# API
def 查单字(字):
    if 原始数据 == None:
        初始化()
    for 字数据 in 原始数据:
        if 字 == 字数据['word']:
            信息 = {}
            信息['字'] = 字数据['word']
            信息['旧体'] = 字数据['oldword'] # 大多与现在相同
            信息['笔画数'] = 字数据['strokes']
            信息['拼音'] = 字数据['pinyin']
            信息['部首'] = 字数据['radicals']
            信息['释义'] = 字数据['explanation']
            信息['其他'] = 字数据['more']
            return 信息


def 一个(部分):
    if 拆字 == None:
        初始化()

    所有字 = []
    for 字 in 拆字:
        if (拆字[字]['部分'].__contains__(部分)):
            所有字.append(字)
    return 所有字


def 左边(部分):
    if 拆字 == None:
        初始化()

    不限位置 = 一个(部分)
    所有字 = []
    for 字 in 不限位置:
        if ((拆字[字]['字型'] == '⿰') and (拆字[字]['部分'][0] == 部分)):
            所有字.append(字)
    return 所有字


def 右边(部分):
    if 拆字 == None:
        初始化()

    不限位置 = 一个(部分)
    所有字 = []
    for 字 in 不限位置:
        if ((拆字[字]['字型'] == '⿰') and (拆字[字]['部分'][1] == 部分)):
            所有字.append(字)
    return 所有字


def 上面(部分):
    if 拆字 == None:
        初始化()

    不限位置 = 一个(部分)
    所有字 = []
    for 字 in 不限位置:
        if ((拆字[字]['字型'] == '⿱') and (拆字[字]['部分'][0] == 部分)):
            所有字.append(字)
    return 所有字


def 下面(部分):
    if 拆字 == None:
        初始化()

    不限位置 = 一个(部分)
    所有字 = []
    for 字 in 不限位置:
        if ((拆字[字]['字型'] == '⿱') and (拆字[字]['部分'][1] == 部分)):
            所有字.append(字)
    return 所有字

# print(查单字('九'))
# print(一个('吴'))
# print(左边('甘'))
# print(右边('亘'))
# print(上面('口'))
# print(下面('天'))