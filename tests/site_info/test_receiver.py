import datetime
import pytest

from midgard.site_info.receiver import Receiver

# Tests: Receiver.get("snx",...)

@pytest.mark.usefixtures("sinex_data")
def test_receiver_sinex_one_station(sinex_data):
    r = Receiver.get("snx", "zimm", datetime.datetime(2020, 1, 1), sinex_data, source_path="/path/to/sinex")
    assert "zimm" in r
    assert len(r) == 1
    
    # Test receiver information
    assert r["zimm"].station == "zimm"
    assert r["zimm"].type == 'TRIMBLE NETR9'
    assert r["zimm"].serial_number == '5429R'
    assert r["zimm"].firmware == '5.37'
    assert r["zimm"].date_from == datetime.datetime(2018, 12, 18, 9, 45)
    assert r["zimm"].date_to == datetime.datetime(2020, 6, 8, 7, 15)
    
@pytest.mark.usefixtures("sinex_data")
def test_receiver_sinex_two_stations_string(sinex_data):
    r = Receiver.get("snx", "zimm, hrao", datetime.datetime(2020, 1, 1), sinex_data, source_path="/path/to/sinex")
    assert "zimm" in r
    assert "hrao" in r
    assert len(r) == 2

@pytest.mark.usefixtures("sinex_data")
def test_receiver_sinex_two_stations_list(sinex_data):
    r = Receiver.get("snx", ["zimm", "hrao"], datetime.datetime(2020, 1, 1), sinex_data, source_path="/path/to/sinex")
    assert "zimm" in r
    assert "hrao" in r
    assert len(r) == 2

@pytest.mark.usefixtures("sinex_data")
def test_receiver_sinex_one_station_error(sinex_data):
    # Station xxxx does not exist
    with pytest.raises(ValueError):
        r = Receiver.get("snx", "xxxx", datetime.datetime(2020, 1, 1), sinex_data, source_path="/path/to/sinex")

@pytest.mark.usefixtures("sinex_data")
def test_receiver_sinex_two_stations_error(sinex_data):
    # Station xxxx does not exist
    with pytest.raises(ValueError):
        r = Receiver.get("snx", "zimm, xxxx", datetime.datetime(2020, 1, 1), sinex_data, source_path="/path/to/sinex")

# Tests: Receiver.get_history("snx",...)

@pytest.mark.usefixtures("sinex_data")
def test_receiver_history_sinex_one_station(sinex_data):
    r = Receiver.get_history("snx", "zimm", sinex_data, source_path="/path/to/sinex")
    assert "zimm" in r
    assert len(r) == 1
    
    # Test receiver history information
    assert len(r["zimm"].history) == 16
    assert len(r["zimm"].date_from) == 16
    assert len(r["zimm"].date_to) == 16
    
@pytest.mark.usefixtures("sinex_data")
def test_receiver_history_sinex_two_stations_string(sinex_data):
    r = Receiver.get_history("snx", "zimm, hrao", sinex_data, source_path="/path/to/sinex")
    assert "zimm" in r
    assert "hrao" in r
    assert len(r) == 2

@pytest.mark.usefixtures("sinex_data")
def test_receiver_history_sinex_two_stations_list(sinex_data):
    r = Receiver.get_history("snx", ["zimm", "hrao"], sinex_data, source_path="/path/to/sinex")
    assert "zimm" in r
    assert "hrao" in r
    assert len(r) == 2

@pytest.mark.usefixtures("sinex_data")
def test_receiver_history_sinex_one_station_error(sinex_data):
    # Station xxxx does not exist
    with pytest.raises(ValueError):
        r = Receiver.get_history("snx", "xxxx", sinex_data, source_path="/path/to/sinex")

@pytest.mark.usefixtures("sinex_data")
def test_receiver_history_sinex_two_stations_error(sinex_data):
    # Station xxxx does not exist
    with pytest.raises(ValueError):
        r = Receiver.get_history("snx", "zimm, xxxx", sinex_data, source_path="/path/to/sinex")

# Tests: Receiver.get("ssc",...)

@pytest.mark.usefixtures("ssc_data")
def test_receiver_ssc_one_station(ssc_data):
    r = Receiver.get("ssc", "gras", datetime.datetime(2020, 1, 1), ssc_data, source_path="/path/to/ssc")
    assert "gras" in r
    assert len(r) == 1
    
    # Test receiver information
    assert r["gras"] is None

@pytest.mark.usefixtures("ssc_data")
def test_receiver_ssc_two_stations_string(ssc_data):
    r = Receiver.get("ssc", "gras, borr", datetime.datetime(2020, 1, 1), ssc_data, source_path="/path/to/ssc")
    assert "gras" in r
    assert "borr" in r
    assert len(r) == 2

@pytest.mark.usefixtures("ssc_data")
def test_receiver_ssc_two_stations_list(ssc_data):
    r = Receiver.get("ssc", ["gras", "borr"], datetime.datetime(2020, 1, 1), ssc_data, source_path="/path/to/ssc")
    assert "gras" in r
    assert "borr" in r
    assert len(r) == 2

@pytest.mark.usefixtures("ssc_data")
def test_receiver_ssc_one_station_error(ssc_data):
    # Station xxxx does not exist
    with pytest.raises(ValueError):
        r = Receiver.get("ssc", "xxxx", datetime.datetime(2020, 1, 1), ssc_data, source_path="/path/to/ssc")

@pytest.mark.usefixtures("ssc_data")
def test_receiver_ssc_two_stations_error(ssc_data):
    # Station xxxx does not exist
    with pytest.raises(ValueError):
        r = Receiver.get("ssc", "gras,xxxx", datetime.datetime(2020, 1, 1), ssc_data, source_path="/path/to/ssc")

# Tests: Receiver.get_history("ssc",...)

@pytest.mark.usefixtures("ssc_data")
def test_receiver_history_ssc_one_station(ssc_data):
    r = Receiver.get_history("ssc", "gras", ssc_data, source_path="/path/to/ssc")
    assert "gras" in r
    assert len(r) == 1
    
    # Test receiver history information
    assert r["gras"].history is None
    assert r["gras"].date_from is None
    assert r["gras"].date_to is None

@pytest.mark.usefixtures("ssc_data")
def test_receiver_history_ssc_two_stations_string(ssc_data):
    r = Receiver.get_history("ssc", "gras, borr", ssc_data, source_path="/path/to/ssc")
    assert "gras" in r
    assert "borr" in r
    assert len(r) == 2

@pytest.mark.usefixtures("ssc_data")
def test_receiver_history_ssc_two_stations_list(ssc_data):
    r = Receiver.get_history("ssc", ["gras", "borr"], ssc_data, source_path="/path/to/ssc")
    assert "gras" in r
    assert "borr" in r
    assert len(r) == 2

@pytest.mark.usefixtures("ssc_data")
def test_receiver_history_ssc_one_station_error(ssc_data):
    # Station xxxx does not exist
    with pytest.raises(ValueError):
        r = Receiver.get_history("ssc", "xxxx", ssc_data, source_path="/path/to/ssc")

@pytest.mark.usefixtures("ssc_data")
def test_receiver_history_ssc_two_stations_error(ssc_data):
    # Station xxxx does not exist
    with pytest.raises(ValueError):
        r = Receiver.get_history("ssc", "gras,xxxx", ssc_data, source_path="/path/to/ssc")
