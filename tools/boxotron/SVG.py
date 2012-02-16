import svgwrite
    
cm = 3.543307

def convArrayTupleCM(points):
    newpoints = []
    for point in points:
        newpoints.append(convTupleCM(point))
    return newpoints

def convTupleCM(point):
    return tuple([x*cm for x in point])

class Drawing():
    def __init__(self):
        name = "test.svg"
        self.dwg = svgwrite.Drawing(filename=name, debug=True)
        self.lines = self.dwg.add(self.dwg.g(id='lines', stroke='black', fill='none', stroke_width='0.1mm'))
        self.constructionlines = self.dwg.add(self.dwg.g(id='constructionlines', stroke='red', opacity='0.50'))

    def saveas(self,filename):
        self.dwg.save()

    def Line(self,points):
        self.lines.add(svgwrite.shapes.Polyline(convArrayTupleCM(points)))

    def CLine(self,points):
        self.constructionlines.add(svgwrite.shapes.Polyline(convArrayTupleCM(points)))

    def Circle(self,cent,radius):
        self.lines.add(self.dwg.circle(center=convTupleCM(cent), r=radius*cm ))
      
    def Rectangle(self,point,width,height):
        self.lines.add(self.dwg.rect(insert=convTupleCM(point),size=convTupleCM((width,height))))

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
