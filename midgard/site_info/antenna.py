"""Antenna information classes

Description:
------------
This module is divided into three different types of classes:

    1. Main class Antenna that provides basic functionality to the user. See examples
    2. Antenna source type classes:
        - There is one class for each source type
        - A class with all relevant site coordinate information for a point in time.
    3. Antenna history source type classes:
        - There is one class for each source type
        - Converts input from source_data to a object of type AntennaHistorySinex, etc and provides functions
          for accessing the history and relevant dates. 
        - The history consist of a time interval for which the entry is valid and an instance of an antenna 
          source type class for each defined time interval.

    If a source type does not contain information about the antenna the module will return 'None'.

Example:
--------
    
    from midgard import parsers
    p = parsers.parse_file(parser_name='sinex_site', file_path='./data/site_info/igs.snx')
    source_data = p.as_dict()
    all_stations = source_data.keys()
    
    Antenna.get("snx", "osls", datetime(2020, 1, 1), source_data, source_path=p.file_path)
    Antenna.get("snx", all_stations, datetime(2020, 1, 1), source_data, source_path=p.file_path)
    
    Antenna.get_history("snx", "osls", source_data, source_path=p.file_path)
    Antenna.get_history("snx", all_stations, source_data, source_path=p.file_path)

"""


# Standard library imports
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple, Union, Callable

# Midgard imports
from midgard.site_info._site_info import SiteInfoBase, SiteInfoHistoryBase, ModuleBase

class Antenna(ModuleBase):
    """Main class for converting antenna information from various sources into unified classes"""
    
    sources: Dict[str, Callable] = dict()


@Antenna.register_source
class AntennaHistorySinex(SiteInfoHistoryBase):

    source: str = "snx"

    def _process_history(
                self, 
                source_data: Dict,
    ) -> Dict[Tuple[datetime, datetime], "AntennaSinex"]:
        """Read antenna site history from SINEX file

        Args:
            source_data:  Source data with site information. If source data are defined, then data are not read
                          from 'source_path'. 

        Returns:
            Dictionary with (date_from, date_to) tuple as key. The values are AntennaSinex objects.
        """
                
        if self.station in source_data:
            if "site_antenna" not in source_data[self.station]:
                raise ValueError(f"Station {self.station!r} is not given in SITE/ANTENNA SINEX block.")
            raw_info = source_data[self.station]["site_antenna"]
        elif self.station.upper() in source_data:
            if "site_antenna" not in source_data[self.station]:
                raise ValueError(f"Station {self.station.upper()!r} is not given in SITE/ANTENNA SINEX block.")
            raw_info = source_data[self.station.upper()]["site_antenna"]
        else:
            raise ValueError(f"Station '{self.station}' unknown in source '{self.source}:{self.source_path}'.")

        return self._create_history(self.station, raw_info)

    def _create_history(self, station: str, raw_info: List)-> Dict:
        """Create dictionary of antenna history for station
        """
        history = dict()
        for antenna_info in raw_info:
            antenna = AntennaSinex(self.station, antenna_info)
            interval = (antenna.date_from, antenna.date_to)
            history[interval] = antenna

        return history


class AntennaSinex(SiteInfoBase):
    """ Antenna class handling SINEX file antenna station information
    """

    source: str = "snx"
    fields: Dict[str, str] = dict(
        type="antenna_type",
        serial_number="serial_number",
        radome_type="radome_type",
        radome_serial_number="radome_type",
    )

    @property
    def date_from(self) -> datetime:
        """ Get antenna installation date from site information attribute

        Returns:
            Antenna installation date
        """
        if self._info["start_time"]:
            return self._info["start_time"]
        else:
            return datetime.min

    @property
    def date_to(self) -> datetime:
        """ Get antenna removing date from site information attribute

        Returns:
            Antenna removing date
        """
        if self._info["end_time"]:
            return self._info["end_time"]
        else:
            return datetime.max - timedelta(days=367)  # TODO: Minus 367 days is necessary because
            #       _year2days(cls, year, scale) in ./midgard/data/_time.py
            #      does not work. Exceeding of datetime limit 9999 12 31.


@Antenna.register_source
class AntennaHistorySsc(SiteInfoHistoryBase):

    source: str = "ssc"

    def _process_history(
                self, 
                source_data: Any,
    ) -> Union[None, Dict[Tuple[datetime, datetime], "AntennaSsc"]]:
        """Read antenna site history from SINEX file

        Args:
            source_data:  Source data with site information. If source data are defined, then data are not read
                          from 'source_path'. 

        Returns:
            Dictionary with (date_from, date_to) tuple as key. The values are AntennaSinex objects.
        """
        if self.station in source_data or self.station.upper() in source_data:
            # Station is defined but SSC files do not contain receiver information
            return None
        else:
            raise ValueError(f"Station {self.station!r} unknown in source '{self.source_path}'.")

# class AntennaSsc(SiteInfoBase):
#     """ Antenna class handling SINEX file antenna station information
#     """
#
#     source: str = "snx"
#     fields: Dict[str, str] = dict(
#         type="antenna_type",
#         serial_number="serial_number",
#         radome_type="radome_type",
#         radome_serial_number="radome_type",
#     )
#
#     @property
#     def date_from(self) -> datetime:
#         """ Get antenna installation date from site information attribute
#
#         Returns:
#             Antenna installation date
#         """
#         if self._info["start_time"]:
#             return self._info["start_time"]
#         else:
#             return datetime.min
#
#     @property
#     def date_to(self) -> datetime:
#         """ Get antenna removing date from site information attribute
#
#         Returns:
#             Antenna removing date
#         """
#         if self._info["end_time"]:
#             return self._info["end_time"]
#         else:
#             return datetime.max - timedelta(days=367)  # TODO: Minus 367 days is necessary because
#             #       _year2days(cls, year, scale) in ./midgard/data/_time.py
#             #      does not work. Exceeding of datetime limit 9999 12 31.
