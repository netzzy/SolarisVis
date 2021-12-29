import os
import re
class InternalClass:

	def __init__( self ):
		self.my=me.parent()
		print ("AnimTimeControl")
		self.myCue=self.getCue()
		return
	def Play(self):
		op.T3.op("local/time").par.play=True
	def Stop(self):
		op.T3.op("local/time").par.play=False
	def PlayOrStop(self):
		op.T3.op("local/time").par.play^=True
	def GoNextCue(self):
		if self.getCue() < self.getMaxCue():
			self.setCue(self.getCue()+1)
		else:
			self.setCue(1)
		op.MIDI.MidiWave(0)
		return 
	def GoPrevCue(self):
		op.MIDI.MidiWave(1)
		if self.getCue() > 1:
			self.setCue(self.getCue()-1)
		else:
			self.setCue(self.getMaxCue())
		return 
	def Rewind (self):
		op.MIDI.MidiWave(1)
		self.setCue(1)
	def getCue(self):
		return self.my.par.Cue.eval()
	def setCue(self, v):
		self.my.par.Cue=v
	def getMaxCue(self):
		return op(op.TC3.par.Cuesdat).numRows-1
	def getCueSecond(self, i):
		return op(op.TC3.par.Cuesdat)[i,0]
	def getFPS(self):
		return op.T3.op("local/time").par.rate

	def SetTimeFrame(self, frame):
		op.T.op("local/time").frame=frame
	def GetCurrentFrame(self):
		return op.T3.op("local/time").frame

	def Update(self):
		if self.myCue!=self.getCue():
			self.SetTimeFrame (self.getCueSecond(self.getCue()) * self.getFPS()  )
		self.myCue=self.getCue()
		#print ()
		return

	#def SetNextExportMode(self):
	#	if int (self.my.par.Exportmode) < 2:
	#		self.my.par.Exportmode=int (self.my.par.Exportmode)+1
	#	else:
	#		self.my.par.Exportmode=0
	#	return

#	def Update (self):
#		if int(self.my.par.Exportmode)  > 0:
#			self.my.par.Cycle=1
#		else: 
#			self.my.par.Cycle=0
#		#myExportMode=op("ExportMode").text

#		#if myExportMode != self.ExportMode:
#		#	if myExportMode == "NoExport":
#		#		self.UpdateParValueExport=False
#		#		self.setNoExportMode()
#		#	elif myExportMode == "ChopExport":
#		#		self.UpdateParValueExport=False
#		#		self.setChopExport()
#		#	elif myExportMode == "ValueExport":
#		#		self.UpdateParValueExport=True
#		#		self.setValueExport()

#		#if myExportMode == "ValueExport" and self.UpdateParValueExport is True:
#		#	self.ParValueExport()

#		#self.ExportMode=myExportMode
#		return
#	def setNoExportMode(self):
#		op("EXPORT").export=False
#		return 
#	def setChopExport(self):
#		op("EXPORT").export=True
#		return 
#	def setValueExport(self):
#		op("EXPORT").export=False
#		self.UpdateParValueExport=True
#		self.ParValueExport()
#		return 
#	def ParValueExport(self):
#		myChopNode=op("EXPORT")
#		for r in myChopNode.chans():
#			myName=r.name
#			myValue=r.eval()
#			if re.search(":", myName):
#				(myExportPath, myExportPar)=re.split(":", myName)
##				print ("%s, %s"%(myExportPath, myExportPar))
#				if op(myExportPath) is not None and hasattr(op(myExportPath).par, str(myExportPar)) is True:
#					setattr(op(myExportPath).par, str(myExportPar), myValue)
#		return 


#	def UpdateOld (self):
#		for i in range (1, 16):
#			vName=getattr(self.my.par, "Var"+str(i))
#			vVar=getattr(self.my.par, "Value"+str(i))
#			vDef=getattr(self.my.par, "Valdef"+str(i))
#			if str(vName) is not "":
#				envVal=""
#				try:
#					envVal=os.environ[str(vName)]
#				except:
#					envVal=vVar

#				vVar.val=envVal
#			else:
#				vVar.val=vDef.val
#	def Store (self):
#		for i in range (1, 16):
#			vName=getattr(self.my.par, "Var"+str(i))
#			vVar=getattr(self.my.par, "Value"+str(i))
			
#			if str(vName) is not "":
#				command='setx '+vName.val+ " "+ vVar.val +"\n\r"
#				os.system(command)
#		ui.messageBox('Warning!!!', 'Project needs to be reloaded, or env variables will be not updated!!!')


#	def Copy (self):
#		for i in range (1, 16):
#			vName=getattr(self.my.par, "Var"+str(i))
#			vVar=getattr(self.my.par, "Value"+str(i))
#			vDef=getattr(self.my.par, "Valdef"+str(i))
#			vDef.val=vVar.val
#	def Rename (self):
#		for i in range (1, 16):
#			vName=getattr(self.my.par, "Var"+str(i))
#			vVar=getattr(self.my.par, "Value"+str(i))
#			vDef=getattr(self.my.par, "Valdef"+str(i))
#			if str(vName) is not "":
#				vVar.label=vName.val
#			else:
#				vVar.label="Value"+str(i)