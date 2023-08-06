import asyncio
import logging


def configure_logging() -> None:
    logging.basicConfig(level="INFO")


async def amain() -> None:
    configure_logging()
    logging.info("Hello World!")


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
