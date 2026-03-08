"""Test 3D plotting functionality"""

import sys
sys.path.insert(0, '..')

from core.code_executor import CodeExecutor
import matplotlib.pyplot as plt

def test_simple_3d():
    """Test simple 3D helix"""
    code = """
ax = plt.subplot(111, projection='3d')
t = np.linspace(0, 4*np.pi, 1000)
x = np.cos(t)
y = np.sin(t)
z = t
ax.plot3D(x, y, z, 'blue', linewidth=2)
ax.set_title('3D Helix')
"""
    executor = CodeExecutor()
    fig, error = executor.execute(code)

    if error:
        print(f"FAILED: {error}")
        return False
    else:
        print("PASS: 3D Helix")
        plt.close(fig)
        return True


if __name__ == '__main__':
    print("Testing 3D Support...")
    if test_simple_3d():
        print("\nSUCCESS: 3D plotting is working!")
    else:
        print("\nFAILED: 3D plotting has issues")
