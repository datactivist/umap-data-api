# uMap Data API

API to provide geospatial datasets for uMap instances. This FastAPI application serves geospatial data in GeoJSON format with support for various input formats including geopackage, shapefile, GeoJSON, and CSV.

## Quick Start

### Installation

Check the [INSTALL.md](INSTALL.md) for detailed installation instructions.

## API Documentation

Once running, visit:

- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Configuration

Environment variables (`.env` file):

```env
APP_NAME=uMap Data API
DEBUG=False
DATA_DIRECTORY=./data
MAX_FEATURES_PER_REQUEST=10000
ALLOWED_ORIGINS=*
```

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
