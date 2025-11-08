# Pokémon Research Team

A multi-agent AI system that demonstrates collaborative research using the AutoGen framework. Professor Oak coordinates research projects while specialized agents collect data, perform analysis, and generate comprehensive reports.

## Concept

This project showcases how AI agents can work together to tackle complex research tasks:

- **Professor Oak** (Planner): Creates research plans and coordinates the team
- **Researcher** (Worker): Collects data from PokéAPI and performs statistical analysis  
- **Reporter** (Summarizer): Synthesizes findings into comprehensive reports with visualizations

**Example Research Goal**: "Analyze all Fire-type Pokémon weaknesses and defensive capabilities"

## Want to learn MAS - Multi-Agent Systems?

This project is designed to showcase the capabilities of multi-agent systems using the AutoGen framework and to help you understand key concepts in multi-agent collaboration. If you are interested in learning more about multi-agent systems, check out the overview here: [lessons/01_overview.md](lessons/01_overview.md)

### Learning Objectives

After exploring this project, you'll understand:

1. **Multi-Agent Systems**: How to design agents with specific roles and responsibilities
2. **AutoGen Framework**: Setting up agent conversations and group chats
3. **API Integration**: Real-time data collection from external services
4. **Data Pipeline Design**: From raw data → analysis → visualization → reporting
5. **Tool Calling**: How agents can use external tools and functions
6. **Collaborative AI**: Agents working together to solve complex problems

## Technology Stack

- **Python 3.8+**: Core programming language
- **AutoGen**: Multi-agent conversation framework
- **PokéAPI**: Real-time Pokémon data source
- **Matplotlib/Seaborn**: Data visualization and charting
- **Pandas**: Data analysis and manipulation
- **Requests**: HTTP API integration

## Quick Start

### Step 1: Clone and Setup

```bash
git clone <your-repo-url>
cd pokemon-research-team

# Run the automated setup script
chmod +x setup.sh
./setup.sh

# OR manual setup:
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Run the Demo

```bash
# Activate the virtual environment if not already active
source venv/bin/activate

# Run the main application
python main.py
```

### Step 3: Choose Your Research Adventure

The interactive menu offers several options:

1. **Fire-type Analysis** - Full workflow demonstration
2. **Simple Lookup** - Quick Pokémon data retrieval
3. **Project Info** - Learn about the system architecture
4. **Exit** - End the session

## Project Structure

```
pokemon-research-team/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── setup.sh                 # Automated setup script
├── main.py                  # Main entry point
│
├── src/                     # Core source code
│   ├── agents/              # AI agent implementations
│   │   ├── research_agents.py    # Professor Oak, Researcher, Reporter
│   │   └── coordinator.py        # AutoGen group chat coordination
│   │
│   ├── tools/               # Utility tools and integrations
│   │   ├── pokemon_api.py        # PokéAPI integration
│   │   └── visualizer.py         # Data visualization tools
│   │
│   └── utils/               # Shared utilities
│
├── examples/                # Demonstration workflows
│   └── fire_type_analysis.py    # Complete Fire-type research example
│
└── data/                    # Generated outputs
    └── visualizations/      # Charts, graphs, and reports
```

## Example Workflows

### Fire-Type Weakness Analysis

This complete workflow demonstrates the full research team in action:

1. **Planning Phase**: Professor Oak creates a structured research plan
2. **Data Collection**: Researcher fetches Fire-type Pokémon data from PokéAPI
3. **Analysis**: Statistical analysis of weaknesses, stats, and patterns
4. **Visualization**: Generate charts showing weakness distributions and comparisons
5. **Reporting**: Comprehensive markdown report with insights and recommendations

**Generated Outputs**:

- Weakness distribution bar chart
- Pokémon stats comparison radar chart
- Research summary dashboard
- CSV data file for further analysis
- Professional markdown report

### Simple Pokémon Lookup

Quick demonstration of the API integration:

```python
from src.tools.pokemon_api import PokemonAPI

api = PokemonAPI()
charizard = api.get_pokemon_by_name("charizard")
print(f"{charizard.name} weaknesses: {charizard.weaknesses}")
```

## Configuration

### AutoGen Setup

**Important**: This project uses placeholder API keys for AutoGen. For full functionality:

1. Get an OpenAI API key from [OpenAI](https://openai.com/api/)
2. Set your API key as an environment variable:

    ```bash
    export OPENAI_API_KEY="your-api-key-here"
    ```

3. Update the agent configurations in `src/agents/research_agents.py`

### Offline Mode

The project can run in a limited offline mode using:

- Pre-built type effectiveness data
- Cached Pokémon information
- Static visualizations

## License

This project is for educational purposes. Pokémon data is provided by [PokéAPI](https://pokeapi.co/).
