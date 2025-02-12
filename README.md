# Cad Pessoa

A FastAPI-based application for managing person records.

## Project Structure

The project is organized as follows:
- `core/` - Core application logic and models
  - `pessoa/` - Person management module
  - `telefone/` - Phone management module
  - `config/` - Application configuration
- `main.py` - Application entry point
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Docker Compose configuration for easy deployment
- `pyproject.toml` and `poetry.lock` - Python dependency management with Poetry
- `tests/` - Unit and integration tests

## Getting Started

### Prerequisites

- Python 3.x
- Poetry for dependency management
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/reinaldosaraiva/cad_pessoa.git
cd cad_pessoa
```

2. Install dependencies using Poetry:
```bash
poetry install
```

### Running the Application

You can run the application either directly with Poetry or using Docker.

#### Using Poetry
```bash
poetry run python main.py
```

#### Using Docker Compose
```bash
docker-compose up
```

## Development

The project uses Poetry for dependency management. To add new dependencies:
```bash
poetry add package-name
```

## License

This project is open source and available under the MIT License.