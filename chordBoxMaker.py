# Extension para Inkscape creada por Marcos Feijoo www.ukelab.es
# Usa y comparte libremente

import sys
import inkex
import simplestyle

#draw an SVG line segment between the given (raw) points
def draw_SVG_line(x1, y1, x2, y2, width, name, parent):
    style = { 'stroke': '#000000', 'stroke-width':str(width), 'stroke-linecap': 'square','fill': 'none' }
    line_attribs = {'style':simplestyle.formatStyle(style),
                    inkex.addNS('label','inkscape'):name,
                    'd':'M '+str(x1)+','+str(y1)+' L '+str(x2)+','+str(y2)}
    inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )

#draw an SVG square
def draw_SVG_square((w, h), (x, y), parent):
		style = {		'stroke'		: 'none',
						'stroke-width'	: '1',
						'fill'		: '#000000'
						}
		attribs = {
				'style'		: simplestyle.formatStyle(style),
				'height'	: str(h),
				'width'		: str(w),
				'x'			: str(x),
				'y'			: str(y)
						}
		circ = inkex.etree.SubElement(parent, inkex.addNS('rect','svg'), attribs )

#draw_SVG_circle(i*dr, 0, 0, #major div circles self.options.r_divs_th, 'none', 'MajorDivCircle'+str(i)+':R'+str(i*dr), grid)
def draw_SVG_circle(r, cx, cy, width, fill, name, parent):
    style = { 'stroke': '#000000', 'stroke-width':str(width), 'fill': fill }
    circ_attribs = {'style':simplestyle.formatStyle(style),
                    'cx':str(cx), 'cy':str(cy), 
                    'r':str(r),
                    inkex.addNS('label','inkscape'):name}
    circle = inkex.etree.SubElement(parent, inkex.addNS('circle','svg'), circ_attribs )

def draw_SVG_label_centred(x, y, string, font_size, name, parent):
    style = {'text-align': 'center', 'vertical-align': 'top',
             'text-anchor': 'middle', 'font-size': str(font_size)+'px',
             'fill-opacity': '1.0', 'stroke': 'none',
             'font-weight': 'normal', 'font-style': 'normal', 'fill': '#000000'}
    label_attribs = {'style':simplestyle.formatStyle(style),
                     inkex.addNS('label','inkscape'):name,
                     'x':str(x), 'y':str(y)}
    label = inkex.etree.SubElement(parent, inkex.addNS('text','svg'), label_attribs)
    label.text = string
	

class chordBoxMakerEffect(inkex.Effect):
	def __init__(self):						
		# Call the base class constructor.
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("--tab",
					action="store", type="string",
					dest="tab")
		self.OptionParser.add_option("--trasteCero",
					action="store", type="string", default='true',
					dest="trasteCero")
		self.OptionParser.add_option("--numTrastes",
					action="store", type="int", default='5',
					dest="numTrastes")
		self.OptionParser.add_option("--numCuerdas",
					action="store", type="int", default='4',
					dest="numCuerdas")
		self.OptionParser.add_option("--tamCaja",
					action="store", type="int", default='10',
					dest="tamCaja")
		self.OptionParser.add_option("--anchoLinea",
					action="store", type="int", default='10',
					dest="anchoLinea")
		self.OptionParser.add_option("--impAyuda",
					action="store", type="string", default='true',
					dest="impAyuda")


	def effect(self):

		parent = self.current_layer
		centre = self.view_center	 #Put in in the centre of the current view
		grp_transform = 'translate' + str( centre )

		grp_name = 'Group Name'
		grp_attribs = {inkex.addNS('label','inkscape'):grp_name,'transform':grp_transform }
		grp = inkex.etree.SubElement(self.current_layer, 'g', grp_attribs) #the group to put everything in

		# recuperar VARIABLES
		t0=self.options.trasteCero
		tc=self.options.tamCaja
		nc=self.options.numCuerdas
		al=self.options.anchoLinea
		nt=self.options.numTrastes
		ia=self.options.impAyuda
		
		# dibujar HORIZONTALES
		for f in range(nt):				
				if t0 == 'true' and f==1:				                         
					draw_SVG_square((((tc*(nc-1))+al), 4*al), (0-(al/2),-(4*al)), grp)
					# draw_SVG_square((w, h), (x, y), parent)
					draw_SVG_line(0, tc*f, tc*(nc-1), tc*f, al, 'linea'+str(f), grp)
	
				else:
					draw_SVG_line(0, tc*f, tc*(nc-1), tc*f, al, 'linea'+str(f), grp)					
			
		
		#dibujar VERTICALES
		for f in range(nc):
			draw_SVG_line(tc*f, 0, tc*f, tc*(nt-1), al, 'linea'+str(f), grp)
		
		# dibujar CIRCULO
		draw_SVG_circle(tc*0.30, 0, -tc, al, 'CentreDot', 'circulo', grp)
		
		if ia == 'true':
			texto="Usa este grafico para anotar acordes y escalas en tu"
			texto2="ukelele, bajo, guitarra, timple, cuatro, mandolina ..."
			texto3="www.ukelab.es - info@ukelab.es"
			draw_SVG_label_centred(tc, tc*(nt+1), texto, tc/3, 'texto', grp)
			draw_SVG_label_centred(tc, tc*(nt+1.5), texto2, tc/3, 'texto2', grp)
			draw_SVG_label_centred(tc, tc*(nt+2), texto3, tc/3, 'texto3', grp)
		
		grp_transform = 'translate' + str( centre )
		

# Create effect instance and apply it.
if __name__ == '__main__':	 #pragma: no cover
	e = chordBoxMakerEffect()
	e.affect()
