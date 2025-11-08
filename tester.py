class test:
    def __init__(self, name, func):
        self.name= name
        self.activate = func
    def tt(self):
        print('uee')

class test2(test):
    def __init__(self, name, func):
        super().__init__(name, func)
    def tt(self):
        print('cia')

lis = [test, test2]
a = lis[0]('gig', 2)
print(type(a).__name__=='test')