from pathlib import Path
import re

import matplotlib

matplotlib.use("Agg")

import gradio as gr
import foundry_twin_project as foundry

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".webp"}

def load_images():
    if not OUTPUT_DIR.is_dir():
        return [], [], (
            "No outputs folder found."
            "Run your project's image-generation code first."
        )

    image_files = sorted(
        (
            path
            for path in OUTPUT_DIR.rglob("*")
            if path.is_file()
            and path.suffix.lower() in IMAGE_TYPES
            and path.resolve().is_relative_to(OUTPUT_DIR)
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True, 

    )

    chip_images = []
    closeup_images = []

    for path in image_files:
        relative_name = str(path.relative_to(OUTPUT_DIR))
        name = relative_name.lower().replace("-","_")

        entry = (str(path), relative_name)

        if any(
            word in name
            for word in ("closeup", "close_up", "crop", "zoom")
        ):
            closeup_images.append(entry)
        else:
            chip_images.append(entry)
    if not image_files:
        return [], [], (
            "NO PNG, JPG, JPEG, or WEBP images found in outputs. "
            "Run your project's image_generation code first."

        )
    visible_chips = chip_images[:48]
    visible_closeups = closeup_images[:24]
    status = (
        f"Showing {len(visible_chips)} chip/simulation images "
        f"and {len(visible_closeups)} close-ups "
        f"from {len(image_files)} saved image files. "
        "Click a thumbnail to enlarge it."
    )
    
    return visible_chips, visible_closeups, status

# Returns the answer and the simulated chip twin.
def run_agent(question):
    if not question.strip():
        raise gr.Error("Enter a question first.")

    try:
        result = foundry.ask_foundry(
            question,
            allow_prompt=False,
        )
        answer = result["answer"]
    except (ValueError, RuntimeError) as exc:
        message = re.sub(
            r"sk-[A-Za-z0-9_-]+",
            "[REDACTED]",
            str(exc),
        )
        answer = (
            f"**AI request failed:** {message}\n\n"
            "Your saved images are still available below."
        )

    chip_images, closeups, status = load_images()

    return answer, chip_images, closeups, status
# --- CUSTOM THEME & STYLING ---
foundry_theme = gr.themes.Base(
    primary_hue="cyan",
    secondary_hue="blue",
    neutral_hue="slate", 
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui"],
    font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "monospace"],
).set(
    body_background_fill="#0b1120",
    body_background_fill_dark="#0b1120",
    block_background_fill="#111827",
    block_background_fill_dark="#111827",
    block_border_color="#1e293b",
    block_border_color_dark="#1e293b",
    block_radius="12px",
    body_text_color="#f1f5f9",
    body_text_color_dark="#f1f5f9",
    block_title_text_color="#f1f5f9",
    input_background_fill="#0f172a",
    input_background_fill_dark="#0f172a",
    input_border_color="#334155",
    input_border_color_dark="#334155",

)

custom_css = """
.gradio-container {
    max-width: 1320px !important; 
    margin: auto;
    padding-top: 24px !important;
}
.header-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
    }
    .header-box h1 {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important; 
        font-size: 2rem !iportant; 
        margin-bottom: 4px !important; 
    }
    button.primary {
        background: linear-gradient(90deg, #0284c7, #2563eb) !important;
        border: none !important;
        color: white !important; 
        font-weight: 600 !important;
        box-shadow: 0 4px 14px 0 rgba(2, 132, 199, 0.35) !important;
        transition: transform 0.1s ease-in-out !important; 
    }
    buttonprimary:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.5) !important;
    }
    .report-card {
        background-color: #111827;
        border: 1px solid #1e293b;
        border-left: 4px solid #38bdf8;
        border-radius: 12px;
        padding: 24px;
        margin-top: 16px;
    }
    .report-card table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
    }
    .report-card th {
        background-color: #1e293b !important; 
        color: #38bdf8 !important; 
    }
    .report-card td, .report-card th {
        border: 1px solid #334155 !important;
        padding: 8px 12px !important;
    }
    """

with gr.Blocks(title="Foundry Digital Twin Agent") as app:
    gr.Markdown(
        "# Foundry Digital Twin Agent\n"
        "View your simulated chip images and show defects up close, "
        "then ask the agent about your results. "

    )

    question = gr.Textbox(
        label="Ask Your Foundry Digital Twin Agent",
        placeholder=(
            "Explain the defects and sampled yield "
            "in my current simulation."
        ),
        lines=3,
    )

    with gr.Row():
        show_images_button = gr.Button(
            "Show saved images - no API call"
        )
        ask_button = gr.Button(
            "Ask AI and show images",
            variant="primary",
        )
    image_status = gr.Markdown()

    # Images appear above the AI output
    chip_gallery = gr.Gallery(
        label="Saved chip and simulation images", 
        columns=4,
        height=420,
        interactive=False,
    )

    closeup_gallery = gr.Gallery(
        label="Saved defect close-ups", 
        columns=2,
        height=420,
        interactive=False,
    )

    answer_output = gr.Markdown()

    image_outputs = [
        chip_gallery,
        closeup_gallery,
        image_status,
    ]

    # Display existing images when the page opens.
    # app.load(
    #   fn=load_images,
    #    inputs=None,
    #    outputs=image_outputs,
    #)

    show_images_button.click(
        fn=load_images,
        inputs=None,
        outputs=image_outputs,
    )

    ask_button.click(
        fn=run_agent,
        inputs=question,
        outputs=[
            answer_output,
            chip_gallery,
            closeup_gallery,
            image_status,
        ]
    )

if __name__ == "__main__":
    app.queue(default_concurrency_limit=1).launch(
        allowed_paths=[str(OUTPUT_DIR)],
        blocked_paths=[str(PROJECT_DIR / ".env")],
    )




