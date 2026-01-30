# === IMPORTATIONS ===
# discord : bibliothèque principale pour interagir avec l'API Discord
import discord
# commands : module pour créer des commandes avec préfixe (ex: !ping)
from discord.ext import commands
# tasks : module pour créer des tâches en arrière-plan (boucles périodiques)
from discord.ext import tasks as discord_tasks
# Intents : permet de définir quels événements le bot peut recevoir de Discord
from discord import Intents
# os : pour accéder aux variables d'environnement (comme le token)
import os
# dotenv : charge les variables depuis un fichier .env (optionnel sur Replit)
from dotenv import load_dotenv
# datetime : pour obtenir la date et l'heure actuelles
from datetime import datetime, timedelta
# json : pour sauvegarder et charger les tâches
import json
# dateutil : pour parser les dates en langage naturel
from dateutil import parser as date_parser
# re : pour les expressions régulières (extraction des paramètres)
import re
# smtplib : pour envoyer des emails via SMTP (Gmail)
import smtplib
# email.mime : pour construire les emails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === CONFIGURATION DU TOKEN ===
# Charge les variables d'environnement depuis le fichier .env (si présent)
load_dotenv()
# Récupère le token du bot depuis les variables d'environnement
# Note : utilise actuellement "BOT_TOKEN", pas "TOKEN_BOT_DISCORD"
TOKEN=os.getenv("BOT_TOKEN")

# === CONFIGURATION DES INTENTS ===
# Les intents définissent quels événements Discord le bot peut écouter
# default() inclut la plupart des événements de base (guilds, members, etc.)
intents = Intents.default()
# message_content = True permet au bot de lire le contenu des messages
# Nécessaire pour que les commandes avec préfixe fonctionnent
intents.message_content = True

# === CRÉATION DU BOT ===
# Crée une instance du bot avec :
# - command_prefix='!' : les commandes commencent par "!"
# - intents : les permissions définies ci-dessus
bot = commands.Bot(command_prefix='!', intents=intents)

# === CONFIGURATION DU RAPPEL ===
# Nom d'utilisateur Discord à mentionner pour les rappels
REMINDER_USER = "Emmanuel"
# ID du salon privé pour les rappels (à configurer)
REMINDER_CHANNEL_ID = os.getenv("REMINDER_CHANNEL_ID")

# === CONFIGURATION EMAIL ===
# Identifiants Gmail pour l'envoi d'emails (Secrets Replit)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Fonction pour envoyer un email de rappel
def send_reminder_email(to_email, event_name, event_date):
    """Envoie un email de rappel via Gmail SMTP."""
    if not EMAIL_USER or not EMAIL_PASS:
        print("Email non configuré (EMAIL_USER ou EMAIL_PASS manquant)")
        return False
    
    try:
        # Crée le message
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = f"Rappel : {event_name}"
        
        # Corps de l'email
        body = f"""Bonjour,

Ceci est un rappel automatique de Punkybot.

📅 Événement : {event_name}
🕐 Date : {event_date}

Rejoignez-nous sur Discord pour plus de détails !

---
Punkybot - Votre assistant Discord
"""
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        # Connexion au serveur Gmail SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())
        
        print(f"Email envoyé à {to_email}")
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'envoi d'email : {e}")
        return False

# === ÉVÉNEMENT : CONNEXION RÉUSSIE ===
# Décorateur @bot.event pour définir un gestionnaire d'événement
# on_ready() est appelé quand le bot est connecté et prêt
@bot.event
async def on_ready():
    # Affiche le nom du bot dans la console une fois connecté
    print(f'Connecté en tant que {bot.user}')
    # Démarre la tâche de vérification des rappels
    if not check_reminders.is_running():
        check_reminders.start()
        print("Tâche de rappel démarrée (vérification toutes les heures)")

# === COMMANDE : !ping ===
# Décorateur @bot.command() pour créer une commande
# La fonction s'appelle "ping", donc la commande est "!ping"
@bot.command()
async def ping(ctx):
    # ctx = contexte de la commande (contient le message, l'auteur, le salon, etc.)
    # ctx.send() envoie un message dans le même salon
    await ctx.send('Pong!')

# === FONCTIONNALITÉ TO-DO ===
# Fichier de sauvegarde des tâches
TODO_FILE = "todo.json"

# Fonction pour charger les tâches depuis le fichier JSON
def load_tasks():
    """Charge les tâches depuis todo.json, retourne une liste vide si erreur."""
    if not os.path.exists(TODO_FILE):
        print("Aucun fichier todo.json trouvé, démarrage avec liste vide.")
        return []
    try:
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"Chargé {len(data)} tâches")
            return data
    except (json.JSONDecodeError, IOError) as e:
        print(f"Erreur lors du chargement de todo.json: {e}. Liste vide utilisée.")
        return []

