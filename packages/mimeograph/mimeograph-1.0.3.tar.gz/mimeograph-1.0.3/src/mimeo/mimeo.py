"""The Mimeo module.

This module is a main module providing the most high level class
in Mimeo:
    * Mimeograph
        A class responsible for the Mimeo processing.
"""
from __future__ import annotations

import asyncio
import logging
import os
import queue
import xml.etree.ElementTree as ElemTree
from concurrent.futures import ThreadPoolExecutor
from types import TracebackType
from typing import Iterable, Iterator

from mimeo.config.mimeo_config import MimeoConfig
from mimeo.consumers import ConsumerFactory
from mimeo.context import MimeoContextManager
from mimeo.exc import NotRunningMimeographError
from mimeo.generators import GeneratorFactory

logger = logging.getLogger(__name__)


class Mimeograph:
    """A class responsible for the Mimeo processing.

    Based on the Mimeo Configuration it instantiates generator and
    consumer to produce desired data.
    For sequential processing it is enough to use its static methods, without
    instantiation [process(), generate(), consume()]. However, Mimeograph exposes
    an interface to process data in parallel [run(), submit(), close()].

    Methods
    -------
    generate(
        mimeo_config: MimeoConfig,
        stringify: bool = False,
    ) -> Iterator[ElemTree.Element | dict | str]
        Generate data from the Mimeo Configuration.

    consume(
        mimeo_config: MimeoConfig,
        data: Iterable,
    )
        Consume data generated from the Mimeo Configuration.

    process(
        mimeo_config: MimeoConfig,
    )
        Process the Mimeo Configuration (generate data and consume).

    run(
    )
        Run the Mimeograph instance.
    stop(
    )
        Stop the Mimeograph instance.
    submit(
        mimeo_config: tuple[str | None, MimeoConfig | None],
    ):
        Put a Mimeo Config with identifier into a queue to process.

    Examples
    --------
    # Simple processing of a mimeo config
    config_path = "SomeEntity-config.json"
    mimeo_config = MimeoConfigFactory.parse(config_path)
    Mimeograph.process(mimeo_config)

    # Generating and consuming data from a mimeo config
    config_path = "SomeEntity-config.json"
    mimeo_config = MimeoConfigFactory.parse(config_path)
    data = Mimeograph.generate(mimeo_config)
    Mimeograph.consume(mimeo_config, data)

    # Processing mimeo configs in parallel
    config_paths = []
    with Mimeograph() as mimeo:
        for config_path in config_paths:
            mimeo_config = MimeoConfigFactory.parse(config_path)
            mimeo.submit((config_path, mimeo_config))

    # Processing mimeo configs in parallel outside context manager
    config_paths = []
    mimeo = Mimeograph()
    mimeo.run()
    for config_path in config_paths:
        mimeo_config = MimeoConfigFactory.parse(config_path)
        mimeo.submit((config_path, mimeo_config))
    mimeo.stop()
    """

    def __init__(
            self,
            workers: int = -1,
    ):
        """Initialize Mimeograph class.

        Parameters
        ----------
        workers : int
            A number of consumer workers
        """
        self._is_running: bool = False
        self._generator_queue: queue.Queue = queue.Queue()
        self._consumer_queue: queue.Queue = queue.Queue()
        self._generate_executor: ThreadPoolExecutor | None = None
        self._consume_executor: ThreadPoolExecutor | None = None
        self._failed_configs = []
        if workers == -1:
            self._consumer_workers = self._get_max_num_of_workers()
        else:
            self._consumer_workers = workers

    def __enter__(
            self,
    ) -> Mimeograph:
        """Enter the Mimeograph instance.

        It runs the Mimeograph instance.

        Returns
        -------
        self : Mimeograph
            A Mimeograph instance
        """
        self.run()
        return self

    def __exit__(
            self,
            exc_type: type | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        """Exit the Mimeograph instance.

        It stops the Mimeograph instance.

        Parameters
        ----------
        exc_type : type | None
            An exception's type
        exc_val : BaseException | None
            An exception's value
        exc_tb  TracebackType | None
            An exception's traceback
        """
        self.stop()

    def run(
            self,
    ):
        """Run the Mimeograph instance.

        It initializes generator and consumer workers and starts their tasks.
        """
        if not self._is_running:
            self._is_running = not self._is_running
            self._generate_executor = ThreadPoolExecutor(
                max_workers=1,
                thread_name_prefix="generator_thread")
            self._consume_executor = ThreadPoolExecutor(
                max_workers=self._consumer_workers,
                thread_name_prefix="consumer_thread")

            self._generate_executor.submit(self._start_generate)
            for _ in range(self._consumer_workers):
                self._consume_executor.submit(self._start_consume)

    def stop(
            self,
    ):
        """Stop the Mimeograph instance.

        It puts a poison pill to generator queue and awaits for all threads to stop
        before shutting executors down.
        """
        if self._is_running:
            self._is_running = not self._is_running
            self._generator_queue.put((None, None))
            self._generator_queue.join()
            self._consumer_queue.join()
            self._generate_executor.shutdown()
            self._consume_executor.shutdown()
            if len(self._failed_configs) > 0:
                logger.info("All configs have been processed. "
                            "The following configs have failed: %s",
                            self._failed_configs)
            else:
                logger.info("All configs have been successfully processed.")
            self._generate_executor = None
            self._consume_executor = None

    def submit(
            self,
            mimeo_config: tuple[str | None, MimeoConfig | None],
    ):
        """Put a Mimeo Config with identifier into a queue to process.

        Parameters
        ----------
        mimeo_config: tuple[str | None, MimeoConfig | None]
            A config ID and a Mimeo Config itself
        """
        if not self._is_running:
            raise NotRunningMimeographError
        logger.info("Putting a config for data generation into queue [%s]",
                    mimeo_config[0])
        self._generator_queue.put(mimeo_config)

    def _start_generate(
            self,
    ):
        """Start a generator task.

        Starts an infinitive loop that will work until a poison pill is being submitted.
        It gets a config from a queue and generates data. Once it took a poison pill,
        puts same to a consumer queue.
        """
        while True:
            logger.fine("Getting a config for data generation from queue")
            config_id, mimeo_config = self._generator_queue.get()
            if mimeo_config is None:
                logger.fine("Closing config generator")
                for _ in range(self._consumer_workers):
                    self._consumer_queue.put((None, None, None))
                self._generator_queue.task_done()
                break

            try:
                data = list(self.generate(mimeo_config, stringify=True))
                logger.fine("Putting data to consume to queue")
                self._consumer_queue.put((config_id, mimeo_config, data))
            except Exception:
                self._failed_configs.append(config_id)
                logger.exception("An unexpected error occurred while generating data "
                                 "from a config [%s]", config_id)
            finally:
                self._generator_queue.task_done()

    def _start_consume(
            self,
    ):
        """Start a consumer task.

        Starts an infinitive loop that will work until a poison pill is being submitted.
        It gets data from a queue and consumes it accordingly to a config.
        """
        while True:
            logger.fine("Getting data to consume from queue")
            config_id, mimeo_config, data = self._consumer_queue.get()
            if mimeo_config is None and data is None:
                logger.fine("Closing data consumer")
                self._consumer_queue.task_done()
                break

            try:
                self.consume(mimeo_config, data)
            except Exception:
                self._failed_configs.append(config_id)
                logger.exception("An unexpected error occurred while consuming data "
                                 "from a config [%s]", config_id)
            finally:
                self._consumer_queue.task_done()

    @classmethod
    def process(
            cls,
            mimeo_config: MimeoConfig,
    ):
        """Process the Mimeo Configuration (generate data and consume).

        Parameters
        ----------
        mimeo_config: MimeoConfig
            A Mimeo Configuration to process
        """
        data = cls.generate(mimeo_config, stringify=True)
        cls.consume(mimeo_config, data)

        logger.info("Data has been processed")

    @classmethod
    def generate(
            cls,
            mimeo_config: MimeoConfig,
            stringify: bool = False,
    ) -> Iterator[ElemTree.Element | dict | str]:
        """Generate data from the Mimeo Configuration.

        Parameters
        ----------
        mimeo_config: MimeoConfig
            A Mimeo Configuration for data generation
        stringify: bool
            Indicate if data should be stringified

        Returns
        -------
        Iterator[ElemTree.Element | dict | str]
            Iterator for generated data
        """
        generator = GeneratorFactory.get_generator(mimeo_config)
        logger.info("Starting data generation")
        with MimeoContextManager(mimeo_config):
            for data in generator.generate(mimeo_config.templates):
                yield data if not stringify else generator.stringify(data)

    @classmethod
    def consume(
            cls,
            mimeo_config: MimeoConfig,
            data: Iterable,
    ):
        """Consume data generated from the Mimeo Configuration.

        Parameters
        ----------
        mimeo_config: MimeoConfig
            A Mimeo Configuration for data generation
        data: Iterable
            Data to consume
        """
        consumer = ConsumerFactory.get_consumer(mimeo_config)
        asyncio.run(consumer.consume(data))

    @staticmethod
    def _get_max_num_of_workers():
        """Get a maximum number of ThreadPoolExecutor workers."""
        return min(32, (os.cpu_count() or 1) + 4)  # Num of CPUs + 4
