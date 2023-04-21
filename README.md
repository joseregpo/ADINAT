# Projet_syst_reseaux
    Implementation de la RFC conçu par l'équipe:
        Raphael Soriano
        Dan Vovc
        Marion Delattre
        Geoffrey Servant
        Louis Langellier
        Jose Gregorio Perez Ojeda
    
    Ce projet comporte la conception au niveau fonctionnel d'un serveur de chat
    Deux clients sont capables de se brancher sur un serveur commun,
    communiquer sur un channel générale, ou, sur demande, creer des channels
    de communcation privés et échanger entre eux
    Ils peuvent également échanger des fichiers

# Prise en Main

## Version minimal et information
    Pour lancer ce projet il faut python en version > 3.10
    Car on se sert de la methode match qui a été implementé dans la version 3.10 du langage

    -- Si la commande d'execution sur windows de python est differente de "python", il faut changer la commande qui s'execute dans les 2 .batch 
    -- Si la commande d'execution sur linux de python est differente de "python", il faut changer la commande qui s'execute dans les 2 .sh 
## SERVEUR
    Le fichier adinat.conf situé à la racine de projet
    permet de définir l'addresse ip et le port sur lequel le serveur
    va écouter.
    Sur ce fichier on trouve les variables :
        ip <---- Adresse IP sur laquelle le serveur va se lancer
        port <--- Por sur lequel le serveur va écouter
        filename <--- Nom du fichier où les logs seront mis

    Par défaut, le serveur va se lancer sur l'addresse 127.0.0.1 (localhost)
    Et sur le Port 8888

## CLIENT

### Commands
    
    signup <username> : allows you to login into the chatroom
    msg <message> : sends a message in the global chatroom,
    msgpv <username>  <user> : sends a message to someone,
    exit : allows you to leave the chatroom,
    afk : avoid you to sends message in the chatroom,
    btk : allows you to send message in the chatroom if you were afk,
    users : Notifies which clients are connected to the server,
    rename <username> : allows you to change your name,
    ping <username> : sends a ping to a user,
    channel <username> : demands the specified user to create a private channel with him,
    acceptchannel <username> : accept the channel creation demand,
    declinechannel <username> : refuse the channel creation demand,
    sharefile <username> <namefile> : Share a file to someone but he has to accept,
    acceptfile <username> <namefile> : accept the file that has been shared by a user,
    declinefile <username> <namefile> : refuse the file that has been shared by a user

## Usage 
    Une fois le fichier adinat.conf a été configuré correctemment, il est possible de lancer un serveur puis des clients.

    Pour lancer le serveur:
        Sur windows il suffit de executer le fichier windows_start_server.bat
        Sur linux il suffit de lancer le fichier linux_start_server.sh
    
    Pour lancer un serveur:
        Sur windows il suffit de executer le fichier windows_start_client.bat
        Sur linux il suffit de lancer le fichier linux_start_client.sh
        
    Une fois le client lancé, l'utilisateur pourra se connecter en tapant la commande signup.
    Une fois connecté, le client sera capable de taper des commandes depuis la ligne de texte en bas de la fenêtre.

    Pour envoyer un fichier Il faut mettre le chemin absolut du fichier dans le système dans les paramètres de la commande
    sharefile :
        sharefile <username> <file_path> <port>
    Toutes les commandes doivent respecter la syntaxe défini
    Les fichiers envoyés vont être placés dans le dossier downloads à la racine du projet

    A droite, se trouve un espace avec les utilisateurs connectés.
    Si un channel de discussion a été ouvert avec un de ces utilisateurs, On peut y accèder
    en cliquant sur son username. Et revenir dans la discussion général en cliquant sur "General"

    La commande exit ferme la connexion mais pas le programme, c'est un comportemment tout à fait normal, pas un bug.

    Il est possible de lancer un client en interface ASCII mais celui-ci n'est pas optimale et peut avoir des problèmes
    car nous avons fait des améliorations après l'implementation du IHM

    Pour le lancer, il suffit de décommenter les lignes 643 à 657 du fichier client.py

## Mocks
    Le Dossier interface_mocks comporte des tests pas fonctionnels qu'on a utilisé au moment de l'implementation d'un IHM

## 
# Authors
    Louis Langellier
    Jose Gregorio Perez Ojeda