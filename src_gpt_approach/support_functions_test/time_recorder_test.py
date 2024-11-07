import unittest

from support_functions.time_recorder import TimeRecorder


class TestTimeRecorder(unittest.TestCase):
    def test_set_time(self):
        recorder = TimeRecorder()
        time = 10_00_000
        recorder.nanoseconds = time
        self.assertEqual(recorder.nanoseconds, time)
        
    def test_get_ns(self):
        recorder = TimeRecorder()
        time = 10_00_000
        recorder.nanoseconds = time
        self.assertEqual(recorder.nanoseconds, time) 
    
    def test_get_ms(self):
        recorder = TimeRecorder()
        time = 10_00_000
        recorder.nanoseconds = time
        self.assertEqual(recorder.milliseconds, time / 1_000_000)
    
    def test_get_sec(self):
        recorder = TimeRecorder()
        time = 10_00_000
        recorder.nanoseconds = time
        self.assertEqual(recorder.seconds, time / 1_000_000_000) 
    
    def test_get_min(self):
        recorder = TimeRecorder()
        time = 10_00_000
        recorder.nanoseconds = time
        self.assertEqual(recorder.minutes, time / 1_000_000_000 / 60) 
        

if __name__ == "__main__":
    unittest.main()