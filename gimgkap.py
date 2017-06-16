#!/usr/bin/env python2

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk,GdkPixbuf

import os
import sys
import numpy
import StringIO

from PIL import Image, ImageDraw, ImageFont,ImageEnhance,ImageFilter


class GImgkapGui:
	def __init__(self):
		self.glabolActionName = ""
		self.builder = Gtk.Builder()
		b = self.builder
		self.builder.add_from_file("gui.glade")
		self.ki = KapImg()
		self.ev = Events(self)
		ev = self.ev
		self.builder.connect_signals(ev)

		
		self.window = self.go("window1")
		#self.window.maximize()
		self.window.resize(900,700)

		self.lStatus = self.go("lStatus")
		self.btPerspective = self.go("btPerspective")
		self.btCrop = self.go("btCrop")
		self.btColor = self.go("btColor")
		self.btEnhance = self.go("ev_btEnhance")
		self.button1 = self.go("button1")

		self.fZoom = self.go("fZoom")
		self.ebIMain = self.go("ebIMain")
		self.iMain = self.go("iMain")
		self.layoutZoom = self.go("layoutZoom")
		self.iZoom = self.go("iZoom")
		self.layoutIMain = self.go("layoutIMain")
		self.lX = self.go("lX")
		self.lY = self.go("lY")
		self.eLat = self.go("eLat")
		self.eLon = self.go("eLon")
		self.lLat = self.go("lLat")
		self.lLon = self.go("lLon")
		self.boxLXY = self.go("boxLXY")
		self.boxELatLon = self.go("boxELatLon")
		self.boxLLatLon = self.go("boxLLatLon")
		
		self.window.show_all()

		self.btCrop.set_visible(False)
		#self.btColor.set_visible(False)
		self.fZoom.set_visible(False)
		self.button1.set_visible(False)

		
		if self.ki.chkIfImgkapIsPressent():
			self.lStatus.set_text("<-- select file *.png | *.jpg | *.kap")
		else:
			self.lStatus.set_text("error ! - no imgkap found :( ")

		
	def go(self, objectName):
		return self.builder.get_object(objectName)

	def moveCross(self,obj, x,y):
		self.layoutIMain.move(obj,x-16, y-16)
		#print x,y

	def makeDetailWindow(self, crosObj=None, values="xy"):
		print "makeDetailWindow values",values
		c = crosObj
		if c.x == None or c.y == None:
			return 0
	
		if values.find("xy")>-1:
			self.boxLXY.set_visible(True)
		else:
			self.boxLXY.set_visible(False)

		if values.find("l")>-1:
			self.boxELatLon.set_visible(True)
			self.boxLLatLon.set_visible(True)
		else:
			self.boxELatLon.set_visible(False)
			self.boxLLatLon.set_visible(False)

		
		fza = self.fZoom.get_allocation()
		layIMai = self.layoutIMain.get_allocation()
		fw = fza.width
		fh = fza.height
		zw = self.ev.pbZoom.get_width()
		zh = self.ev.pbZoom.get_height()
		CropW = 150
		CropH = 150
		off = 16		

		print "1	x,y",c.x,c.y,"lat,lon",c.lat,c.lon

		self.lX.set_text("x: %s"% int(c.x))
		self.lY.set_text("y: %s"% int(c.y))
		self.eLat.set_text("%s"%c.lat)
		self.eLon.set_text("%s"%c.lon)
		
		zx = c.x*self.ev.zoom - 150*0.5
		zxOff = 0
		if zx < 0:
			zxOff = -zx
			zx = 0

		zy = c.y*self.ev.zoom - 150*0.5
		zyOff = 0
		if zy < 0:
			zyOff = -zy
			zy = 0

		if zx+CropW >= zw:
			CropW = zw - zx
			zxOff = -CropW*0.5+(CropW)-75
		if zy+CropH >= zh:
			CropH = zh - zy
			zyOff= -CropH*0.5+CropH-75

		#print "x",c.x,"y",c.y,"CropW",CropW,"CropH",CropH,"zxOff",zxOff,"zyOff",zyOff
		

		self.iZoom.set_from_pixbuf( self.ev.pbZoom.new_subpixbuf( zx,zy, CropW,CropH) )
		self.layoutZoom.move(self.iZoom, zxOff, zyOff)

		#print 1
		if layIMai.width*0.5 > c.x:
			#print "x"
			xoff = c.x + off
		else:
			xoff = c.x-fza.width-16

		if layIMai.height*0.5 > c.y:
			#print "y"
			yoff = c.y + off
		else:
			yoff = c.y-fza.height-16
		self.layoutIMain.move(self.fZoom, xoff,yoff)
		#print "x",x,"y",y,"xoff",xoff,"yoff",yoff,layIMai.width,layIMai.height
		self.fZoom.set_visible(True)
		print "2	x,y",c.x,c.y,"lat,lon",c.lat,c.lon


	def run(self):
		Gtk.main()



