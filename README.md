# Pet Name Generator 🐾

A delightful containerized FastAPI application with a beautiful web interface for generating creative pet names. Perfect for pet adoption centers, veterinary clinics, or anyone looking for the perfect name for their furry (or scaly) friend!

## Features

- 🌐 **Beautiful Web Interface**: Quasi-modern, responsive frontend with animations
- 🐕 **Multiple Pet Types**: Dogs, cats, birds, fish, and rabbits
- 🎲 **Random Name Generation**: Get random names or select from curated lists
- � **PWA Support**: Works offline and can be installed as an app
- 🎨 **Modern Design**: Beautiful gradient backgrounds and smooth animations
- 🎯 **Interactive UI**: Click animations, hover effects, and visual feedback
- �📊 **Flexible API**: RESTful endpoints with comprehensive documentation
- 🐳 **Containerized**: Ready-to-deploy Docker container
- 🏥 **Health Checks**: Built-in health monitoring
- 📚 **Auto Documentation**: Interactive API docs with Swagger UI
- 🧠 **Fun Pet Facts**: Learn interesting facts about your chosen pet type
- ⌨️ **Keyboard Shortcuts**: Space for generate, R for random, C to copy

## Quick Start

### Using Docker Compose (Recommended)

1. Clone or download the project files
2. Run the application:

```bash
docker-compose up --build
```

3. Access the application:
   - **Web Interface**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Alternative Docs**: http://localhost:8000/redoc

### Using Docker

```bash
# Build the image
docker build -t pet-name-api .

# Run the container
docker run -p 8000:8000 pet-name-api
```

```bash
# Build the image
docker build -t pet-name-api .

# Run the container
docker run -p 8000:8000 pet-name-api
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## API Endpoints

### Core Endpoints

- `GET /` - Web interface (frontend)
- `GET /health` - Health check endpoint

### Pet Name Generation

- `GET /pets/{pet_type}/names` - Get names for a specific pet type
  - Parameters: `count` (1-10, default 3), `random_selection` (boolean)
- `GET /pets/{pet_type}/random` - Get a single random name for a pet type

### Pet Facts

- `GET /pets/{pet_type}/facts` - Get facts for a specific pet type
  - Parameters: `count` (1-5, default 1)
- `GET /pets/{pet_type}/facts/random` - Get a single random fact for a pet type
- `GET /facts` - Get random facts from all pet types
  - Parameters: `count` (1-10, default 3)
- `GET /facts/random` - Get a single random fact from any pet type

### Supported Pet Types

- 🐕 `dog` - Popular dog names
- 🐱 `cat` - Adorable cat names
- 🐦 `bird` - Colorful bird names
- 🐠 `fish` - Aquatic-themed names
- 🐰 `rabbit` - Cute rabbit names

## Web Interface Features

The beautiful web interface includes:

### 🎨 **Visual Design**
- Modern gradient backgrounds with glassmorphism effects
- Smooth animations and hover effects
- Responsive design that works on all devices
- Beautiful typography with Google Fonts

### 🖱️ **Interactive Elements**
- Click animations with ripple effects
- Hover transformations and scaling
- Visual feedback for all interactions
- Animated pet type selection cards

### 🎯 **User Experience**
- One-click pet type selection
- Adjustable name count with +/- buttons
- Copy individual names or all names to clipboard
- Visual success/error messages
- Loading animations during API calls

### ⌨️ **Keyboard Shortcuts**
- `Space` - Generate names
- `R` - Get random name
- `C` - Copy names to clipboard
- `Escape` - Close error messages

### 📱 **PWA Features**
- Works offline with service worker
- Can be installed as a standalone app
- App-like experience on mobile devices
- Fast loading with smart caching

### 🎓 **Educational Content**
- Learn fascinating facts about each pet type
- Educational content fetched dynamically from the API
- Extensive collection of interesting pet facts

## Example Usage

### Get Random Dog Names

```bash
curl "http://localhost:8000/pets/dog/names?count=3"
```

Response:
```json
{
  "pet_type": "dog",
  "names": ["Buddy", "Luna", "Charlie"],
  "count": 3
}
```

### Get Dog Facts

```bash
curl "http://localhost:8000/pets/dog/facts"
```

Response:
```json
{
  "pet_type": "dog",
  "facts": ["Dogs have been domesticated for over 15,000 years"],
  "count": 1
}
```

### Get a Single Random Bird Name

```bash
curl "http://localhost:8000/pets/bird/random"
```

Response:
```json
{
  "pet_type": "bird",
  "name": "Rainbow"
}
```

### Get Random Facts from All Pet Types

```bash
curl "http://localhost:8000/facts?count=2"
```

Response:
```json
{
  "facts": [
    "Dogs have been domesticated for over 15,000 years",
    "Cats spend 70% of their lives sleeping"
  ],
  "count": 2
}
```

**Note:** Check out the API docs for more examples.

## Configuration

### Environment Variables

The application supports the following environment variables:

- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)

### Docker Health Checks

The container includes health checks that verify the API is responding correctly:

- **Interval**: 30 seconds
- **Timeout**: 30 seconds
- **Retries**: 3
- **Start Period**: 5 seconds

## Development

### Adding New Pet Types

To add support for new pet types:

1. Add the pet type, names, and facts to `PET_NAMES_DB` and `PET_FACTS_DB` in `main.py`
2. The API will automatically support the new pet type for both names and facts

### Extending the API

The codebase is structured for easy extension:

- **Models**: Pydantic models for request/response validation
- **Data**: Pet names and facts databases as dictionaries
- **Routes**: FastAPI route handlers with clear separation of concerns
- **Validation**: Built-in request/response validation with OpenAPI docs

## API Documentation

Once running, visit these URLs for interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Production Deployment

### Docker Deployment

For production deployment:

1. **Security**: Use secrets management for sensitive data
2. **Monitoring**: Implement proper logging and monitoring
3. **Scaling**: Use a container orchestration platform like Kubernetes for scaling

### Performance Considerations

- The API is stateless and suitable for horizontal scaling
- Consider adding Redis for caching if extending functionality
- Database integration can be added for dynamic pet name management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the GNU General Public License v2.0 (GPLv2).

## Support

For questions or issues:

1. Check the interactive API documentation at `/docs`
2. Review the health endpoint at `/health`
3. Test the API endpoints using the included `test_api.py` script
4. Open an issue in the repository

---

Made with ❤️ for pet lovers everywhere! 🐾
