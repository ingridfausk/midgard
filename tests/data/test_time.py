""" Tests for the data.time module"""
from datetime import datetime, timedelta

# Third party imports
import pytest
import numpy as np

# Midgard imports
from midgard.data import time


@pytest.fixture()
def t(request):
    return request.getfixturevalue(request.param.__name__)


@pytest.fixture
def t_dt_utc_s():
    """Time, format datetime, scale utc, single entry"""
    return time.Time(datetime(2015, 6, 30) + timedelta(hours=23, minutes=59, seconds=20), scale="utc", fmt="datetime")


@pytest.fixture
def t_dt_utc_sa():
    """Time, format datetime, scale utc, array entry with single value"""
    return time.Time(
        [datetime(2015, 6, 30) + timedelta(hours=23, minutes=59, seconds=20)], scale="utc", fmt="datetime"
    )


@pytest.fixture
def t_dt_utc_a():
    """Time, format datetime, scale utc, array entry"""
    return time.Time(
        [datetime(2015, 6, 30) + timedelta(hours=23, minutes=59, seconds=i) for i in range(0, 2)],
        scale="utc",
        fmt="datetime",
    )


@pytest.fixture
def t_dt_utc_s2():
    """Time, format datetime, scale utc, single entry"""
    return time.Time(
        datetime(2015, 6, 30), val2=timedelta(hours=23, minutes=59, seconds=20), scale="utc", fmt="datetime"
    )


@pytest.fixture
def t_dt_utc_a2():
    """Time, format datetime, scale utc, array entry"""
    return time.Time(
        [datetime(2015, 6, i + 1) for i in range(0, 2)],
        val2=[timedelta(hours=23, minutes=59, seconds=i) for i in range(0, 2)],
        scale="utc",
        fmt="datetime",
    )


@pytest.fixture
def t_jd_utc_s():
    """Time, format julian date, scale utc, single entry"""
    return time.Time(2_451_544.5, scale="utc", fmt="jd")


@pytest.fixture
def t_jd_utc_a():
    """Time, format julian date, scale utc, array entry"""
    return time.Time([2_451_544.5 + i for i in range(0, 2)], scale="utc", fmt="jd")


@pytest.fixture
def t_jd_utc_s2():
    """Time, format julian date, scale utc, single entry"""
    return time.Time(2_451_544.0, val2=0.5, scale="utc", fmt="jd")


@pytest.fixture
def t_jd_utc_a2():
    """Time, format julian date, scale utc, array entry"""
    return time.Time([2_451_544.0 + i for i in range(0, 2)], val2=[0.5 for i in range(0, 2)], scale="utc", fmt="jd")


@pytest.fixture
def t_around_leapsecond():
    """Epochs just before and after leap second on June 30th 2015"""
    return time.Time(
        [datetime(2015, 6, 30) + timedelta(hours=23, minutes=59, seconds=i) for i in range(55, 65)],
        scale="utc",
        fmt="datetime",
    )


@pytest.mark.parametrize(
    "t",
    (
        t_dt_utc_s,
        t_dt_utc_sa,
        t_dt_utc_a,
        t_jd_utc_s,
        t_jd_utc_a,
        t_dt_utc_s2,
        t_dt_utc_a2,
        t_jd_utc_s2,
        t_jd_utc_a2,
        t_around_leapsecond,
    ),
    indirect=True,
)
def test_conversions(t):
    scales = time.TimeArray._scales()
    formats = time.TimeArray._formats()
    for scale in scales.keys():
        converted_t = getattr(getattr(t, scale), t.scale)

        for fmt in formats:
            try:
                t_fmt = getattr(t, fmt)
            except ValueError as err:
                # some formats are only available for certain scales
                assert t.scale != "gps" and "gps" in fmt
                print(f"{fmt} is not a valid format for {t.scale}. As expected.")
                continue

            if t.size == 1:
                assert t_fmt == getattr(converted_t, fmt)
            else:
                if fmt == "datetime":
                    assert np.equal(t_fmt, getattr(converted_t, fmt)).all()
                elif isinstance(t_fmt, tuple):
                    for a, b in zip(t_fmt, getattr(converted_t, fmt)):
                        assert np.allclose(a, b)
                elif t_fmt.dtype.kind in {"U", "S"}:
                    assert np.char.equal(t_fmt, getattr(converted_t, fmt)).all()
                else:
                    assert np.allclose(getattr(t, fmt), getattr(converted_t, fmt))
            print(f"t.{fmt} == t.{scale}.{t.scale}.{fmt} OK")


def test_now():
    time.Time.now()


