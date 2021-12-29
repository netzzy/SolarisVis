import os
import re
isDebugVerbose=False
from UtilsClass import IOP
from SceneObjectBase import *

class ContentMasterBase (SceneToggleObject, IOP):
	def __init__(self, ownerComp):
		self.ownerComp=ownerComp
		self.I = IOP(self)
		self.ActiveList=list()
#		BaseClassesLocation.SceneToggleObject.__init__(self)

		
		for myPreset in self.ownerComp.findChildren(tags=['ContentPreset']):
			myPreset.par.reinitextensions.pulse()
		self.SelectDevice()
		self.PrepareAllPresets(True)


		return
	def Reinit (self):
		self.ownerComp.par.reinitextensions.pulse()

	def Customoperation(self):
		# for myPreset in self.ownerComp.findChildren(tags=['ContentPreset']):
		# 	print ("Processing {}".format(myPreset.path))
		# 	myPreset.copy(op(self.ownerComp.op("LocalPresetClass")))
		for myPreset in self.ownerComp.findChildren(tags=['ContentPreset']):
			myContent=myPreset.CheckContentComp()
			print ("Processing {}".format(myContent))
			if myContent.op("LocalPresetClass") is None:
				# myContent.copy(op(self.ownerComp.op("LocalPresetClass")))
				#myContent.par.extension1.val='op("./LocalPresetClass").module.LocalPresetClass(me)'
				#myContent.par.promoteextension1=True
				#myContent.op("LocalPresetClass").destroy()
				myContent.copy(op(self.ownerComp.op("LocalPresetClass")))
		pass
		

	def PrepareAllPresets(self, cookstate):
		i=0
		for myPreset in self.ownerComp.findChildren(tags=['ContentPreset']):
			myPreset.allowCooking=cookstate
			#myPreset.GarbadgeCollect()
			#myPreset.Copycustomparup()
			
		
			
	def GetActivePresetTops(self):
		tops=[]
		sops=[]
		for item in self.ActiveList:
			if self.ownerComp.op(item).op("PROJ_FRONT_OUT") is not None:
				tops.append(self.ownerComp.op(item).op("PROJ_FRONT_OUT").path)
			if self.ownerComp.op(item).op("LASER_MASER_OUT") is not None:
				sops.append(self.ownerComp.op(item).op("LASER_MASER_OUT").path)
			
		# return [" ".join(tops)]
		return [" ".join(tops), " ".join(sops)]		
		
	def GetActivePresetNames(self):
		return ", ".join(self.ActiveList)

	def SelectDevice(self):
		"""
		
		if op.vp_obj_picker.SelectedObject is not self.ownerComp:
			op.vp_obj_picker.SelectedObject=self.ownerComp
		else:
			op.vp_obj_picker.SelectedObject=None
		"""
	def Update(self):
		# _currentPreset=str(self.CurrentPreset)
		self.ActiveList=[] 
		for myPreset in self.ownerComp.findChildren(tags=['ContentPreset']):
			myPreset.Update()
			if myPreset.Armed == 1:
				self.ActiveList.append(myPreset.name)
		self.Autoopencontentcomp()
		self.ActivePresets=self.GetActivePresetNames()
		[tops, mysops]=self.GetActivePresetTops()
		# [tops]=self.GetActivePresetTops()
		self.ownerComp.op("PROJ_FRONT_OUT").par.top=tops
		
		self.ownerComp.op("LASER_MASER_IN").par.sops=mysops

		"""
		# print ("Compare {}, {}".format(_currentTox, toxName))
		if _currentTox == toxName:
			# print ("Match: {}".format(self.ownerComp.op(toxName).name))
			self.ownerComp.op(toxName).Enable()
		else:
			self.ownerComp.op(toxName).Disable()
			# print ("Disable: {}".format(self.ownerComp.op(toxName).name))
		"""
		return 
	@property
	def CurrentTox(self):
		v=""
		try:
			v=self.ownerComp.I.SelectedTox[0,0]
		except:
			v=""
		return v
	@property
	def CycleIndex (self):
		v=0
		try:
			v=int(self.ownerComp.par.Index)
		except:
			v=0
		return float(v)
	@CycleIndex.setter
	def CycleIndex (self, v):
		self.ownerComp.par.Index=float(v)
		__CycleIndex=v
	@property
	def CycleMax(self):
		return self.ownerComp.par.Max
	@property
	def CycleDefVal(self):
		return self.ownerComp.par.Default

	def Cycle(self):
		# print ("Index: {}".format(self.CycleIndex))
		val=self.CycleIndex+1
		if val < self.CycleMax:
			self.CycleIndex=val


	def CycleBack(self):
		# print ("Index: {}".format(self.CycleIndex))
		val=self.CycleIndex-1
		if val >= 0:
			self.CycleIndex=val


	def CycleForwkSub(self):
		# print ("Index: {}".format(self.CycleIndex))
		val=self.CycleSubIndex+1
		if val < self.CycleSubMax:
			self.CycleSubIndex=val


	def CycleBackSub(self):
		# print ("Index: {}".format(self.CycleIndex))
		val=self.CycleSubIndex-1
		if val >= 0:
			self.CycleSubIndex=val

	def Default (self):
		self.CycleIndex=self.CycleDefVal

	def Autoopencontentcomp(self):
		if self.Isautoopencontentcomp:
			if "ContentPreset" in ui.panes.current.owner.tags and self.CompHistoryDat[0,0]=="/project1/VideoProjectorContent":
				newPath="{}/{}".format(ui.panes.current.owner.path, ui.panes.current.owner.name)
				ui.panes.current.owner=op(newPath)

	@property
	def CompHistoryDat(self):
		return self.ownerComp.op("CompHistory/COMP_HISTORY")

	@property
	def Isautoopencontentcomp(self):
		return self.ownerComp.par.Isautoopencontentcomp

	@property
	def ActivePresets(self):
		return self.ownerComp.par.Active
	@ActivePresets.setter
	def ActivePresets(self, v):
		self.ownerComp.par.Active=v
		__ActivePresets=v