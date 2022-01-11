import requests
import pandas as pd

try:
	# We are creating an empty list called "results".
	results = []
	# National Bridge Inventory (NBI) Bridges API documentation page is here: https://hifld-geoplatform.opendata.arcgis.com/datasets/national-bridge-inventory-nbi-bridges/api
	# NBI guide is here: https://www.fhwa.dot.gov/bridge/mtguide.pdf
	url = "https://geo.dot.gov/server/rest/services/Hosted/National_Bridge_Inventory_DS/FeatureServer/0/query"
	payload = "where=(state_code_001=36)%20AND%20(county_code_003=59%20OR%20county_code_003=103)&outFields=county_code_003,structure_number_008,location_009,facility_carried_007,features_desc_006a,owner_022,year_built_027,year_reconstructed_106,date_of_inspect_090,bridge_condition&outSR=4326&f=json"
	# "requests" documentation page is here: https://docs.python-requests.org/en/master/user/quickstart/
	request = requests.get(url, params=payload)
	for bridge in request.json()["features"]:
		result = {}
		result["structure_number"] =  bridge["attributes"]["structure_number_008"]
		if bridge["attributes"]["county_code_003"] == 59:
			result["county"] = "Nassau"
		elif bridge["attributes"]["county_code_003"] == 103:
			result["county"] = "Suffolk"
		else:
			result["county"] = ""
		result["location"] =  bridge["attributes"]["location_009"]
		result["feature_carried"] =  bridge["attributes"]["facility_carried_007"]
		result["feature_crossed"] =  bridge["attributes"]["features_desc_006a"]
		if bridge["attributes"]["owner_022"] == 1:
			result["owner"] = "State Highway Agency"
		elif bridge["attributes"]["owner_022"] == 2:
			result["owner"] = "County Highway Agency"
		elif bridge["attributes"]["owner_022"] == 3:
			result["owner"] = "Town or Township Highway Agency"
		elif bridge["attributes"]["owner_022"] == 4:
			result["owner"] = "City or Municipal Highway Agency"
		elif bridge["attributes"]["owner_022"] == 11:
			result["owner"] = "State Park, Forest, or Reservation Agency"
		elif bridge["attributes"]["owner_022"] == 12:
			result["owner"] = "Local Park, Forest, or Reservation Agency"
		elif bridge["attributes"]["owner_022"] == 21:
			result["owner"] = "Other State Agencies"
		elif bridge["attributes"]["owner_022"] == 25:
			result["owner"] = "Other Local Agencies"
		elif bridge["attributes"]["owner_022"] == 26:
			result["owner"] = "Private (other than railroad)"
		elif bridge["attributes"]["owner_022"] == 27:
			result["owner"] = "Railroad"
		elif bridge["attributes"]["owner_022"] == 31:
			result["owner"] = "State Toll Authority"
		elif bridge["attributes"]["owner_022"] == 32:
			result["owner"] = "Local Toll Authority"
		elif bridge["attributes"]["owner_022"] == 60:
			result["owner"] = "Other Federal Agencies (not listed below)"
		elif bridge["attributes"]["owner_022"] == 61:
			result["owner"] = "Indian Tribal Government"
		elif bridge["attributes"]["owner_022"] == 62:
			result["owner"] = "Bureau of Indian Affairs"
		elif bridge["attributes"]["owner_022"] == 63:
			result["owner"] = "Bureau of Fish and Wildlife"
		elif bridge["attributes"]["owner_022"] == 64:
			result["owner"] = "U.S. Forest Service"
		elif bridge["attributes"]["owner_022"] == 66:
			result["owner"] = "National Park Service"
		elif bridge["attributes"]["owner_022"] == 67:
			result["owner"] = "Tennessee Valley Authority"
		elif bridge["attributes"]["owner_022"] == 68:
			result["owner"] = "Bureau of Land Management"
		elif bridge["attributes"]["owner_022"] == 69:
			result["owner"] = "Bureau of Reclamation"
		elif bridge["attributes"]["owner_022"] == 70:
			result["owner"] = "Corps of Engineers (Civil)"
		elif bridge["attributes"]["owner_022"] == 71:
			result["owner"] = "Corps of Engineers (Military)"
		elif bridge["attributes"]["owner_022"] == 72: 
			result["owner"] = "Air Force"
		elif bridge["attributes"]["owner_022"] == 73:
			result["owner"] = "Navy/Marines"
		elif bridge["attributes"]["owner_022"] == 74:
			result["owner"] = "Army"
		elif bridge["attributes"]["owner_022"] == 75:
			result["owner"] = "NASA"
		elif bridge["attributes"]["owner_022"] == 76:
			result["owner"] = "Metropolitan Washington Airports Service"
		elif bridge["attributes"]["owner_022"] == 80:
			result["owner"] = "Unknown"
		else:
			result["owner"] = ""
		result["year_built"] =  bridge["attributes"]["year_built_027"]
		if bridge["attributes"]["year_reconstructed_106"] == 0:
			result["year_reconstructed"] = ""
		else:
			result["year_reconstructed"] =  bridge["attributes"]["year_reconstructed_106"]
		result["date_of_last_inspection_mmyy"] =  str(bridge["attributes"]["date_of_inspect_090"]).zfill(4)
		if bridge["attributes"]["bridge_condition"] == "G":
			result["bridge_condition"] = "Good"
		elif bridge["attributes"]["bridge_condition"] == "F":
			result["bridge_condition"] = "Fair"
		elif bridge["attributes"]["bridge_condition"] == "P":
			result["bridge_condition"] = "Poor"
		else:
			result["bridge_condition"] = ""
		result["latitude"] =  bridge["geometry"]["y"]
		result["longitude"] =  bridge["geometry"]["x"]
		results.append(result)
	# "pandas" documentation page is here: https://pandas.pydata.org/docs/index.html
	df = pd.DataFrame(results)
	df.to_csv("csv/bridge-inspections.csv", index=False)
except:
	pass