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

    def test_accepts_structured_multiword_owner_action(self):
        result = transform_note("Action: Alex Morgan | send the launch brief | Friday")
        self.assertEqual(
            result["actions"],
            [{"owner": "Alex Morgan", "task": "send the launch brief", "due": "Friday", "status": "needs_confirmation"}],
        )

    def test_rejects_empty_note(self):
        with self.assertRaisesRegex(ValueError, "note must contain"):
            transform_note("   ")

if __name__ == "__main__":
    unittest.main()

class MeetingRelayCliTests(unittest.TestCase):
    def test_cli_emits_json_for_local_note(self):
        import json
        import subprocess
        import sys
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            note = Path(directory) / "note.txt"
            note.write_text("Decision: Ship a limited pilot.\nAction: Alex to send the brief by Friday.\n")
            result = subprocess.run(
                [sys.executable, "meeting_relay.py", str(note)],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["actions"][0]["status"], "needs_confirmation")

    def test_cli_rejects_empty_local_note(self):
        import subprocess
        import sys
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            note = Path(directory) / "empty.txt"
            note.write_text("   ")
            result = subprocess.run(
                [sys.executable, "meeting_relay.py", str(note)],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("note must contain text", result.stderr)
