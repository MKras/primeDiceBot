#!python3

import primeDiceClass as primedice
import primeDiceTesterClass as primedice_tester
import config
import sys
import time
import logging
import strategy

import json


def countdown(t): # in seconds
    for i in range(t,0,-1):
        if(not i % 10):
          #print ('sleeping for %d seconds\r' % i,)
          sys.stdout.write(str(i)+' ')
          sys.stdout.flush()
        time.sleep(1)
        
logging.basicConfig(filename='primeDiceBot.log',level = logging.DEBUG)


logging.debug("Start")

helpme = primedice.helpers()
helpme.config_check(config)
user = primedice.primedice()
user.login(config.username, config.password)
logging.info( "Current Balance = %s" % (user.balance)) 
init_balance = user.balance
game = strategy.MultyplyStrategy(user)    
game.critical_lose = -200
#game.target = user.balance*1.5
while(user.balance >= init_balance):
    init_balance = user.balance
    game.target = 110
    game.start()
    countdown(120)


'''game = primedice_tester.primedice_tester(200)
test_strat = strategy.MultyplyStrategy(game)    
init_balance = game.balance
test_strat.critical_lose = -200
while(game.balance >= init_balance):
    init_balance = game.balance
    test_strat.target = 110
    test_strat.start()    
    countdown(10)
print("EXIT")'''