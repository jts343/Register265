#
# Register - CS265
# register.py
# Jeff Shea
# 12/8/14
# Python 2.7
#

__author__ = "Jeff Shea, 2014"

import sys
import os

"""
CS265 Register (Final Project)
Creates and manages a register till and keeps record of dollar bill denominations
Return values:
0 	SUCCESS (drawer was successfully changed)
1 	Bad arguments (format/number)
2 	Amounts don't jibe. E.g., left- and right-hand side of change aren't equal, or amount tendered is less than purchase price
3 	Drawer has insufficient money or denominations to make proper change
4 	Unable to read/write data file.
"""

def error(errCode):
    if(errCode == 1):
        print "ERROR: Bad arguments"
        sys.exit()
    elif(errCode == 2):
        print "ERROR: Amounts are not equal"
        sys.exit()
    elif(errCode == 3):
        print "ERROR: Drawer has insufficient money to complete transaction"
        sys.exit()
    elif(errCode == 4):
        print "ERROR: Unable to read/write reference file"
        sys.exit()
    elif(errCode < 0 or errCode > 4):
        print "Unknown Error!"
        sys.exit()

class Register():
    ones = 0
    fives = 0
    tens = 0
    twenties = 0
    total = 0
    sales = 0

    #constructor opens reference file if it exists and initializes drawer with saved data
    def __init__(self):
        if(os.path.isfile("regSrc.txt")):
            regSrc = open("regSrc.txt",mode="r").readlines()
            regSrc = regSrc[0].split()

            Register.ones = int(regSrc[0])
            Register.fives = int(regSrc[1])
            Register.tens = int(regSrc[2])
            Register.twenties = int(regSrc[3])
            Register.total = Register.ones + (Register.fives * 5) + (Register.tens * 10) + (Register.twenties * 20)
            Register.sales = int(regSrc[5])
        else:
            print "Register must be initialized first, creating empty drawer..."
            print "Empty drawer created, please initialize before attempting transactions."
            regSrc = open("regSrc.txt",mode="w")
            regSrc.write("0 0 0 0 0 0")
            sys.exit()

    #initialize register with bill denominations
    def init(self,a,b,c,d):
        Register.ones = a
        Register.fives = b
        Register.tens = c
        Register.twenties = d
        Register.total = a + (b*5) + (c*10) + (d*20)
        Register.sales = 0

    #make purchase and return chanage based on current drawer status
    def purchase(self,chargeAmt,givenAmt):
        #print "Entered purchase function"
        change = int(givenAmt - chargeAmt)
        oneRet = 0
        fivRet = 0
        tenRet = 0
        twyRet = 0
        while(change >= 0):
            #print change
            #print "while iterate"
            if(change > 20 and Register.twenties > 0):
                change -= 20
                Register.twenties -= 1
                twyRet += 1
            elif(change > 10 and Register.tens > 0):
                change -= 10
                Register.tens -= 1
                tenRet += 1
            elif(change > 5 and Register.fives > 0):
                change -= 5
                Register.fives -= 1
                fivRet += 1
            elif(change > 0 and Register.ones > 0):
                change -= 1
                Register.ones -= 1
                oneRet += 1
            elif(change > 0 and Register.ones <= 0):
                print change , Register.ones
                error(3)
            elif(change == 0):
                #Success
                Register.sales += 1
                #print "Transaction complete"
                print oneRet , fivRet , tenRet , twyRet
                break
            else:
                error(-1)

    #makes change according to requested bill denominations
    def change(self,change,bills_requested):
        change.__delitem__(0)
        for i in range(len(bills_requested)):
            change[i] = int(change[i])
            bills_requested[i] = int(bills_requested[i])
        changeSum = change[0] + change[1]*5 + change[2]*10 + change[3]*20
        billsSum = bills_requested[0] + bills_requested[1]*5 + bills_requested[2]*10 + bills_requested[3]*20

        if(changeSum != billsSum):
            error(2)
        elif( Register.ones < bills_requested[0] or Register.fives < bills_requested[1] or Register.tens < bills_requested[2] or Register.twenties < bills_requested[3]):
            error(3)
        else:
            Register.ones += change[0]
            Register.ones -= bills_requested[0]

            Register.fives += change[1]
            Register.fives -= bills_requested[1]

            Register.tens += change[2]
            Register.tens -= bills_requested[2]

            Register.twenties += change[3]
            Register.twenties -= bills_requested[3]

            print bills_requested[0] , bills_requested[1] , bills_requested[2] , bills_requested[3]

    def report(self):
        if(os.path.isfile("regSrc.txt")):
            regSrc = open("regSrc.txt").readlines()
            regSrc = regSrc[0].split()
            print regSrc[5] , " : " , regSrc[4] , " = " , regSrc[0] , regSrc[1] , regSrc[2] , regSrc[3]
        else:
            error(4)

#prints drawer status to reference file. Takes the Register object as an argument
def printToFile(Register):
    sys.stdout = open( 'regSrc.txt' , 'w' )
    print Register.ones , Register.fives , Register.tens , Register.twenties , Register.ones + (Register.fives * 5) + (Register.tens * 10) + (Register.twenties * 20) , Register.sales

def main():
    #parse arguments
    if(len(sys.argv) < 3):
        error(1)
    sepf = 0
    lhsArgs = []
    rhsArgs = []
    till = Register()
    if(sys.argv[1] == "report"):
        till.report()
        sys.exit()

    for i in range(len(sys.argv)):
        if(sepf == 0):
            if(sys.argv[i] == "="):
                sepf = 1
            else:
                lhsArgs.append(sys.argv[i])
        else:
            rhsArgs.append(sys.argv[i])

    for i in range(len(rhsArgs)):
        rhsArgs[i] = int(rhsArgs[i])

    #print "Checkpoint 1" #made it through parsing arguments into separate lists (rhs, lhs)
    lhsArgs.__delitem__(0)
    if(lhsArgs[0] != 'report'):
        rhsArgsSum = rhsArgs[0] + (rhsArgs[1] * 5) + (rhsArgs[2] * 10) + (rhsArgs[3] * 20)
        lhsArgs[1] = int(lhsArgs[1])
    #print lhsArgs
    #print rhsArgs

    #print "Checkpoint 2" #made it through changing argument list values from strings to ints
    if(lhsArgs[0] == "init"):
        if(rhsArgsSum != lhsArgs[1]):
            error(2)
        else:
            till.init(rhsArgs[0],rhsArgs[1],rhsArgs[2],rhsArgs[3])
            # print "Register opened with:"
            # print "$1 : " , till.ones
            # print "$5 : " , till.fives
            # print "$10: " , till.tens
            # print "$20: " , till.twenties
            # print ""
            # print "Total : $", till.total

    elif(lhsArgs[0] == "purchase" and lhsArgs[1] > 0):
        if(lhsArgs[1] > rhsArgsSum):
            error(2)
        else:
            till.ones += rhsArgs[0]
            till.fives += rhsArgs[1]
            till.tens += rhsArgs[2]
            till.twenties += rhsArgs[3]
            till.purchase(lhsArgs[1],rhsArgsSum)

    elif(lhsArgs[0] == "change"):
        till.change(lhsArgs,rhsArgs)

    printToFile(till)

if __name__ == '__main__':
    main()