# Fonction pour sauvegarder les tâches dans le fichier JSON
def save_tasks():
    """Sauvegarde les tâches dans todo.json."""
    try:
        with open(TODO_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        print(f"Sauvegardé {len(tasks)} tâches")
    except IOError as e:
        print(f"Erreur lors de la sauvegarde: {e}")

# Charge les tâches au démarrage du bot
tasks = load_tasks()

# === COMMANDE : !todo ===
# Commande avec sous-commandes : add, list, done
# Utilise *args pour capturer tout le texte après la sous-commande
@bot.command()
async def todo(ctx, subcommand: str = None, *, args: str = None):
    # Vérifie qu'une sous-commande est fournie
    if subcommand is None:
        await ctx.send("Usage : `!todo add <texte>`, `!todo list`, `!todo done <numéro>`")
        return
    
    # === SOUS-COMMANDE : add ===
    # Ajoute une nouvelle tâche à la liste
    if subcommand.lower() == "add":
        # Vérifie que du texte est fourni
        if args is None or args.strip() == "":
            await ctx.send("Erreur : Veuillez fournir un texte pour la tâche. Exemple : `!todo add Acheter du pain`")
            return
        # Ajoute la tâche à la liste
        tasks.append(args.strip())
        save_tasks()
        await ctx.send(f"Tâche ajoutée : **{args.strip()}**")
    
    # === SOUS-COMMANDE : list ===
    # Affiche toutes les tâches numérotées
    elif subcommand.lower() == "list":
        # Vérifie si la liste est vide
        if len(tasks) == 0:
            await ctx.send("La liste de tâches est vide.")
            return
        # Construit la liste numérotée
        message = "**Liste des tâches :**\n"
        for i, task in enumerate(tasks, start=1):
            message += f"{i}. {task}\n"
        await ctx.send(message)
    
    # === SOUS-COMMANDE : done ===
    # Supprime une tâche par son numéro
    elif subcommand.lower() == "done":
        # Vérifie qu'un numéro est fourni
        if args is None:
            await ctx.send("Erreur : Veuillez fournir le numéro de la tâche. Exemple : `!todo done 1`")
            return
        # Vérifie que c'est un nombre valide
        try:
            task_num = int(args.strip())
        except ValueError:
            await ctx.send("Erreur : Le numéro doit être un nombre entier.")
            return
        # Vérifie que le numéro est dans la plage valide
        if task_num < 1 or task_num > len(tasks):
            await ctx.send(f"Erreur : Numéro invalide. Choisissez entre 1 et {len(tasks)}.")
            return
        # Supprime la tâche (index = numéro - 1)
        removed_task = tasks.pop(task_num - 1)
        save_tasks()
        await ctx.send(f"Tâche terminée : **{removed_task}**")
    
    # === SOUS-COMMANDE INCONNUE ===
    else:
        await ctx.send("Sous-commande inconnue. Utilisez : `add`, `list` ou `done`.")

# === FONCTIONNALITÉ SPORT ===
# Dictionnaire pour convertir les raccourcis en noms complets
SPORT_ALIASES = {
    "krav": "Krav Maga",
    "body-combat": "Body Combat",
    "bodycombat": "Body Combat",
    "zumba": "Zumba",
    "yoga": "Yoga Vinyasa",
    "pump": "Body Pump",
    "body-pump": "Body Pump",
    "bodypump": "Body Pump",
    "gym": "Gym",
    "piscine": "Piscine",
}

# Routine hebdomadaire
ROUTINE_HEBDO = """**Ma routine sportive hebdomadaire :**
🟢 **Lun** : Yoga Vinyasa / Combat
🔵 **Mar** : Body Combat / Pump
🟡 **Mer** : Zumba
🔴 **Jeu** : Krav Maga
🔵 **Ven** : Body Combat / Pump
🔴 **Sam** : Krav Maga / Gym
🏊 **Dim** : Piscine / Détente"""

# === COMMANDE : !sport ===
# Enregistre une séance de sport avec la date
@bot.command()
async def sport(ctx, *, activity: str = None):
    # Vérifie qu'une activité est fournie
    if activity is None:
        await ctx.send("Usage : `!sport <activité>` ou `!sport routine`")
        return
    
    # Nettoie l'entrée
    activity = activity.strip().lower()
    
    # === SOUS-COMMANDE : routine ===
    # Affiche la routine hebdomadaire
    if activity == "routine":
        await ctx.send(ROUTINE_HEBDO)
        return
    
    # Récupère la date actuelle formatée
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Convertit le raccourci en nom complet si disponible
    sport_name = SPORT_ALIASES.get(activity, activity.title())
    
    # Crée un embed Discord pour afficher la séance
    embed = discord.Embed(
        title="🏋️ Séance enregistrée",
        description=f"**{sport_name}** – {date_now}",
        color=discord.Color.green()
    )
    embed.set_footer(text="Routine hebdo Punkybot")
    
    # Envoie l'embed
    await ctx.send(embed=embed)

# === FONCTIONNALITÉ PLANNING ===
# Fichier de sauvegarde du planning
PLANNING_FILE = "planning.json"

# Fonction pour charger le planning depuis le fichier JSON
def load_planning():
    """Charge le planning depuis planning.json, retourne une liste vide si erreur."""
    if not os.path.exists(PLANNING_FILE):
        print("Aucun fichier planning.json trouvé, démarrage avec liste vide.")
        return []
    try:
        with open(PLANNING_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"Chargé {len(data)} événements")
            return data
    except (json.JSONDecodeError, IOError) as e:
        print(f"Erreur lors du chargement de planning.json: {e}. Liste vide utilisée.")
        return []

# Fonction pour sauvegarder le planning dans le fichier JSON
def save_planning():
    """Sauvegarde le planning dans planning.json."""
    try:
        with open(PLANNING_FILE, "w", encoding="utf-8") as f:
            json.dump(planning, f, ensure_ascii=False, indent=2)
        print(f"Sauvegardé {len(planning)} événements")
    except IOError as e:
        print(f"Erreur lors de la sauvegarde du planning: {e}")

# Charge le planning au démarrage du bot
planning = load_planning()

# === COMMANDE : !plan ===
# Planifie un événement avec date/heure et email
# Format : !plan "<événement>" <email>
@bot.command()
async def plan(ctx, *, args: str = None):
    # Vérifie que des arguments sont fournis
    if args is None:
        await ctx.send('Usage : `!plan "<événement avec date>" <email>`\nExemple : `!plan "samedi 15h30 cours Python" alessandro@exemple.com`')
        return
    
    # Parse les arguments : extrait le texte entre guillemets et l'email
    match = re.match(r'"([^"]+)"\s+(\S+@\S+)', args)
    if not match:
        await ctx.send('Format invalide. Utilisez : `!plan "<événement>" <email>`')
        return
    
    event_text = match.group(1)
    email = match.group(2)
    
    # Parse la date/heure depuis le texte de l'événement
    try:
        parsed_date = date_parser.parse(event_text, fuzzy=True, dayfirst=True)
        date_str = parsed_date.strftime("%A %d/%m à %Hh%M")
    except (ValueError, TypeError):
        date_str = "date non reconnue"
        parsed_date = None
    
    # Crée l'entrée du planning
    event_entry = {
        "event": event_text,
        "date": parsed_date.isoformat() if parsed_date else None,
        "date_display": date_str,
        "email": email
    }
    
    # Ajoute au planning et sauvegarde
    planning.append(event_entry)
    save_planning()
    
    # Crée un embed de confirmation
    embed = discord.Embed(
        title="📅 Rappel planifié",
        description=f"**{event_text}**",
        color=discord.Color.blue()
    )
    embed.add_field(name="Date", value=date_str, inline=True)
    embed.add_field(name="Email", value=email, inline=True)
    embed.set_footer(text="Rappel planifié → email envoyé")
    
    await ctx.send(embed=embed)

# === TÂCHE DE RAPPEL AUTOMATIQUE ===
# Vérifie toutes les heures si un événement est dans moins d'1 heure
@discord_tasks.loop(hours=1)
async def check_reminders():
    """Vérifie le planning et envoie des rappels pour les événements proches."""
    print(f"Vérification des rappels à {datetime.now().strftime('%H:%M')}")
    
    # Recharge le planning depuis le fichier (au cas où modifié)
    current_planning = load_planning()
    
    if not current_planning:
        print("Aucun événement dans le planning")
        return
    
    # Récupère le salon de rappel
    if REMINDER_CHANNEL_ID:
        try:
            channel = bot.get_channel(int(REMINDER_CHANNEL_ID))
        except ValueError:
            channel = None
    else:
        channel = None
    
    now = datetime.now()
    one_hour_later = now + timedelta(hours=1)
    events_to_remove = []
    
    for i, event in enumerate(current_planning):
        if event.get("date"):
            try:
                event_date = datetime.fromisoformat(event["date"])
                # Si l'événement est dans moins d'1 heure
                if now <= event_date <= one_hour_later:
                    # Construit le message de rappel
                    reminder_msg = f"⏰ **Rappel** @{REMINDER_USER} : **{event['event']}** dans moins d'1 heure !"
                    
                    if channel:
                        # Envoie dans le salon configuré
                        await channel.send(reminder_msg)
                        print(f"Rappel Discord envoyé : {event['event']}")
                    else:
                        print(f"Rappel (pas de salon configuré) : {event['event']}")
                    
                    # Envoie l'email de rappel si configuré
                    if event.get("email"):
                        send_reminder_email(
                            event["email"],
                            event["event"],
                            event.get("date_display", event_date.strftime("%d/%m/%Y à %H:%M"))
                        )
                    
                    # Marque l'événement pour suppression après rappel
                    events_to_remove.append(i)
                    
            except (ValueError, TypeError) as e:
                print(f"Erreur de date pour l'événement : {e}")
    
    # Supprime les événements rappelés (en ordre inverse pour éviter les décalages d'index)
    if events_to_remove:
        global planning
        for i in reversed(events_to_remove):
            planning.pop(i)
        save_planning()
        print(f"{len(events_to_remove)} événement(s) supprimé(s) après rappel")

@check_reminders.before_loop
async def before_check_reminders():
    """Attend que le bot soit prêt avant de démarrer la boucle."""
    await bot.wait_until_ready()

# === DÉMARRAGE DU BOT ===
# Lance le bot avec le token récupéré
# Cette ligne bloque l'exécution et maintient le bot en ligne
bot.run(TOKEN)