class Events:
	def __init__(self,gui):
		a = "	:)	"
		self.gui = gui
		self.ki = gui.ki
		self.iLT_drag = False
		self.iRB_drag = False
		
	def ev_window_destroy(self,obj):
		print("bey!!!")
		Gtk.main_quit()


	def ev_win_press(self,obj,ev):
		print "ev_win_press"
		print "key %s" %ev.keyval
		if ev.keyval == 113:
			try:
				Gtk.main_quit(*args)
			except:
				sys.exit(0)
		if ev.keyval == 108:
			print "load"
			self.ev_bt(obj)

	"""
	def ev_layIMai_press(self,obj,ev):
		print "ev_layIMai_press"

	def ev_layIMai_release(self,obj,ev):
		print "ev_layIMai_release"

	def ev_layIMai_motion(self,obj,ev):
		print "ev_layIMai_motion"
		wp = obj.get_parent_window().get_pointer()
		print wp[0], wp[1], wp[2]
	"""

	def ev_btPerspective(self,obj): 
		print "ev_btPerspective"
		if self.gui.glabolActionName == "perspective":
			res = self.gui.mip.endPerspective( self.gui )
			if res == "OK":
				self.gui.glabolActionName = "perspectiveDone"
			else:
				self.gui.lStatus.set_text(res)
		else:
			self.gui.glabolActionName = "perspective"
			mip = MyImageProcess()
			mip.startPerspective( self.gui )
			self.gui.mip = mip

	def ev_btEnhance(self,obj):
		print "ev_btEnhance"
		mip = MyImageProcess()
		mip.startEnhance( self.gui )

		
	def ev_btOk(self,obj):
		print "ev_btOk"
		g = self.gui
		g.fZoom.set_visible(False)


	def ev_eLat_changed(self,obj):
		print "ev_eLat_changed"
		self.chkLLData()
 
	def ev_eLon_changed(self,obj):
		print "ev_eLon_changed"
		self.chkLLData()



	def chkLData(self,str_):
		print "str_",str_
		s = "%s"%str_.replace(",",".")
		
		if ( s.find("d") > -1 or s.find("'") > -1 ) and (s.find(".") > -1 or s.find(".") == -1):
			return s
		
		try:
			l = float(s)
			if ("%s"%l) == ("%s"%s):
				return l
		except:
			return "NaN"

		return "NaN"


	def chkLLData(self):
		if self.gui.eventOnCross.updateInProgress == False:
			self.gui.lLat.set_text( str(self.chkLData( self.gui.eLat.get_text() )) )
			self.gui.lLon.set_text( str(self.chkLData( self.gui.eLon.get_text() )) )
			self.gui.eventOnCross.lat = self.chkLData( self.gui.eLat.get_text() )
			self.gui.eventOnCross.lon = self.chkLData( self.gui.eLon.get_text() )

	
	def ev_btUp(self,obj):
		print "ev_btUp"
		self.gui.eventOnCross.moveCrossBy(0,-1)

	def ev_btRight(self,obj):
		print "ev_btRight"
		self.gui.eventOnCross.moveCrossBy(1,0)

	def ev_btDown(self,obj):
		print "ev_btDown"
		self.gui.eventOnCross.moveCrossBy(0,1)

	def ev_btLeft(self,obj):
		print "ev_btLeft"
		self.gui.eventOnCross.moveCrossBy(-1,0)


	def ev_bt(self,obj):
		#self.loadFile("/home/yoyo/Apps/gimgkap/testFiles/5-02.kap")
		#self.loadFile("/home/yoyo/Apps/gimgkap/testFiles/8-54.kap")
		self.loadFile("/home/yoyo/Apps/gimgkap/testFiles/IMG_20170612_071755712_mini.jpg")

	def ev_fcbt(self,obj):
		print "ev_fcbt"
		self.loadFile(obj.get_filename())

	def ev_btCrop(self,obj):
		print "ev_btCrop"

	def ev_btColor(self,obj):
		print "ev_btColor"
		mip = MyImageProcess()
		mip.startColor( self.gui )

	def ev_btSaveAs(self,obj):
		print "ev_btSaveAs"
		dialog = Gtk.FileChooserDialog("Please choose a image file or kap file", self.gui.window,
			Gtk.FileChooserAction.SAVE,
			(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
		
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print("Save As")
			print("File selected: " + dialog.get_filename())
			self.ki.saveAs( self.gui, dialog.get_filename() )
			dialog.destroy()
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")
			dialog.destroy()


	def updateCrossys(self):
		print "updateCrossys"
		g = self.gui
		k = self.ki		

		cc = CrossContainer(g)
		cc.makeCross( g.layoutIMain, 2, title="LatLon", 
			points=[ 
				(k.x0, k.y0, k.lat0, k.lon0),
				(k.x1, k.y1, k.lat1, k.lon1)
				] )
		g.cc = cc
		g.lStatus.set_text("You can now correct/set corners top left and bottom right")


	def loadFile(self,filePath, makeNewCross=True):
		ft = self.ki.chkFileType(filePath)
		if ft == "kap":
			self.ki.analize(filePath)
			if self.ki.analizeStatus():
				self.gui.lStatus.set_text("kap file ok :)")
				tmpFilePath = self.ki.extractImage(filePath)
				self.loadAndSetUpWidgets(tmpFilePath,makeNewCross=makeNewCross)
			else:
				self.gui.lStatus.set_text("kap file error no reference points found :(")
		elif ft == "img":
			self.ki.makeCleanStart()
			self.ki.tmpImgFile = filePath
			self.loadAndSetUpWidgets( filePath, makeNewCross=makeNewCross)

			self.gui.lStatus.set_text("img loaded :) - now you need to set up corners")

	def loadAndSetUpWidgets(self, filePath, makeNewCross=True):
		self.zoom = 2
		z = self.zoom
		self.pbOrg = GdkPixbuf.Pixbuf.new_from_file(filePath)
		self.pbOrgW = self.pbOrg.get_width()
		self.pbOrgH = self.pbOrg.get_height()
		self.ki.setImgMaxs(self.pbOrgW,self.pbOrgH)

		if self.ki.x0 == None:
			self.ki.x0 = 0
			self.ki.y0 = 0
			self.ki.x1 = self.ki.pbOrgW-1
			self.ki.y1 = self.ki.pbOrgH-1

		self.pbZoom = self.pbOrg.scale_simple(
			self.pbOrgW*z, 
			self.pbOrgH*z, 
			GdkPixbuf.InterpType.BILINEAR)

		g = self.gui
		g.layoutIMain.set_size_request(self.pbOrg.get_width(), self.pbOrg.get_height())
		g.iMain.set_from_pixbuf(self.pbOrg)

		if makeNewCross:
			self.updateCrossys()



class MyImageProcess:
	def __init__(self):
		a = 0


	def find_coeffs(self,pa, pb):
		matrix = []
		for p1, p2 in zip(pa, pb):
			matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
			matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

		A = numpy.matrix(matrix, dtype=numpy.float)
		B = numpy.array(pb).reshape(8)

		res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
		return numpy.array(res).reshape(8)


	def startPerspective(self, gui):
		if gui.cc <> None:
			gui.cc.destroy()

		cc = CrossContainer(gui)
		cc.makeCross( gui.layoutIMain, 4, title="perspective")
		gui.cc = cc
		self.cc = cc
		gui.lStatus.set_text("Perspective correction, set corners of image to correct...")

	def endPerspective(self, gui):
		from PIL import Image

		print "processPerspective"
		res = self.cc.chkData(True, False)
		print res
		if res == False:
			return "Need to set corners of the image to process..."

		img = Image.open(gui.ki.tmpImgFile)

		frac = 25
		width = int(round(self.cc.getWidth()/fra)*fra)
		height = int(round(self.cc.getHeight()/fra)*fra)
		
		
		tl = self.cc.getTL()
		tr = self.cc.getTR()
		bl = self.cc.getBL()
		br = self.cc.getBR()
		print tl,"				",tr
		print bl,"				",br
		print "w,h",width,height

		coeffs = self.find_coeffs(
			[(0, 0), (width, 0), (width, height), (0, height)],
			[(tl[0], tl[1]), (tr[0], tr[1]), (br[0],br[1]), (bl[0],bl[1])])

		img = img.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)

		gui.cc.destroy()

		img.save("/tmp/gimgkap_transform.png")		
		gui.ev.loadFile("/tmp/gimgkap_transform.png")

		return "OK"	

	def startEnhance(self, gui):
		img = Image.open(gui.ki.tmpImgFile)
		enhancer = ImageEnhance.Sharpness(img)
		factor = 7.0 / 4.0
		img = enhancer.enhance(factor)
		img.save("/tmp/gimgkap_enhanced.png")
		gui.ev.loadFile("/tmp/gimgkap_enhanced.png",False)
		
	def addScale(self, box, title, min, max):
		box.add( Gtk.Label(title) )
		scale = Gtk.HScale()
		scale.set_range(min,max)
		scale.set_value(1.0)
		scale.connect("value-changed", self.changedCB)
		box.add(scale)
		return scale

	def startColor(self, gui):
		self.gui = gui
		gmsg = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL| Gtk.DialogFlags.DESTROY_WITH_PARENT, 
				Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, 
				"Set contrast")

		box = Gtk.VBox()
		self.scaleContrast = self.addScale(box, "Contrast:", 0.0, 5.0)
		self.scaleBrightness = self.addScale(box, "Brightness:", 0.0, 2.0)
		self.scaleColor = self.addScale(box, "Color:", 0.0, 5.0)
		c = gmsg.get_children()
		c[0].add(box)

		self.imgForContrast = Image.open(gui.ki.tmpImgFile)

		gmsg.show_all()
		res = gmsg.run()
		print "res",res
		if res == -5:
			img = self.change_contrast( 
				self.imgForContrast,
				self.scaleContrast.get_value(),
				self.scaleBrightness.get_value(),
				self.scaleColor.get_value()
				)
			img.save("/tmp/gimgkapColor.png")
			self.gui.ev.loadFile("/tmp/gimgkapColor.png",False)
		elif res == -4:
			self.gui.ev.loadFile(gui.ki.tmpImgFile, False)
		gmsg.destroy()



	def changedCB(self,obj):
		print "changedColor",obj.get_value()
		img = self.change_contrast( 
			self.imgForContrast,
			self.scaleContrast.get_value(),
			self.scaleBrightness.get_value(),
			self.scaleColor.get_value()
			)
		#img.save("/tmp/gimgkapContrast.png")
		#pb = GdkPixbuf.Pixbuf.new_from_file("/tmp/gimgkapContrast.png")
		#self.gui.iMain.set_from_file("/tmp/gimgkapContrast.png")
		self.gui.iMain.set_from_pixbuf( self.image_to_pixbuf(img) )

	def change_contrast(self,img, contrast,brightness,color):
		image = img
		con = ImageEnhance.Contrast(image)
		image = con.enhance(contrast)
		bright = ImageEnhance.Brightness(image)
		image = bright.enhance(brightness)
		col = ImageEnhance.Color(image)
		image = col.enhance(color)
		#image.show()
		return image

	def image_to_pixbuf(self, image):
		fd = StringIO.StringIO()
		image.save(fd, "ppm")
		contents = fd.getvalue()
		fd.close()
		loader = GdkPixbuf.PixbufLoader()
		loader.write(contents)
		pixbuf = loader.get_pixbuf()
		loader.close()
		return pixbuf


