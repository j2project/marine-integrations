"""
@package mi.dataset.driver.wfp.flortk.driver
@file marine-integrations/mi/dataset/driver/wfp/flortk/driver.py
@author Bill French
@author Roger Unwin
@brief Driver for the wfp/flortk
Release notes:

initial release
"""

__author__ = 'Roger Unwin'
__license__ = 'Apache 2.0'

from mi.core.log import get_logger ; log = get_logger()

from mi.dataset.dataset_driver import SimpleDataSetDriver
from mi.dataset.parser.flortk import FlortkParser
from mi.dataset.parser.flortk import FlortkParserDataParticle
from mi.dataset.harvester import AdditiveSequentialFileHarvester


class WfpFLORTKDataSetDriver(SimpleDataSetDriver):
    @classmethod
    def stream_config(cls):
        return [FlortkParserDataParticle.type()]

    def _build_parser(self, parser_state, infile):
        config = self._parser_config
        config.update({
            'particle_module': 'mi.dataset.parser.flortk',
            'particle_class': 'FlortkParserDataParticle'
        })
        log.debug("MYCONFIG: %s", config)
        self._parser = FlortkParser(
            config,
            parser_state,
            infile,
            self._save_parser_state,
            self._data_callback
        )

        return self._parser

    def _build_harvester(self, harvester_state):
        self._harvester = AdditiveSequentialFileHarvester(
            self._harvester_config,
            harvester_state,
            self._new_file_callback,
            self._exception_callback
        )

        return self._harvester

