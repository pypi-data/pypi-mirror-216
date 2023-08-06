from callibri_ecg_lib import CallibriMath


def main():
    callibri_math = CallibriMath(250, 127, 30)
    callibri_math.init_filter()

    rawData = [float(x) for x in range(25)]
    callibri_math.push_data(rawData)
    callibri_math.process_data_arr()

    is_corrupted = callibri_math.initial_signal_corrupted()
    print("Is Corrupted: " + str(is_corrupted))

    if callibri_math.rr_detected():
        hr = callibri_math.get_hr()
        print("hr: " + str(hr))




if __name__ == '__main__':
    main()
