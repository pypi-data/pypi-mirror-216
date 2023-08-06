import streamlit.components.v1 as components
import streamlit as st

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "my_component",
        url="http://localhost:3001",
    )
else:
    build_dir = "./frontend/build"
    _component_func = components.declare_component("streamlit-xterm", path=build_dir)

def terminal(text, key=None):
    component_value = _component_func(text=text, key=key, default=None)
    return component_value

if not _RELEASE:
    st.subheader("Terminal Test")
    terminal(text="test")

