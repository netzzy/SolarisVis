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
			
			scriptOp.appendRow([fix.id, "%g" % fix.order, fix.name, fix.global_object_location])

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