import asyncio
import logging
from datetime import datetime
from typing import Callable

from .config import Config


class App:
    def __init__(
        self,
        config: Config,
        get_time_func: Callable[[], datetime] = datetime.now,
    ) -> None:
        self.config = config
        self.get_time_func = get_time_func

        # Initializing
        self._connectors = [account.connector() for account in config.accounts]

        logging.info("Initial states are assumed to be correct.")
        self._previous_light_states = self._light_states(self.get_time_func())

    @property
    def lights(self) -> set[str]:
        timers = self.config.on
        # return {light for light in [timer.lights for timer in timers]}
        return {light for timer in timers for light in timer.lights}

    async def run(self, interval: float = 300) -> None:
        while True:
            await asyncio.gather(
                self.update(),
                asyncio.sleep(interval),
            )

    async def update(self) -> None:
        time = self.get_time_func()
        current_light_states = self._light_states(time)

        changed_light_states = {}
        for light in self.lights:
            prev = self._previous_light_states[light]
            curr = current_light_states[light]

            if prev != curr:
                changed_light_states[light] = curr

        logging.info("---")
        logging.info(f"The time is {time}")
        logging.info(f"The (previous) light states were: {self._previous_light_states}")
        logging.info(f"The (current)  light states are:  {current_light_states}")
        logging.info(f"The (changed)  light states are:  {changed_light_states}")

        for light, state in changed_light_states.items():
            logging.info(f"Turning {'on' if state else 'off'} the {light} light.")
            for connector in self._connectors:
                await connector.set_light_state(light, state)

        # Finally, update previous light states
        self._previous_light_states = current_light_states

    def _light_states(self, time: datetime) -> dict[str, bool]:
        location = self.config.location

        # Assume all lights to be off
        light_states = {light: False for light in self.lights}

        # Update lights whose timers are on
        timers = self.config.on
        for timer in timers:
            if timer.is_active(time, location):
                for light in timer.lights:
                    light_states[light] = True

        return light_states
