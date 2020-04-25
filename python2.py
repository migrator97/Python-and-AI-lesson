# -*-coding:utf-8 -*-
# @Time:2020/4/23 5:12 下午
# @Author:WX
# @File:python2.py

import re
import datetime
import numpy as np


# 是否数字
def is_num(num):
    flag = True
    try:
        float(num)
    except ValueError:
        flag = False
    return flag


# 身份证号校验
def validate_id_num(id_num):
    # 校验省份
    def check_prov(_id_num):
        provence = {11: "北京", 12: "天津", 13: "河北", 14: "山西", 15: "内蒙古",
                    21: "辽宁", 22: "吉林", 23: "黑龙江", 31: "上海", 32: "江苏",
                    33: "浙江", 34: "安徽", 35: "福建", 36: "江西", 37: "山东",
                    41: "河南", 42: "湖北 ", 43: "湖南", 44: "广东", 45: "广西",
                    46: "海南", 50: "重庆", 51: "四川", 52: "贵州", 53: "云南",
                    54: "西藏 ", 61: "陕西", 62: "甘肃", 63: "青海", 64: "宁夏",
                    65: "新疆", 71: "台湾", 81: "香港", 82: "澳门"}
        return int(_id_num[0:2]) in provence

    # 校验合法日期
    def check_birthday(_id_num):
        try:
            datetime.date(int(_id_num[6:10]), int(_id_num[10:12]), int(_id_num[12:14]))
        except:
            return False
        else:
            return True

    # 校验码
    def checkcode(_id_num):
        sub_id_num = np.array([i for i in _id_num[0:17]]).astype(int)
        factor = np.array([[7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]]).T
        parity = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
        return parity[np.dot(sub_id_num, factor)[0] % 11] == int(_id_num[-1])

    pattern = re.compile(r'^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$')
    return not pattern.match(id_num) is None and check_prov(id_num) and check_birthday(id_num) and checkcode(id_num)


# 信息打印和上报
def info_report(list_name, person_list):
    file = open(list_name + '.txt', 'w+')
    file.writelines(list_name + '\n      身份证号      体温\n')
    print(list_name + '：\n      身份证号      体温')
    for key in eval(person_list).keys():
        print(key + ' ' + str(eval(person_list)[key]))
        file.writelines(key + ' ' + str(eval(person_list)[key]) + '\n')
    file.close()


class Person:
    def __init__(self, id_num, temp):
        self.id_num = id_num
        self.temp = temp

    def is_fever(self):
        return float(self.temp) >= 37.3

    def is_wuhanren(self):
        return self.id_num[0:4] == '4201'

    def check_ncov(self):
        if not self.is_fever() and self.is_wuhanren():
            status = 'guancha'
            words = '您是武汉籍人员，无发烧症状，请居家观察！'
        elif self.is_fever() and not self.is_wuhanren():
            status = 'guancha'
            words = '您不是武汉籍人员 ，但有发烧症状，请居家观察！'
        elif self.is_fever() and self.is_wuhanren():
            status = 'geli'
            words = '您是武汉籍人员且有发烧症状，系统已上报，请配合隔离！'
        else:
            status = 'zhengchang'
            words = '恭喜您，没有中奖，可以走了！'
        return status, words


if __name__ == '__main__':
    guancha = {}
    geli = {}
    zhengchang = {}  # 初始化

    while True:
        _id_num = input('请输入身份证号，取消或结束请直接回车：')  # 输入身份证号
        if _id_num == '':
            break
        elif not validate_id_num(_id_num):
            print('身份证号码错误！')
            continue

        _temp = input('请输入体温，取消或结束请直接回车：')  # 输入体温
        if _temp == '':
            break
        elif not is_num(_temp) or float(_temp) >= 39 or float(_temp) <= 36:
            print('体温输入错误！')
            continue

        person = Person(_id_num, _temp)  # 实例化
        s, w = person.check_ncov()
        eval(s)[person.id_num] = person.temp
        print(w)

    info_report('居家观察名单', 'guancha')
    info_report('隔离上报名单', 'geli')
