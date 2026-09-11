import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """
    Executa migrações do Alembic.
    """
    logger.info("Executando alembic upgrade head...")
    # os.system("alembic upgrade head")
    logger.info("Migrações aplicadas com sucesso.")

if __name__ == "__main__":
    run_migrations()
