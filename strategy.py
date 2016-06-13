
import logging
import random
import math
import time
import sys


class BseStrategy():
    def __init__(self, user, strategy_changer = None):
        self.start_balance = user.balance
        self.max_gain = 0
        self.curr_gain = 0
        self.user = user
        self.run = True
        self.itr = 0
        self.lost = 0
        self.win = 0
        self.win_lost = False
        self.last_win_lost = False
        self.last_amount = 0
        self.gain = 50
        self.condition = "<"
        self.nominal = 2
        self.coef = 2
        self.win_count = 0
        self.lost_count = 0
        self.target = None
        self.critical_lose = None
        
        
    def start(self):
        pass

    def update_state(self, win, amount, gain, condition):
      self.win_lost = win
      self.curr_gain = self.user.balance - self.start_balance
      self.itr = self.itr + 1
      self.last_amount = amount
      self.gain = gain
      self.condition = condition
      
      if (self.last_win_lost is not self.win_lost):
          if(self.win_lost):
              self.win_count = 0
          else:
              self.lost_count = 0      
      
      if(win):
          self.win = self.win + 1
          self.win_lost = True
          self.win_count = self.win_count + 1
      else:
          self.lost = self.lost + 1
          self.win_lost = False
          self.lost_count = self.lost_count + 1
      
      if(self.max_gain < (self.user.balance - self.start_balance ) ):
          self.max_gain = self.user.balance - self.start_balance
      
      if(self.win_lost):
          res = "+"
      else:
          res = "-"
      
      self.last_win_lost = self.win_lost
      
      log_str = res+' amount = '+str(self.amount)+' curr_gain  = '+str(round(self.curr_gain))+' balance = '+str(self.user.balance)+' win = '+str(self.win)+' lost = '+str(self.lost)+' iter = '+str(self.itr)+' lost_count = '+str(self.lost_count)+' win_count = '+str(self.win_count)
      logging.debug(log_str )
      print(log_str )
      pass
    
    def start(self):
      pass
    
    def stop(self):
      self.run = False
      pass
    
    def reset_curr_gain(self):
      self.curr_gain = 0
      self.start_balance = self.user.balance
      pass 
    
    def update_bet_condition(self):
      pass
    
    def start(self): 
        self.run = True
        self.reset_curr_gain()
        while (self.run):            
            bet_feedback = self.user.bet(self.amount, self.gain, self.condition)            
            try:
              self.update_state(bet_feedback["win"], self.amount, self.gain, self.condition)
            except Exception as ex:
                logging.critical('update_state Exception: '+str(ex))
                sys.exit(0)                
            self.update_bet_condition()
            time.sleep(self.user.sleep_interval)
        pass
  
class MultyplyStrategy(BseStrategy):
    def __init__(self, user, strategy_changer = None):
        super(MultyplyStrategy, self).__init__(user, strategy_changer)
        self.nominal = 2
        self.amount = self.nominal
        self.coef = 2
        
    def set_target(self, target):
        self.target = target
    def set_critical_lose(self, critical_lose):
        self.critical_lose = critical_lose
    
    def update_bet_condition(self):      
      if self.win_lost:
          self.amount = self.nominal
      else:
          #if( self.amount*self.coef/2 >self.curr_gain and self.curr_gain > 0):
          #if( self.curr_gain < 0):
          if(self.lost_count > 6):
            self.amount = 1
          else:
            self.amount = self.amount*self.coef
          #self.amount = self.amount*self.coef       
      if self.user.balance <= 0 :
        log_str = 'i = '+str(self.itr)+' max_gain = '+str(self.max_gain)  
        logging.debug(log_str )
        logging.debug("Failed. Exit")
        print(log_str)  
        print ("Failed. Exit")
        #return #sys.exit(0)
        self.run = False
      
      if ((self.target is not None) and (self.curr_gain >= self.target)):
          log_str = 'tsrget '+str(self.target)+' reached '
          logging.debug(log_str )
          print(log_str)
          self.run = False  
                    
      if ((self.critical_lose is not None) and (self.critical_lose > self.curr_gain - self.amount)):
          log_str = 'critical_lose '+str(self.critical_lose)+' reached '
          logging.debug(log_str )
          print(log_str)
          self.run = False  
      pass

