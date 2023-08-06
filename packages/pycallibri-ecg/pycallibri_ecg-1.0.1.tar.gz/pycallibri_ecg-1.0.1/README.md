# Mathematical library for working with ECG data from the Callibri sensor.
 
The main functionality is the calculation of cardio-interval lengths, heart rate and Stress Index (SI).

During the first 6 seconds the algorithm is learning, if no 5 RR-intervals are found in the signal 
5 RR-intervals are not found, the training is repeated. Further work with the library is iterative (adding new data, calculating indicators).

## Initialization
### Determine the basic parameters

1. Raw signal sampling frequency. Integer type. The allowed values are 250 or 1000.
2. Data processing window size. Integer type. Valid values of sampling_rate / 4 or sampling_rate / 2.
3. Number of windows to calculate SI. Integer type. Allowable values [20...50].
4. The averaging parameter of the IN calculation. Default value is 6.

### Creating a library instance
Firstly you need to determine lybrary parameters and then put them to library. Tne next step is initialize the filters. In the current version the filters are built-in and clearly defined: Butterworth 2nd order BandPass 5_15 Hz.

You can initialize averaging for SI calculation. It is optional value.

##### Python
```python
# 1. Raw signal sampling frequency
samplingRate = 250
# 2. Data processing window size
dataWindow = samplingRate / 2
# 3. Number of windows to calculate SI
nwinsForPressureIndex = 30
callibri_math = CallibriMath(samplingRate, dataWindow, nwinsForPressureIndex)
callibri_math.init_filter()

# optional
# 4. The averaging parameter of the IN calculation. Default value is 6.
pressureIndexAverage = 6
callibri_math.set_pressure_average(pressureIndexAverage)
```

## Initializing a data array for transfer to the library:
The size of the transmitted array has to be of a certain length:
- 25 values for a signal frequency of 250 Hz 
- 100 values for a signal frequency of 1000 Hz

##### Python
```python
rawData = [float(x) for x in range(25)]
# or
rawData = [float(x) for x in range(100)]
```
## Optional functions (not necessary for the library to work)
Check for initial signal corruption. This method should be used if you want to detect and notify of a distorted signal explicitly. 

##### Python
```python
if callibri_math.initial_signal_corrupted():
    # Signal corrupted!!!
```
### Work with the library
1. Adding and process data:

##### Python
```python
callibri_math.push_data(samples)
callibri_math.process_data_arr()
```
2. Getting the results:

##### Python
```python
if callibri_math.rr_detected():
    # check for a new peak in the signal
    # RR-interval length
    rr = math.get_rr()
    # HR     
    hr = math.get_hr()
    # SI
    pi = math.get_pressure_index()
    # Moda
    moda = math.get_moda()
    # Amplitude of mode
    amplModa = math.get_ampl_moda()
    # Variation range
    variationDist = math.get_variation_dist()
    callibri_math.set_rr_checked()
```

## Finishing work with the library:

##### Python
```python
del callibri_math
```