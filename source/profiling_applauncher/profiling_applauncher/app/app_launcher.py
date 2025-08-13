import cProfile
import pstats
import signal

from isaaclab.app import AppLauncher as BaseAppLauncher

class AppLauncher(BaseAppLauncher):
    """Custom AppLauncher class that can profile performance."""

    def __init__(self, *args, profiler=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._profiler = profiler
        if self._profiler is not None:
            self._profiler.enable()
            print("[INFO] Profiling enabled. Press Ctrl+C to stop profiling and save stats.")

        self._profile_saved = False

        signal.signal(signal.SIGINT, self._interrupt_signal_handle_callback)

    def save_profiling_data(self):
        """Disable profiling and save stats to a file when the script exits."""
        if self._profiler is None or self._profile_saved:
            return

        self._profiler.disable()
        print(f"[INFO] Saving profiling data to profile.prof")

        ps = pstats.Stats(self._profiler)

        # Optional: strip directory paths to make output shorter
        # ps.strip_dirs()

        # # Sort by cumulative time in function
        # ps.sort_stats("cumulative")

        # Print stats to the file
        ps.dump_stats("profile.prof")
        self._profile_saved = True

        # print filepath of the saved profile
        print(f"[INFO] Profiling data saved to profile.prof")

    def _interrupt_signal_handle_callback(self, signum, frame):
        """Handle interrupt signal and save profiling data."""
        self.save_profiling_data()
        # close the app
        self._app.close()
        # raise the error for keyboard interrupt
        raise KeyboardInterrupt