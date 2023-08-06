import ctypes
import pathlib
import platform
import sys

_libname = None
_filters_lib = None
if sys.platform == "win32":
    arc = platform.architecture()
    if arc[0].__contains__("64"):
        _libname = pathlib.Path(__file__).parent.resolve() / "libs" / "x64" / "callibri_utils-x64.dll"
        _filters_lib = pathlib.Path(__file__).parent.resolve() / "libs" / "x64" / "filters.dll"
    else:
        _libname = pathlib.Path(__file__).parent.resolve() / "libs" / "x86" / "callibri_utils-x86.dll"
        _filters_lib = pathlib.Path(__file__).parent.resolve() / "libs" / "x86" / "filters.dll"
elif sys.platform.startswith("linux"):
    print('Add linux lib')
elif sys.platform == "darwin":
    print('Add macos lib')
else:
    raise FileNotFoundError("This platform (%s) is currently not supported by pycallibri-ecg-lib." % sys.platform)

ctypes.windll.LoadLibrary(str(_filters_lib))
_callibri_lib = ctypes.CDLL(str(_libname))


class CallibriMath:
    def __init__(self, sampling_rate: int, data_window: int, nwins_for_pressure_index: int):
        callibri_math_lib = ctypes.POINTER(ctypes.c_void_p)

        self.create_callibri_math_lib = _callibri_lib.createCallibriMathLib
        self.create_callibri_math_lib.restype = ctypes.POINTER(callibri_math_lib)
        self.create_callibri_math_lib.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int)

        self.free_callibri_math_lib = _callibri_lib.freeCallibriMathLib
        self.free_callibri_math_lib.restype = None
        self.free_callibri_math_lib.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._init_filter = _callibri_lib.CallibriMathLibInitFilter
        self._init_filter.restype = None
        self._init_filter.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._push_data = _callibri_lib.CallibriMathLibPushData
        self._push_data.restype = None
        self._push_data.argtypes = (ctypes.POINTER(callibri_math_lib), ctypes.c_void_p, ctypes.c_size_t)

        self._process_data_arr = _callibri_lib.CallibriMathLibProcessDataArr
        self._process_data_arr.restype = None
        self._process_data_arr.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._get_rr = _callibri_lib.CallibriMathLibGetRR
        self._get_rr.restype = ctypes.c_double
        self._get_rr.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._get_pressure_index = _callibri_lib.CallibriMathLibGetPressureIndex
        self._get_pressure_index.restype = ctypes.c_double
        self._get_pressure_index.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._get_hr = _callibri_lib.CallibriMathLibGetHR
        self._get_hr.restype = ctypes.c_double
        self._get_hr.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._get_moda = _callibri_lib.CallibriMathLibGetModa
        self._get_moda.restype = ctypes.c_double
        self._get_moda.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._get_ampl_moda = _callibri_lib.CallibriMathLibGetAmplModa
        self._get_ampl_moda.restype = ctypes.c_double
        self._get_ampl_moda.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._get_variation_dist = _callibri_lib.CallibriMathLibGetVariationDist
        self._get_variation_dist.restype = ctypes.c_double
        self._get_variation_dist.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._initial_signal_corrupted = _callibri_lib.CallibriMathLibInitialSignalCorrupted
        self._initial_signal_corrupted.restype = ctypes.c_bool
        self._initial_signal_corrupted.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._reset_data_process = _callibri_lib.CallibriMathLibResetDataProcess
        self._reset_data_process.restype = None
        self._reset_data_process.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._set_rr_checked = _callibri_lib.CallibriMathLibSetRRchecked
        self._set_rr_checked.restype = None
        self._set_rr_checked.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._set_pressure_average = _callibri_lib.CallibriMathLibSetPressureAverage
        self._set_pressure_average.restype = None
        self._set_pressure_average.argtypes = (ctypes.POINTER(callibri_math_lib), ctypes.c_int)

        self._rr_detected = _callibri_lib.CallibriMathLibRRdetected
        self._rr_detected.restype = ctypes.c_bool
        self._rr_detected.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._clear_data = _callibri_lib.CallibriMathLibClearData
        self._clear_data.restype = None
        self._clear_data.argtypes = (ctypes.POINTER(callibri_math_lib),)

        self._native_ptr = self.create_callibri_math_lib(sampling_rate, data_window, nwins_for_pressure_index)

    def init_filter(self):
        self._init_filter(self._native_ptr)

    def push_data(self, samples: list):
        self._push_data(self._native_ptr, (ctypes.c_double * len(samples))(*samples), len(samples))

    def process_data_arr(self):
        self._process_data_arr(self._native_ptr)

    def get_rr(self) -> float:
        return self._get_rr(self._native_ptr)

    def get_pressure_index(self) -> float:
        return self._get_pressure_index(self._native_ptr)

    def get_hr(self) -> float:
        return self._get_hr(self._native_ptr)

    def get_moda(self) -> float:
        return self._get_moda(self._native_ptr)

    def get_ampl_moda(self) -> float:
        return self._get_ampl_moda(self._native_ptr)

    def get_variation_dist(self) -> float:
        return self._get_variation_dist(self._native_ptr)

    def initial_signal_corrupted(self) -> bool:
        return self._initial_signal_corrupted(self._native_ptr)

    def reset_data_process(self):
        self._reset_data_process(self._native_ptr)

    def set_rr_checked(self):
        self._set_rr_checked(self._native_ptr)

    def set_pressure_average(self, t: int):
        self._set_pressure_average(self._native_ptr, ctypes.c_int(t))

    def rr_detected(self) -> bool:
        return self._rr_detected(self._native_ptr)

    def clear_data(self):
        self._clear_data(self._native_ptr)

    def __del__(self):
        if self._native_ptr is not None:
            self.free_callibri_math_lib(self._native_ptr)
            self._native_ptr = None
