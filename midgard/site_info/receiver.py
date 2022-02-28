"""Receiver information classes

Description:
------------
This module is divided into three different types of classes:

    1. Main class Receiver that provides basic functionality to the user. See examples
    2. Receiver source type classes:
        - There is one class for each source type
        - A class with all relevant site coordinate information for a point in time.
    3. Receiver history source type classes:
        - There is one class for each source type
        - Converts input from source_data to a object of type ReceiverHistorySinex, etc and provides functions
          for accessing the history and relevant dates. 
        - The history consist of a time interval for which the entry is valid and an instance of a receiver 
          source type class for each defined time interval.

    If a source type does not contain information about the receiver the module will return 'None'.

Example:
--------
    
    from midgard import parsers
    p = parsers.parse_file(parser_name='sinex_site', file_path='./data/site_info/igs.snx')
    source_data = p.as_dict()
    all_stations = source_data.keys()
    
    Receiver.get("snx", "osls", datetime(2020, 1, 1), source_data, source_path=p.file_path)
    Receiver.get("snx", all_stations, datetime(2020, 1, 1), source_data, source_path=p.file_path)
    
    Receiver.get_history("snx", "osls", source_data, source_path=p.file_path)
    Receiver.get_history("snx", all_stations, source_data, source_path=p.file_path)

"""

# Standard library imports
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple, Union, Callable

# Midgard imports
from midgard.site_info._site_info import SiteInfoBase, SiteInfoHistoryBase, ModuleBase


class Receiver(ModuleBase):
    """Main class for converting receiver information from various sources into unified classes"""
    
    sources: Dict[str, Callable] = dict()


@Receiver.register_source
class ReceiverHistorySinex(SiteInfoHistoryBase):

    source: str = "snx"

    def _process_history(
                self, 
                source_data: Dict,
    ) -> Dict[Tuple[datetime, datetime], "ReceiverSinex"]:
        """Read receiver site history from SINEX file

        Args:
            source_data:  Source data with site information. If source data are defined, then data are not read
                          from 'source_path'.

        Returns:
            Dictionary with (date_from, date_to) tuple as key. The values are ReceiverSinex objects.
        """

        if self.station in source_data:
            if "site_receiver" not in source_data[self.station]:
                raise ValueError(f"Station {self.station!r} is not given in SITE/RECEIVER SINEX block.")
            raw_info = source_data[self.station]["site_receiver"]
        elif self.station.upper() in source_data:
            if "site_receiver" not in source_data[self.station]:
                raise ValueError(f"Station {self.station.upper()!r} is not given in SITE/RECEIVER SINEX block.")
            raw_info = source_data[self.station.upper()]["site_receiver"]
        else:
            raise ValueError(f"Station {self.station!r} unknown in source '{self.source_path}'.")
        
        return self._create_history(self.station, raw_info)

    def _create_history(self, station: str, raw_info: List) -> Dict:
        """Create dictionary of antenna history for station
        """
        history = dict()
        for receiver_info in raw_info:
            receiver = ReceiverSinex(self.station, receiver_info)
            interval = (receiver.date_from, receiver.date_to)
            history[interval] = receiver

        return history


class ReceiverSinex(SiteInfoBase):
    """ Receiver class handling SINEX file receiver station information
    """

    source: str = "snx"
    fields: Dict[str, str] = dict(type="receiver_type", serial_number="serial_number", firmware="firmware")

    @property
    def date_from(self) -> datetime:
        """ Get receiver installation date from site information attribute

        Returns:
            Receiver installation date
        """
        if self._info["start_time"]:
            return self._info["start_time"]
        else:
            return datetime.min

    @property
    def date_to(self) -> datetime:
        """ Get receiver removing date from site information attribute

        Returns:
            Receiver removing date
        """
        if self._info["end_time"]:
            return self._info["end_time"]
        else:
            return datetime.max - timedelta(days=367)  # TODO: Minus 367 days is necessary because
            #       _year2days(cls, year, scale) in ./midgard/data/_time.py
            #      does not work. Exceeding of datetime limit 9999 12 31.


@Receiver.register_source
class ReceiverHistorySsc(SiteInfoHistoryBase):

    source: str = "ssc"

    def _process_history(
                self, 
                source_data: Any = None,
    ) -> Union[None, Dict[Tuple[datetime, datetime], "ReceiverSinex"]]:
        """Read receiver site history from SINEX file

        Args:
            source_data:  Source data with site information. If source data are defined, then data are not read
                          from 'source_path'.

        Returns:
            Dictionary with (date_from, date_to) tuple as key. The values are ReceiverSinex objects.
        """
        if self.station in source_data or self.station.upper() in source_data:
            # Station is defined but SSC files do not contain receiver information
            return None
        else:
            raise ValueError(f"Station {self.station!r} unknown in source '{self.source_path}'.")


class ReceiverSsc(SiteInfoBase):
    """ Receiver class handling SINEX file receiver station information
    """

    source: str = "ssc"
    fields: Dict[str, str] = dict(type="receiver_type", serial_number="serial_number", firmware="firmware")

    @property
    def date_from(self) -> datetime:
        """ Get receiver installation date from site information attribute

        Returns:
            Receiver installation date
        """
        if self._info["start_time"]:
            return self._info["start_time"]
        else:
            return datetime.min

    @property
    def date_to(self) -> datetime:
        """ Get receiver removing date from site information attribute

        Returns:
            Receiver removing date
        """
        if self._info["end_time"]:
            return self._info["end_time"]
        else:
            return datetime.max - timedelta(days=367)  # TODO: Minus 367 days is necessary because
            #       _year2days(cls, year, scale) in ./midgard/data/_time.py
            #      does not work. Exceeding of datetime limit 9999 12 31.
