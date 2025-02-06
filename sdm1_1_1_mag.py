import cmath
import time
import adi
import numpy as np  # Import numpy to handle NaN values

# Electrode Names Dictionary
electrode_name = [
    "R26_C56_C57",  # Electrode 0
    "R24_C54_C56",  # Electrode 1
    "R22_C52_C54",  # Electrode 2
    "R18_C50_C52",  # Electrode 3
    "R16_C48_C50",  # Electrode 4
    "R14_C46_C48",  # Electrode 5
    "R12_C44_C46",  # Electrode 6
    "R10_C42_C44",  # Electrode 7
    "R8_C40_C42",   # Electrode 8
]  # Electrode 15

def main():
    # ----------------------------------------------------------------------------------------------------
    # DEVICE SETTINGS
    # ----------------------------------------------------------------------------------------------------
    cn0565 = adi.cn0565(uri="serial:/dev/ttyACM0,230400,8n1n")
    # reset the cross point switch

    amplitude = 100
    frequency = 80000
    baudrate = 230400

    cn0565.gpio1_toggle = True
    cn0565.excitation_amplitude = amplitude  # Set amplitude
    cn0565.excitation_frequency = frequency  # Hz # Set frequency between 10kHz to 80kHz
    cn0565.magnitude_mode = False
    cn0565.impedance_mode = True

    print("--------------------------------------------------------------")
    print("Amplitude: " + str(amplitude) + "mV")
    print("Frequency: " + str(frequency) + " Hz")
    print("Baud Rate: " + str(baudrate))
    print("--------------------------------------------------------------\n")

    cn0565.immediate = True

    cn0565.add(0x71)
    cn0565.add(0x70)

    fplus = 1
    splus = 4
    fminus = 4
    sminus = 1

    cn0565[fplus][0] = True
    cn0565[splus][1] = True
    cn0565[sminus][2] = True
    cn0565[fminus][3] = True

    # Array for storing magnitude of impedance per iteration
    magnitudes = []

    for neg_e in range(0, 8):  # setting neg_e = Electrode 1 to Electrode 15
        for pos_e in range(0, 8):  # setting pos_e = Electrode 0 to neg_e

            cn0565.open_all()
            cn0565[pos_e][0] = True
            cn0565[pos_e][1] = True
            cn0565[neg_e][2] = True
            cn0565[neg_e][3] = True

            # Command CN0565 to measure impedance at specified electrodes using specified frequency
            try:
                res = cn0565.channel["voltage0"].raw

                print("--------------------------------------------------------------")
                print("Electrode " + str(neg_e) + " - Electrode " + str(pos_e))
                print(electrode_name[neg_e] + " - " + electrode_name[pos_e])
                print("--------------------------------------------------------------")
                print("Rectangular: " + str(res))
                (mag, radph) = cmath.polar(res)
                degph = radph * 180 / cmath.pi
                degphb = 360 + degph
                print(f"Polar: Magnitude:{mag} Phase(degrees): {degph} or {degphb}")

                # store magnitude reading of each pair to array
                magnitudes.append(mag if not np.isnan(mag) else 'NaN')

            except KeyError:
                print(f"Error: Channel 'voltage0' not found for Electrode {neg_e} and Electrode {pos_e}.")

    # At the end of execution, print only the magnitude values
    print("\nMagnitude Values: ", ', '.join(map(str, magnitudes)))


main()

