from pathlib import Path
from commands import Command
from device import Device

def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())

def _get_file_data(file_path: Path) -> list[str]:
    """Reads the file data"""
    with open(file_path, 'r') as file:
        return file.readlines()

def _determine_inputs(file_data: list[str]) -> list[str]:
    """Processes file data to ignore blank and comment lines"""
    input_data = []
    for line in file_data:
        line = line.strip()
        if len(line) == 0 or line.startswith('#'):
            continue
        input_data.append(line)
    return input_data

def _process_inputs(inputs: list[str]):
    """Processes the input lines into simulation parameters"""
    time_length = 0
    devices = {}
    initial_events = []

    for token in inputs:
        line = token.split()
        if line[0] == 'LENGTH':
            time_length = int(line[1])
        elif line[0] == 'DEVICE':
            devices[int(line[1])] = Device(int(line[1]))
        elif line[0] == 'PROPAGATE':
            from_id = int(line[1])
            to_id = int(line[2])
            delay = int(line[3])
            devices[from_id].add_prop(to_id, delay)
        elif line[0] == 'ALERT' or line[0] == 'CANCEL':
            sender_id = int(line[1])
            description = line[2]
            start_time = int(line[3])
            for receiver_id, delay in devices[sender_id].get_prop_dict().items():
                send_command = Command(line[0], sender_id, receiver_id, description, start_time, True)
                initial_events.append((start_time, send_command))

    return time_length, devices, initial_events

def main() -> None:
    """Runs the full simulation"""
    input_file_path = _read_input_file_path()

    if not input_file_path.exists():
        print('FILE NOT FOUND')
        return

    file_data = _get_file_data(input_file_path)
    inputs = _determine_inputs(file_data)
    time_length, devices, event_list = _process_inputs(inputs)

    event_list.sort(key=lambda x: x[0])

    while event_list:
        time, event = event_list.pop(0)

        sender_id = event.get_sender()
        receiver_id = event.get_receiver()
        description = event.get_message()
        event_type = event.get_type()
        is_sending = event.sending()

        if is_sending:
            if event_type == 'CANCEL':
                devices[sender_id].add_cancelled(description)

            event.print()

            delay = devices[sender_id].get_prop_dict()[receiver_id]
            receive_command = Command(event_type, sender_id, receiver_id, description, time + delay, False)
            event_list.append((time + delay, receive_command))

        else:
            event.print()
            device = devices[receiver_id]

            if event_type == 'CANCEL':
                if description not in device.get_cancelled():
                    device.add_cancelled(description)
                    for neighbor_id in device.get_prop_dict().keys():
                        send_command = Command('CANCEL', receiver_id, neighbor_id, description, time, True)
                        event_list.append((time, send_command))

            elif event_type == 'ALERT':
                if description not in device.get_cancelled():
                    for neighbor_id in device.get_prop_dict().keys():
                        send_command = Command('ALERT', receiver_id, neighbor_id, description, time, True)
                        event_list.append((time, send_command))

        event_list.sort(key=lambda x: x[0])

    print(f'@{time_length}: END')

if __name__ == '__main__':
    main()
