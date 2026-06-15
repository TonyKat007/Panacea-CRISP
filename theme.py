import gradio as gr

def get_theme():
    return gr.themes.Base(
        primary_hue=gr.themes.colors.emerald,
        neutral_hue=gr.themes.colors.slate,
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "sans-serif"],
        radius_size=gr.themes.sizes.radius_lg,
    ).set(
        body_background_fill="#020617",
        body_text_color="#e2e8f0",
        block_background_fill="#0f172a",
        block_border_width="0px",
        block_label_background_fill="#0f172a",
        block_label_text_color="#94a3b8",
        input_background_fill="#1e293b",
        input_border_color="#334155",
        button_primary_background_fill="#10b981",
        button_primary_background_fill_hover="#059669",
        button_primary_text_color="#020617",
        button_primary_border_color="#34d399",
        button_secondary_background_fill="#334155",
        button_secondary_text_color="#e2e8f0",
        slider_color="#10b981",
        block_title_text_color="#10b981",
    )
