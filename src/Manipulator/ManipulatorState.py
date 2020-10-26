class ManipulatorState(object):

    name = "state"
    allowed = []

    def switch(self, state):
        if state.name in self.allowed:
            print('Current: {} => switched to new state {}'.format(self, state.name))
            self.__class__ = state
        else:
            print('Current: {} => switched to new state {} not possible.'.format(self, state.name))

    def __str__(self):
        return self.name