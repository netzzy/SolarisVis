inFloatingpaneOrFixed=True


def laserEnableOutput(info):
	op.laz_tx.par.Enableout.pulse()
	pass
def laserDisableOutput(info):
	op.laz_tx.par.Disableout.pulse()
	pass

def isProjWindowOpen():
	return bool(me.ipar.states.Projwindow)

def projWindowSettings(info):
	op(me.ipar.SetiComp.P2).openParameters()

def onProjBlind(info):
	if bool(me.ipar.states.Projblind) is not True:
		op.pproj.op("FREEZER_NULL").lock=True
		
		ui.status="Выход на проектор заморожен на текущем кадре"
	else: 
		op.pproj.op("FREEZER_NULL").lock=False
		ui.status="Выход на проектор разморожен"
def OS_ENV_IMPORTER(info):
	op.Env.openParameters()
def Autoprojtoggle(info):
	op.p.par.Autoopenproj=bool(op.p.par.Autoopenproj)^True

def Autocontroltoggle(info):
	op.p.par.Autoopencontrol=bool(op.p.par.Autoopencontrol)^True	
def onNdiDroidSwitch (info):
	op.cam.par.Cam1=int(bool(int(op.cam.par.Cam1))^True)
	pass

def onVCamSwitch (info):
	op.cam.par.Cam2=int(bool(int(op.cam.par.Cam2))^True)
def onAdbCam(info):
	op.ssui.par.Tab=2
	pass
def onProjWindow(info):
	print (me.ipar.SetiComp.P2)
	if bool(me.ipar.states.Projwindow) is not True:
		op(me.ipar.SetiComp.P2).par.winopen.pulse()
		ui.status="Окно на проектор открыто"
	else:
		op(me.ipar.SetiComp.P2).par.winclose.pulse()
		ui.status="Окно на проектор закрыто"

def onOpenStoner(info):
	op.pproj.op("stoner").par.Open.pulse()
	pass

def openCompPane(name):
	global inFloatingpaneOrFixed
	if inFloatingpaneOrFixed:
		p = ui.panes.createFloating(type=PaneType.NETWORKEDITOR, name=op(name).name)
		p.owner=op(name)
	else:
		ui.panes[0].owner=op(name)

def onP(info):
	openCompPane(ipar.SetiComp.P)
	pass
def onP1(info):
	openCompPane(ipar.SetiComp.P1)
	pass
def onP2(info):
	openCompPane(ipar.SetiComp.P2)
	pass

def onL(info):
	openCompPane(ipar.SetiComp.L)
	pass
def onA(info):
	openCompPane(ipar.SetiComp.A)
	pass
def onL1(info):
	openCompPane(ipar.SetiComp.L1)
	pass
def onC(info):
	openCompPane(ipar.SetiComp.C)
	pass
def onM(info):
	openCompPane(ipar.SetiComp.M)
	pass
def onCQ(info):
	openCompPane(ipar.SetiComp.Cq)
	pass
def onCQUI(info):
	openCompPane(ipar.SetiComp.Cqui)
	pass
