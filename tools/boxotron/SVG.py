import svgwrite
    
cm = 35.43307

class Drawing():
    def __init__(self):
        name = "test.svg"
        self.dwg = svgwrite.Drawing(filename=name, debug=True)
        self.lines = self.dwg.add(self.dwg.g(id='lines', stroke='black'))

    def saveas(self,filename):
        self.dwg.save()

    def Line(self,points):
        self.lines.add(svgwrite.shapes.Polyline(points))

    def Circle(self,cent,radius):
        self.lines.add(self.dwg.circle(center=cent, r=radius ))
      
    def Rectangle(self,point,width,height):
        self.lines.add(self.dwg.rect(insert=point,size=(width,height)))

    def convCm(points):
        newpoints = []
        for point in points:
            newpoints.append(tuple([x*cm for x in point]))
        return newpoints
""" 

def basic_shapes(name):
    lines = dwg.add(dwg.g(id='lines', fill='black'))
    points = convCm([ (0,0),(2,0),(2,2),(0,2),(0,0) ])
   
    print points
    lines.add(svgwrite.shapes.Polyline(points))
    dwg.save()

if __name__ == '__main__':
    basic_shapes('basic_shapes.svg')
"""
