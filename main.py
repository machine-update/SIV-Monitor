import csv
import random
from datetime import datetime

LOG_FILE = "logs_systeme.csv"
REPORT_FILE = "rapport.txt"

def generate_data():
    temperature = random.randint(35, 95)
    connexion = random.choice(["OK", "OK", "OK", "PERDUE"])
    alimentation = random.randint(20, 100)
    ecran = random.choice(["OK", "OK", "OK", "ERREUR"])
    gps = random.choice(["OK", "OK", "OK", "SIGNAL_FAIBLE"])
    audio = random.choice(["OK", "OK", "ERREUR"])

    anomalies = []

    if temperature > 75:
        anomalies.append("Température élevée")
    if connexion == "PERDUE":
        anomalies.append("Connexion perdue")
    if ecran == "ERREUR":
        anomalies.append("Erreur écran voyageurs")
    if gps == "SIGNAL_FAIBLE":
        anomalies.append("Signal GPS faible")
    if audio == "ERREUR":
        anomalies.append("Erreur annonce sonore")

    statut = "ALERTE" if anomalies else "OK"

    return {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "connexion": connexion,
        "alimentation": alimentation,
        "ecran": ecran,
        "gps": gps,
        "audio": audio,
        "statut": statut,
        "anomalies": ", ".join(anomalies) if anomalies else "Aucune"
    }

def main():
    total_tests = 50
    total_alertes = 0

    with open(LOG_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "date", "temperature", "connexion", "alimentation",
            "ecran", "gps", "audio", "statut", "anomalies"
        ])
        writer.writeheader()

        for _ in range(total_tests):
            data = generate_data()
            writer.writerow(data)

            if data["statut"] == "ALERTE":
                total_alertes += 1

    taux_fiabilite = ((total_tests - total_alertes) / total_tests) * 100

    with open(REPORT_FILE, "w", encoding="utf-8") as report:
        report.write("Rapport de supervision - SIV Monitor\n")
        report.write("====================================\n\n")
        report.write(f"Nombre total de tests : {total_tests}\n")
        report.write(f"Nombre total d'alertes : {total_alertes}\n")
        report.write(f"Taux de bon fonctionnement : {taux_fiabilite:.2f}%\n")

    print("Données générées avec succès.")
    print("Fichier logs_systeme.csv créé.")
    print("Fichier rapport.txt créé.")

if __name__ == "__main__":
    main()