import asyncio
from app.routes.contracts import process_contract_embeddings

async def main():
    result = await process_contract_embeddings()
    print(f"Embedding process completed with result: {result}")

if __name__ == "__main__":
    asyncio.run(main())