class CrossContainer:
	def __init__(self,gui):
		self.gui = gui
		self.cross = []

	def destroy(self):
		for c in self.cross:
			c.destroy()
		self.gui.cc = None

	def makeCross(self, layout, count, title="", points=[]):
		for i in range(0, count):
			try:
				v = points[i]
			except:
				v = None
			c = Cross(gui=self.gui, no=i, title=title, values=v)
			c.addWidget( layout )
			self.cross.append(c)

	def set_visible(self, status):
		for c in self.cross:
			c.set_visible(status)

	def getXY(self, crossNo):
		return [self.cross[crossNo].x, self.cross[crossNo].y]

	def getTL(self):
		return self.getXY(0)

	def getTR(self):
		return self.getXY(1)

	def getBR(self):
		return self.getXY(2)

	def getBL(self):
		return self.getXY(3)

	def getWidth(self):
		tl = self.getTL()
		br = self.getBR()

		return br[0]-tl[0] 

	def getHeight(self):
		tl = self.getTL()
		br = self.getBR()

		return br[1]-tl[1] 


	def chkData(self, xySet, LLSet):
		for c in self.cross:
			if xySet and ( c.x == None or c.y == None):
				return False
			if LLSet and ( c.lat == None or c.lon == None ):
				return False

		return True

