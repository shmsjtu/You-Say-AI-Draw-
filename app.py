"""Main Streamlit application for You Say I Draw."""

import streamlit as st
import matplotlib.pyplot as plt
from typing import Optional

from config import get_settings
from core import (
    build_system_prompt,
    format_user_prompt,
    CodeExecutor,
    get_llm_client,
)
from utils import clean_llm_response, validate_user_input


def init_session_state():
    """Initialize Streamlit session state."""
    if 'history' not in st.session_state:
        st.session_state.history = []

    if 'executor' not in st.session_state:
        settings = get_settings()
        st.session_state.executor = CodeExecutor(timeout=settings.timeout_seconds)

    if 'llm_client' not in st.session_state:
        settings = get_settings()

        # Validate configuration
        is_valid, error = settings.validate_config()
        if not is_valid:
            st.session_state.llm_client = None
            st.session_state.config_error = error
        else:
            try:
                st.session_state.llm_client = get_llm_client(
                    provider=settings.llm_provider,
                    api_key=settings.get_api_key(),
                    model=settings.model_name,
                    temperature=settings.temperature,
                    max_tokens=settings.max_tokens,
                    base_url=settings.get_base_url(),
                )
                st.session_state.config_error = None
            except Exception as e:
                st.session_state.llm_client = None
                st.session_state.config_error = str(e)


def render_header():
    """Render page header."""
    st.title("🥧 你说我画 - You Say I Draw")
    st.markdown("### 让 AI 把你的想象画成数学图形")
    st.markdown("---")


def render_examples():
    """Render example prompts."""
    st.markdown("#### 💡 提示示例：")

    # 2D examples
    st.markdown("**2D 图形：**")
    examples_2d = [
        "画一个圆",
        "画一个心形",
        "画一个笑脸",
        "画一个愤怒的包子",
        "画一朵玫瑰花",
        "画一个五角星",
        "画一个螺旋",
        "画一只蝴蝶",
    ]

    cols = st.columns(4)
    for idx, example in enumerate(examples_2d):
        col = cols[idx % 4]
        if col.button(example, key=f"example_2d_{idx}", use_container_width=True):
            st.session_state.user_input = example

    # 3D examples
    st.markdown("**3D 图形：**")
    examples_3d = [
        "画一个 3D 螺旋",
        "画一个 3D 球体",
        "画一个 3D 圆环",
        "画一个 3D 波浪曲面",
    ]

    cols_3d = st.columns(4)
    for idx, example in enumerate(examples_3d):
        col = cols_3d[idx % 4]
        if col.button(example, key=f"example_3d_{idx}", use_container_width=True):
            st.session_state.user_input = example


def render_input_section() -> Optional[str]:
    """
    Render input section and return user prompt if valid.

    Returns:
        User prompt string if valid, None otherwise
    """
    # Text input
    user_input = st.text_input(
        "输入你的想象：",
        placeholder="例如：画一个笑脸",
        key="input_box",
        value=st.session_state.get('user_input', '')
    )

    # Generate button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        generate_clicked = st.button("🎨 生成图形", type="primary", use_container_width=True)
    with col2:
        show_code = st.checkbox("显示代码", value=False)

    st.session_state.show_code = show_code

    if generate_clicked:
        # Validate input
        is_valid, error = validate_user_input(user_input)
        if not is_valid:
            st.error(f"❌ {error}")
            return None

        return user_input

    return None


def generate_and_render(user_prompt: str):
    """
    Generate code from LLM and render the figure.

    Args:
        user_prompt: User's prompt text
    """
    settings = get_settings()
    executor = st.session_state.executor
    llm_client = st.session_state.llm_client

    # Check if client is initialized
    if llm_client is None:
        st.error(f"❌ 配置错误: {st.session_state.config_error}")
        st.info("💡 请检查 .env 文件中的 API 密钥配置")
        return

    try:
        # Build prompts
        system_prompt = build_system_prompt()
        formatted_prompt = format_user_prompt(user_prompt)

        # Call LLM
        with st.spinner("🤔 AI 正在思考..."):
            raw_code = llm_client.generate_code(formatted_prompt, system_prompt)

        # Clean response
        cleaned_code = clean_llm_response(raw_code)

        # Show code if requested
        if st.session_state.get('show_code', False):
            with st.expander("📝 生成的代码", expanded=True):
                st.code(cleaned_code, language='python')

        # Execute code
        with st.spinner("🎨 正在绘制图形..."):
            fig, error = executor.execute(cleaned_code)

        if error:
            st.error(f"❌ 代码执行失败: {error}")

            # Show problematic code for debugging
            with st.expander("🔍 查看生成的代码"):
                st.code(cleaned_code, language='python')

            st.info("💡 提示：尝试换一个描述方式，或者重新生成")
        else:
            # Success! Display the figure
            st.success("✅ 图形生成成功！")
            st.pyplot(fig)

            # Add to history
            st.session_state.history.append({
                'prompt': user_prompt,
                'code': cleaned_code,
                'figure': fig,
            })

            # Clear input
            st.session_state.user_input = ''

            # Close figure to free memory
            plt.close(fig)

    except Exception as e:
        st.error(f"❌ 发生错误: {str(e)}")
        st.info("💡 请检查网络连接和 API 密钥配置")

        if settings.debug_mode:
            st.exception(e)


def render_history():
    """Render history section."""
    if not st.session_state.history:
        return

    st.markdown("---")
    st.markdown("### 📜 历史记录")

    # Show last 5 items in reverse order
    for idx, item in enumerate(reversed(st.session_state.history[-5:])):
        with st.expander(f"🎨 {item['prompt']}", expanded=(idx == 0)):
            st.pyplot(item['figure'])
            if st.checkbox(f"显示代码 #{len(st.session_state.history) - idx}", key=f"history_code_{idx}"):
                st.code(item['code'], language='python')


def render_footer():
    """Render page footer."""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 0.9em;'>
            <p>🥧 Happy Pi Day! | 使用 Streamlit + NumPy + Matplotlib 构建</p>
            <p>⚠️ 本项目使用 LLM 生成代码，在沙箱环境中安全执行</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    """Main application entry point."""
    # Page configuration
    settings = get_settings()
    st.set_page_config(
        page_title=settings.page_title,
        page_icon="🥧",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Configure matplotlib for Chinese font support (Windows)
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
    except Exception:
        pass  # Ignore font configuration errors

    # Initialize session state
    init_session_state()

    # Render UI
    render_header()

    # Show configuration status in sidebar
    with st.sidebar:
        st.markdown("### ⚙️ 配置状态")

        if st.session_state.llm_client:
            st.success(f"✅ LLM: {settings.llm_provider.upper()}")
            st.info(f"📦 模型: {settings.model_name}")
        else:
            st.error("❌ LLM 未配置")
            if st.session_state.config_error:
                st.warning(st.session_state.config_error)

        st.markdown("---")
        st.markdown("### 📖 使用说明")
        st.markdown("""
        1. 在输入框中描述你想要的图形
        2. 点击"生成图形"按钮
        3. AI 会将你的想法转化为数学方程并绘制

        **安全提示：**
        - 代码在沙箱环境中执行
        - 仅允许使用 numpy 和 matplotlib
        - 自动拦截危险操作
        """)

    render_examples()

    st.markdown("---")

    # Input section
    user_prompt = render_input_section()

    # Generate if user submitted
    if user_prompt:
        generate_and_render(user_prompt)

    # History section
    render_history()

    # Footer
    render_footer()


if __name__ == "__main__":
    main()
