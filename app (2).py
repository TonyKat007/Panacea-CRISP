import gradio as gr
import os
import json
from datetime import datetime

import theme
import model
import config

# Model is lazy-loaded on first PREDICT call inside @spaces.GPU

MAX_MEASUREMENTS = 25
INITIAL_N = 4          # show 4 measurement rows on first load
EXAMPLE = config.EXAMPLE_PROFILE


# ============================================================================
# CUSTOM CSS — dark scientific aesthetic
# ============================================================================

CUSTOM_CSS = """
.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 24px !important;
}
.gradio-container, body {
    background: #020617 !important;
    color: #e2e8f0 !important;
}

/* Hero header */
.hero {
    background: linear-gradient(135deg, #064e3b 0%, #022c22 50%, #020617 100%);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 24px;
    border: 1px solid #134e4a;
}
.hero h1 {
    font-size: 38px !important;
    font-weight: 700 !important;
    margin: 0 0 6px 0 !important;
    color: #ecfdf5 !important;
    letter-spacing: -0.02em;
}
.hero .subtitle {
    color: #6ee7b7 !important;
    font-style: italic;
    font-size: 16px;
    margin-bottom: 14px;
}
.hero .description {
    color: #cbd5e1 !important;
    font-size: 14px;
    line-height: 1.6;
}
.hero a {
    color: #34d399 !important;
    text-decoration: none;
    border-bottom: 1px dashed #34d399;
}

/* Step cards — gr.Column with elem_classes renders as a visible <div>;
   force transparent backgrounds on internal Gradio wrappers so the card shows through */
.gradio-container .step-card,
div.step-card {
    background: #0a1428 !important;
    border: 1px solid #334155 !important;
    border-radius: 14px !important;
    padding: 28px !important;
    margin: 0 0 40px 0 !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
}
.step-card > .form,
.step-card > .gr-form,
.step-card > .gr-block,
.step-card > .gr-group {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
.step-label {
    font-family: inherit !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    color: #10b981 !important;
    text-transform: uppercase;
    margin-right: 10px;
}
.step-title {
    font-family: inherit !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #10b981 !important;
    margin-bottom: 22px !important;
    display: block;
    letter-spacing: 0.02em;
}
.step-hint {
    color: #94a3b8 !important;
    font-size: 12px !important;
    margin-bottom: 16px !important;
    line-height: 1.5;
}

/* Inputs */
input, textarea, select {
    background: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}
input:focus, textarea:focus {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2) !important;
}
label {
    color: #94a3b8 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase;
}

/* ── Dropdown popup (fixes transparent-overlay bug) ──────────────────────── */
[role="listbox"], .options, ul[role="listbox"], .wrap-inner ul {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.7) !important;
    z-index: 1000 !important;
    backdrop-filter: blur(8px);
}
[role="option"], li.item {
    background: transparent !important;
    color: #e2e8f0 !important;
    padding: 8px 12px !important;
    cursor: pointer !important;
}
[role="option"]:hover, li.item:hover {
    background: #334155 !important;
}
[role="option"][aria-selected="true"], li.item.selected {
    background: rgba(16, 185, 129, 0.15) !important;
    color: #6ee7b7 !important;
    font-weight: 600 !important;
}

/* ── Radio horizontal layout ─────────────────────────────────────────────── */
.gr-radio fieldset, .gr-radio .wrap, fieldset.svelte-radio {
    display: flex !important;
    flex-direction: row !important;
    gap: 12px !important;
    flex-wrap: nowrap !important;
}
.gr-radio label, fieldset.svelte-radio label {
    white-space: nowrap !important;
    font-size: 13px !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}

/* ── Measurement table header ────────────────────────────────────────────── */
.measurement-header {
    display: grid;
    grid-template-columns: 4fr 3fr 3fr;
    gap: 8px;
    padding: 0 4px 10px;
    font-family: 'JetBrains Mono', 'SF Mono', ui-monospace, monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #64748b;
    border-bottom: 1px solid #1e293b;
    margin-bottom: 12px;
}

/* Primary button */
.gr-button-primary, button.primary {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: #020617 !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 24px !important;
    font-size: 14px !important;
    text-transform: uppercase;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important;
}
.gr-button-primary:hover, button.primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4) !important;
}

/* Secondary button */
.gr-button-secondary, button.secondary {
    background: #1e293b !important;
    color: #cbd5e1 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    font-size: 12px !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase;
}

/* Question preview */
.question-box textarea {
    font-family: 'JetBrains Mono', 'SF Mono', ui-monospace, monospace !important;
    font-size: 13px !important;
    background: #0c1322 !important;
    color: #cbd5e1 !important;
    border-left: 3px solid #10b981 !important;
}

/* Chatbot */
.chatbot {
    background: #0c1322 !important;
}
.chatbot .message {
    background: #1e293b !important;
    border-radius: 10px !important;
    padding: 16px !important;
    line-height: 1.6 !important;
}

/* Clinical disclaimer footer */
.disclaimer {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.25);
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 24px;
    color: #fca5a5;
    font-size: 12px;
    text-align: center;
    letter-spacing: 0.02em;
}

footer { display: none !important; }
"""


