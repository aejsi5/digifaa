class Error():
    def __init__(self, error):
        self.code = error
        self.get_name()
    
    def get_name(self, *args, **kwargs):
        if self.code == 'UP_001':
            self.name = 'File not allowed'
            self.name_ger = 'Datei nicht erlaubt'
            self.description = 'Der Dateityp ist nicht zulässig.'
        if self.code == 'UP_002':
            self.name = 'Incorrect Coding'
            self.name_ger = 'Datei falsch codiert'
            self.description = 'Der Dateicodierungstyp ist nicht zulässig. CSV Datein müssen nach UTF-8 codiert sein'
        if self.code == 'UP_003':
            self.name = 'Not Null Constraint'
            self.name_ger = 'Pflichtfeldangabe fehlt'
            self.description = 'Die Fahrgestellnummer muss beim Import von Fahrzeugen angegeben werden'
        if self.code == 'UP_004':
            self.name = 'Not Null Constraint'
            self.name_ger = 'Pflichtfeldangabe fehlt'
            self.description = 'Fahrgestellnummer, Rückrufcode und Werkstatt müssen beim Import der Fahrzeughistorie angegeben werden'
        if self.code == 'UP_005':
            self.name = 'PK Error'
            self.name_ger = 'Fahrgestellnummer unbekannt'
            self.description = 'Die Fahrgestellnummer ist unbekannt. Der Datensatz wurde nicht importiert. Aktualisieren Sie ggf. die Fahrzeugliste'
        if self.code == 'UP_006':
            self.name = 'PK Error'
            self.name_ger = 'Rückrufcode unbekannt'
            self.description = 'Der angegebene Rückrufcode ist unbekannt. Der Datensatz wurde nicht importiert. Legen Sie ggf. einen neuen Rückruf an.'
        if self.code == 'UP_007':
            self.name = 'PK Error'
            self.name_ger = 'WerkstattID unbekannt'
            self.description = 'Die angegebene Werkstatt ist unbekannt. Der Datensatz wurde nicht importiert. Aktualisieren Sie ggf. die Werkstattliste.'
        if self.code == 'UP_008':
            self.name = 'Unexpected error'
            self.name_ger = 'Unerwarteter Fehler'
            self.description = 'Keine Fehlerbeschreibung verfügbar.'