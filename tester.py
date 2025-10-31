class test:
    def __init__(self, name, func):
        self.name= name
        self.activate = func
def tt():
    print('uhh')

a = test('ciao', tt)

a.activate()