# me - this DAT
# scriptOp - the OP which is cooking
#
# press 'Setup Parameters' in the OP to call this function to re-create the parameters.

# called whenever custom pulse parameter is pushed
def onPulse(par):
	return

def onCook(scriptOp):
	if hasattr(parent.curycue.ext, "CuryCueClass"): 
		scriptOp.clear()
		for fix in parent.curycue.LocalFixtureData:
			myLocation=""
			
			scriptOp.appendRow([fix.id, "%g" % fix.order, fix.name, fix.original_location if fix.original_location!=fix.global_object_location else fix.global_object_location])

	#scriptOp.copy(scriptOp.inputs[0])	# no need to call .clear() above when copying
	#scriptOp.insertRow(['color', 'size', 'shape'], 0)
	#scriptOp.appendRow(['red', '3', 'square'])
	#scriptOp[1,0] += '**'

	return

def onSetupParameters(scriptOp):
	"""Auto-generated by Component Editor"""
	# manual changes to anything other than parJSON will be	# destroyed by Comp Editor unless doc string above is	# changed

	TDJSON = op.TDModules.mod.TDJSON
	parJSON = """
	{
		"Custom": {}
	}
	"""
	parData = TDJSON.textToJSON(parJSON)
	TDJSON.addParametersFromJSONOp(scriptOp, parData, destroyOthers=True)