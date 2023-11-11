from directories import Directories
import os, subprocess

class Flutter:

    def run_flutter_app():
        try:
            os.chdir(Directories.PROJECT_LOCATION)
            flutter_executable = "C:\\src\\flutter\\bin\\flutter.bat"
            cmd = [flutter_executable, "run", "-d", "chrome"]
            print("<Update: Application is running...")
            completed_process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                check=True
            )
            print("<Update: Flutter app built successfully>")
        except Exception as e:
            print("<Error: An error occurred: " + str(e) + ">")
            # self.raise_bug("Resolve this bug: " + str(error))
            # self.run_flutter_clean_and_pub_get(e)