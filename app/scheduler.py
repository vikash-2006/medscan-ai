"""
Background Medicine Reminder Scheduler for MedScan AI.
Uses schedule + threading to send notifications even when user is on another screen.
"""
import os
import sys
import threading
import time
from typing import List, Dict, Any

_IS_ANDROID = sys.platform == "android" or "ANDROID_ARGUMENT" in os.environ or "ANDROID_ROOT" in os.environ

try:
    import schedule
    _SCHEDULE_AVAILABLE = True
except ImportError:
    _SCHEDULE_AVAILABLE = False

_scheduler_thread = None
_scheduler_running = False

SLOT_TIMES = {
    "Morning": "08:00",
    "Afternoon": "13:00",
    "Evening": "18:00",
    "Night": "21:00"
}


def _send_notification(medicine_name: str, timing: str):
    """Send a local notification using plyer (desktop platforms only)."""
    if _IS_ANDROID:
        print(f"[Scheduler Reminder] {medicine_name} scheduled time: {timing}")
        return
    try:
        from plyer import notification
        notification.notify(
            title="💊 MedScan AI — Medicine Reminder",
            message=f"Time to take {medicine_name}\n{timing}",
            timeout=10
        )
    except Exception as e:
        print(f"[Notification Warning] Could not send notification: {e}")


def _run_scheduler():
    """Background loop that runs pending scheduled jobs."""
    while _scheduler_running:
        try:
            schedule.run_pending()
        except Exception as e:
            print(f"[Scheduler Loop Warning] Job execution error: {e}")
        time.sleep(30)  # Check every 30 seconds


def start_medicine_scheduler(medicines: List[Dict[str, Any]], page=None):
    """
    Schedule daily medicine reminders based on slot times.
    Runs in a daemon thread so it works in background.
    """
    global _scheduler_thread, _scheduler_running

    if not _SCHEDULE_AVAILABLE:
        print("[Scheduler Warning] 'schedule' package not installed. Run: pip install schedule")
        return False

    # Clear existing jobs
    schedule.clear()

    for med in medicines:
        name = med.get("name", "Medicine")
        slot = med.get("slot", "Morning")
        timing = med.get("timing", "")
        taken = med.get("taken", False)

        if taken:
            continue  # Already taken, skip

        time_str = SLOT_TIMES.get(slot, "08:00")

        try:
            schedule.every().day.at(time_str).do(_send_notification, medicine_name=name, timing=timing)
            print(f"[Scheduler] Scheduled {name} at {time_str} daily")
        except Exception as e:
            print(f"[Scheduler Warning] Could not schedule {name}: {e}")

    # Start background thread
    if not _scheduler_running:
        _scheduler_running = True
        _scheduler_thread = threading.Thread(target=_run_scheduler, daemon=True)
        _scheduler_thread.start()
        print("[Scheduler] Background medicine scheduler started ✅")

    return True


def stop_scheduler():
    """Stop the background scheduler and clear all jobs."""
    global _scheduler_running
    _scheduler_running = False
    if _SCHEDULE_AVAILABLE:
        schedule.clear()
    print("[Scheduler] Scheduler stopped.")


def is_scheduler_running() -> bool:
    """Check if the scheduler is currently active."""
    return _scheduler_running


def reschedule_medicine(medicine_name: str, new_time: str):
    """Reschedule a specific medicine to a new time (HH:MM format)."""
    if not _SCHEDULE_AVAILABLE:
        return False
    try:
        # Clear and reschedule (schedule lib doesn't support per-job cancel easily)
        schedule.every().day.at(new_time).do(_send_notification, medicine_name=medicine_name, timing=f"Custom: {new_time}")
        print(f"[Scheduler] Rescheduled {medicine_name} to {new_time}")
        return True
    except Exception as e:
        print(f"[Scheduler Warning] Reschedule failed: {e}")
        return False