def test_properties():
    t0 = time.Time(datetime(2000, 1, 1, 1, 1, 1), scale="utc", fmt="datetime")
    assert t0.year == 2000
    assert t0.month == 1
    assert t0.day == 1
    assert t0.hour == 1
    assert t0.minute == 1
    assert t0.second == 1
    assert t0.sec_of_day == 3661
    assert t0.yydddsssss == "00:001:03661"
    assert t0.doy == 1

    t1 = time.Time([datetime(2000, 1, 1, 1, 1, 1), datetime(2001, 1, 1, 1, 1, 1)], scale="utc", fmt="datetime")
    assert (t1.year == np.array([2000, 2001])).all()
    assert (t1.month == np.array([1, 1])).all()
    assert (t1.day == np.array([1, 1])).all()
    assert (t1.hour == np.array([1, 1])).all()
    assert (t1.minute == np.array([1, 1])).all()
    assert (t1.second == np.array([1, 1])).all()
    assert (t1.sec_of_day == np.array([3661, 3661])).all()
    assert (t1.yydddsssss == np.array(["00:001:03661", "01:001:03661"])).all()
    assert (t1.doy == np.array([1, 1])).all()


def test_is_tests():
    t = time.Time(datetime(2000, 1, 1, 1, 1, 1), scale="utc", fmt="datetime")
    dt = time.TimeDelta(30, scale="utc", fmt="seconds")

    assert time.Time.is_time(t) == True
    assert time.Time.is_time(dt) == False
    assert time.Time.is_time(8) == False
    assert time.Time.is_timedelta(t) == False
    assert time.Time.is_timedelta(dt) == True
    assert time.Time.is_timedelta(9) == False


def test_empty_object():
    time.Time([], scale="utc", fmt="datetime")

@pytest.mark.parametrize(
    "t",
    (
        t_dt_utc_a,
    ),
    indirect=True,
)
def test_slice(t):
    scales = time.TimeArray._scales()
    formats = time.TimeArray._formats()
    for scale in scales.keys():
        converted_t = getattr(t, scale)
        for fmt in formats:
            try:
                t_fmt = getattr(converted_t, fmt)
                print(f"Creating time time.Time({t_fmt}, {scale}, {fmt})")
                new_time_from_fmt = time.Time(t_fmt, scale=scale, fmt=fmt)
            except ValueError as err:
                # some formats are only available for certain scales
                assert converted_t.scale != "gps" and "gps" in fmt
                print(f"{fmt} is not a valid format for {converted_t.scale}. As expected.")
                continue
            assert len(converted_t[0:2]) == 2
            print(f"t.{scale}[0:2] == 2 OK")
            assert len(new_time_from_fmt[0:2]) == 2
            print(f"t.{scale}.{fmt}[0:2] == 2 OK")


def test_math_s():
    _t1 = time.Time(val=datetime(2009, 11, 2), scale="utc", fmt="datetime")
    _t2 = time.Time(val=datetime(2011, 5, 5), scale="utc", fmt="datetime")
    _td1 = time.TimeDelta(val=timedelta(seconds=30), scale="utc", fmt="timedelta")
    _td2 = time.TimeDelta(val=timedelta(days=10), scale="utc", fmt="timedelta")

    # Test1 time + timedelta -> time
    new_t = _t1 + _td1
    assert new_t.datetime == datetime(2009, 11, 2, 0, 0, 30)
    assert new_t.cls_name == "TimeArray"

    # Test2 timedelta + time -> time
    new_t = _td1 + _t1
    assert new_t.datetime == datetime(2009, 11, 2, 0, 0, 30)
    assert new_t.cls_name == "TimeArray"

    # Test3 time - timedelta -> time
    new_t = _t1 - _td1
    assert new_t.datetime == datetime(2009, 11, 1, 23, 59, 30)
    assert new_t.cls_name == "TimeArray"

    # Test4 timedelta - time -> error
    with pytest.raises(TypeError):
        new_t = _td1 - _t1

    # Test5 time - time -> timedelta
    new_td = _t1 - _t2
    assert (new_td.timedelta == timedelta(days=-549))
    assert new_td.cls_name == "TimeDeltaArray"

    # Test6 time + time -> Error
    with pytest.raises(TypeError):
        new_t = _t1 + _t2

    # Test7 timedelta + timedelta -> timedelta
    new_td = _td1 + _td2
    assert new_td.timedelta == timedelta(days=10, seconds=30)
    assert new_td.cls_name == "TimeDeltaArray"

    # Test8 timedelta - timedelta -> timedelta
    new_td = _td1 - _td2
    assert new_td.timedelta == timedelta(days=-10, seconds=30)
    assert new_td.cls_name == "TimeDeltaArray"

    # Test9 time > time -> Bool
    assert (_t1 > _t2) == False

    # Test10 time < time -> Bool
    assert (_t1 < _t2) == True

    # Test11 timedelta > timedelta -> Bool
    assert (_td1 > _td2) == False

    # Test12 timedelta < timedelta -> Bool
    assert (_td1 < _td2) == True
