# uMap Data API

API to provide geospatial datasets for uMap instances. This FastAPI application serves geospatial data in GeoJSON format.

## Quick Start

### Installation

Check the [INSTALL.md](INSTALL.md) for detailed installation instructions.

## API Documentation

Once running, visit:

- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Sources de données

Voici les prétraitements nécessaires pour chaque source de données :
- Les données doivent être découpées en fichiers GeoJSON par zone géographique (ex: région, département ou commune).
- Le système de coordonnées doit être WGS 84 (EPSG:4326).
- Les données doivent être au format GeoJSON valide.

Pour ajouter ou modifier des sources de données, ajoutez les fichiers de source de données dans le répertoire `data/`.
Le dossier doit être nommé ainsi : `data/<source_name>/<source_name>_<geographic_filter>.geojson`  
Par exemple `data/arbresnamr/arbresnamr_Toulouse.geojson`  
Les données et leurs filtres seront automatiquement chargées au démarrage de l'application si le système de nommage est respecté.

Attention : l’outil n’est pas un outil de géomatique, il ne permet pas de réaliser de géotraitement sur les données importées. Si vous souhaitez afficher des données comprenant une analyse, vous devez réaliser l’analyse en amont dans un logiciel du type QGis, travailler la symbologie et réaliser un export des données avec la symbologie intégrée pour ensuite l’importer dans le POC.

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions, please use the GitHub issue tracker.