class Cross:
	def __init__(self, gui=None, no=0, title="", x=None, y=None, lat=None, lon=None, values=None):
		self.gui = gui
		self.no = no
		self.title = title
		self.x = x
		self.y = y
		self.lat = lat
		self.lon = lon

		self.imgW = 32
		self.imgH = 32

		self.drag = False
		l = 0

		if values<>None:
			l = len(values)
			if l>=2:
				self.x = int(values[0])
				self.y = int(values[1])
			if l==4:
				self.lat = values[2]
				self.lon = values[3]

		print "Cross init no ",no," -> values",values,"len",l,"x,y",self.x,self.y,"lat,lon",self.lat,self.lon

		self.updateInProgress = False

		self.initGui()

	def destroy(self):
		self.layout.remove(self.eb)

	def getXY(self):
		if self.x == None:
			x = 40 * (self.no+1)
		else:
			x = self.x
		if self.y == None:
			y = 40 * (self.no+1)
		else:
			y = self.y

		return [ int(x-self.imgW*0.5), int( y-self.imgH*0.5) ]
 
	
	def addWidget(self, layout):
		print "addWidget x,y",self.x,self.y
		self.layout = layout
		layout.add( self.eb )
		x,y = self.getXY()
		self.moveTo( x, y, False)
		#xoff,yoff = self.getXY()
		#self.moveTo( xoff, yoff )

	def set_visible(self, status):
		self.eb.set_visible(status)

	def initGui(self):
		self.eb = Gtk.EventBox()
		self.eb.connect("button-press-event", self.ev_press)
		self.eb.connect("button-release-event", self.ev_release)
		self.eb.connect("motion-notify-event", self.ev_move)

		self.icon = Gtk.Image()
		self.icon.set_from_file("./imgCross.png")
		self.eb.add(self.icon)

		self.eb.show_all()

	def moveTo(self, x, y, updateDetailWindow=True):
		print "moveTo"
		self.x = x
		self.y = y
		self.gui.ki.chkMinMax( self )
		x,y = self.getXY()
		self.layout.move(self.eb, x, y)		
		#print "x,y",x,y,"lat,lon",self.lat,self.lon
		if updateDetailWindow:
			if self.title == "perspective":
				self.gui.makeDetailWindow(crosObj=self, values="xy")
			elif self.title == "LatLon":
				self.gui.makeDetailWindow(crosObj=self, values="xyl")

	def moveCrossBy(self, xm, ym):
		print "moveCrossBy"
		c = self
		x = c.x + xm
		y = c.y + ym
		self.moveTo(x,y)

	def ev_press(self,obj,ev):
		print "ev_press title[%s] no[%s]" % (self.title, self.no)
		self.updateInProgress = True
		self.gui.eventOnCross = self
		self.drag = True
		if self.title == "perspective":
			self.gui.makeDetailWindow(crosObj=self, values="xy")
			if self.no == 0:
				self.gui.lStatus.set_text("set top left corner")
			elif self.no == 1:
				self.gui.lStatus.set_text("set top right corner")
			elif self.no == 2:
				self.gui.lStatus.set_text("set bottom right corner")
			elif self.no == 3:
				self.gui.lStatus.set_text("set bottom left corner")
		elif self.title == "LatLon":
			self.gui.makeDetailWindow(crosObj=self, values="xyl")
			if self.no == 0:
				self.gui.lStatus.set_text("set top left or right corner")
			if self.no == 1:
				self.gui.lStatus.set_text("set bottom left or right corner")

		self.updateInProgress = False

	def ev_release(self,obj,ev):
		print "ev_release"
		self.drag = False

	def ev_move(self,obj,ev):
		print "ev_move"
		pw = obj.get_parent_window().get_pointer()
		self.moveTo( pw[1], pw[2])
		
			





