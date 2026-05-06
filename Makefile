.PHONY: help install lint test train predict docker-build docker-up docker-down

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -e ".[dev,test,training]"

lint: ## Run linting and formatting checks
	ruff check src/ tests/
	ruff format --check src/ tests/
	mypy src/

format: ## Auto-format code
	ruff format src/ tests/
	ruff check --fix src/ tests/

test: ## Run all tests
	pytest tests/ -v --cov=src --cov-report=term-missing

test-unit: ## Run unit tests only
	pytest tests/unit/ -v

test-integration: ## Run integration tests only
	pytest tests/integration/ -v

docker-build: ## Build Docker image
	docker build -f docker/Dockerfile -t math-prediction:latest .

docker-up: ## Start all services
	docker compose -f docker/docker-compose.yml up -d

docker-down: ## Stop all services
	docker compose -f docker/docker-compose.yml down
