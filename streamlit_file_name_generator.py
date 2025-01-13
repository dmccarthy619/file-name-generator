import streamlit as st
from datetime import datetime
import re

# Updated Predefined mappings for VORGANG, DOKUMENT, and BESCHREIBUNG
vorgang_dokument_map = {
    "001_Hauptverfahren": [
        "AAA_Identitat", 
        "BBB_Aufenthaltstitel", 
        "CCC_Wirtschaftliche-Voraussetzung", 
        "DDD_Unbescholtenheit", 
        "EEE_Sprachkenntnis", 
        "FFF_Kenntnis-Leben-in-Deutschland",
        "GGG_Bekenntnis-zur-Freiheitlich-Demokratischen-Grundordnung"
    ],
    "002_Entscheidung": [
        "AAA_Einbürgerungsurkunde", 
        "BBB_Bescheid", 
        "CCC_Aktennotiz", 
        "DDD_Vermerk", 
        "EEE_Revision"
    ],
    "003_Schriftverkehr": [
        "AAA_Briefwechsel", 
        "BBB_Mitteilung", 
        "CCC_Aufforderung-zur-Nachreichung", 
        "DDD_Eingangsbestätigung"
    ]
}

dokument_beschreibung_map = {
    # 001_Hauptverfahren
    ("001_Hauptverfahren", "AAA_Identitat"): [
        "National-Pass", 
        "Geburtsurkunde", 
        "Staatsangehörigkeitsnachweis", 
        "Namensänderungsurkunde",
        "ZZZ_Miscellaneous"
    ],
    ("001_Hauptverfahren", "BBB_Aufenthaltstitel"): [
        "EAT", 
        "Reiseausweis für Ausländer", 
        "Niederlassungserlaubnis", 
        "Blaukarte EU",
        "ZZZ_Miscellaneous"
    ],
    ("001_Hauptverfahren", "CCC_Wirtschaftliche-Voraussetzung"): [
        "Arbeitsvertrag", 
        "Gehaltsabrechnung(en)",
        "Ausbildungsvertrag",
        "Mietvertrag", 
        "Jobcenter-Bescheid", 
        "BAföG-Bescheid", 
        "Steuerbescheid",
        "ZZZ_Miscellaneous"
    ],
    ("001_Hauptverfahren", "DDD_Unbescholtenheit"): [
        "Polizeiliches Führungszeugnis", 
        "Auszug aus dem Bundeszentralregister",
        "Verfassungschutz Anfrage",
        "ZZZ_Miscellaneous"
    ],
    ("001_Hauptverfahren", "EEE_Sprachkenntnis"): [
        "Sprachzertifikat-B1",
        "Sprachzertifikat-B2",
        "Sprachzertifikat-C1",
        "Schulzeugnisse",
        "Schulabschluss",
        "Nachweis über Teilnahme an Integrationskursen",
        "ZZZ_Miscellaneous"
    ],
    ("001_Hauptverfahren", "FFF_Kenntnis-Leben-in-Deutschland"): [
        "Einbürgerungstest-Zertifikat", 
        "Relevante-Abschluss",
        "ZZZ_Miscellaneous"
    ],
    ("001_Hauptverfahren", "GGG_Bekenntnis-zur-Freiheitlich-Demokratischen-Grundordnung"): [
        "Erklärung über Loyalität zum Grundgesetz", 
        "Persönliches Anschreiben",
        "ZZZ_Miscellaneous"
    ],

    # 002_Entscheidung
    ("002_Entscheidung", "AAA_Einbürgerungsurkunde"): [
        "Urkundenvorlage", 
        "Entwurfsformular",
        "ZZZ_Miscellaneous"
    ],
    ("002_Entscheidung", "BBB_Bescheid"): [
        "Einbürgerungsbescheid", 
        "Ablehnungsbescheid",
        "ZZZ_Miscellaneous"
    ],
    ("002_Entscheidung", "CCC_Aktennotiz"): [
        "Vermerk zur Entscheidungsfindung", 
        "Interne Kommunikation",
        "ZZZ_Miscellaneous"
    ],
    ("002_Entscheidung", "DDD_Vermerk"): [
        "Aktennotiz über fehlende Unterlagen", 
        "Beratungsvermerk",
        "ZZZ_Miscellaneous"
    ],
    ("002_Entscheidung", "EEE_Revision"): [
        "Revisionsantrag", 
        "Widerspruchsschreiben",
        "ZZZ_Miscellaneous"
    ],

    # 003_Schriftverkehr
    ("003_Schriftverkehr", "AAA_Briefwechsel"): [
        "Schreiben an den Antragsteller", 
        "Antwortschreiben",
        "ZZZ_Miscellaneous"
    ],
    ("003_Schriftverkehr", "BBB_Mitteilung"): [
        "Mitteilung über den Verfahrensstand", 
        "Zwischenbescheid",
        "ZZZ_Miscellaneous"
    ],
    ("003_Schriftverkehr", "CCC_Aufforderung-zur-Nachreichung"): [
        "Aufforderung zur Vorlage fehlender Unterlagen",
        "ZZZ_Miscellaneous"
    ],
    ("003_Schriftverkehr", "DDD_Eingangsbestätigung"): [
        "Eingangsbestätigung für Antragsunterlagen",
        "ZZZ_Miscellaneous"
    ]
}

