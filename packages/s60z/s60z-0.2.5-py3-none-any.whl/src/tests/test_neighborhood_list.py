from ..gui.neighborhood_list import E_UTRA


def test_lookup_table_band_4():
    tl = E_UTRA
    assert tl.lookup_table(2110) == "4"


def test_lookup_table_band_66():
    table_lookup = E_UTRA
    assert table_lookup.lookup_table(729) == "12"


def test_lookup_table_band_71():
    table_lookup = E_UTRA
    assert table_lookup.lookup_table(617) == "71"


def test_lookup_table_band_7():
    table_lookup = E_UTRA
    assert table_lookup.lookup_table(2690) == "7"


def test_lookup_table_band_11():
    table_lookup = E_UTRA
    assert table_lookup.lookup_table(1497) == "11"


def test_lookup_table_band_5():
    table_lookup = E_UTRA
    assert table_lookup.lookup_table(894) == "5"


def test_lookup_table_band_2():
    table_lookup = E_UTRA
    assert table_lookup.lookup_table(1990) == "2"


def test_lookup_table_band_10():
    table_lookup = E_UTRA
    assert table_lookup.lookup_table(2170) == "10"


def test_lookup_table_band_3():
    table_lookup = E_UTRA
    assert table_lookup.lookup_table(1880) == "3"


def test_lookup_table_band_12():
    table_lookup = E_UTRA
    assert table_lookup.lookup_table(729) == "12"


def test_lookup_table_band_21():
    table_lookup = E_UTRA
    assert table_lookup.lookup_table(1512) == "21"


def test_lookup_table_band_28():
    table_lookup = E_UTRA
    assert table_lookup.lookup_table(803) == "28"
