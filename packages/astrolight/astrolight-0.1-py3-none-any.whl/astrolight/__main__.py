import asyncio
import logging
import yaml
from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path

from .app import App
from .config import Config


def configure_logging() -> None:
    logging.basicConfig(level="INFO")


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config.yml"))
    parser.add_argument("--interval", type=float, default=300)
    parser.add_argument("--time-multiplier", type=float, default=1)
    return parser.parse_args()


async def amain() -> None:
    configure_logging()
    args = parse_args()

    config_file: Path = args.config
    with config_file.open() as f:
        config = Config.parse_obj(yaml.load(f, Loader=yaml.BaseLoader))

    time_multiplier: float = args.time_multiplier
    start_time = datetime.now()

    def get_time_func() -> datetime:
        return start_time + time_multiplier * (datetime.now() - start_time)

    interval: float = args.interval / time_multiplier

    app = App(config, get_time_func)
    await app.run(interval)


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
