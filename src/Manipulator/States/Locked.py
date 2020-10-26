from ..ManipulatorState import ManipulatorState

class Locked(ManipulatorState): 
    name = "LOCKED"
    allowed = ['UNLOCKED']