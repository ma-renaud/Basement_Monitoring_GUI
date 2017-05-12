from unittest import TestCase
from serial_decoder import SerialDecoder


class SerialDecoderStub(SerialDecoder):
    def __init__(self):
        SerialDecoder.__init__(self)
        self.trace = ""

    def reception_start(self):
        self.trace += 'S'

    def receive_data(self):
        self.trace += 'D'

    def append_received_data(self):
        self.trace += 'A'

    def reception_complete(self):
        self.trace += 'E'


class TestSerialDecoder(TestCase):
    def test_start_char_state_change(self):
        decoder = SerialDecoderStub()
        decoder.decode('<')

        self.assertEqual(decoder.trace, 'S')

    def test_receive_four_char_then_end(self):
        decoder = SerialDecoderStub()
        decoder.decode('<bleh>')

        self.assertEqual(decoder.trace, 'SDDDDAE')

    def test_receive_two_data(self):
        decoder = SerialDecoderStub()
        decoder.decode('<24.5,48.3>')

        self.assertEqual(decoder.trace, 'SDDDDADDDDAE')
