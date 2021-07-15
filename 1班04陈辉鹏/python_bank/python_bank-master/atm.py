import time
from card import Card
from user import User
from admin import Admin
import random


class ATM(object):
    def outer(self, func):
        def inner():
            print('请输入以下开户所需的个人信息：')
            func()
            print('您的银行卡已开户成功，请牢记您的密码和卡号')

        return inner()

    def createUser(self):  # 开户
        name = input('姓名：')
        idCard = input('身份证：')
        phone = input('电话：')
        prestoreMoney = int(input('存款金额：'))
        if prestoreMoney < 0:
            print('对不起，存款金额输入有误，开户失败')
            return -1

        onePasswd = input('请设置密码：')
        if not self.checkPasswd(onePasswd):
            print('对不起，密码输入错误，开户失败')
            return -1

        cardStr = self.randomCardId()
        card = Card(cardStr, onePasswd, prestoreMoney)
        user = User(name, idCard, phone, card)
        self.allUsers[cardStr] = user
        print('卡号：%s' % cardStr)
        time.sleep(2)

    def searchInfo(self):  # 查询
        card = input('请输入卡号：')
        user = self.allUsers.get(card)
        if not user:
            print('对不起，没有此卡号，查询失败')
            return -1

        print('账号：%s  姓名：%s  余额：%d' % (user.card.cardId, user.name, user.card.cardMoney))

    def getMoney(self):  # 取款
        card = input('请输入卡号：')
        user = self.allUsers.get(card)
        if not user:
            print('对不起，没有此卡号')
            return -1

        if not self.checkPasswd(user.card.cardPasswd):
            print('对不起，密码错误')
            return -1
        tempMoney = int(input('输入取款的金额：'))
        if tempMoney < 0:
            print('对不起，存款金额输入有误，取款失败')
            return -1
        user.card.cardMoney = user.card.cardMoney - tempMoney
        print('取款成功')

    def saveMoney(self):  # 存款
        card = input('请输入卡号：')
        user = self.allUsers.get(card)
        if not user:
            print('对不起，没有此卡号')
            return -1

        if not self.checkPasswd(user.card.cardPasswd):
            print('对不起，密码错误')
            return -1
        tempMoney = int(input('请入存取的金额：'))
        if tempMoney < 0:
            print('对不起，存款金额输入有误，存取失败')
            return -1
        user.card.cardMoney = user.card.cardMoney + tempMoney
        print('存取成功')

    def transferMoney(self):  # 转账
        card1 = input('请输入对方卡号：')
        user1 = self.allUsers.get(card1)
        if not user1:
            print('对不起，对方卡号不存在')
            return -1
        card2 = input('请输入自己卡号：')
        user2 = self.allUsers.get(card2)
        if not user2:
            print('对不起，没有此卡号')
            return -1

        if not self.checkPasswd(user2.card.cardPasswd):
            print('对不起，密码错误')
            return -1
        tempMoney = int(input('请输入要转账的金额：'))
        if tempMoney < 0 or user2.card.cardMoney < tempMoney:
            print('对不起，转账金额输入有误或余额不足，请稍后再试')
            return -1
        user1.card.cardMoney = user1.card.cardMoney + tempMoney
        user2.card.cardMoney = user2.card.cardMoney - tempMoney
        print('请稍等，转帐中...')
        time.sleep(2)
        print('转账成功')

    def changePasswd(self):  # 改密
        card = input('请输入卡号：')
        user = self.allUsers.get(card)
        if not user:
            print('对不起，没有此卡号')
            return -1

        if not self.checkPasswd(user.card.cardPasswd):
            print('对不起，密码错误')
            return -1
        cardId = input('请输入身份证：')
        if cardId != user.idCard:
            print('对不起，身份证错误')
            return -1
        tempPasswd = input('请设置密码：')
        passwd = input('确认密码：')
        if passwd != tempPasswd:
            print('对不起，密码不一致')
            return -1
        user.card.cardPasswd = passwd
        print('修改密码成功')

    def destory(self):  # 注销卡号
        cardnum = input('请输入卡号：')
        user = self.allUsers.get(cardnum)
        if not user:
            print('对不起，没有此卡号')
            return -1
        if not self.checkPasswd(user.card.cardPasswd):
            print('对不起，密码错误')
            return -1
        idcard = input('输入身份证：')
        if user.idCard != idcard:
            print('对不起，身份证错误')
            return -1
        del self.allUsers[cardnum]
        print('请稍等，正在注销...')
        time.sleep(3)
        print('此卡号：%s已注销成功' % cardnum)

    def admin(self):  # 后台查看所有用户
        ad = Admin()
        if ad.adminLogin():
            return -1
        print('已存在账号信息：')
        for i, j in self.allUsers.items():
            print('卡号：%s  姓名：%s  身份证：%s  电话：%s  金额：%d' % (i, j.name, j.idCard, j.phone, j.card.cardMoney))
        time.sleep(5)

    def checkPasswd(self, realPasswd):  # 验证密码
        for i in range(3):
            tempPasswd = input('请输入密码：')
            if tempPasswd == realPasswd:
                return True
        return False

    def randomCardId(self):  # 随机卡号
        while True:
            str = ''
            for i in range(6):
                ch = chr(random.randrange(ord('0'), ord('9') + 1))
                str += ch
            if not self.allUsers.get(str):
                return str
