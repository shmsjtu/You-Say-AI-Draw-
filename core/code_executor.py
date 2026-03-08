"""Sandboxed code execution engine for LLM-generated matplotlib code."""

import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from typing import Tuple, Optional, Dict, Any

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D  # 3D plotting support


class CodeExecutor:
    """Sandboxed executor for LLM-generated matplotlib code."""

    def __init__(self, timeout: int = 5):
        """
        Initialize code executor.

        Args:
            timeout: Execution timeout in seconds (currently not enforced,
                    would require multiprocessing for true timeout)
        """
        self.timeout = timeout

        # Configure matplotlib for non-interactive use
        matplotlib.use('Agg')
        plt.ioff()

        # Define allowed modules and builtins (whitelist approach)
        self.allowed_builtins = {
            # Math operations
            'abs': abs,
            'min': min,
            'max': max,
            'sum': sum,
            'round': round,
            'pow': pow,

            # Iteration
            'range': range,
            'len': len,
            'enumerate': enumerate,
            'zip': zip,

            # Type conversions
            'int': int,
            'float': float,
            'str': str,
            'list': list,
            'tuple': tuple,
            'dict': dict,

            # Logic
            'True': True,
            'False': False,
            'None': None,
        }

    def validate_code(self, code: str) -> Tuple[bool, Optional[str]]:
        """
        Pre-execution validation checks.

        Args:
            code: Code string to validate

        Returns:
            (is_valid, error_message) tuple
        """
        if not code or not code.strip():
            return False, "代码为空"

        # Check code length (prevent DoS)
        if len(code) > 10000:
            return False, "代码过长（超过 10000 字符）"

        # Check for dangerous patterns (blacklist)
        dangerous_patterns = [
            ('import ', '不允许使用 import 语句'),
            ('from ', '不允许使用 from 语句'),
            ('__import__', '不允许使用 __import__'),
            ('eval(', '不允许使用 eval'),
            ('exec(', '不允许使用 exec'),
            ('compile(', '不允许使用 compile'),
            ('open(', '不允许使用文件操作'),
            ('file(', '不允许使用文件操作'),
            ('input(', '不允许使用 input'),
            ('os.', '不允许访问操作系统模块'),
            ('sys.', '不允许访问系统模块'),
            ('subprocess', '不允许使用子进程'),
            ('__builtins__', '不允许访问内置模块'),
            ('globals(', '不允许访问全局变量'),
            ('locals(', '不允许访问局部变量'),
            ('vars(', '不允许访问变量字典'),
            ('dir(', '不允许使用 dir'),
            ('getattr', '不允许使用 getattr'),
            ('setattr', '不允许使用 setattr'),
            ('delattr', '不允许使用 delattr'),
            ('hasattr', '不允许使用 hasattr'),
        ]

        code_lower = code.lower()
        for pattern, error_msg in dangerous_patterns:
            if pattern.lower() in code_lower:
                return False, f"安全检查失败: {error_msg}"

        # Check for basic matplotlib usage
        if 'plt.' not in code:
            return False, "代码中未检测到 matplotlib 绘图命令 (plt.)"

        return True, None

    def execute(self, code: str) -> Tuple[Optional[plt.Figure], Optional[str]]:
        """
        Execute code in isolated namespace.

        Args:
            code: Python code to execute

        Returns:
            (figure, error_message) tuple
            - figure: matplotlib Figure object if successful, None if failed
            - error_message: Error string if execution failed, None if successful
        """
        # Validate before execution
        is_valid, error = self.validate_code(code)
        if not is_valid:
            return None, error

        # Create a fresh figure
        fig, ax = plt.subplots(figsize=(8, 6))

        # Create isolated namespace with only allowed modules
        namespace: Dict[str, Any] = {
            'np': np,
            'plt': plt,
            'Axes3D': Axes3D,  # Allow 3D plotting
            '__builtins__': self.allowed_builtins,
        }

        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            # Execute code in isolated namespace
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, namespace, namespace)

            # Check if a figure was created
            if fig.get_axes():
                return fig, None
            else:
                # No axes created, try to get current figure
                current_fig = plt.gcf()
                if current_fig and current_fig.get_axes():
                    return current_fig, None
                else:
                    plt.close(fig)
                    return None, "代码执行成功但未生成图形"

        except NameError as e:
            plt.close(fig)
            error_msg = str(e)
            if 'is not defined' in error_msg:
                return None, f"变量错误: {error_msg}\n提示：仅允许使用 np (numpy) 和 plt (matplotlib)"
            return None, f"名称错误: {error_msg}"

        except SyntaxError as e:
            plt.close(fig)
            return None, f"语法错误: {e.msg} (第 {e.lineno} 行)"

        except ValueError as e:
            plt.close(fig)
            return None, f"数值错误: {str(e)}\n提示：检查数学运算和参数范围"

        except TypeError as e:
            plt.close(fig)
            return None, f"类型错误: {str(e)}"

        except ZeroDivisionError:
            plt.close(fig)
            return None, "数学错误: 除零错误"

        except MemoryError:
            plt.close(fig)
            return None, "内存错误: 代码使用了过多内存"

        except Exception as e:
            plt.close(fig)
            error_type = type(e).__name__
            error_msg = str(e)

            # Capture stderr if available
            stderr_output = stderr_capture.getvalue()
            if stderr_output:
                return None, f"{error_type}: {error_msg}\n\n详细信息:\n{stderr_output}"

            return None, f"{error_type}: {error_msg}"

        finally:
            # Clean up captures
            stdout_capture.close()
            stderr_capture.close()
