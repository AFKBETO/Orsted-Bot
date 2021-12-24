from dataclasses import dataclass, field
from datetime import datetime

def parse_line(line):
    try:
        if ':' in line:
            k = line.find(':')
            key = line[:k].strip()
            val = parse_number(line[k+1:])
            return [key,val]
        else:
            return None
    except:
        return None


def parse_number(raw):
    try:
        return int(raw)
    except:
        return raw.strip(" ")

@dataclass(order=True)
class User:
  id:str
  exp:int = field(default = 0)
  last_message:datetime = field(default = datetime(2000,1,1), init = False)
  last_gain:int = field(default = 0, init = False)

  def add_exp(self,amount:int):
    self.exp += amount
    self.last_gain = amount
    if self.exp < 0:
      self.exp = 0
      self.last_gain = 0
    
    if self.last_gain > 30:
      self.last_gain = 30
  
  def reset_exp(self):
    self.exp = 0
  
  def penalty(self):
    self.add_exp(-300)
    self.last_gain = 0

  def set_last_message(self):
    self.last_message = datetime.utcnow()