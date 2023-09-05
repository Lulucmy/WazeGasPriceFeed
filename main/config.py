##   Config for the script   ##

class URL:
    # Path to governement price data
    __govURL__ = "URL_TO_GOVERNEMENT_DATA"

    # Path to stations data file
    # Replace SHEETSID by the ID of the Google Sheets file & SHEETNAME by the name of the sheet
    # Edit the range if needed, to match the columns of your sheet
    # The range must be in the form A:A,B:B,E:E,F:F (stationid, venue_id, lat, lon)
    __stationsURL__ = "https://docs.google.com/spreadsheets/d/SHEETSID/gviz/tq?tqx=out:csv&sheet=SHEETNAME&range=A:A,B:B,E:E,F:F"

class Feed:
    # Define the gas names to use in the feed
    # Waze Gas name in DB <=> Gas name in Feed
    # gazole 	-> 		Gazole
    # 95 		-> 		SP95-E10
    # 98 		-> 		E85
    # gpl 		-> 		GPL
    gas_map = {"Gazole": "gazole", "SP95": "SP95", "E10" : "95", "E85": "98", "GPLc": "gpl"}

    # Define if SP95 replace E10 when unavailable
    overrideSP95 = True

class Stats:
    # Define the webhook URL to send statistics (to public channel) / Daily
    __extURL__ = "https://canary.discord.com/api/webhooks/"

    # Define the webhook URL to send statistics (to private channel) / Hourly
    __intURL__ = "https://canary.discord.com/api/webhooks/"

class Init:
    # Define the brand names to use in the feed
    __brandnames__ = {
    "total": {"total", "access", "totalenergies"}, 
    "inter": {"intermarch", "intermarche", "intermarch\u00e9", "mousquetaire", "mousquetaires"}, 
    "carre": {"carrefour"}, 
    "lecle": {"e.leclerc", "leclerc"}, 
    "aucha": {"auchan"}, 
    "casin": {"casino", "g\u00e9ant", "geant", "CASINO"}, 
    "avia": {"avia"}, 
    "dynef": {"dyneff", "dynef"}, 
    "elan": {"elan"}, 
    "esso": {"esso"}, 
    "vito": {"vito"},
    "cora": {"cora"},
    "systu": {"u", "systemu", "superu", "utile"},
    "agip": {"agip", "eni"},
    "bp": {"bp"},
    "shell": {"shell"},
    "gulf": {"gulf"},
    "spar": {"spar"},
    "atac": {"atac", "attac"},
    "as24": {"as24", "as"},
    "dats": {"dats24", "dats"},
    "match": {"match"},
    "netto": {"netto"},
    "bi1": {"bi1"}
}