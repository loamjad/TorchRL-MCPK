import struct
import numpy as np


class MathHelper:
    SIN_TABLE = None

    @classmethod
    def _static_init(cls):
        cls.SIN_TABLE = np.sin(np.arange(65536, dtype=np.float64) * np.pi * np.float64(2.0) / np.float64(65536.0)).astype(np.float32)

    @staticmethod
    def sin(value: np.float32) -> np.float32:
        return MathHelper.SIN_TABLE[int(value * np.float32(10430.378)) & 65535]

    @staticmethod
    def cos(value: np.float32) -> np.float32:
        return MathHelper.SIN_TABLE[int(value * np.float32(10430.378) + np.float32(16384.0)) & 65535]
    
MathHelper._static_init()
