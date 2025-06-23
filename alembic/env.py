import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
load_dotenv(override=True)

from app.db import Base

from app.models.user_model import User
from app.models.currency_model import Currency
from app.models.wallet_model import Wallet
from app.models.wallet_currency_model import WalletCurrency

target_metadata = Base.metadata
config = context.config

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

db_conn_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
config.set_main_option('sqlalchemy.url', db_conn_string)  # Add this to load the database URL
config.set_main_option("version_locations", "/tmp/alembic_versions")


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    print(connectable)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
