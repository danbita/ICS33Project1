import unittest
from device import Device
from commands import Command
from project1 import _determine_inputs, _process_inputs

'''
The following unittests are split into 3 groups: tests regarding the device class, tests regarding 
the command class, and tests for the helper methods. I can test the entire simulation of the 
main loop of project 1, but doing this allows me to test for all of the functions that are used in 
that loop to ensure that they are behaving correctly.
'''

class TestDevice(unittest.TestCase):
    def test_device_creation(self):
        device = Device(1)
        self.assertEqual(device.get_id(), 1)
        self.assertEqual(device.get_prop_dict(), {})
        self.assertEqual(device.get_cancelled(), set())

    def test_add_one_propagation(self):
        device = Device(2)
        device.add_prop(3, 500)
        self.assertEqual(device.get_prop_dict(), {3: 500})

    def test_add_multiple_propagations(self):
        device = Device(4)
        device.add_prop(5, 100)
        device.add_prop(6, 200)
        device.add_prop(7, 300)
        self.assertEqual(device.get_prop_dict(), {5: 100, 6: 200, 7: 300})

    def test_add_one_cancelled(self):
        device = Device(5)
        device.add_cancelled("Intrusion")
        self.assertIn("Intrusion", device.get_cancelled())
        self.assertEqual(len(device.get_cancelled()), 1)

    def test_add_multiple_cancelled(self):
        device = Device(6)
        device.add_cancelled("Intrusion")
        device.add_cancelled("Fire")
        device.add_cancelled("Medical")
        self.assertSetEqual(device.get_cancelled(), {"Intrusion", "Fire", "Medical"})

    def test_cancelling_an_already_cancelled_alert(self):
        device = Device(8)
        device.add_cancelled("Fire")
        device.add_cancelled("Fire")
        self.assertEqual(len(device.get_cancelled()), 1)


class TestCommand(unittest.TestCase):
    def test_creating_command_class_and_getters(self):
        command = Command('ALERT', 1, 2, 'TestMessage', 100, True)
        self.assertEqual(command.get_type(), 'ALERT')
        self.assertEqual(command.get_sender(), 1)
        self.assertEqual(command.get_receiver(), 2)
        self.assertEqual(command.get_message(), 'TestMessage')
        self.assertEqual(command.time(), 100)
        self.assertTrue(command.sending())


class TestHelperFunctions(unittest.TestCase):
    def test_determine_inputs_removes_comments_and_blanks(self):
        lines = [
            "# This is a comment",
            "DEVICE 1",
            "",
            "   ",
            "PROPAGATE 1 2 1000"
        ]
        processed = _determine_inputs(lines)
        self.assertEqual(processed, ['DEVICE 1', 'PROPAGATE 1 2 1000'])

    def test_determine_inputs_empty(self):
        lines = []
        processed = _determine_inputs(lines)
        self.assertEqual(processed, [])

    def test_process_inputs_devices(self):
        inputs = [
            "LENGTH 10000",
            "DEVICE 1",
            "DEVICE 2",
            "PROPAGATE 1 2 500"
        ]
        time_length, devices, initial_events = _process_inputs(inputs)

        self.assertEqual(time_length, 10000)
        self.assertIn(1, devices)
        self.assertIn(2, devices)
        self.assertEqual(devices[1].get_prop_dict(), {2: 500})
        self.assertEqual(devices[2].get_prop_dict(), {})
        self.assertEqual(initial_events, [])

    def test_process_inputs_initial_events(self):
        inputs = [
            "LENGTH 5000",
            "DEVICE 1",
            "DEVICE 2",
            "PROPAGATE 1 2 750",
            "ALERT 1 Fire 0"
        ]
        time_length, devices, initial_events = _process_inputs(inputs)

        self.assertEqual(time_length, 5000)
        self.assertEqual(len(initial_events), 1)

        time, event = initial_events[0]
        self.assertEqual(time, 0)
        self.assertEqual(event.get_type(), 'ALERT')
        self.assertEqual(event.get_sender(), 1)
        self.assertEqual(event.get_receiver(), 2)
        self.assertEqual(event.get_message(), 'Fire')


if __name__ == '__main__':
    unittest.main()
