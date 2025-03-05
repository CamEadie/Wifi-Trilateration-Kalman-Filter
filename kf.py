import numpy as np
from abc import ABC, abstractmethod

class BaseKalmanFilter(ABC):
    def __init__(self, state_dims: int, 
                       meas_dims: int,
                       noise_dims: int,
                       acceleration_variance: float) -> None:
        self._state_dims = state_dims
        self._meas_dims = meas_dims
        self._noise_dims = noise_dims

        # Mean state of GRV
        self._x = np.zeros(self._state_dims)

        # Covariance of state of GRV
        self._P = np.eye(self._state_dims)

        self._acceleration_variance = acceleration_variance

    @abstractmethod
    def F(self, dt: float) -> np.ndarray:
        F = np.eye(self._state_dims)
        return F

    @abstractmethod
    def G(self, dt: float) -> np.ndarray:
        G = np.zeros((self._state_dims, self._noise_dims))
        return G

    @abstractmethod
    def H(self) -> np.ndarray:
        H = np.zeros((self._meas_dims, self._state_dims))
        return H

    def predict(self, dt: float) -> None:
        F = self.F(dt)
        G = self.G(dt)
        I_meas = np.eye(self._meas_dims)

        # x = F x (if there were control inputs add "+ B u" to add input to the state)
        # P = F P Ft + G aI Gt
        self._x = F.dot(self._x)
        self._P = F.dot(self._P).dot(F.T) + G.dot(self._acceleration_variance * I_meas).dot(G.T)

    def update(self, meas_value: np.ndarray, meas_variance: np.ndarray) -> None:
        z = np.array(meas_value)
        R = np.array(meas_variance)
        H = self.H()
        I_state = np.eye(self._state_dims)

        # y = z - H x
        # S = H P Ht + R
        # K = P Ht S^-1
        # x = x + K y
        # P = (I - K H) * P
        y = z - H.dot(self._x)
        S = H.dot(self._P).dot(H.T) + R
        K = self._P.dot(H.T).dot(np.linalg.pinv(S)) # Use the pseudo-inverse for stability
        self._x = self._x + K.dot(y)
        self._P = (I_state - K.dot(H)).dot(self._P)

    @property
    def mean(self) -> np.ndarray:
        return self._x

    @property
    def cov(self) -> np.ndarray:
        return self._P
    
class KalmanFilter1D(BaseKalmanFilter):
    def __init__(self, initial_x: float, 
                       initial_v: float,
                       acceleration_variance: float) -> None:
        super().__init__(state_dims=2, meas_dims=1, noise_dims=1, acceleration_variance=acceleration_variance)
        
        self.iX = 0
        self.iV_X = 1

        # Mean state of GRV
        self._x[self.iX] = initial_x
        self._x[self.iV_X] = initial_v

    def F(self, dt: float) -> np.ndarray:
        F = super().F(dt)
        F[self.iX, self.iV_X] = dt
        return F

    def G(self, dt: float) -> np.ndarray:
        G = super().G(dt)
        G[self.iX, self.iX] = 0.5 * dt**2
        G[self.iV_X, self.iX] = dt
        return G

    def H(self) -> np.ndarray:
        H = super().H()
        H[self.iX, self.iX] = 1
        return H

    @property
    def pos_x(self) -> float:
        return self._x[self.iX]
    
    @property
    def vel_x(self) -> float:
        return self._x[self.iV_X]
    
class KalmanFilter2D(BaseKalmanFilter):
    def __init__(self, initial_x: float, 
                       initial_y: float,
                       initial_v_x: float,
                       initial_v_y: float,
                       acceleration_variance: float) -> None:
        super().__init__(state_dims=4, meas_dims=2, noise_dims=2, acceleration_variance=acceleration_variance)
        
        self.iX = 0
        self.iY = 1
        self.iV_X = 2
        self.iV_Y = 3

        # Mean state of GRV
        self._x[self.iX] = initial_x
        self._x[self.iY] = initial_y
        self._x[self.iV_X] = initial_v_x
        self._x[self.iV_Y] = initial_v_y

    def F(self, dt: float) -> np.ndarray:
        F = super().F(dt)
        F[self.iX, self.iV_X] = dt
        F[self.iY, self.iV_Y] = dt
        return F

    def G(self, dt: float) -> np.ndarray:
        G = super().G(dt)
        G[self.iX, self.iX] = 0.5 * dt**2
        G[self.iY, self.iY] = 0.5 * dt**2
        G[self.iV_X, self.iX] = dt
        G[self.iV_Y, self.iY] = dt
        return G

    def H(self) -> np.ndarray:
        H = super().H()
        H[self.iX, self.iX] = 1
        H[self.iX, self.iX] = 1
        return H

    @property
    def pos_x(self) -> float:
        return self._x[self.iX]
    
    @property
    def pos_y(self) -> float:
        return self._x[self.iY]
    
    @property
    def vel_x(self) -> float:
        return self._x[self.iV_X]

    @property
    def vel_y(self) -> float:
        return self._x[self.iV_Y]