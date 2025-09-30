import streamlit as st
import re
from pathlib import Path


def convert_admonitions(markdown_text: str) -> str:
    """
    Convert Docusaurus-style admonitions to Streamlit-compatible format
    """
    # Convert :::info blocks
    markdown_text = re.sub(
        r":::info\s+(.+?)\s+:::", r"> ℹ️ **Info**: \1", markdown_text, flags=re.DOTALL
    )

    # Convert :::warning blocks
    markdown_text = re.sub(
        r":::warning\s+(.+?)\s+:::",
        r"> ⚠️ **Warning**: \1",
        markdown_text,
        flags=re.DOTALL,
    )

    # Convert :::tip blocks
    markdown_text = re.sub(
        r":::tip\s+(.+?)\s+:::", r"> 💡 **Tip**: \1", markdown_text, flags=re.DOTALL
    )

    return markdown_text


def convert_details(markdown_text: str) -> str:
    """
    Convert HTML details/summary to markdown expandable sections
    """

    def replace_details(match):
        summary = re.search(r"<summary>(.*?)</summary>", match.group(1)).group(1)
        content = re.sub(r"<summary>.*?</summary>", "", match.group(1)).strip()
        return f"\n<details>\n<summary>{summary}</summary>\n\n{content}\n</details>\n"

    return re.sub(
        r"<details>(.*?)</details>", replace_details, markdown_text, flags=re.DOTALL
    )


def cleanup_markdown(markdown_text: str) -> str:
    """
    Clean up any remaining incompatibilities
    """
    # Remove any HTML comments
    markdown_text = re.sub(r"<!--.*?-->", "", markdown_text, flags=re.DOTALL)

    # Convert HTML tags to markdown where possible
    markdown_text = markdown_text.replace("<strong>", "**").replace("</strong>", "**")
    markdown_text = markdown_text.replace("<em>", "_").replace("</em>", "_")

    return markdown_text


def load_and_convert_markdown(file_path: str) -> str:
    """
    Load markdown file and convert it to Streamlit-compatible format
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Apply conversions
    content = convert_admonitions(content)
    content = convert_details(content)
    content = cleanup_markdown(content)

    return content


def display_markdown_content(filename: str):
    """
    Main function to display the converted markdown content
    """
    st.set_page_config(page_title="Python Course", page_icon="🐍", layout="wide")

    # Add custom CSS for better markdown rendering
    st.markdown(
        """
        <style>
        .stMarkdown {
            font-size: 1.1rem;
            line-height: 1.7;
        }
        code {
            padding: 2px 5px;
            background-color: #f6f8fa;
            border-radius: 3px;
        }
        details {
            margin: 1em 0;
            padding: 0.5em 1em;
            background-color: #f8f9fa;
            border-radius: 4px;
        }
        details summary {
            cursor: pointer;
            font-weight: bold;
        }
        blockquote {
            border-left: 3px solid #ccc;
            margin: 1em 0;
            padding-left: 1em;
            color: #666;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Load and display content
    content = load_and_convert_markdown(filename)
    st.markdown(content, unsafe_allow_html=True)
