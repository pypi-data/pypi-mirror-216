import numpy as np
import pytest

from h5parm import DataPack
from h5parm.datapack import load_array_file
from h5parm.utils import make_example_datapack, make_soltab, get_uniform_directions_on_S2, create_empty_datapack, \
    directions_from_sky_model, format_direction_bbs, parse_coordinates_bbs


def test_datapack():
    datapack = make_example_datapack(4, 5, 6, ["X"], clobber=True)
    phase, axes = datapack.phase
    datapack.phase = phase + 1.
    phasep1, axes = datapack.phase
    assert np.all(np.isclose(phasep1, phase + 1.))
    datapack.select(ant='RS509', time=slice(0, 1, 1))
    phase, axes = datapack.phase
    assert phase.shape == (1, 4, 1, 5, 1)
    datapack.select(ant='CS')
    phase, axes = datapack.phase
    assert phase.shape == (1, 4, 48, 5, 6)
    datapack.select(ant='RS*', time=slice(0, 1, 1))
    phase, axes = datapack.phase
    for a in axes['ant']:
        assert b'RS' in a
    assert len(axes['ant']) == 14
    datapack.select(time=[1, 3], dir=[0, 1, 3])
    phase, axes = datapack.phase
    with pytest.raises(IndexError):
        datapack.select(time=[0, 1, 3], dir=[0, 1, 3])
        phase, axes = datapack.phase
    assert 'sol001' not in datapack.solsets
    make_soltab(datapack, to_solset='sol001')
    assert 'sol001' in datapack.solsets


def test_get_uniform_directions_on_S2():
    directions = get_uniform_directions_on_S2(100, [0, 85], 4)
    import pylab as plt
    plt.scatter(directions[:, 0], directions[:, 1])
    plt.show()


def test_create_empty_datapack():
    create_empty_datapack(Nd=2,
                          Nf=2,
                          Nt=1,
                          pols=None,
                          field_of_view_diameter=4.,
                          start_time=None,
                          time_resolution=30.,
                          min_freq=122.,
                          max_freq=166.,
                          array_file=None,
                          phase_tracking=None,
                          directions=None,
                          save_name='test_datapack.h5',
                          clobber=True,
                          seed=None)
    with DataPack('test_datapack.h5', readonly=True) as dp:
        phase, axes = dp.phase
        _, antennas = dp.get_antennas(axes['ant'])
        _, directions = dp.get_directions(axes['dir'])
        _, times = dp.get_times(axes['time'])
        _, freqs = dp.get_freqs(axes['freq'])
        _, pols = dp.get_pols(axes['pol'])
        assert len(directions) == 2
        assert len(times) == 1
        assert len(freqs) == 2
        assert len(pols) == 1

    sky_model_bbs = "# (Name, Type, Ra, Dec, I) = format\n" \
                    "A, POINT, 00:00:00.123456, +37.07.47.12345, 1.0\n" \
                    "B, POINT, 00:00:00.123456, +37.37.47.12345, 1.0"
    with open('test_sky_model.bbs', 'w') as f:
        f.write(sky_model_bbs)

    directions = directions_from_sky_model('test_sky_model.bbs')
    assert len(directions) == 2

    assert format_direction_bbs(directions[0]) == ("00:00:00.123456", "+37.07.47.12345")

    assert format_direction_bbs(parse_coordinates_bbs('00:00:00.123456', '+37.07.47.12345')) == (
    "00:00:00.123456", "+37.07.47.12345")
    assert format_direction_bbs(parse_coordinates_bbs('00:00:00.123456', '-37.07.47.12345')) == (
    "00:00:00.123456", "-37.07.47.12345")

    Nd = len(directions)
    create_empty_datapack(Nd=Nd,
                          Nf=2,
                          Nt=1,
                          pols=None,
                          field_of_view_diameter=4.,
                          start_time=None,
                          time_resolution=30.,
                          min_freq=122.,
                          max_freq=166.,
                          array_file=None,
                          phase_tracking=None,
                          directions=directions,
                          save_name='test_datapack.h5',
                          clobber=True,
                          seed=None)
    with DataPack('test_datapack.h5', readonly=True) as dp:
        phase, axes = dp.phase
        _, antennas = dp.get_antennas(axes['ant'])
        _, directions = dp.get_directions(axes['dir'])
        _, times = dp.get_times(axes['time'])
        _, freqs = dp.get_freqs(axes['freq'])
        _, pols = dp.get_pols(axes['pol'])
        print(directions)
        assert len(directions) == 2
        assert len(times) == 1
        assert len(freqs) == 2
        assert len(pols) == 1
        dp.save_array_file('test_array.cfg')
        labels, antennas_m = load_array_file('test_array.cfg')
        assert np.allclose(antennas_m, dp.antennas[1])
