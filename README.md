# Desafio Power2go

Simple GraphQL API created with Flask, Graphene and SQLAlchemy.

The service is available through AWS Elastic Beanstalk at the http://desafio-power2go.eba-q3dvqm3b.us-east-2.elasticbeanstalk.com/graphql.

## Prerequisites

1. Python 3.10 (I don't know if it works with higher or lower versions)
2. Virtual env

    ```sh
    pip3 install virtualenv
    ```

## How to install locally?

1. Clone this repository

    ```sh
    git clone https://github.com/tio-bryan/desafio_power2go.git
    ```

2. Go to root of this project

    ```sh
    cd desafio_power2go
    ```

3. Create a virtual env

    ```sh
    python3 -m venv venv
    ```

4. Activate the virtual env

    ```sh
    . venv/bin/activate
    ```

5. Install dependencies

    ```sh
    pip3 install -r requirements.txt
    ```

5. Run the web server

    ```sh
    python3 application.py
    ```

6. Open [http://localhost:5000/graphql](http://localhost:5000/graphql) or [http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql) on your preferred browser

7. (Optional) To deactivate the virtual env
    ```sh
    deactivate
    ```

## How to deploy on cloud service

Just follow the steps in the official Elastic Beanstalk [tutorial](https://docs.aws.amazon.com/pt_br/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)