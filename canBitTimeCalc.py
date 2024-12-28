import matplotlib.pyplot as plt

def find_can_parameters(clock_mcu, target_sampling_point, target_speed_kbps):
    available_parameters = []
    for prescaler in range(1, 1024):  # Range of prescaler from 1 to 1024
        for seg1 in range(1, 16):     # Range of seg1 from 1 to 16 (max for CAN)
            for seg2 in range(1, 8):  # Range of seg2 from 1 to 8 (max for CAN)
                total_segments = 1 + seg1 + seg2
                speed_kbps = (clock_mcu / prescaler) / total_segments / 1000
                sampling_point = ((1 + seg1) / total_segments) * 100

                if abs(speed_kbps - target_speed_kbps) < 1:
                    bit_time = (1 / (clock_mcu / prescaler)) * total_segments * 1e6
                    tq_time = (1 / (clock_mcu / prescaler)) * 1e6  # Time for one TQ
                    available_parameters.append((prescaler, seg1, seg2, bit_time, sampling_point, speed_kbps, tq_time))

                    if abs(sampling_point - target_sampling_point) < 1:
                        return prescaler, seg1, seg2, bit_time, sampling_point, speed_kbps, tq_time, available_parameters
    return None, None, None, None, None, None, None, available_parameters

def visualize_can_parameters_graphically(seg1, seg2, sampling_point, bit_time, total_segments, tq_time, speed_kbps):
    sampling_pos = (1 + seg1) / total_segments

    fig, ax = plt.subplots()
    ax.plot([-1, total_segments + 1], [0, 0], color="black", linewidth=2) 

    ax.fill_betweenx([-0.1, 0.1], 0, 1, color="red", alpha=0.3, label="Sync Segment")
    ax.fill_betweenx([-0.1, 0.1], 1, 1 + seg1, color="blue", alpha=0.3, label="SEG1")
    ax.fill_betweenx([-0.1, 0.1], 1 + seg1, total_segments, color="green", alpha=0.3, label="SEG2")
    
    ax.plot([sampling_pos * total_segments, sampling_pos * total_segments], [-0.3, 0.3], color="purple", linestyle="--", label="Sampling Point")
    ax.text(sampling_pos * total_segments, 0.6, 'Sampling Point', horizontalalignment='center', verticalalignment='center', color='purple')

    for i in range(total_segments + 1):
        ax.plot([i, i], [-0.1, 0.1], color="black", linestyle="--")
        ax.text(i, -0.4, f'{i}', horizontalalignment='center', verticalalignment='center', color='black')
    
    ax.text(total_segments + 1, -0.4, "TQ", horizontalalignment='center', verticalalignment='center', color='black')

    ax.set_ylim([-1, 1])
    ax.axis("off")
    plt.legend()
    plt.title("STM32 CAN Bit Segments Visualization")

    ax.text(total_segments / 2, -0.9, f'MCU Clock: {clock_mcu} Hz\n Prescaler: {prescaler}\n TQ Time: {tq_time:.2f} us\nSEG1 Time: {seg1 * tq_time:.2f} us\n SEG1: {seg1}\nSEG2 Time: {seg2 * tq_time:.2f} us\n SEG2: {seg2}\nTotal Bit Time: {bit_time:.2f} us\nSampling Point: {sampling_point:.2f} %\nCAN Bus speed: {speed_kbps:.2f} kbit/s', horizontalalignment='center', verticalalignment='center')

    plt.show()

choice = input("Do you want to calculate SEG1, SEG2, and prescaler (1) or provide them manually (2)? ")

if choice.lower() == '1':
    clock_mcu = int(input("Enter MCU clock frequency (Hz, for STM32 type a APBx freq): "))
    target_sampling_point = float(input("Enter desired sampling point (%): "))
    target_speed_kbps = float(input("Enter desired data rate (kbit/s): "))

    prescaler, seg1, seg2, bit_time, sampling_point, speed_kbps, tq_time, available_parameters = find_can_parameters(clock_mcu, target_sampling_point, target_speed_kbps)

    if prescaler is not None:
        print(f"Prescaler: {prescaler}")
        print(f"SEG1: {seg1}")
        print(f"SEG2: {seg2}")
        print(f"Bit time: {bit_time:.2f} us")
        print(f"Sampling point: {sampling_point:.2f} %")
        print(f"CAN Bus speed: {speed_kbps:.2f} kbit/s")
        print(f"TQ time: {tq_time:.2f} us")
        visualize_can_parameters_graphically(seg1, seg2, sampling_point, bit_time, total_segments=1 + seg1 + seg2, tq_time=tq_time, speed_kbps=speed_kbps)
    else:
        print("Could not find appropriate parameters for given values.")
        print("Available parameters:")
        for params in available_parameters:
            print(f"CAN Bus speed: {params[5]:.2f} kbit/s, Prescaler: {params[0]}, SEG1: {params[1]}, SEG2: {params[2]}, Sampling Point: {params[4]:.2f} %, TQ time: {params[6]:.2f} us")

else:
    clock_mcu = int(input("Enter MCU clock frequency (Hz, for STM32 type a APBx freq): "))
    prescaler = int(input("Enter prescaler: "))
    seg1 = int(input("Enter SEG1: "))
    seg2 = int(input("Enter SEG2: "))

    total_segments = 1 + seg1 + seg2
    sampling_point = ((1 + seg1) / total_segments) * 100
    bit_time = (1 / (clock_mcu / prescaler)) * total_segments * 1e6
    tq_time = (1 / (clock_mcu / prescaler)) * 1e6  # Time for one TQ
    speed_kbps = (clock_mcu / prescaler) / total_segments / 1000

    print(f"Sampling point: {sampling_point:.2f} %")
    print(f"CAN Bus speed: {speed_kbps:.2f} kbit/s")
    visualize_can_parameters_graphically(seg1, seg2, sampling_point, bit_time, total_segments, tq_time, speed_kbps)
