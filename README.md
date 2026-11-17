# Foundry Digital Twin Agent

This agent is a Python classroom project that combines semiconductor design simulation, synthesis chip inspection, and an AI FoundryAssistant agent. This helps users and industry leaders to explore how design choices affect modeled performance, power, temperature, yield, cost, and manufacturing capacity. 

Customers and users can generate a simulation, examine chip images and see defects up close, and ask questions about the result. The agent calls project tools to obtain calculations and supporting notes before explaining its findings. 

## What does the Foundry Assistant Agent do?

The agent uses an OpenAI llm connected to four Python tools:
| Too | Purpose |
|--- | --- |
| `simulate_design` | Calculates the current design's modeled in metrics and constraint checks. |
| `optimize_design` | Searches candidate designs for options that satisfy the configured goals. |
| `get_inspection_summary` | Reports generated defect counts, sample information, and sampled model yield. | 
| `retrieve_notes` | Retrieves relevant project notes to support an explanation or verify defects within hardware. |

My model chooses tools based on the user's question. Python executes those tools and returns their results to the model. The agent can make additional tool calls within a configured round limit before producing its answer.

The interface displays the actual tool trace so users can see which tools ran. 

## Simulation and Inspection Features

The simulation evaluates:

- Performance in tera-operations per second (TOPS).
- Power consumption and junction temperature. 
- Die area and estimated dies per wafer.
- Modeled yield and cost per good die. 
- Manufacturing-stage capacity and bottlenecks 
- Estimated lot duration. 
- Whether the design meets its configured goals. 

The inspection component generates synthetic chip images, defect annotations, close-up views, and sample statistics. 

Display profiles use Intel 18A and a hypothetical Panther Lake / 18A-P label. These labels provide  a demonstration conext; the calculations are based on synthetic assumptions. 

## Example Questions

- "Which constraints does my current design fail?"
- "Does the design search find any feasible alternatives?"
- "Summarize the generated defects and sampled yield."
- "What is the modeled manufacturing bottleneck?"
- "Which project notes support your explanation?"

The search may find no feasible design. The agent should report that result and explain the constraints. 

## Project files
| File | Role |
|---|---|
| `app.py` | Gradio web interface and button callbacks. |
| ` foundry_twin_project.py` | Simulation, optimization, inspection generation, and agent logic. | 
| `requirements.txt` | Dependencies for the web application. |
| `README.md` | Project description and setup instructions. |
| `test_app.py` | Offline checks, including mocked agent requests. |
| `env.example` | Template for local configuration. |
| `.gitignore` | Excludes local credentials and environment files. |

`foundry_twin_project.py` and `Foundry_Twin_Project.ipynb` are the original standalone and notebook versions. 

The web application imports `foundry_core.py`. Changes made only in the original script or notebook must be transferred into that module to affect the web application. 

## Run Locally in VS code

```bash 
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy pillow matplotlib python-dotenv ipykernel
python "foundry_twin_project.py"
source .venv/bin/activate
python -m pip install -r requirements.txt 
python app.py
```