# ============================================================================
# QUESTION BUILDER
# ============================================================================

def build_question(species, biosample, measurements, target_antibiotic):
    species = (species or "").strip() or "bacterial"
    biosample = (biosample or "").strip()
    target = (target_antibiotic or "").strip()
    if not target:
        return "Please select a target antibiotic."

    susc, resist = [], []
    for ab, pheno, mic in measurements:
        if not ab or not str(ab).strip():
            continue
        ab = str(ab).strip()
        mic = str(mic or "").strip()
        entry = f"{ab} ({mic})" if mic else ab
        if str(pheno).lower() == "susceptible":
            susc.append(entry)
        elif str(pheno).lower() == "resistant":
            resist.append(entry)

    parts = []
    if susc:
        parts.append("susceptible to " + ", ".join(susc))
    if resist:
        parts.append("resistant to " + ", ".join(resist))
    if not parts:
        profile_str = "no prior susceptibility data available"
    elif len(parts) == 1:
        profile_str = parts[0]
    else:
        profile_str = " and ".join(parts)

    if biosample:
        intro = f"You are given a {species} clinical isolate (BioSample {biosample})"
        subject = biosample
    else:
        intro = f"You are given a {species} clinical isolate"
        subject = "this isolate"

    return (
        f"{intro} tested against multiple antibiotics. "
        f"Phenotype profile: {profile_str}. "
        f"Based on the phenotype pattern across antibiotics, determine whether "
        f"the isolate is susceptible or resistant to {target}. "
        f"Provide a concise reasoning and end your answer with exactly: "
        f"'Therefore, {subject} is susceptible/resistant to {target}.'"
    )


def extract_verdict(text):
    if not text:
        return None
    cleaned = text.replace("**", "")
    sentences = [s.strip() for s in cleaned.replace("?", ".").replace("!", ".").split(".")]
    for sent in reversed(sentences):
        s = sent.lower()
        has_s = "susceptible" in s
        has_r = "resistant" in s
        if has_s and not has_r:
            return "susceptible"
        if has_r and not has_s:
            return "resistant"
    return None


# ============================================================================
# UI HELPERS
# ============================================================================

def _row_updates(new_count):
    updates = []
    for i in range(MAX_MEASUREMENTS):
        visible = i < new_count
        updates.append(gr.update(visible=visible))
        updates.append(gr.update(visible=visible))
        updates.append(gr.update(visible=visible))
    return updates


def add_measurement(count):
    new_count = min(count + 1, MAX_MEASUREMENTS)
    return [new_count] + _row_updates(new_count)


def remove_measurement(count):
    new_count = max(count - 1, 1)
    return [new_count] + _row_updates(new_count)


def load_example():
    n = len(EXAMPLE["measurements"])
    updates = [EXAMPLE["species"], "", EXAMPLE["target_antibiotic"], n]
    for i in range(MAX_MEASUREMENTS):
        if i < n:
            ab, pheno, mic = EXAMPLE["measurements"][i]
            updates += [
                gr.update(value=ab, visible=True),
                gr.update(value=pheno, visible=True),
                gr.update(value=mic, visible=True),
            ]
        else:
            updates += [
                gr.update(value=None, visible=False),
                gr.update(value="susceptible", visible=False),
                gr.update(value="", visible=False),
            ]
    return updates


