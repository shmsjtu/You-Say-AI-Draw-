"""Security tests for code executor."""

import pytest
import numpy as np
import matplotlib.pyplot as plt

import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.code_executor import CodeExecutor


class TestCodeExecutorSecurity:
    """Security tests for sandboxed code execution."""

    def setup_method(self):
        """Set up test fixtures."""
        self.executor = CodeExecutor(timeout=5)

    def test_blocks_import_statement(self):
        """Test that import statements are blocked."""
        code = "import os; os.system('ls')"
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid
        assert error is not None
        assert 'import' in error.lower()

    def test_blocks_from_import(self):
        """Test that from...import statements are blocked."""
        code = "from os import system; system('ls')"
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid
        assert 'from' in error.lower()

    def test_blocks_eval_exploit(self):
        """Test that eval() is blocked."""
        code = "eval('__import__(\"os\").system(\"ls\")')"
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid
        assert 'eval' in error.lower()

    def test_blocks_exec_exploit(self):
        """Test that exec() is blocked."""
        code = "exec('import os; os.system(\"ls\")')"
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid
        assert 'exec' in error.lower()

    def test_blocks_open_file(self):
        """Test that file operations are blocked."""
        code = "open('/etc/passwd', 'r').read()"
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid
        assert 'open' in error.lower()

    def test_blocks_os_module(self):
        """Test that os module access is blocked."""
        code = "os.system('rm -rf /')"
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid
        assert 'os.' in error.lower()

    def test_blocks_sys_module(self):
        """Test that sys module access is blocked."""
        code = "sys.exit(1)"
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid
        assert 'sys.' in error.lower()

    def test_blocks_subprocess(self):
        """Test that subprocess module is blocked."""
        code = "subprocess.call(['ls', '-l'])"
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid
        assert 'subprocess' in error.lower()

    def test_blocks_builtins_access(self):
        """Test that __builtins__ access is blocked."""
        code = "__builtins__['eval']('1+1')"
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid

    def test_blocks_globals_access(self):
        """Test that globals() is blocked."""
        code = "globals()['os']"
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid
        assert 'globals' in error.lower()

    def test_blocks_getattr_exploit(self):
        """Test that getattr is blocked."""
        code = "getattr(__builtins__, 'eval')('1+1')"
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid
        assert 'getattr' in error.lower()

    def test_rejects_empty_code(self):
        """Test that empty code is rejected."""
        code = ""
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid

    def test_rejects_long_code(self):
        """Test that overly long code is rejected."""
        code = "x = 1\n" * 10000  # > 10000 characters
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid
        assert '过长' in error

    def test_rejects_code_without_matplotlib(self):
        """Test that code without matplotlib is rejected."""
        code = "x = np.array([1, 2, 3])"
        is_valid, error = self.executor.validate_code(code)

        assert not is_valid
        assert 'plt.' in error


class TestCodeExecutorValidExecution:
    """Tests for valid code execution."""

    def setup_method(self):
        """Set up test fixtures."""
        self.executor = CodeExecutor(timeout=5)

    def test_allows_simple_circle(self):
        """Test execution of simple circle code."""
        code = """
t = np.linspace(0, 2*np.pi, 100)
x = np.cos(t)
y = np.sin(t)
plt.plot(x, y)
plt.axis('equal')
"""
        is_valid, error = self.executor.validate_code(code)
        assert is_valid
        assert error is None

        fig, error = self.executor.execute(code)
        assert fig is not None
        assert error is None
        plt.close(fig)

    def test_allows_parametric_equation(self):
        """Test execution of parametric equation."""
        code = """
t = np.linspace(0, 2*np.pi, 100)
x = 16 * np.sin(t)**3
y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
plt.fill(x, y, 'red', alpha=0.7)
plt.axis('equal')
plt.title('Heart')
"""
        is_valid, error = self.executor.validate_code(code)
        assert is_valid

        fig, error = self.executor.execute(code)
        assert fig is not None
        assert error is None
        plt.close(fig)

    def test_allows_polar_plot(self):
        """Test execution of polar plot."""
        code = """
theta = np.linspace(0, 2*np.pi, 100)
r = 1 + 0.5 * np.sin(5 * theta)
ax = plt.subplot(111, projection='polar')
ax.plot(theta, r)
"""
        is_valid, error = self.executor.validate_code(code)
        assert is_valid

        fig, error = self.executor.execute(code)
        assert fig is not None
        assert error is None
        plt.close(fig)

    def test_allows_scatter_plot(self):
        """Test execution of scatter plot."""
        code = """
t = np.linspace(0, 2*np.pi, 50)
x = np.cos(t)
y = np.sin(t)
plt.scatter(x, y, c=t, cmap='viridis')
plt.axis('equal')
"""
        is_valid, error = self.executor.validate_code(code)
        assert is_valid

        fig, error = self.executor.execute(code)
        assert fig is not None
        assert error is None
        plt.close(fig)

    def test_catches_syntax_error(self):
        """Test that syntax errors are caught gracefully."""
        code = """
t = np.linspace(0, 2*np.pi, 100)
x = np.cos(t)
y = np.sin(t
plt.plot(x, y)
"""
        # Validation should pass (syntax check not done at validation)
        is_valid, _ = self.executor.validate_code(code)
        assert is_valid

        # Execution should fail with syntax error
        fig, error = self.executor.execute(code)
        assert fig is None
        assert error is not None
        assert '语法错误' in error

    def test_catches_name_error(self):
        """Test that undefined variables are caught."""
        code = """
plt.plot(undefined_variable, undefined_variable)
"""
        is_valid, _ = self.executor.validate_code(code)
        assert is_valid

        fig, error = self.executor.execute(code)
        assert fig is None
        assert error is not None
        assert '错误' in error

    def test_catches_math_error(self):
        """Test that math errors are caught."""
        code = """
x = np.array([1, 2, 3])
y = x / 0
plt.plot(x, y)
"""
        is_valid, _ = self.executor.validate_code(code)
        assert is_valid

        # This might raise RuntimeWarning instead of exception
        # but should not crash the executor
        fig, error = self.executor.execute(code)
        # Either succeeds with inf/nan or fails gracefully
        if fig is not None:
            plt.close(fig)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
