from kf import KalmanFilter1D, KalmanFilter2D
import numpy as np

import unittest

class TestKalmanFilter1D(unittest.TestCase):
    def test_can_construct(self):
        x = 0.2
        v = 0.3
        a = 1.2

        kf = KalmanFilter1D(x, v, a)
        self.assertAlmostEqual(kf.pos_x, x)
        self.assertAlmostEqual(kf.vel_x, v)

    def test_after_predict_mean_and_cov_are_right_shape(self):
        x = 0.2
        v = 0.3
        a = 1.2

        kf = KalmanFilter1D(x, v, a)
        kf.predict(dt=0.1)

        self.assertEqual(kf.mean.shape, (2, ))
        self.assertEqual(kf.cov.shape, (2, 2))

    def test_calling_predict_increases_uncertainty(self):
        x = 0.2
        v = 0.3
        a = 1.2

        kf = KalmanFilter1D(x, v, a)
        
        for _ in range(10):
            det_before = np.linalg.det(kf.cov)
            kf.predict(dt=0.1)
            det_after = np.linalg.det(kf.cov)

            self.assertGreater(det_after, det_before)

    def test_calling_update_decreases_uncertainty(self):
        x = 0.2
        v = 0.3
        a = 1.2

        kf = KalmanFilter1D(x, v, a)
        for _ in range(10):
            det_before = np.linalg.det(kf.cov)
            kf.update(meas_value=0.1, meas_variance=0.01)
            det_after = np.linalg.det(kf.cov)

            self.assertLess(det_after, det_before)

class TestKalmanFilter2D(unittest.TestCase):
    def test_can_construct(self):
        x = 0.2
        y = 0.5
        v_x = 0.3
        v_y = 0.8
        a = 1.2

        kf = KalmanFilter2D(x, y, v_x, v_y, a)
        self.assertAlmostEqual(kf.pos_x, x)
        self.assertAlmostEqual(kf.pos_y, y)
        self.assertAlmostEqual(kf.vel_x, v_x)
        self.assertAlmostEqual(kf.vel_y, v_y)

    def test_after_predict_mean_and_cov_are_right_shape(self):
        x = 0.2
        y = 0.5
        v_x = 0.3
        v_y = 0.8
        a = 1.2

        kf = KalmanFilter2D(x, y, v_x, v_y, a)
        kf.predict(dt=0.1)

        self.assertEqual(kf.mean.shape, (4, ))
        self.assertEqual(kf.cov.shape, (4, 4))

    def test_calling_predict_increases_uncertainty(self):
        x = 0.2
        y = 0.5
        v_x = 0.3
        v_y = 0.8
        a = 1.2

        kf = KalmanFilter2D(x, y, v_x, v_y, a)
        
        for _ in range(10):
            det_before = np.linalg.det(kf.cov)
            kf.predict(dt=0.1)
            det_after = np.linalg.det(kf.cov)

            self.assertGreater(det_after, det_before)

    def test_calling_update_decreases_uncertainty(self):
        x = 0.2
        y = 0.5
        v_x = 0.3
        v_y = 0.8
        a = 1.2

        kf = KalmanFilter2D(x, y, v_x, v_y, a)
        for _ in range(10):
            print(_)
            det_before = np.linalg.det(kf.cov)
            kf.update(meas_value=[0.1, 0.2], meas_variance=[[4, 2], [2, 4]])
            det_after = np.linalg.det(kf.cov)

            self.assertLess(det_after, det_before)