def update_question_preview(species, biosample, target, *measurement_fields):
    measurements = []
    for i in range(MAX_MEASUREMENTS):
        ab = measurement_fields[i * 3]
        pheno = measurement_fields[i * 3 + 1]
        mic = measurement_fields[i * 3 + 2]
        measurements.append((ab, pheno, mic))
    return build_question(species, biosample, measurements, target)


# ============================================================================
# INFERENCE
# ============================================================================

def run_prediction(question, history):
    # Each PREDICT starts a fresh trace — no prior context, no echoed user question
    history = []

    if not question or "Please select" in question:
        history.append({"role": "assistant", "content": "⚠️ Please complete the form first."})
        yield history, gr.update(interactive=True, value="▶  Predict")
        return

    history.append({"role": "assistant", "content": "⏳ Loading model & starting generation..."})
    yield history, gr.update(interactive=False, value="●  Running")

    try:
        accumulated = ""
        for partial in model.run_inference_stream(question):
            accumulated = partial
            history[-1] = {"role": "assistant", "content": accumulated}
            yield history, gr.update(interactive=False, value="●  Running")
    except Exception as e:
        accumulated = f"**Error during inference:** `{e}`"
        history[-1] = {"role": "assistant", "content": accumulated}

    # Final pass: add verdict banner
    verdict = extract_verdict(accumulated)
    if verdict:
        verdict_color = "🟢" if verdict == "susceptible" else "🔴"
        banner = f"\n\n---\n\n## {verdict_color} Final Verdict: **{verdict.upper()}**"
        history[-1] = {"role": "assistant", "content": accumulated + banner}
    else:
        history[-1] = {
            "role": "assistant",
            "content": accumulated + "\n\n---\n\n*(verdict could not be extracted automatically)*",
        }

    yield history, gr.update(interactive=True, value="▶  Predict")


def export_result(history, question):
    if not history:
        return None
    last = history[-1]
    if not isinstance(last, dict):
        return None
    reasoning = last.get("content", "")
    verdict = extract_verdict(reasoning)
    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "model": model.MODEL_ID,
        "question": question,
        "reasoning_trace": reasoning,
        "predicted_label": verdict,
    }
    os.makedirs("tmp", exist_ok=True)
    out_path = "tmp/prediction.json"
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return out_path


# ============================================================================
# UI
# ============================================================================

