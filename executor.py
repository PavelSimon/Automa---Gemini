import subprocess
import os
import tempfile
import logging
from pathlib import Path
from typing import Dict, Any
import resource
import signal
import time

logger = logging.getLogger(__name__)

class ScriptExecutor:
    """Basic script executor with sandboxing features"""

    def __init__(self, timeout: int = 30, memory_limit: int = 100 * 1024 * 1024):  # 100MB
        self.timeout = timeout
        self.memory_limit = memory_limit

    def execute_script(self, script_content: str, script_name: str = "script.py") -> Dict[str, Any]:
        """
        Execute a Python script with basic sandboxing

        Args:
            script_content: The Python script content as string
            script_name: Name of the script file

        Returns:
            Dict containing execution results
        """
        result = {
            "success": False,
            "output": "",
            "error": "",
            "return_code": None,
            "execution_time": 0
        }

        # Create temporary directory for script execution
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / script_name

            # Write script content to file
            try:
                script_path.write_text(script_content)
            except Exception as e:
                result["error"] = f"Failed to write script: {str(e)}"
                return result

            # Execute the script
            start_time = time.time()

            try:
                # Basic sandboxing: run in subprocess with resource limits
                env = os.environ.copy()
                # Remove potentially dangerous environment variables
                env.pop('LD_PRELOAD', None)
                env.pop('LD_LIBRARY_PATH', None)

                # Run the script with timeout and resource limits
                process = subprocess.Popen(
                    ['python3', str(script_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=temp_dir,
                    env=env,
                    preexec_fn=self._set_limits if os.name != 'nt' else None
                )

                try:
                    stdout, stderr = process.communicate(timeout=self.timeout)
                    result["return_code"] = process.returncode
                    result["output"] = stdout.decode('utf-8', errors='ignore')
                    result["error"] = stderr.decode('utf-8', errors='ignore')
                    result["success"] = process.returncode == 0

                except subprocess.TimeoutExpired:
                    process.kill()
                    result["error"] = f"Script execution timed out after {self.timeout} seconds"
                    result["return_code"] = -1

            except Exception as e:
                result["error"] = f"Execution failed: {str(e)}"
                result["return_code"] = -1

            finally:
                execution_time = time.time() - start_time
                result["execution_time"] = round(execution_time, 2)

        return result

    def _set_limits(self):
        """Set resource limits for the subprocess (Unix only)"""
        try:
            # Set memory limit
            resource.setrlimit(resource.RLIMIT_AS, (self.memory_limit, self.memory_limit))
            # Set CPU time limit
            resource.setrlimit(resource.RLIMIT_CPU, (self.timeout, self.timeout))
            # Prevent fork bombs
            resource.setrlimit(resource.RLIMIT_NPROC, (10, 10))
        except Exception as e:
            logger.warning(f"Could not set resource limits: {str(e)}")

    def validate_script(self, script_content: str) -> Dict[str, Any]:
        """
        Basic script validation

        Args:
            script_content: The Python script content

        Returns:
            Dict with validation results
        """
        result = {
            "valid": True,
            "warnings": [],
            "errors": []
        }

        # Check for dangerous imports
        dangerous_imports = [
            'os.system', 'subprocess.call', 'subprocess.run', 'subprocess.Popen',
            'eval', 'exec', 'importlib', 'sys.exit', 'os._exit'
        ]

        lines = script_content.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            for dangerous in dangerous_imports:
                if dangerous in line and not line.startswith('#'):
                    result["warnings"].append(
                        f"Line {i}: Potentially dangerous operation '{dangerous}' detected"
                    )

        # Check for file operations
        file_operations = ['open(', 'file(', '.read()', '.write(']
        for i, line in enumerate(lines, 1):
            for op in file_operations:
                if op in line and not line.startswith('#'):
                    result["warnings"].append(
                        f"Line {i}: File operation '{op}' detected - ensure proper sandboxing"
                    )

        return result

# Global executor instance
executor = ScriptExecutor()

def execute_python_script(script_content: str, script_name: str = "script.py") -> Dict[str, Any]:
    """Convenience function to execute a Python script"""
    return executor.execute_script(script_content, script_name)

def validate_python_script(script_content: str) -> Dict[str, Any]:
    """Convenience function to validate a Python script"""
    return executor.validate_script(script_content)
