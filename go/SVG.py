import svgwrite

"""
simple wrapper for svgwrite that replaces all the original sdxf calls from boxotron
"""
    
#I don't understand this magic number - and I can't get svgwrite to let me specify polylines with mm/cm
#SVGBUST
cm = 3.543307

#helper routines to scale pixels to cm, mainly because polylines can't be given units along with the dimensions
#SVGBUST
def convArrayTupleCM(points):
    newpoints = []
    for point in points:
        newpoints.append(convTupleCM(point))
    return newpoints

def convTupleCM(point):
    return tuple([x*cm for x in point])

#main class
class Drawing():
    def __init__(self,name):
        self.dwg = svgwrite.Drawing(filename=name, debug=True)
        self.styles = {}
        self.styles['line'] = self.dwg.add(self.dwg.g(id='lines', stroke='black', fill='none', stroke_width='0.3mm'))
        self.styles['cline']= self.dwg.add(self.dwg.g(id='constructionlines', stroke='red', opacity='0.50'))
        self.styles['cut']= self.dwg.add(self.dwg.g(id='cutlines', stroke='black', stroke_width='0.3mm', fill='none'))
        self.styles['mline'] = self.dwg.add(self.dwg.g(id='mazelines', stroke='black', stroke_width='0.3mm'))
        self.styles['engrave'] = self.dwg.add(self.dwg.g(id='engravlines', fill='none', stroke='blue', stroke_width='0.3mm'))

    def saveas(self):
        self.dwg.save()

    def idLine(self,id,points):
        self.styles[id].add(svgwrite.shapes.Polyline(convArrayTupleCM(points)))

    def idCircle(self,id,cent,radius):
        self.styles[id].add(self.dwg.circle(center=convTupleCM(cent), r=radius*cm ))

    def idRectangle(self,id,point,width,height):
        self.styles[id].add(self.dwg.rect(insert=convTupleCM(point),size=convTupleCM((width,height))))

    def idText(self,id,text,point,height):
        self.styles[id].add(svgwrite.text.Text(text,convTupleCM(point)))

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
