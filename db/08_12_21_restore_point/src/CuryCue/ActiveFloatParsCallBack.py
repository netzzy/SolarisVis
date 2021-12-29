
def onCook(scriptOp):
	if hasattr(parent.curycue.ext, "CuryCueClass"): 	
		scriptOp.clear()
		
		for myPar in parent.curycue.ActiveFields:
			if myPar.par_text_value=='':
				myChan = scriptOp.appendChan(myPar.full_par_path)
				myChan[0]=myPar.par_value
			else:
				# ЕСЛИ ЕСТЬ ТАКОЙ ОБЪЕКТ 
				if hasattr(op(myPar.fixture_ref.global_object_location), "par"):
					# ЕСЛИ ЕСТЬ ТАКОЙ ПАРАМЕТР
					if hasattr(op(myPar.fixture_ref.global_object_location).par, myPar.par_name):
						theTextPar=getattr(op(myPar.fixture_ref.global_object_location).par, myPar.par_name)
						if theTextPar!=myPar.par_text_value:
							setattr(op(myPar.fixture_ref.global_object_location).par,
									myPar.par_name, myPar.par_text_value)

			pass
	return




















def onPulse(par):
	return

def onSetupParameters(scriptOp):
	"""Auto-generated by Component Editor"""
	# manual changes to anything other than parJSON will be	# destroyed by Comp Editor unless doc string above is	# changed

	TDJSON = op.TDModules.mod.TDJSON
	parJSON = """
	{
		"Settings": {
			"Cueid": {
				"name": "Cueid",
				"label": "Cueid",
				"page": "Settings",
				"style": "Int",
				"size": 1,
				"default": 0,
				"enable": true,
				"startSection": false,
				"readOnly": false,
				"enableExpr": null,
				"min": 0.0,
				"max": 1.0,
				"normMin": 0.0,
				"normMax": 1.0,
				"clampMin": false,
				"clampMax": false
			}
		}
	}
	"""
	parData = TDJSON.textToJSON(parJSON)
	TDJSON.addParametersFromJSONOp(scriptOp, parData, destroyOthers=True)