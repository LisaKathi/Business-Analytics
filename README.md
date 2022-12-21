# Business-Analytics

Link zur App: https://lexodl-online-shopper-app-app-dc0833.streamlit.app/#online-shopper-revenue-predictor-app

Kaufen oder nicht kaufen? Diese Frage stellen sich nicht nur für Besucher von Online Shopping Portalen, sondern auch die Betreiber der Webseiten. Zum einem ist Kenntnis über Kunden ein großer Vorteil für effektives Marketing. Zum anderen hilft es realistische Budgets zu erstellen, wenn Einnahmen verlässig vorhersagen werden können. Wissen über Kaufentscheidungen ist daher eine wertvolle Ressource für zahlreiche Unternehmen.  Deshalb haben wir uns das Ziel gesetzt, eine Daten-App zu kreieren die genau diese Frage beantworten kann.

Zum Datensatz:

Der Datensatz besteht aus Merkmalsvektoren, die zu 12.330 Sitzungen gehören. Der Datensatz wurde so gebildet, dass jede Sitzung zu einem anderen Nutzer in einem Zeitraum von einem Jahr gehört, um jede Tendenz zu einer bestimmten Kampagne, einem speziellen Tag, einem Nutzerprofil oder einem Zeitraum zu vermeiden. Der Datensatz besteht aus 10 numerischen und 8 kategorischen Attributen. Das Attribut "Revenue" kann als Klassenbezeichnung verwendet werden. 

"Administrative", "Administrative Duration", "Informational", "Informational Duration", "Product Related" und "Product Related Duration" stellen die Anzahl der verschiedenen Arten von Seiten dar, die der Besucher in dieser Sitzung besucht hat, sowie die Gesamtzeit, die er in jeder dieser Seitenkategorien verbracht hat. Die Werte dieser Merkmale werden aus den URL-Informationen der vom Nutzer besuchten Seiten abgeleitet und in Echtzeit aktualisiert, wenn ein Nutzer eine Aktion durchführt, z. B. von einer Seite zu einer anderen wechselt. 

Die Merkmale "Bounce Rate", "Exit Rate" und "Page Value" stellen die von "Google Analytics" für jede Seite der E-Commerce-Website gemessenen Metriken dar. Der Wert der Funktion "Bounce Rate" für eine Webseite bezieht sich auf den Prozentsatz der Besucher, die die Website von dieser Seite aus betreten und dann verlassen ("abspringen"), ohne während dieser Sitzung weitere Anfragen an den Analyseserver zu stellen. Der Wert des Merkmals "Exit Rate" für eine bestimmte Webseite wird als der Prozentsatz aller Seitenaufrufe auf der Seite berechnet, die die letzte in der Sitzung waren. Das Merkmal "Page Value" stellt den Durchschnittswert für eine Webseite dar, die ein Nutzer vor Abschluss einer E-Commerce-Transaktion besucht hat. 

Das Merkmal"Special Day" zeigt die Nähe der Besuchszeit auf der Website zu einem bestimmten besonderen Tag (z. B. Muttertag, Valentinstag) an, an dem die Sitzungen mit größerer Wahrscheinlichkeit mit einer Transaktion abgeschlossen werden. Der Wert dieses Attributs wird unter Berücksichtigung der Dynamik des E-Commerce bestimmt, wie z. B. die Dauer zwischen dem Bestelldatum und dem Lieferdatum. Für den Valentinstag beispielsweise nimmt dieser Wert zwischen dem 2. und 12. Februar einen Wert ungleich Null an, vor und nach diesem Datum ist er gleich Null, es sei denn, er liegt in der Nähe eines anderen besonderen Tages, und am 8. Februar beträgt er maximal 1. 

Der Datensatz enthält auch das Betriebssystem, den Browser, die Region, den Verkehrstyp, den Besuchertyp (wiederkehrender oder neuer Besucher), einen booleschen Wert, der angibt, ob das Datum des Besuchs ein Wochenende ist, und den Monat des Jahres.
