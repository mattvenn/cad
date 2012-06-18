import svgwrite

"""
simple wrapper for svgwrite that replaces all the original sdxf calls from boxotron
"""
    
#main class
class Drawing():
    def __init__(self,name,width,height):
        widthmm = "%fmm" % width
        heightmm = "%fmm" % height
        self.dwg = svgwrite.Drawing(filename=name, debug=True, size=(widthmm,heightmm))
        self.dwg.viewbox(width=width,height=height)
        self.styles = {}
        self.styles['line'] = self.dwg.add(self.dwg.g(id='lines', stroke='black', fill='none', stroke_width='0.3'))
        self.styles['cline']= self.dwg.add(self.dwg.g(id='constructionlines', stroke='red', opacity='0.50'))
        self.styles['cut']= self.dwg.add(self.dwg.g(id='cutlines', stroke='black', stroke_width='0.3', fill='none'))
        self.styles['mline'] = self.dwg.add(self.dwg.g(id='mazelines', stroke='black', stroke_width='0.3'))
        self.styles['engrave'] = self.dwg.add(self.dwg.g(id='engravlines', fill='none', stroke='blue', stroke_width='0.3'))

    def saveas(self):
        self.dwg.save()

    def text(self,id,point,text,font_size):
        self.styles[id].add(svgwrite.text.Text(text, insert=point, font_family='sans-serif', font_size = font_size))

    def idLine(self,id,points):
        self.styles[id].add(svgwrite.shapes.Polyline(points))

    def idCircle(self,id,cent,radius):
        self.styles[id].add(self.dwg.circle(center=cent, r=radius ))

    def idRectangle(self,id,point,width,height):
        self.styles[id].add(self.dwg.rect(insert=point,size=(width,height)))

    def idText(self,id,text,point,height):
        self.styles[id].add(svgwrite.text.Text(text,point))

