# Budget Tracker – Flask & MySQL

Dieses Repository enthält eine Webanwendung zur Verwaltung persönlicher Ausgaben und Budgets.  
Die Applikation wurde im Rahmen der Praxisarbeit **Datenbanken und Webentwicklung (DBWE)** an der **ipso Bildung** entwickelt und erfüllt die fachlichen sowie technischen Anforderungen der Aufgabenstellung.

Die Anwendung basiert auf **Python (Flask)** und einer **relationalen MySQL-Datenbank**.  
Neben einer interaktiven Weboberfläche steht zusätzlich ein **RESTful Web-API** für den Zugriff auf ausgewählte Daten zur Verfügung.

---

## Inhaltsverzeichnis

- Projektübersicht  
- Funktionsumfang  
- Technologien  
- Architektur  
- Installation & Setup  
- Datenbankstruktur  
- Benutzerhandbuch  
- REST API  
- Tests  
- Deployment  
- Sicherheit  
- Projektkontext  
- Lizenz  

---

## Projektübersicht

Der Budget Tracker ermöglicht es Benutzern, ihre Ausgaben strukturiert zu erfassen, zu kategorisieren und auszuwerten.  
Ziel der Applikation ist eine einfache, sichere und übersichtliche Verwaltung persönlicher Finanzdaten über den Webbrowser sowie über eine API-Schnittstelle.

---

## Funktionsumfang

### Benutzerverwaltung
- Registrierung mit eindeutigem Benutzernamen und E-Mail-Adresse
- Login und Logout
- Sichere Passwortspeicherung mittels Hashing

### Ausgabenverwaltung
- Erfassen neuer Ausgaben (Betrag, Kategorie, Datum, Beschreibung)
- Bearbeiten und Löschen bestehender Ausgaben
- Benutzerbezogene Datenisolation

### Dashboard
- Übersicht aller erfassten Ausgaben
- Grafische Auswertung der Ausgaben nach Kategorien

### REST API
- Lesender Zugriff auf Ausgabendaten
- Nutzung ohne Browser möglich (z. B. Postman oder curl)

---

## Technologien

| Komponente         | Technologie                          |
|-------------------|--------------------------------------|
| Programmiersprache | Python ≥ 3.9                        |
| Web-Framework      | Flask                               |
| Datenbank          | MySQL                               |
| Datenbankzugriff   | mysql.connector (Raw SQL)           |
| Authentifizierung | Flask-Login                         |
| Webserver          | Flask Dev Server / Gunicorn         |
| Frontend           | HTML5, CSS3, Bootstrap              |

---

## Architektur

Die Applikation ist serverseitig mit Flask umgesetzt und folgt einer klaren Trennung zwischen:

- Routen und Geschäftslogik (Flask)
- Direktem Datenbankzugriff über SQL-Abfragen
- Präsentation mittels HTML-Templates

Die Persistenz der Daten erfolgt vollständig relational in MySQL.  
Die Geschäftslogik umfasst Validierungen, Benutzerzuordnung sowie Zugriffskontrolle und ist serverseitig implementiert.

---

## Installation & Setup

### Voraussetzungen
- Python 3.9 oder höher
- MySQL oder MariaDB
- Git

### Repository klonen
```bash
git clone https://github.com/<username>/Budget-Tracker-Flask-MySQL.git
cd Budget-Tracker-Flask-MySQL
```

## Virtuelle Umgebung erstellen

```bash
python -m venv .venv
source .venv/binactivate    # Linux / macOS
.venv\Scripts\activate      # Windows
```

## Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```
## Applikation starten

```bash
flask run
```
