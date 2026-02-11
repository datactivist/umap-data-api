# uMap Data API

API pour fournir des jeux de données géospatiales aux instances uMap. Cette application FastAPI sert des données géospatiales au format GeoJSON.

## Démarrage rapide

### Installation

Consultez le fichier [INSTALL.md](INSTALL.md) pour des instructions d'installation détaillées.

## Documentation de l'API

Une fois l'application lancée, visitez :

- Documentation de l'API : `http://localhost:8000/docs`
- Documentation alternative : `http://localhost:8000/redoc`

## Sources de données

Voici les prétraitements nécessaires pour chaque source de données :

- Les données doivent être découpées en fichiers GeoJSON par zone géographique (ex: région, département ou commune).
- Le système de coordonnées doit être WGS 84 (EPSG:4326).
- Les données doivent être au format GeoJSON valide.

Pour ajouter ou modifier des sources de données, ajoutez les fichiers de source de données dans le répertoire `data/processed/`.

Le dossier doit être nommé ainsi : `data/processed/<source_name>/<source_name>_<geographic_filter>.geojson`

Par exemple :

- `data/processed/arbresnamr/arbresnamr_Toulouse.geojson`
- `data/processed/arbresnamr/arbresnamr_Paris.geojson`

Les données et leurs filtres seront automatiquement chargées au démarrage de l'application si le système de nommage est respecté. Dans l'exemple ci-dessus, le nom de la source est `arbresnamr` et les filtres géographiques disponibles sont `Toulouse` et `Paris`.

Attention : l’outil n’est pas un outil de géomatique, il ne permet pas de réaliser de géotraitement sur les données importées. Si vous souhaitez afficher des données comprenant une analyse, vous devez réaliser l’analyse en amont dans un logiciel du type QGis, travailler la symbologie et réaliser un export des données avec la symbologie intégrée pour ensuite l’importer dans le POC.

## Licence

Ce projet est sous licence selon les termes spécifiés dans le fichier LICENSE.

## Contribuer

1. Créez un fork du dépôt
2. Créez une branche de fonctionnalité
3. Effectuez vos modifications
4. Ajoutez des tests
5. Soumettez une pull request

## Support

Pour les problèmes et questions, veuillez utiliser le système de suivi des problèmes GitHub.
