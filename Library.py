import random
from datetime import datetime
import csv

livres = {}
Emprunts = {}
utilisateurs = {}

def ProgrammePrincipal():
    while True:
        print(f"{'-'*15} Menu Principal {'-'*15}")
        print("1.Gestion des Livres")
        print("2.Gestion des Emprunts")
        print("3.Recherche de Livres")
        print("4.Statistiques sur les Livres")
        print("5.Gestion des Utilisateurs")
        print("6.Quitter")
        print('-' * 40)
        choix = input("Entrer votre choix: ")
        if choix == '1':
            GestionLivres()
        elif choix == '2':
            GestionEmprunts()
        elif choix == '3':
            RechercheLivres()
        elif choix == '4':
            StatistiquesLivres()
        elif choix == '5':
            GestionUtilisateurs()
        elif choix == '6':
            break
        else:
            print("Choix non trouver")

def generate_isbn13():
    # Prefix is always 978 or 979
    prefix = random.choice(["978", "979"])
    
    # Registration group (e.g., 0, 1, etc. for English-speaking areas)
    registration_group = str(random.randint(0, 9))
    
    # Registrant (publisher, typically 2-7 digits)
    registrant = str(random.randint(100, 9999))
    
    # Publication identifier (specific title/edition, typically 1-6 digits)
    publication = str(random.randint(100, 99999))
    
    # Combine parts without the check digit
    isbn_without_check = prefix + registration_group + registrant + publication
    
    # Calculate the check digit
    check_digit = calculate_check_digit(isbn_without_check)
    
    # Return the full ISBN-13
    return isbn_without_check + str(check_digit)

def calculate_check_digit(isbn_without_check):
    """Calculate the check digit for an ISBN-13."""
    total = 0
    for i, digit in enumerate(isbn_without_check):
        if i % 2 == 0:
            total += int(digit)  # Multiply odd-positioned digits by 1
        else:
            total += 3 * int(digit)  # Multiply even-positioned digits by 3
    
    remainder = total % 10
    return 0 if remainder == 0 else 10 - remainder

#==================== Gestion des Livres ==================
def GestionLivres():
    while True:
        print(f"{'-'*10} Gestion des Livres {'-'*10}")
        print("1.Ajouter Livre")
        print("2.Supprimer Livre")
        print("3.Quitter")
        print('-' * 30)
        choix = input("Entrer votre choix: ")
        if choix == '1':
            ajouterLivre()
        elif choix == '2':
            supprimerLivre()
        elif choix == '3':
            break
        else:
            print("Choix non trouver")

def ajouterLivre():
    titre = input("Entrer le titre du livre: ").title().strip()
    auteur = input("Entrer l'auteur du livre: ").title().strip()
    quantite = int(input("Entrer la quantite du livre: "))
    isbn = generate_isbn13()
    print(f"ISBN généré: {isbn}")
    if isbn in livres:
        print(f"Un livre avec l'ISBN {isbn} existe déjà.")
        return
    livres[isbn] = {
        "Titre": titre,
        "Auteur": auteur,
        "Quantite": quantite
    }
    print(f"Livre '{titre}' ajouté avec succès.")
    Enregistrer_Livre()

def supprimerLivre():
    isbn = input("Entrez l'ISBN du livre a supprimer: ")
    if isbn not in livres:
        print(f"Le livre avec l'ISBN {isbn} n'existe pas.")
        return
    del livres[isbn]
    print(f"Livre avec l'ISBN {isbn} supprime avec succès.")
    Enregistrer_Livre()
#====================================================================

#==================== Gestion des Emprunts ==================
def GestionEmprunts():
    while True:
        print(f"{'-'*10} Gestion des Emprunts {'-'*10}")
        print("1.Emprunter Livre")
        print("2.Retourner Livre")
        print("3.Calcul Amende")
        print("4.Quitter")
        print('-' * 30)
        choix = input("Entrer votre choix: ")
        if choix == '1':
            EmprunterLivre()
        elif choix == '2':
            RetournerLivre()
        elif choix == '3':
            CalculAmende()
        elif choix == '4':
            break
        else:
            print("Choix non trouver")

def EmprunterLivre():
    cinCl = input("Entrer le CIN du client: ")
    if cinCl not in utilisateurs:
        print("Client n'existe pas")
        return
    isbn = input("Entrer l'ISBN du livre: ")
    if isbn not in livres:
        print(f"Le livre avec l'ISBN {isbn} n'existe pas.")
        return

    if livres[isbn]['Quantite'] <= 0:
        print(f"Le livre '{(livres[isbn]['Titre'])}' n'est pas disponible pour le moment.")
        return

    Emprunts[cinCl] = isbn
    livres[isbn]['Quantite'] -= 1
    print(f"Livre '{livres[isbn]['Titre']}' emprunté avec succès par le client {cinCl}.")
    Enregistrer_Livre()
    Enregistrer_Emprunts()

