Budget Tracker – Flask & MySQL 💸

Ein moderner Budget-Tracker zur Verwaltung persönlicher Ausgaben.
Entwickelt im Rahmen des Moduls Datenbanken und Webentwicklung (DBWE) an der ipso Bildung.
Die Anwendung beinhaltet Benutzerverwaltung, Datenbankanbindung, Dashboard, Visualisierung und eine REST-API.

⚙️ Funktionsübersicht
🔐 Benutzerverwaltung

Registrierung mit Benutzername, E-Mail und Passwort

Sicheres Login/Logout

Passwort-Hashing

💼 Ausgabenverwaltung

Erfassen von Ausgaben (Betrag, Kategorie, Datum, Beschreibung)

Bearbeiten und Löschen

Nutzerbezogene Datenhaltung

📊 Dashboard

Übersicht aller Ausgaben

Pie-Chart-Visualisierung (Chart.js)

Kategorisierte Auswertung

🌐 REST-API

Lesender Zugriff auf Ausgabendaten

Aufrufbar via Browser, curl oder Postman

Authentifiziert über Session

🧰 Technologiestack

Backend: Python 3.x, Flask, mysql-connector-python
Datenbank: MySQL oder MariaDB
Frontend: Jinja2, HTML/CSS, optional Bootstrap, Chart.js via CDN
Deployment: Lokal via python app.py, optional Gunicorn im Produktivbetrieb

📁 Projektstruktur
Budget-Tracker-Flask-MySQL-/
├─ app.py               # Hauptapplikation
├─ db_config.py         # MySQL-Konfiguration
├─ setup_db.py          # Erstellung der DB & Tabellen
├─ requirements.txt     # Python-Abhängigkeiten
├─ templates/
│  ├─ index.html
│  ├─ login.html
│  ├─ register.html
│  └─ dashboard.html
└─ static/
   └─ style.css

🚀 Installation & Setup
1. Voraussetzungen

Python 3.9+

MySQL-Server

MySQL-Benutzer mit Erstellungsrechten

2. Repository klonen
git clone https://github.com/zerosploit-0/Budget-Tracker-Flask-MySQL-.git
cd Budget-Tracker-Flask-MySQL-

3. Virtuelle Umgebung erstellen
python -m venv venv


Linux/macOS:

source venv/bin/activate


Windows:

venv\Scripts\activate

4. Abhängigkeiten installieren
pip install -r requirements.txt

5. MySQL konfigurieren

In db_config.py:

db_config = {
    "host": "localhost",
    "user": "dein_user",
    "password": "dein_passwort",
    "database": "budget_tracker"
}

6. Datenbank erstellen
python setup_db.py

7. Anwendung starten
python app.py


Webseite unter:

http://127.0.0.1:5000


Relevante Routen:

/ – Startseite

/register – Registrierung

/login – Login

/dashboard – Dashboard

📡 REST-API

Beispielendpunkt:

GET /api/expenses


Ausgabe als JSON

Authentifizierung über Session

Aufrufbar via z. B.:

curl -X GET http://127.0.0.1:5000/api/expenses

🧪 Testübersicht

Folgende Funktionen wurden manuell getestet:

✔ Registrierung

✔ Login & Fehlermeldungen bei falschen Inputs

✔ Ausgaben erfassen

✔ Ausgaben bearbeiten/löschen

✔ Pie-Chart aktualisiert sich korrekt

✔ REST-API liefert erwartetes JSON

Die Webseite wurde vollständig getestet, daher wurde auf ein separates Testprotokoll verzichtet.

👤 Autor

Student: zerosploit-0
Modul: DBWE – Datenbanken und Webentwicklung
Schule: ipso Bildung

Dieses Projekt zeigt den praktischen Einsatz von Flask, relationalen Datenbanken, API-Design und moderner Webentwicklung.