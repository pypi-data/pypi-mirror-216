from os.path import join
import time
from time import sleep
import tempfile
import pytest

import numpy as np

from barktools.base_utils import RingBuffer
from barktools.base_utils import Clocker
from barktools.base_utils import generate_name
from barktools.compute_utils import bind_angle, bind_angle_degrees, angular_diff, angular_diff_degrees

from tests.test_helper import TMP_DIR

class TestRingBuffer:
    
    def test_1(self):
        buffer_size = 3
        ring_buffer = RingBuffer(buffer_size=buffer_size)
        items_to_put = [0,1,2,3,4,5,6,7,8,9]
        for item in items_to_put:
            ring_buffer.put(item)
        assert ring_buffer.items() == [9,7,8]
        assert ring_buffer.n_last(2) == [8,9]

    def test_2(self):
        buffer_size = 1
        ring_buffer = RingBuffer(buffer_size=buffer_size)
        for item in [1,2,3,4]:
            ring_buffer.put(item)
        assert ring_buffer.last() == 4  

class TestClocker:

    def test_1(self):
        with tempfile.TemporaryDirectory() as tmp_dir:

            # Simulate process and make measurements
            clocker = Clocker(tmp_dir)
            clocker.add_targets('sleep_centi', 'sleep_milli')

            for _ in range(100):
                clocker.clock('sleep_centi')
                sleep(0.01)
                clocker.clock('sleep_milli')
                sleep(0.001)
            centi_path = join(tmp_dir, "sleep_centi.txt")
            milli_path = join(tmp_dir, "sleep_milli.txt")
            del(clocker) # NOTE: Necessary for tempfile to clean tmp_dir
            
            # Assert that measurements are acceptable
            individual_centi_tol = 5e-2
            mean_centi_tol = 2e-3
            centi_times = []
            with open(centi_path, 'r') as file:
                for line in file:
                    centi_times.append(float(line))
            assert all([abs(centi_time-0.01) < individual_centi_tol for centi_time in centi_times])
            centi_times_mean = sum(centi_times)/len(centi_times)
            assert abs(centi_times_mean-0.01) <  mean_centi_tol

            individual_milli_tol = 5e-2
            mean_milli_tol = 2e-3
            milli_times = []
            with open(milli_path, 'r') as file:
                for line in file:
                    milli_times.append(float(line))
            assert all([abs(milli_time-0.001) < individual_milli_tol for milli_time in milli_times])
            milli_times_mean = sum(milli_times)/len(milli_times)
            assert abs(milli_times_mean-0.001) <  mean_milli_tol

def test_generate_name():
    names = []
    for _ in range(10000):
        names.append(generate_name())

def test_bind_angles():
    deg2rad = np.pi/180.0
    assert bind_angle(10*deg2rad, 0) == pytest.approx(10*deg2rad)
    assert bind_angle(-10*deg2rad, 0) == pytest.approx(350*deg2rad)
    assert bind_angle(370*deg2rad, 0) == pytest.approx(10*deg2rad)
    assert bind_angle(-370*deg2rad, 0) == pytest.approx(350*deg2rad)

    assert bind_angle(10*deg2rad, -np.pi) == pytest.approx(10*deg2rad)
    assert bind_angle(-10*deg2rad, -np.pi) == pytest.approx(-10*deg2rad)
    assert bind_angle(370*deg2rad, -np.pi) == pytest.approx(10*deg2rad)
    assert bind_angle(-370*deg2rad, -np.pi) == pytest.approx(-10*deg2rad)

def test_bind_angles_degrees():
    assert bind_angle_degrees(10, 0) == pytest.approx(10)
    assert bind_angle_degrees(-10, 0) == pytest.approx(350)
    assert bind_angle_degrees(370, 0) == pytest.approx(10)
    assert bind_angle_degrees(-370, 0) == pytest.approx(350)

    assert bind_angle_degrees(10, -180) == pytest.approx(10)
    assert bind_angle_degrees(-10, -180) == pytest.approx(-10)
    assert bind_angle_degrees(370, -180) == pytest.approx(10)
    assert bind_angle_degrees(-370, -180) == pytest.approx(-10)

def test_angular_diff():
    deg2rad = np.pi/180.0
    assert angular_diff(30*deg2rad, 20*deg2rad) == pytest.approx(10*deg2rad)
    assert angular_diff(20*deg2rad, 30*deg2rad) == pytest.approx(-10*deg2rad)
    assert angular_diff(10*deg2rad, 350*deg2rad) == pytest.approx(20*deg2rad)
    assert angular_diff(350*deg2rad, 10*deg2rad) == pytest.approx(-20*deg2rad)
    assert (angular_diff(180*deg2rad, 0*deg2rad) == pytest.approx(180*deg2rad) or angular_diff(180*deg2rad, 0*deg2rad) == pytest.approx(-180*deg2rad))
    assert (angular_diff(0*deg2rad, 180*deg2rad) == pytest.approx(180*deg2rad) or angular_diff(0*deg2rad, 180*deg2rad) == pytest.approx(-180*deg2rad))
    assert angular_diff(90*deg2rad, 200*deg2rad) == pytest.approx(-110*deg2rad)
    assert angular_diff(10*deg2rad, 200*deg2rad) == pytest.approx(170*deg2rad)
    assert angular_diff(200*deg2rad, 10*deg2rad) == pytest.approx(-170*deg2rad)

def test_angular_diff_degrees():
    assert angular_diff_degrees(30, 20) == pytest.approx(10)
    assert angular_diff_degrees(20, 30) == pytest.approx(-10)
    assert angular_diff_degrees(10, 350) == pytest.approx(20)
    assert angular_diff_degrees(350, 10) == pytest.approx(-20)
    assert (angular_diff_degrees(180, 0) == pytest.approx(180) or angular_diff_degrees(180, 0) == pytest.approx(-180))
    assert (angular_diff_degrees(0, 180) == pytest.approx(180) or angular_diff_degrees(0, 180) == pytest.approx(-180))
    assert angular_diff_degrees(90, 200) == pytest.approx(-110)
    assert angular_diff_degrees(10, 200) == pytest.approx(170)
    assert angular_diff_degrees(200, 10) == pytest.approx(-170)
