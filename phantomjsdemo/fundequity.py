# -*- coding: utf-8 -*-
from datetime import date

# 基金净值信息
class FundEquity(object):
    def __init__(self):
        # 类实例即对象的属性
        self.__serial = 0  # 序号
        self.__date = None  # 日期
        self.__code = ""  # 基金代码
        self.__name = ""  # 基金名称
        self.__equity = 0.0  # 单位净值
        self.__accumulationEquity = 0.0  # 累计净值
        self.__increment = 0.0  # 增长值
        self.__growthRate = 0.0  # 增长率
        self.__canBuy = False # 是否可以购买
        self.__canRedeem = True # 是否能赎回

    @property
    def serial(self):
        return self.__serial

    @serial.setter
    def serial(self, value):
        self.__serial = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        # 数据检查
        if not isinstance(value, date):
            raise ValueError('date must be date type!')
        self.__date = value

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        self.__code = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def equity(self):
        return self.__equity

    @equity.setter
    def equity(self, value):
        self.__equity = value

    @property
    def accumulationEquity(self):
        return self.__accumulationEquity

    @accumulationEquity.setter
    def accumulationEquity(self, value):
        self.__accumulationEquity = value

    @property
    def increment(self):
        return self.__increment

    @increment.setter
    def increment(self, value):
        self.__increment = value

    @property
    def growthRate(self):
        return self.__growthRate

    @growthRate.setter
    def growthRate(self, value):
        self.__growthRate = value

    @property
    def canBuy(self):
        return self.__canBuy

    @canBuy.setter
    def canBuy(self, value):
        self.__canBuy = value

    @property
    def canRedeem(self):
        return self.__canRedeem

    @canRedeem.setter
    def canRedeem(self, value):
        self.__canRedeem = value
    # 类似其它语言中的toString()函数
    def __str__(self):
        return '[serial:%s,date:%s,code:%s,name:%s,equity:%.4f,\
accumulationEquity:%.4f,increment:%.4f,growthRate:%.4f%%,canBuy:%s,canRedeem:%s]'\
               % (self.serial, self.date.strftime("%Y-%m-%d"), self.code, self.name, float(self.equity), \
                  float(self.accumulationEquity), float(self.increment), \
                  float(self.growthRate), self.canBuy, self.canRedeem)