"""测试 3D 绘图功能"""

import sys
sys.path.insert(0, '..')

from core.code_executor import CodeExecutor
import matplotlib.pyplot as plt

def test_3d_helix():
    """测试 3D 螺旋"""
    code = """
ax = plt.subplot(111, projection='3d')
t = np.linspace(0, 4*np.pi, 1000)
x = np.cos(t)
y = np.sin(t)
z = t
ax.plot3D(x, y, z, 'blue', linewidth=2)
ax.set_title('3D 螺旋')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
"""
    executor = CodeExecutor()
    fig, error = executor.execute(code)

    if error:
        print(f"Error: {error}")
        return False
    else:
        print("3D Helix: OK")
        plt.savefig('test_3d_helix.png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        return True


def test_3d_sphere():
    """测试 3D 球体"""
    code = """
ax = plt.subplot(111, projection='3d')
u = np.linspace(0, 2*np.pi, 50)
v = np.linspace(0, np.pi, 50)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, cmap='viridis', alpha=0.8)
ax.set_title('3D 球体')
"""
    executor = CodeExecutor()
    fig, error = executor.execute(code)

    if error:
        print(f"❌ 错误: {error}")
        return False
    else:
        print("✅ 3D 球体绘制成功")
        plt.savefig('test_3d_sphere.png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        return True


def test_3d_torus():
    """测试 3D 圆环"""
    code = """
ax = plt.subplot(111, projection='3d')
u = np.linspace(0, 2*np.pi, 50)
v = np.linspace(0, 2*np.pi, 50)
u, v = np.meshgrid(u, v)
R = 2
r = 1
x = (R + r*np.cos(v)) * np.cos(u)
y = (R + r*np.cos(v)) * np.sin(u)
z = r * np.sin(v)
ax.plot_surface(x, y, z, cmap='plasma', alpha=0.9)
ax.set_title('3D 圆环')
"""
    executor = CodeExecutor()
    fig, error = executor.execute(code)

    if error:
        print(f"❌ 错误: {error}")
        return False
    else:
        print("✅ 3D 圆环绘制成功")
        plt.savefig('test_3d_torus.png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        return True


def test_3d_wave_surface():
    """测试 3D 波浪曲面"""
    code = """
ax = plt.subplot(111, projection='3d')
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
x, y = np.meshgrid(x, y)
r = np.sqrt(x**2 + y**2)
z = np.sin(r) / r
ax.plot_surface(x, y, z, cmap='coolwarm', alpha=0.9)
ax.set_title('3D 波浪曲面')
"""
    executor = CodeExecutor()
    fig, error = executor.execute(code)

    if error:
        print(f"❌ 错误: {error}")
        return False
    else:
        print("✅ 3D 波浪曲面绘制成功")
        plt.savefig('test_3d_wave.png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        return True


if __name__ == '__main__':
    print("=" * 50)
    print("Testing 3D Plotting Functionality")
    print("=" * 50)

    tests = [
        ("3D Helix", test_3d_helix),
        ("3D Sphere", test_3d_sphere),
        ("3D Torus", test_3d_torus),
        ("3D Wave Surface", test_3d_wave_surface),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        print(f"\nTesting {name}...")
        if test_func():
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)

    if failed == 0:
        print("\nAll 3D tests passed!")
    else:
        print(f"\n{failed} test(s) failed")
