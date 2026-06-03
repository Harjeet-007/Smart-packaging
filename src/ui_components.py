"""Reusable UI components for Streamlit dashboard"""

import streamlit as st
from typing import Dict, Tuple, Optional


def render_metric_card(
    label: str,
    value: str,
    subtext: str = "",
    color: str = "#00d4ff"
) -> None:
    """
    Render a metric card component.
    
    Args:
        label: Card label (uppercase)
        value: Main value to display
        subtext: Subtitle/subtext
        color: Color for value text
    """
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color:{color};">{value}</div>
        <div class="metric-sub">{subtext}</div>
    </div>""", unsafe_allow_html=True)


def render_status_box(
    icon: str,
    label: str,
    advice: str,
    status: str,
    color: str,
    rgb: Tuple[int, int, int],
    distance: float,
    timestamp: str
) -> None:
    """
    Render status alert box.
    
    Args:
        icon: Status icon emoji
        label: Status label text
        advice: Actionable advice
        status: Timeline status (ACTIVE/EXPIRED)
        color: Status color
        rgb: RGB values
        distance: Euclidean distance
        timestamp: Packaging timestamp
    """
    st.markdown(f"""
    <div class="status-box" style="border-color:{color}; margin-top:24px;">
        <div class="status-title" style="color:{color};">{
            icon} {label} &nbsp;·&nbsp; {status}</div>
        <p class="status-body"><strong style="color:#c8d8e8;">Actionable Insight:</strong> {advice}</p>
        <span class="status-badge">RGB Matrix: {rgb}</span>
        &nbsp;
        <span class="status-badge">Δ Distance: {distance:.2f}</span>
        &nbsp;
        <span class="status-badge">Packaged: {timestamp}</span>
    </div>""", unsafe_allow_html=True)


def render_color_patch(rgb: Tuple[int, int, int], label: str = "") -> None:
    """
    Render color preview patch.
    
    Args:
        rgb: RGB tuple
        label: Optional label text
    """
    if not label:
        label = f"RGB {rgb}"
    
    st.markdown(f"""
    <div class="color-patch" style="background:rgb{rgb};">
        {label}
    </div>""", unsafe_allow_html=True)


def render_section_label(text: str) -> None:
    """
    Render section label.
    
    Args:
        text: Label text
    """
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def render_divider() -> None:
    """
    Render horizontal divider.
    """
    st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)


def render_header(title: str, subtitle: str = "") -> None:
    """
    Render dashboard header.
    
    Args:
        title: Main title
        subtitle: Optional subtitle
    """
    st.markdown(f"""
    <div class="dash-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_footer(timestamp: str) -> None:
    """
    Render dashboard footer.
    
    Args:
        timestamp: Current timestamp
    """
    st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; font-family:'IBM Plex Mono',monospace; font-size:0.68rem; color:#1e3a5f; padding-bottom:10px;">
        BIOPOLYMER PACKAGING INTELLIGENCE SYSTEM &nbsp;·&nbsp; LAST SCAN: {timestamp}
    </div>
    """, unsafe_allow_html=True)


def render_analysis_results(analysis: Dict) -> None:
    """
    Render complete analysis results.
    
    Args:
        analysis: Dictionary from analyze_rgb()
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card(
            "Predicted pH",
            str(analysis['predicted_ph']),
            "Color-correlation model"
        )
    
    with col2:
        render_metric_card(
            "Confidence",
            f"{analysis['confidence']:.2%}",
            "Prediction reliability"
        )
    
    with col3:
        render_metric_card(
            "Distance",
            f"{analysis['distance']:.2f}",
            "Euclidean distance"
        )
    
    with col4:
        render_metric_card(
            "Status",
            analysis['freshness_icon'],
            analysis['freshness_label']
        )
