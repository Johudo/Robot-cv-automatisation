from ..ManipulatorState import ManipulatorState

class Unlocked(ManipulatorState): 
    name = "UNLOCKED"
    allowed = ['LOCKED']