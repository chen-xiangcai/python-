from admin import Admin
from atm import ATM
import pickle
import os
import time


def main():
    admin = Admin()
    admin.adminView()
    if admin.adminLogin():
        return -1
    path = os.path.join(os.getcwd(), 'allUsers.txt')
    f = open(path, 'rb')
    allUsers = pickle.load(f)
    atm = ATM(allUsers)

    while True:
        admin.sysFunctionView()
        option = input('请选择业务：')
        if option == '1':
            atm.outer(atm.createUser)
        elif option == '2':
            atm.searchInfo()
        elif option == '3':
            atm.getMoney()
        elif option == '4':
            atm.saveMoney()
        elif option == '5':
            atm.transferMoney()
        elif option == '6':
            atm.changePasswd()
        elif option == '0':
            atm.destory()
        elif option == 'q':
            if not admin.adminLogin():
                path = os.path.join(os.getcwd(), 'allUsers.txt')
                f = open(path, 'wb')
                pickle.dump(atm.allUsers, f)
                f.close()
                return -1
        elif option == 'a':
            atm.admin()

        time.sleep(2)