def RetournerLivre():
    cinCl = input("Entrer le CIN du client: ")
    isbn = input("Entrer l'ISBN du livre: ")

    del Emprunts[cinCl]

    livres[isbn]['Quantite'] += 1
    print(f"Le livre avec l'ISBN {isbn} a été retourné avec succès.")
    Enregistrer_Livre()
    Enregistrer_Emprunts()

def CalculAmende():
    date_prevue = input("Entrer la date de retour prévue (DD/MM/YYYY): ")
    date_reel = input("Entrer la date réel de retour (DD/MM/YYYY): ")

    prevue = datetime.strptime(date_prevue, "%d/%m/%Y")
    reel = datetime.strptime(date_reel, "%d/%m/%Y")

    retard = (reel - prevue).days

    if retard > 0:
        amende = retard * 5
        print(f"Le retard: {retard} jours")
        print(f"L'amende: {amende} Dh")
    else:
        print("Aucun retard, aucune amende.")
#============================================================

#==================== Recherche de Livres ==================
def RechercheLivres():
    resultats = []

    mot_cle = input("Entrez un mot-clé pour la recherche: ")
    
    for isbn, details in livres.items():
        if mot_cle.lower() in details['Titre'].lower() or mot_cle.lower() in details['Auteur'].lower():
            resultats.append(details)

    if resultats:
        print("Résultats de la recherche:")
        for livre in resultats:
            print(f"Titre: {livre['Titre']}, Auteur: {livre['Auteur']}, Quantité: {livre['Quantite']}")
    else:
        print("Aucun livre trouvé pour le mot-clé donné.")
#===========================================================

#==================== Statistiques sur les Livres ==================
def StatistiquesLivres():
    livres_disponibles = 0

    total_livres = len(livres)
    total_empruntes = len(Emprunts)

    for info in livres.values():
        if info['Quantite'] > 0:
            livres_disponibles += 1

    print("=== Statistiques ===")
    print(f"Nombre total de livres: {total_livres}")
    print(f"Nombre de livres empruntés: {total_empruntes}")
    print(f"Nombre de livres disponibles: {livres_disponibles}")
#===================================================================

#==================== Gestion des Utilisateurs ==================
def GestionUtilisateurs():
    while True:
        print(f"{'-'*10} Gestion des Utilisateurs {'-'*10}")
        print("1.Ajouter Utilisateur")
        print("2.Supprimer Utilisateur")
        print("3.Quitter")
        print('-' * 30)
        choix = input("Entrer votre choix: ")
        if choix == '1':
            AjouterUtilisateur()
        elif choix == '2':
            SupprimerUtilisateur()
        elif choix == '3':
            break
        else:
            print("Choix non trouver")

def AjouterUtilisateur():
    nom = input("Entrer votre nom: ").capitalize()
    prenom = input("Entrer votre prenom: ").capitalize()
    cin = input("Entrer votre CIN: ")
    if cin in utilisateurs:
        print(f"Un client avec le CIN {cin} existe déjà.")
        return
    utilisateurs[cin] = {
        "Nom": nom,
        "Prénom": prenom
    }
    print(f"Client '{nom} {prenom}' ajouté avec succès.")
    Enregistrer_Utilisateurs()

def SupprimerUtilisateur():
    cin = input("Entrer le CIN du client a supprimer: ")
    if cin not in utilisateurs:
        print("Utilisateur n'existe pas")
        return
    del utilisateurs[cin]
    print(f"L'utilisateur avec le CIN '{cin}' supprime avec succès.")
    Enregistrer_Utilisateurs()
#============================================================

#==================== Enregistrer les donnees CSV ==================
def Enregistrer_Livre():
    with open('livres.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Titre", "Auteur", "ISBN", "Qantite"])

        for isbn, info in livres.items():
            writer.writerow([info['Titre'], info['Auteur'], isbn, info['Quantite']])

def Enregistrer_Emprunts():
    with open('Emprunts.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["CIN", "ISBN"])

        for cin, isbn in Emprunts.items():
            writer.writerow([cin, isbn])

def Enregistrer_Utilisateurs():
    with open('Utilisateurs.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Nom", "Prénom", "CIN"])

        for cin, info in utilisateurs.items():
            writer.writerow([info['Nom'], info['Prénom'], cin])
#====================================================================

#==================== Charger les données CSV ==================
def Charger_données():
    with open('livres.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                titre, auteur, isbn, quantite = row
                livres[isbn] = {
                    "Titre": titre,
                    "Auteur": auteur,
                    "Quantite": int(quantite)
                }
            print("Livres chargés avec succès.")

    with open('Emprunts.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            cin, isbn = row
            Emprunts[cin] = isbn
        print("Emprunts chargés avec succès.")

    with open('Utilisateurs.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            nom, prenom, cin = row
            utilisateurs[cin] = {
                "Nom": nom,
                "Prénom": prenom
            }
        print("Utilisateurs chargés avec succès.")  

#====================================================================

Charger_données()
ProgrammePrincipal()