class KapImg:
	def __init__(self):
		self.makeCleanStart()

	def makeCleanStart(self):
		self.refs = []
		self.scale = 0
		self.p0Status = False
		self.x0 = None
		self.y0 = None
		self.lat0 = None
		self.lon0 = None
		self.p1Status = False
		self.x1 = None
		self.y1 = None
		self.lat1 = None
		self.lon1 = None

	def setImgMaxs(self,w,h):
		self.pbOrgW = w
		self.pbOrgH = h


	def makeMinMax(self,val,max):
		if val < 0 :
			return 0
		if val >= max:
			return max
		return val

	def chkMinMax(self, crossObj):
		crossObj.x = self.makeMinMax(crossObj.x, self.pbOrgW)
		crossObj.y = self.makeMinMax(crossObj.y, self.pbOrgH)

	def llToStr(self, ll):
		return ("%s"%ll).replace("'","d")

	def saveAs(self, gui, filePath):
		print "saveAs"

		if filePath[-4:] <> ".kap":
			filePath+= ".kap"

		print "	target file [%s]"%filePath

		c0 = gui.cc.cross[0]
		c1 = gui.cc.cross[1]

		w = c1.x-c0.x
		h = c1.y-c0.y
		try:
			lw = c1.lon-c0.lon
			lh = c1.lat-c0.lat
			sw = w/lw
			sh = h/lh
			print "w,h",w,h,"lw,lh",lw,lh,"sw,sh",sw,sh
		except:
			a = 0

		cmd = "imgkap "+\
			"\"%s\" " % self.tmpImgFile +\
			"\"%s\" \"%s\" \"%s;%s\" " % ( self.llToStr(c0.lat), self.llToStr(c0.lon), c0.x, c0.y) +\
			"\"%s\" \"%s\" \"%s;%s\" " % ( self.llToStr(c1.lat), self.llToStr(c1.lon), c1.x-1, c1.y-1) +\
			"\"%s\"" %filePath
		print "	cmd\n\t------------------------------------\n\t%s\n\t------------------------------------" % cmd
		r = self.execute(cmd)
		if r == 0:
			gmsg = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL| Gtk.DialogFlags.DESTROY_WITH_PARENT, 
				Gtk.MessageType.INFO, Gtk.ButtonsType.OK, 
				"File is ready in \n'" + filePath + "'")
		else:
			gmsg = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL| Gtk.DialogFlags.DESTROY_WITH_PARENT, 
				Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, 
				"Something weant wrong :(")
		gmsg.show_all()
		gmsg.run()
		gmsg.destroy()
		print "DONE"



	def extractImage(self, filePath):
		self.tmpImgFile = "/tmp/imgFromKap.png"
		cmd = "imgkap \"%s\" %s" % (filePath, self.tmpImgFile)
		os.system(cmd)
		return self.tmpImgFile


	def analize(self,filePath):
		self.makeCleanStart()
		f = open( filePath )
		print "	analize ... [%s]" % filePath

		while True:
			l = f.readline()
			if l and self.is_ascii(l[0:1]):
				self.parse( l )	
				if len(self.refs) == 4:
					break
			else:
				return 0


	def parse(self, line):
		if line[:7] == "KNP/SC=":
			t = line[7:].split(",")
			self.scale = int( t[0] )
		
		if line[:4] == "REF/":
			t = line[4:-2].split(",")
			self.refs.append(line)

			x = int( t[1] )
			y = int( t[2] )
			lat = float( t[3] )
			lon = float( t[4] )

			if self.x0 == None:
				self.x0 = x
				self.y0 = y 
				self.lat0 = lat
				self.lon0 = lon
				self.x1 = x
				self.y1 = y 
				self.lat1 = lat
				self.lon1 = lon

			if self.x0 >= x and self.y0 >= y:
				self.p0Status = True
				self.x0 = x
				self.y0 = y
				self.lat0 = lat
				self.lon = lon

			if self.x1 <= x and self.y1 <= y:
				self.p1Status = True
				self.x1 = x
				self.y1 = y 
				self.lat1 = lat
				self.lon1 = lon


	def is_ascii(self,s):
		return all(ord(c) < 128 for c in s)


	def analizeStatus(self):
		if self.p0Status and self.p1Status and self.x0 <> self.x1 and self.y0 <> self.y1:
			print "\n".join(self.refs)
			return True
		return False



	def chkFileType(self,path):
		tr = ""
		try:
			GdkPixbuf.Pixbuf.new_from_file(path)
			tr = "img"
		except:
			a = 0

		if tr == "":
			t = path.split(".")
			if t[-1] == "kap":
				tr = "kap"

		return tr


	def chkIfImgkapIsPressent(self):
		return self.cmd("imgkap")


	def cmd(self, cmd):
		import subprocess
		return subprocess.call("type " + cmd, shell=True, 
			stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

	def execute(self, cmd):
		r = os.system(cmd)
		return r

if __name__ == "__main__":
	gui = GImgkapGui()
	gui.run()
	#k = KapImg()
	#k.execute("ls /sys")