def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y%m%d")
        return True
    except ValueError:
        return False

def generate_file_name(person, description, date_submitted, additional_info, date_of_document):
    if not person or not description or not date_submitted:
        return "Fehler: Bitte alle Pflichtfelder ausfüllen (*)."
    
    if not validate_date_format(date_submitted.replace(".", "")):
        return "Fehler: Eingangsdatum muss im Format JJJJ.MM.TT sein."
    
    if date_of_document and not validate_date_format(date_of_document.replace(".", "")):
        return "Fehler: Datum des Dokuments muss im Format JJJJ.MM.TT sein."
    
    if additional_info and not re.match(r'^[a-zA-Z0-9 ]*$', additional_info):
        return "Fehler: Zusätzliche Info darf nur Buchstaben, Zahlen und Leerzeichen enthalten."
    
    # Replace spaces with dashes in description and additional_info
    description = description.replace(" ", "-")
    additional_info = additional_info.replace(" ", "-")
    
    if date_of_document:
        if additional_info:
            return f"{person}_{description}_{date_submitted}_{additional_info}_von-{date_of_document}"
        else:
            return f"{person}_{description}_{date_submitted}_von-{date_of_document}"
    else:
        if additional_info:
            return f"{person}_{description}_{date_submitted}_{additional_info}"
        else:
            return f"{person}_{description}_{date_submitted}"


# Streamlit App
st.title("Dateiname Generator")

# Input Fields
vorgang = st.selectbox("Vorgang *", [""] + list(vorgang_dokument_map.keys()))
dokument = st.selectbox(
    "Dokument *", 
    [""] + (vorgang_dokument_map.get(vorgang, []) if vorgang else [])
)
person = st.selectbox("Person *", [""] + ["Ast1", "Ast2"] + [f"Kind{i}" for i in range(1, 11)])
beschreibung = st.selectbox(
    "Beschreibung *", 
    [""] + (dokument_beschreibung_map.get((vorgang, dokument), []) if vorgang and dokument else [])
)
date_submitted = st.text_input("Eingangsdatum (YYYY.MM.DD) *", datetime.now().strftime("%Y.%m.%d"))
additional_info = st.text_input("Zusätzliche Info")
date_of_document = st.text_input("Datum des Dokuments (YYYY.MM.DD)")

# Generate File Name
if st.button("Dateiname generieren"):
    result = generate_file_name(
        person, beschreibung, date_submitted.replace(".", ""), additional_info, date_of_document.replace(".", "")
    )
    st.text_area("Generierter Dateiname:", value=result, height=100)
    if not result.startswith("Fehler:"):
        st.download_button("Dateiname kopieren", result, file_name="generated_filename.txt")
