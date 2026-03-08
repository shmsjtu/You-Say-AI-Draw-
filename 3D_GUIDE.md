# 3D 图形绘制指南

## ✨ 新功能：支持 3D 数学图形！

现在 "你说我画" 应用支持绘制 3D 数学图形了！你可以创建各种立体图形，包括螺旋、球体、曲面等。

---

## 🎨 3D 示例提示词

### 基础 3D 图形

**3D 螺旋：**
```
画一个 3D 螺旋
```

**3D 球体：**
```
画一个 3D 球体
```

**3D 圆环（甜甜圈）：**
```
画一个 3D 圆环
```

**3D 波浪曲面：**
```
画一个 3D 波浪曲面
```

### 创意 3D 图形

**3D 玫瑰曲线：**
```
画一个 3D 玫瑰形状
```

**3D 莫比乌斯带：**
```
画一个 3D 莫比乌斯带
```

**3D 山脉地形：**
```
画一个 3D 山脉
```

**3D 双螺旋：**
```
画一个 3D DNA 双螺旋
```

---

## 📚 技术说明

### 如何生成 3D 图形

LLM 会生成使用 matplotlib 3D 功能的代码。以下是典型的 3D 代码结构：

#### 示例 1: 3D 螺旋
```python
ax = plt.subplot(111, projection='3d')
t = np.linspace(0, 4*np.pi, 1000)
x = np.cos(t)
y = np.sin(t)
z = t
ax.plot3D(x, y, z, 'blue', linewidth=2)
ax.set_title('3D 螺旋')
```

#### 示例 2: 3D 球面
```python
ax = plt.subplot(111, projection='3d')
u = np.linspace(0, 2*np.pi, 50)
v = np.linspace(0, np.pi, 50)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, cmap='viridis', alpha=0.8)
ax.set_title('球面')
```

#### 示例 3: 3D 曲面
```python
ax = plt.subplot(111, projection='3d')
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
x, y = np.meshgrid(x, y)
r = np.sqrt(x**2 + y**2)
z = np.sin(r) / r
ax.plot_surface(x, y, z, cmap='coolwarm')
ax.set_title('波浪曲面')
```

---

## 🔧 可用的 3D 绘图函数

### 线条和点

- `ax.plot3D(x, y, z)` - 绘制 3D 曲线
- `ax.scatter3D(x, y, z)` - 绘制 3D 散点图

### 曲面

- `ax.plot_surface(x, y, z)` - 绘制 3D 曲面
- `ax.plot_wireframe(x, y, z)` - 绘制线框图
- `ax.contour3D(x, y, z)` - 绘制 3D 等高线

### 其他

- `ax.plot_trisurf(x, y, z)` - 三角网格曲面
- `ax.bar3d(x, y, z, dx, dy, dz)` - 3D 柱状图

### 设置标签

- `ax.set_xlabel('X')` - 设置 X 轴标签
- `ax.set_ylabel('Y')` - 设置 Y 轴标签
- `ax.set_zlabel('Z')` - 设置 Z 轴标签
- `ax.set_title('标题')` - 设置图形标题

---

## 🎯 坐标系统

### 参数方程

3D 图形通常使用参数方程表示：

```python
x = x(t)
y = y(t)
z = z(t)
```

### 球坐标

也可以使用球坐标系统：

```python
x = r * sin(theta) * cos(phi)
y = r * sin(theta) * sin(phi)
z = r * cos(theta)
```

### 网格数据

对于曲面，使用网格数据：

```python
x, y = np.meshgrid(x_range, y_range)
z = f(x, y)
```

---

## 💡 提示

### 获得更好的 3D 效果

1. **明确指定维度**：在提示词中包含 "3D"
   - ✅ "画一个 3D 螺旋"
   - ❌ "画一个螺旋"（可能生成 2D）

2. **描述立体特征**：
   - "画一个立体的..."
   - "画一个有深度的..."
   - "画一个三维的..."

3. **指定视角**：
   - "从上方看的 3D..."
   - "旋转的 3D..."

### 常见问题

**Q: 为什么我的图形是 2D 的？**

A: 确保在提示词中明确包含 "3D" 或 "立体" 等关键词。

**Q: 3D 图形可以旋转吗？**

A: 在 Streamlit 界面中显示的是静态图像，但生成的是标准的 matplotlib 3D 图形。

**Q: 可以同时显示多个 3D 对象吗？**

A: 可以！在同一个坐标系中绘制多个对象即可。

---

## 🌟 创意 3D 图形示例

### 数学艺术

- **洛伦兹吸引子**：混沌系统的 3D 可视化
- **克莱因瓶**：4D 物体在 3D 中的投影
- **超立方体**：4D 立方体的 3D 投影

### 自然形态

- **DNA 双螺旋**：两条缠绕的螺旋
- **贝壳螺旋**：对数螺线的 3D 版本
- **花朵**：3D 玫瑰曲线

### 几何图形

- **柏拉图立体**：五种正多面体
- **网格球体**：球面的网格表示
- **扭曲立方体**：变形的立方体

---

## 📊 性能建议

### 优化渲染速度

1. **减少采样点**：
   ```python
   # 快速预览
   u = np.linspace(0, 2*np.pi, 30)  # 较少点

   # 高质量渲染
   u = np.linspace(0, 2*np.pi, 100)  # 更多点
   ```

2. **简化曲面**：
   - 使用 `plot_wireframe` 代替 `plot_surface`
   - 减少网格密度

3. **限制数据范围**：
   - 避免过大的坐标范围
   - 适当的 z 轴范围

---

## 📝 完整示例

### 示例：3D 玫瑰曲线

提示词：
```
画一个 3D 玫瑰曲线，要有花瓣的感觉
```

可能生成的代码：
```python
ax = plt.subplot(111, projection='3d')
t = np.linspace(0, 2*np.pi, 1000)
r = 1 + np.sin(4*t)
x = r * np.cos(t)
y = r * np.sin(t)
z = np.sin(3*t)
ax.plot3D(x, y, z, 'red', linewidth=2)
ax.set_title('3D 玫瑰曲线')
```

---

**享受 3D 数学艺术创作！🎨📐**
