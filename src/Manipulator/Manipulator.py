from .States.Unlocked import Unlocked

class Manipulator(object):
   
   def __init__(self, model='HP'):
      self.model = model
      # State of the computer - default is off.
      self.state = Unlocked()
   
   def change(self, state):
      """ Change state """
      self.state.switch(state)