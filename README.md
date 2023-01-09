# check-maker

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/stigsanek/check-maker/pyci.yml?branch=main)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/stigsanek/check-maker)
![Code Climate coverage](https://img.shields.io/codeclimate/coverage/stigsanek/check-maker)

API microservice for generating checks by orders

## Description

"Check Maker" is API microservice for generating checks by orders.

A delivery restaurant chain has many locations where orders are prepared for customers. Every customer wants a receipt along with their order, containing detailed information about the order. The kitchen staff also wants the receipt so that during the process of cooking and packing the order, they don't forget to put everything they need. "Check Maker" helps with this.

[Celery](https://docs.celeryq.dev/en/stable/) asynchronous queue (based on [Redis](https://redis.io/) message broker) is used to perform check rendering tasks. Conversion to PDF is performed via [wkhtmltopdf](https://wkhtmltopdf.org/).

### Work scheme

![Kroki diagram](https://kroki.io/ditaa/svg/eNpTUNDWRQbaCvgBmmouBYUaFPkaAvrRVFNNv2tQAAn6HQMCqGw_-fopDX8iLVbAsBiuMbkoNbEkVSE5IzU5uxhNYXpqCUwiLb9IoaAoM6-EKpbi9RbxGvGHPjU0ojpN1w6WgjwhCm10ccUI4ainVKE2sVbDzK0hQomCR4ivj0JJvkKAixuh5FmDHnAkFg81mAIEspcNmnO0sUUOun6XxJLEpMTiVCKzp3NqTmpRJTH2Y4DBVjwAAIMR7l4=)

1. The service receives information about the new order, creates checks in the database for all printers the merchant point from the order and sets asynchronous tasks to generate PDF files for these checks. If the merchant point does not have any printers, returns an error.

2. Asynchronous worker Celery using wkhtmltopdf generate a PDF file from an HTML template.

3. The application polls the service for new checks. First a list of receipts that have already been generated for a particular printer is requested, then a PDF file for each receipt is downloaded and sent for printing.

## Usage

You can deploy the project via Docker.

Docker is a platform designed to help developers build, share, and run modern applications.
You can read more about this tool on [the official Docker website](https://www.docker.com/).
You need to [install Docker Desktop](https://www.docker.com/products/docker-desktop/).
Docker Desktop is an application for the building and sharing of containerized applications and microservices.

#### Environment

Depending on the application mode, different environment files are used.
For development mode, the `.env.dev` file with basic settings has already been created.
For production mode, you need to create an `.env.prod` file:

```
# Database environment
POSTGRES_DB=check_maker
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# App environment
SECRET_KEY=prod
ALLOWED_HOSTS=127.0.0.1
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# Celery environment
CELERY_BROKER_URL=redis://redis:6379
CELERY_RESULT_BACKEND=${CELERY_BROKER_URL}

# Wkhtmltopdf environment
WKHTMLTOPDF_URL=http://wkhtmltopdf:80
```

#### Run development mode

```bash
>> docker-compose -f compose.dev.yml up -d --build

...
...
...
Creating check-maker_db_1          ... done
Creating check-maker_wkhtmltopdf_1 ... done
Creating check-maker_redis_1       ... done
Creating check-maker_app_1         ... done
Creating check-maker_celery_1      ... done
Creating check-maker_flower_1      ... done
```

* Open [http://127.0.0.1:8000/swagger-ui/](http://127.0.0.1:8000/swagger-ui/) or [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) in your browser for to see all the API methods.

* Open [http://127.0.0.1:5555/](http://127.0.0.1:5555/) in your browser to monitor task processing.

#### Run production mode

```bash
>> docker-compose -f compose.prod.yml up -d --build

...
...
...
Creating check-maker_db_1          ... done
Creating check-maker_wkhtmltopdf_1 ... done
Creating check-maker_redis_1       ... done
Creating check-maker_app_1         ... done
Creating check-maker_celery_1      ... done
Creating check-maker_flower_1      ... done
```

* Open [http://127.0.0.1:8000/swagger-ui/](http://127.0.0.1:8000/swagger-ui/) or [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) in your browser for to see all the API methods.

* Open [http://127.0.0.1:5555/](http://127.0.0.1:5555/) in your browser to monitor task processing.
