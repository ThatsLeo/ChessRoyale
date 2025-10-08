x='a'
y='b'
a=[
    [0,0,0,1,1,1,1,1],
    [0,0,1,1,1,0,0,1],
    [0,1,1,x,1,0,y,1],
    [0,0,1,1,1,1,1,0],
    [0,0,0,1,0,0,0,0],
    ]

class Gio:
    def __init__(self, ciao):
        a='a'
        self.a=ciao

i = Gio('b')
print(getattr(i, 'a'))
print(getattr(i, 'self.a'))