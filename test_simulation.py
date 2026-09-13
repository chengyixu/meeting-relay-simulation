import unittest
from simulation import transform_note

class MeetingRelayTests(unittest.TestCase):
    def test_creates_deduplicated_confirmable_actions(self):
        result = transform_note("""# Meeting
        Action: Alex to send the launch brief by Friday.
        ACTION: Alex to send the launch brief by Friday.
        Decision: Ship a limited pilot.
        Action: Priya to schedule a customer review.
        """)
        self.assertEqual(result["decisions"], ["Ship a limited pilot."])
        self.assertEqual(
            result["actions"],
            [
                {"owner": "Alex", "task": "send the launch brief", "due": "Friday", "status": "needs_confirmation"},
                {"owner": "Priya", "task": "schedule a customer review", "due": None, "status": "needs_confirmation"},
            ],
        )

    def test_rejects_empty_note(self):
        with self.assertRaisesRegex(ValueError, "note must contain"):
            transform_note("   ")

if __name__ == "__main__":
    unittest.main()
