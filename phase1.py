""" importations et fonction avec Argparse  """
import datetime as dt
import argparse
import json
import requests


def analyser_commande():
    """
    Générer un interpréteur de commande.

    Returns:
        Un objet Namespace tel que retourné par parser.parse_args().
        Cet objet aura l'attribut «symboles» représentant la liste des
        symboles à traiter, et les attributs «début», «fin» et «valeur»
        associés aux arguments optionnels de la ligne de commande.
    """
    parser = argparse.ArgumentParser(
        description=('Mon programme sert à aller chercher des valeurs'
        'précises grâce à un symbole boursier')
    )

    parser.add_argument(
    'symbole',
    metavar='symbole',
    type=str,
    nargs='+',
    help="symbole boursier",
)

    parser.add_argument(
    '-v', '--valeur',
    metavar='{fermeture, ouverture, min, max, volume}',
    type=str,
    dest='valeur',
    default='fermeture',
    choices=['fermeture', 'ouverture', 'min', 'max', 'volume'],
    help="Valeur recherchée (par défaut valeur de fermeture)",
)

    parser.add_argument(
    '-d', '--début',
    metavar='DATE',
    type=str,
    dest='début',
    help="date de début(la plus ancienne)",
)

    parser.add_argument(
    '-f', '--fin',
    metavar='DATE',
    type=str,
    dest='fin',
    default=dt.date.today().strftime('%Y-%m-%d'),
    help="date de fin(la plus récente, donc par défaut today)",
)

    return parser.parse_args()

def produire_historique(nom_symbole, debut_historique, fin_historique, valeur_desiree):
    """ cette fonction sert à produire l'historique associé à un symbole  """

    historique = []

    if debut_historique is None:
        debut_historique = fin_historique

    url = f'https://pax.ulaval.ca/action/{nom_symbole}/historique/'

    params = {
    'début': debut_historique,
    'fin': fin_historique,
    }

    reponse = requests.get(url=url, params=params, timeout=15)

    reponse = json.loads(reponse.text)

    for day in reversed(reponse['historique'].items()):

        historique.append((dt.datetime.strptime(day[0], '%Y-%m-%d').date(),
                          day[1][valeur_desiree]))

    print(f'titre={nom_symbole}: valeur={valeur_desiree}, '
          f'debut={repr(dt.datetime.strptime(debut_historique, "%Y-%m-%d").date())}, ' 
          f'fin={repr(dt.datetime.strptime(fin_historique, "%Y-%m-%d").date())}')
    print(historique)

args = analyser_commande()

titre = args.symbole
valeur = args.valeur
debut = args.début
fin  = args.fin

for mon_symbole in titre:
    produire_historique(mon_symbole, debut, fin, valeur)
