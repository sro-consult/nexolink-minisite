# Mettre à jour la carte des consultants nexoLink

La section « Les consultants du réseau nexoLink » du site affiche une carte de France
avec un point anonyme par consultant. Voici comment la tenir à jour.

## Le plus simple : demander à Claude

Dans une session Claude Code ouverte sur le workspace nexoLink, dire simplement :

- **Arrivée** : « Nouvel arrivant sur la carte du site : il est à Bergerac »
- **Départ** : « Retire de la carte le consultant de Guignes »

Claude s'occupe de tout : il retrouve les coordonnées de la commune, met à jour la
liste, régénère la carte dans `index.html`, fait valider le rendu par une capture,
puis commit et push après ton feu vert. Vercel met le site en ligne dans la minute.

Claude conserve la liste des localisations dans sa mémoire persistante, donc la
demande fonctionne même dans une nouvelle conversation.

## Comment ça marche en dessous

Deux fichiers dans le repo `sro-consult/nexolink-minisite` :

| Fichier | Rôle |
|---------|------|
| `consultants-carte.csv` | La liste des consultants, une ligne par personne au format `label;latitude;longitude`. **Fichier privé, jamais commité** (le repo est public et les villes ne doivent pas être citées) : il est dans le `.gitignore`. |
| `generer-carte.py` | Le script qui lit le CSV et réécrit le SVG de la carte entre les marqueurs `CARTE-CONSULTANTS:DEBUT` et `CARTE-CONSULTANTS:FIN` dans `index.html`. |

## Mise à jour manuelle (sans Claude)

1. Éditer `consultants-carte.csv` : ajouter ou supprimer une ligne
   (coordonnées de la commune trouvables sur Google Maps, clic droit sur la carte).
2. Lancer :

```bash
python3 generer-carte.py
```

3. Vérifier le rendu en ouvrant `index.html` dans un navigateur.
4. Commit et push de `index.html` uniquement (le CSV reste local) :

```bash
git add index.html && git commit -m "Mise à jour carte consultants" && git push
```

## Points d'attention

- Ne jamais commiter le CSV : les points sur la carte restent volontairement flous,
  la liste des communes ne doit pas se retrouver sur GitHub.
- Si le CSV est perdu, Claude peut le reconstituer depuis sa mémoire.
- Les points affichent tous « Consultant nexoLink » au survol, jamais de nom ni de ville.
