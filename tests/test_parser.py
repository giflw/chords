import unittest
from chordsmd.parser import parse_chord

class TestParser(unittest.TestCase):
    def test_simple_maj(self):
        res = parse_chord("C")
        self.assertEqual(res, {'root': 'C', 'quality': '', 'bass': None})

    def test_minor(self):
        res = parse_chord("Amin")
        self.assertEqual(res, {'root': 'A', 'quality': 'min', 'bass': None})

    def test_sharp(self):
        res = parse_chord("F#")
        self.assertEqual(res, {'root': 'F#', 'quality': '', 'bass': None})

    def test_flat_extensions(self):
        res = parse_chord("Bb7b9")
        self.assertEqual(res, {'root': 'Bb', 'quality': '7b9', 'bass': None})

    def test_bass(self):
        res = parse_chord("D/F#")
        self.assertEqual(res, {'root': 'D', 'quality': '', 'bass': 'F#'})

    def test_complex(self):
        res = parse_chord("G#m7b5/C#")
        self.assertEqual(res, {'root': 'G#', 'quality': 'm7b5', 'bass': 'C#'})

    def test_invalid(self):
        self.assertIsNone(parse_chord("Hello"))
        self.assertIsNone(parse_chord("Chord with spaces"))
        self.assertIsNone(parse_chord("Zmaj7")) # Z is not a note

if __name__ == '__main__':
    unittest.main()
