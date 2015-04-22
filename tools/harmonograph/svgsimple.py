from pysvg.structure import svg
from pysvg.builders import *
from pysvg.shape import *
style=StyleBuilder()
style.setFilling("none")
style.setStroke("#000")
style.setStrokeWidth(2)

class svgsimple():
    
    def create(self,w,h):
        self.dwg = svg(width=w,height=h)

    def start_path(self,x,y):
        self.p = path()
        self.p.set_style(style.getStyle())
        self.p.appendMoveToPath(x,y)

    def extend_path(self,x,y):
        self.p.appendLineToPath(x,y,relative=False)

    def end_path(self):
        self.dwg.addElement(self.p)
    
    def save(self,name):
        self.dwg.save(name)

if __name__ == '__main__':
    s = svgsimple()
    s.create(200,200)
    s.start_path(10,10)
    s.extend_path(20,20)
    s.end_path()
    s.start_path(100,150)
    s.extend_path(50,20)
    s.end_path()
    s.save("path.svg")
