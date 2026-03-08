"""Validation utilities for user input and LLM responses."""

import re
from typing import Tuple, Optional


def clean_llm_response(response: str) -> str:
    """
    Clean LLM response to extract pure code.

    Handles cases where LLM ignores instructions and wraps code in markdown.

    Args:
        response: Raw LLM response

    Returns:
        Cleaned code string
    """
    # Remove markdown code blocks if present
    if '```python' in response:
        # Extract code between ```python and ```
        match = re.search(r'```python\s*(.*?)\s*```', response, re.DOTALL)
        if match:
            response = match.group(1)
    elif '```' in response:
        # Extract code between ``` and ```
        match = re.search(r'```\s*(.*?)\s*```', response, re.DOTALL)
        if match:
            response = match.group(1)

    # Remove common explanation patterns
    lines = response.strip().split('\n')
    code_lines = []

    for line in lines:
        stripped = line.strip()

        # Skip empty lines at the start
        if not code_lines and not stripped:
            continue

        # Skip pure explanation lines (Chinese text without code markers)
        # Keep lines that have code-like patterns: =, (, ), [, ], etc.
        if stripped:
            # If line contains code patterns or is a comment, keep it
            if any(pattern in line for pattern in ['=', '(', ')', '[', ']', 'np.', 'plt.', '#']):
                code_lines.append(line)
            # Skip lines that look like pure explanatory text
            elif re.match(r'^[^\w]*[a-zA-Z\u4e00-\u9fa5\s,.:;!?，。：；！？]+[^\w]*$', stripped):
                continue
            else:
                code_lines.append(line)

    cleaned = '\n'.join(code_lines).strip()

    # Final cleanup: remove leading/trailing quotes if present
    cleaned = cleaned.strip('"\'')

    return cleaned


def validate_user_input(user_input: str) -> Tuple[bool, Optional[str]]:
    """
    Validate user input prompt.

    Args:
        user_input: User's prompt text

    Returns:
        (is_valid, error_message) tuple
    """
    # Check if empty
    if not user_input or not user_input.strip():
        return False, "请输入一个提示词"

    # Check length
    if len(user_input) < 2:
        return False, "提示词太短，请至少输入 2 个字符"

    if len(user_input) > 500:
        return False, "提示词太长，请保持在 500 字符以内"

    # Check for suspicious patterns (potential injection attempts)
    suspicious_patterns = [
        r'import\s+os',
        r'import\s+sys',
        r'__import__',
        r'eval\s*\(',
        r'exec\s*\(',
        r'open\s*\(',
        r'subprocess',
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            return False, "检测到不安全的内容，请输入正常的图形描述"

    return True, None
