from unittest import TestCase, TextTestRunner, defaultTestLoader
from source.clockFace import TimeGenerator
from datetime import  datetime

class TestClockFace(TestCase):

    @classmethod
    def setUpClass(self):
        print("Test Start")
        self.timegen = TimeGenerator()

    @classmethod
    def tearDownClass(self):
        print("Test Done")

    def test_time_oclock(self):
        time = self.timegen.get_words_from_time(h=1,m=00)
        self.assertEqual(time,"it is one o'clock")

    def test_time_upper_case(self):
        self.timegen = TimeGenerator(case='upper',format='24')
        time = self.timegen.get_words_from_time(h=18,m=30)
        self.assertEqual(time,"IT IS HALF PAST EIGHTEEN")

    def test_half_past_one(self):
        time = self.timegen.get_words_from_time(h=1,m=30)
        self.assertEqual(time,"it is half past one")

    def test_quarter_to_13_format_24(self):
        self.timegen = TimeGenerator(case='lower',format='24')
        time = self.timegen.get_words_from_time(h=13,m=45)
        self.assertEqual(time,"it is quarter to thirteen")

    def test_quarter_to_13_format_12(self):
        self.timegen = TimeGenerator(case='lower',format='12')
        time = self.timegen.get_words_from_time(h=13,m=45)
        self.assertEqual(time,"it is quarter to one")

    def test_quarter_to_13_format_24_upper(self):
        self.timegen = TimeGenerator(case='upper',format='24')
        time = self.timegen.get_words_from_time(h=13,m=45)
        self.assertEqual(time,"IT IS QUARTER TO THIRTEEN")

    def test_quarter_to_13_format_12_upper(self):
        self.timegen = TimeGenerator(case='upper',format='12')
        time = self.timegen.get_words_from_time(h=13,m=45)
        self.assertEqual(time,"IT IS QUARTER TO ONE")

    def test_get_current_hour(self):
        current_hour = datetime.now().hour
        self.assertEqual(self.timegen.get_current_hour(),current_hour)

    def test_fail_current_minute_with_approx_minute(self):
        current_minute = datetime.now().minute

        # if the current minute is like 10,20,.. then approximate = current minute
        if current_minute % 5 == 0:
            self.assertEqual(self.timegen.get_approximate_minute(),current_minute)
        else:
            self.assertNotEqual(self.timegen.get_approximate_minute(),current_minute)
    
    def test_random_time(self):
        time = self.timegen.get_words_from_time(h=None,m=None)
        assumed_time = "half past two"

        # Handling a corner case:
        # when the current_time and assumed_time is same,
        # happens if the test runs exactly at half past two
        system_time = datetime.now()
        if system_time.minute == 30 and system_time.hour == 2:
            self.assertEqual(time,assumed_time)
        else:
            self.assertNotEqual(time,assumed_time)

def run():
    TextTestRunner().run(defaultTestLoader.loadTestsFromTestCase(TestClockFace))

if __name__ == '__main__':

    run()