with gr.Blocks(title="BacteReason") as demo:

    measurement_count = gr.State(INITIAL_N)

    # Hero header
    gr.HTML("""
        <div class="hero">
            <h1>🦠 BacteReason</h1>
            <div class="description">
                BacteReason is a fine-tuned <b>QwQ-32B</b> that predicts whether a bacterial isolate
                is susceptible or resistant to a target antibiotic, while explaining the underlying
                molecular mechanism. It was distilled from reasoning traces generated by
                <b>Claude Opus 4.5</b> + <a href="https://togomcp.rdfportal.org/">TogoMCP</a>
                (UniProt, ChEMBL, GO, PDB, etc).
                See the <a href="https://huggingface.co/Playingyoyo/BacteReason">model weights</a>.
                Like all AI models, BacteReason can hallucinate — predictions are for research only.
            </div>
        </div>
    """)

    with gr.Row():

        # ── LEFT: input form ─────────────────────────────────────────────────
        with gr.Column(scale=4):

            with gr.Column(elem_classes="step-card"):
                gr.HTML('<div class="step-title"><span class="step-label">STEP 01 //</span>Species</div>')
                species = gr.Dropdown(
                    label=None, show_label=False,
                    choices=config.SPECIES_LIST,
                    value=EXAMPLE["species"], allow_custom_value=True,
                    container=False,
                )
                # Hidden — never shown in UI; empty default keeps the question phrasing
                # clean ("...clinical isolate tested against..." instead of "(BioSample X)...").
                biosample = gr.Textbox(value="", visible=False)

            with gr.Column(elem_classes="step-card"):
                gr.HTML('<div class="step-title"><span class="step-label">STEP 02 //</span>Phenotype profile</div>')

                gr.HTML(
                    '<div class="measurement-header">'
                    '<div>Antibiotic</div><div>Result</div><div>MIC (optional)</div>'
                    '</div>'
                )

                m_antibiotics, m_phenotypes, m_mics = [], [], []
                example_n = INITIAL_N
                for i in range(MAX_MEASUREMENTS):
                    visible = i < example_n
                    if visible and i < len(EXAMPLE["measurements"]):
                        ab_val, pheno_val, mic_val = EXAMPLE["measurements"][i]
                    else:
                        ab_val, pheno_val, mic_val = None, "susceptible", ""

                    with gr.Row():
                        ab = gr.Dropdown(
                            choices=config.ANTIBIOTIC_LIST, value=ab_val,
                            allow_custom_value=True, show_label=False,
                            container=False, scale=4, visible=visible,
                        )
                        pheno = gr.Radio(
                            choices=["susceptible", "resistant"], value=pheno_val,
                            show_label=False, container=False, scale=3, visible=visible,
                        )
                        mic = gr.Textbox(
                            value=mic_val, placeholder="MIC",
                            show_label=False, container=False, scale=3, visible=visible,
                        )
                    m_antibiotics.append(ab)
                    m_phenotypes.append(pheno)
                    m_mics.append(mic)

                with gr.Row():
                    add_btn = gr.Button("+ Add measurement", variant="secondary", size="sm")
                    remove_btn = gr.Button("− Remove last", variant="secondary", size="sm")

            with gr.Column(elem_classes="step-card"):
                gr.HTML('<div class="step-title"><span class="step-label">STEP 03 //</span>Target antibiotic</div>')
                target = gr.Dropdown(
                    label=None, show_label=False,
                    choices=config.ANTIBIOTIC_LIST,
                    value=EXAMPLE["target_antibiotic"],
                    allow_custom_value=True,
                    container=False,
                )

            example_btn = gr.Button("📋  Load demo example", variant="secondary")

        # ── RIGHT: question preview + output ─────────────────────────────────
        with gr.Column(scale=6):

            with gr.Column(elem_classes="step-card"):
                gr.HTML('<div class="step-title"><span class="step-label">STEP 04 //</span>Submit question</div>')

                question_box = gr.Textbox(
                    label="Auto-built question (editable)",
                    value=build_question(
                        EXAMPLE["species"], "",
                        EXAMPLE["measurements"][:INITIAL_N], EXAMPLE["target_antibiotic"],
                    ),
                    lines=6, interactive=True,
                    elem_classes="question-box",
                )

                run_btn = gr.Button("▶  Predict", variant="primary", size="lg")

                chatbot = gr.Chatbot(
                    show_label=False, height=640, layout="panel",
                    value=[], elem_classes="chatbot",
                )

                download_btn = gr.DownloadButton(
                    "📥  Download result (JSON)",
                    size="sm",
                )

    # ── EVENTS ────────────────────────────────────────────────────────────────
    measurement_components = []
    for ab, pheno, mic in zip(m_antibiotics, m_phenotypes, m_mics):
        measurement_components.extend([ab, pheno, mic])

    add_btn.click(
        add_measurement, inputs=measurement_count,
        outputs=[measurement_count] + measurement_components, api_name=False,
    )
    remove_btn.click(
        remove_measurement, inputs=measurement_count,
        outputs=[measurement_count] + measurement_components, api_name=False,
    )

    all_form_inputs = [species, biosample, target] + measurement_components
    for inp in all_form_inputs:
        inp.change(
            update_question_preview, inputs=all_form_inputs,
            outputs=question_box, show_progress="hidden", api_name=False,
        )

    example_btn.click(
        load_example,
        outputs=[species, biosample, target, measurement_count] + measurement_components,
        api_name=False,
    )

    run_btn.click(
        run_prediction, inputs=[question_box, chatbot],
        outputs=[chatbot, run_btn], api_name=False,
    )

    def _update_download(history, question):
        path = export_result(history, question)
        if path and os.path.exists(path):
            return gr.DownloadButton(value=path, visible=True)
        return gr.DownloadButton(value=None, visible=True)

    chatbot.change(
        _update_download, inputs=[chatbot, question_box],
        outputs=download_btn, api_name=False,
    )


if __name__ == "__main__":
    demo.launch(theme=theme.get_theme(), css=CUSTOM_CSS)