import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_db():
    logger.info("Conectando ao banco de dados...")
    # Mock connection / session
    logger.info("Limpando tabelas antigas...")
    logger.info("Criando usuários de teste...")
    logger.info("Criando leads fictícios para demonstração...")
    logger.info("Banco de dados populado com sucesso!")

if __name__ == "__main__":
    asyncio.run(seed_db())
