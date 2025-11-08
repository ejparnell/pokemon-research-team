# Lesson 4: Integrating Data and Visualization

So, we have our command center/brains (agents) ready to go; now it's time to give them the tools to gather and visualize data, just like true Pokémon Professors! Let's channel our inner Professor Oak or a data-driven Nurse Joy and get down to business.

By the end of this lesson, you'll have:

- Built a robust PokéAPI integration system
- Created a comprehensive data visualization toolkit
- Connected these tools to your AI agents
- Learned how to make agents work with external APIs and data sources

## Understanding the Data Flow Architecture

Before we start coding, let's understand how all the pieces fit together:

```
User Request → Professor Oak → Researcher Agent → PokéAPI → Data Processing → Visualizer → Reporter Agent → Final Report
```

There are many moving parts, but never fear - we have a guide here.

### The Component Breakdown

1. **PokéAPI Integration** (`pokemon_api.py`): Fetches real Pokémon data from the internet
2. **Data Visualizer** (`visualizer.py`): Creates charts and graphs from the data
3. **Agent Integration**: How our agents use these tools to conduct research
4. **Complete Workflow**: Putting it all together for end-to-end research

## Step 1: Setting Up the Tools Directory

First, let's make sure we have the proper structure for our tools:

```bash
# Navigate to your project directory
cd pokemon-research-team

# Create the tools directory if it doesn't exist
mkdir -p src/tools
touch src/tools/__init__.py
```

This creates a proper Python package structure for our data tools.

## Step 2: Building the PokéAPI Integration

Now let's build our connection to the real world of Pokémon data! We'll create this step by step, understanding each piece as we go.

### Starting with Imports and Data Structures

Create `src/tools/pokemon_api.py` and let's begin with the foundation:

```python
"""
PokéAPI integration utilities for fetching Pokémon data.
"""
import requests
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
```

**Why These Imports?**

- `requests`: The gold standard for making HTTP API calls in Python
- `json`: For parsing API responses (though `requests` handles most of this)
- `typing`: Makes our code more reliable with type hints
- `dataclasses`: Creates clean, structured data objects

### Creating the Pokémon Data Structure

Next, let's define what a Pokémon looks like in our system:

```python
@dataclass
class PokemonStats:
    """Data class for Pokémon stats."""
 name: str
 types: List[str]
 hp: int
 attack: int
 defense: int
 special_attack: int
 special_defense: int
 speed: int
 weaknesses: List[str]
 resistances: List[str]
```

**Why Use a Dataclass?**

- Automatically creates `__init__`, `__repr__`, and other methods
- Makes the code more readable and maintainable
- Provides type safety for our Pokémon data
- Easy to pass between functions and agents

### Building the Core API Class

Now let's create the main class that handles all our PokéAPI interactions:

```python
class PokemonAPI:
    """Class for interacting with the PokéAPI."""
    
 BASE_URL = "https://pokeapi.co/api/v2"
    
    def __init__(self):
        self.session = requests.Session()
        self.type_effectiveness = self._load_type_effectiveness()
```

**Key Design Decisions:**

- `requests.Session()`: Reuses connections for better performance
- `BASE_URL`: Central configuration for the API endpoint
- `type_effectiveness`: Preloaded data for calculating weaknesses/resistances

### Implementing Type Effectiveness Logic

The type system is crucial for analyzing Pokémon battles. Let's build this systematically:

```python
    def _load_type_effectiveness(self) -> Dict:
        """Load type effectiveness chart from PokéAPI."""
        try:
 response = self.session.get(f"{self.BASE_URL}/type")
            if response.status_code == 200:
                # For now, we'll use a simplified type effectiveness chart
                # In a full implementation, we'd fetch and parse all type data
                return self._get_simplified_type_chart()
        except requests.RequestException:
            pass
        return self._get_simplified_type_chart()
```

**Why This Approach?**

- Tries to fetch live data first (future enhancement)
- Falls back to a local chart for reliability
- Handles network errors gracefully
- Easy to extend for full API integration later

### Creating the Type Effectiveness Chart

Now let's implement the core type matchup data:

```python
    def _get_simplified_type_chart(self) -> Dict:
        """Simplified type effectiveness chart."""
        return {
            "fire": {
                "weaknesses": ["water", "ground", "rock"],
                "resistances": ["fire", "grass", "ice", "bug", "steel", "fairy"]
 },
            "water": {
                "weaknesses": ["electric", "grass"],
                "resistances": ["fire", "water", "ice", "steel"]
 },
            "grass": {
                "weaknesses": ["fire", "ice", "poison", "flying", "bug"],
                "resistances": ["water", "electric", "grass", "ground"]
 },
            "electric": {
                "weaknesses": ["ground"],
                "resistances": ["electric", "flying", "steel"]
 },
            # Continue adding all 18 types...
```

**Pro Tip**: I'm showing an abbreviated version here. In your actual file, you'll want to include all 18 Pokémon types. This data structure enables easy calculation of type matchups for any Pokémon.

### Fetching Individual Pokémon Data

Let's build the core function that fetches a single Pokémon's information:

```python
    def get_pokemon_by_name(self, name: str) -> Optional[PokemonStats]:
        """Fetch Pokémon data by name."""
        try:
 response = self.session.get(f"{self.BASE_URL}/pokemon/{name.lower()}")
            if response.status_code == 200:
 data = response.json()
                return self._parse_pokemon_data(data)
        except requests.RequestException as e:
            print(f"Error fetching Pokémon {name}: {e}")
        return None
```

**Error Handling Strategy:**

- Uses `try/except` for network issues
- Returns `None` on failure (easy to check)
- Logs errors for debugging
- Handles case-insensitive names

### Parsing the API Response

The PokéAPI returns complex nested JSON. Let's parse it into our clean structure:

```python
    def _parse_pokemon_data(self, data: Dict) -> PokemonStats:
        """Parse Pokémon data from API response."""
 name = data['name']
 types = [t['type']['name'] for t in data['types']]
        
        # Parse stats
 stats = {}
        for stat in data['stats']:
 stat_name = stat['stat']['name'].replace('-', '_')
 stats[stat_name] = stat['base_stat']
        
        # Calculate type effectiveness
 weaknesses = set()
 resistances = set()
        
        for ptype in types:
            if ptype in self.type_effectiveness:
 weaknesses.update(self.type_effectiveness[ptype]['weaknesses'])
 resistances.update(self.type_effectiveness[ptype]['resistances'])
        
        # Remove resistances from weaknesses (dual-type logic)
 weaknesses = list(weaknesses - resistances)
        
        return PokemonStats(
            name=name,
            types=types,
            hp=stats.get('hp', 0),
            attack=stats.get('attack', 0),
            defense=stats.get('defense', 0),
            special_attack=stats.get('special_attack', 0),
            special_defense=stats.get('special_defense', 0),
            speed=stats.get('speed', 0),
            weaknesses=weaknesses,
            resistances=list(resistances)
 )
```

**Key Logic Points:**

- Handles stat name formatting (API uses hyphens, Python prefers underscores)
- Calculates dual-type interactions correctly
- Uses sets for efficient weakness/resistance calculations
- Provides default values to prevent crashes

### Fetching Pokémon by Type

Let's add functionality to get all Pokémon of a specific type:

```python
    def get_pokemon_by_type(self, pokemon_type: str) -> List[str]:
        """Get list of Pokémon names by type."""
        try:
 response = self.session.get(f"{self.BASE_URL}/type/{pokemon_type.lower()}")
            if response.status_code == 200:
 data = response.json()
                return [pokemon['pokemon']['name'] for pokemon in data['pokemon']]
        except requests.RequestException as e:
            print(f"Error fetching type {pokemon_type}: {e}")
        return []
```

### Adding Analysis Capabilities

Now let's create a powerful analysis function that our agents can use:

```python
    def analyze_type_weaknesses(self, pokemon_type: str) -> Dict:
        """Analyze common weaknesses for a Pokémon type."""
 pokemon_names = self.get_pokemon_by_type(pokemon_type)
        
        # Sample a few Pokémon for analysis (to avoid hitting API limits)
 sample_size = min(10, len(pokemon_names))
 sample_pokemon = pokemon_names[:sample_size]
        
 weakness_count = {}
 total_pokemon = 0
        
        for name in sample_pokemon:
 pokemon = self.get_pokemon_by_name(name)
            if pokemon:
 total_pokemon += 1
                for weakness in pokemon.weaknesses:
 weakness_count[weakness] = weakness_count.get(weakness, 0) + 1
        
        # Calculate percentages
 weakness_percentages = {}
        for weakness, count in weakness_count.items():
 weakness_percentages[weakness] = (count / total_pokemon) * 100
        
        return {
            'type': pokemon_type,
            'analyzed_pokemon_count': total_pokemon,
            'weakness_percentages': weakness_percentages,
            'most_common_weakness': max(weakness_percentages.items(), key=lambda x: x[1]) if weakness_percentages else None
 }
```

**Why This Analysis Function is Powerful:**

- Respects API rate limits by sampling
- Provides statistical analysis, not just raw data
- Returns structured results perfect for visualization
- Handles edge cases (empty results, API failures)

## Step 3: Building the Visualization System

Now let's create beautiful charts and graphs! Create `src/tools/visualizer.py`:

### Setting Up the Visualization Imports

```python
"""
Visualization tools for Pokémon research data.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path
```

**Visualization Stack Explanation:**

- `matplotlib`: The foundation of Python plotting
- `seaborn`: Makes matplotlib beautiful and easier to use
- `pandas`: Handles data manipulation and CSV export
- `numpy`: Mathematical operations and array handling
- `pathlib`: Modern, cross-platform file path handling

### Creating the Visualizer Class Foundation

```python
class PokemonDataVisualizer:
    """Creates charts and graphs for Pokémon research data."""
    
    def __init__(self, output_dir: str = "data/visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up plotting style
 plt.style.use('seaborn-v0_8')
 sns.set_palette("husl")
```

**Design Choices:**

- Auto-creates output directory for organized file management
- Sets consistent visual styling across all charts
- Uses seaborn's modern color palette for attractive charts

### Building the Weakness Distribution Chart

This is the core visualization our agents will use most:

```python
    def plot_weakness_distribution(self, weakness_data: Dict[str, float], 
                                 pokemon_type: str, 
                                 save_path: Optional[str] = None) -> str:
        """Create a bar chart showing weakness distribution."""
 fig, ax = plt.subplots(figsize=(12, 8))
        
        # Sort weaknesses by percentage
 sorted_weaknesses = sorted(weakness_data.items(), 
                                 key=lambda x: x[1], reverse=True)
        
 weakness_types = [w[0].title() for w in sorted_weaknesses]
 percentages = [w[1] for w in sorted_weaknesses]
        
        # Create bar plot
 bars = ax.bar(weakness_types, percentages, 
                     color=sns.color_palette("husl", len(weakness_types)))
        
        # Customize the plot
 ax.set_title(f'{pokemon_type.title()}-type Pokémon Weakness Distribution', 
                    fontsize=16, fontweight='bold')
 ax.set_xlabel('Weakness Types', fontsize=12)
 ax.set_ylabel('Percentage of Pokémon Affected (%)', fontsize=12)
 ax.set_ylim(0, max(percentages) * 1.1)
        
        # Add percentage labels on bars
        for bar, percentage in zip(bars, percentages):
 height = bar.get_height()
 ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{percentage:.1f}%', ha='center', va='bottom', fontsize=10)
        
        # Rotate x-axis labels for better readability
 plt.xticks(rotation=45, ha='right')
 plt.tight_layout()
        
        # Save the plot
        if save_path is None:
 save_path = self.output_dir / f"{pokemon_type}_weakness_distribution.png"
        
 plt.savefig(save_path, dpi=300, bbox_inches='tight')
 plt.close()  # Important: prevents memory leaks!
        
        return str(save_path)
```

**Chart Features Explained:**

- **Sorting**: Shows most common weaknesses first
- **Color coding**: Each weakness type gets a distinct color
- **Data labels**: Exact percentages displayed on bars
- **Professional styling**: Publication-ready appearance
- **Auto-saving**: Returns path for agent reference

### Creating Radar Charts for Stats Comparison

Let's build a spectacular radar chart for comparing Pokémon stats:

```python
    def plot_stats_comparison(self, pokemon_stats: List[Dict[str, Any]], 
                            title: str = "Pokémon Stats Comparison",
                            save_path: Optional[str] = None) -> str:
        """Create a radar chart comparing Pokémon stats."""
        # Convert to DataFrame
 df = pd.DataFrame(pokemon_stats)
        
        # Select numeric stats columns
 stat_columns = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed']
 available_stats = [col for col in stat_columns if col in df.columns]
        
        if not available_stats:
            raise ValueError("No stat columns found in the data")
        
        # Create radar chart
 fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Calculate angles for each stat
 angles = np.linspace(0, 2 * np.pi, len(available_stats), endpoint=False)
 angles = np.concatenate((angles, [angles[0]]))  # Complete the circle
        
        # Plot each Pokémon (limit to first 5 for clarity)
 colors = sns.color_palette("husl", min(5, len(df)))
        
        for i, (_, pokemon) in enumerate(df.head(5).iterrows()):
 values = [pokemon[stat] for stat in available_stats]
 values += [values[0]]  # Complete the circle
            
 ax.plot(angles, values, 'o-', linewidth=2, 
                   label=pokemon.get('name', f'Pokémon {i+1}'), 
                   color=colors[i])
 ax.fill(angles, values, alpha=0.25, color=colors[i])
        
        # Customize the plot
 ax.set_xticks(angles[:-1])
 ax.set_xticklabels([stat.replace('_', ' ').title() for stat in available_stats])
 ax.set_ylim(0, max([df[stat].max() for stat in available_stats]) * 1.1)
 ax.set_title(title, size=16, fontweight='bold', pad=20)
 ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
        
 plt.tight_layout()
        
        # Save the plot
        if save_path is None:
 save_path = self.output_dir / f"{title.lower().replace(' ', '_')}.png"
        
 plt.savefig(save_path, dpi=300, bbox_inches='tight')
 plt.close()
        
        return str(save_path)
```

**Radar Chart Magic:**

- **Polar projection**: Creates the circular radar appearance
- **Multi-layered**: Shows up to 5 Pokémon simultaneously
- **Filled areas**: Semi-transparent fills show stat distributions
- **Dynamic scaling**: Adjusts to the data range automatically

### Adding Comprehensive Summary Charts

Let's create a dashboard-style summary chart:

```python
    def create_research_summary_chart(self, research_data: Dict[str, Any],
                                    save_path: Optional[str] = None) -> str:
        """Create a comprehensive summary chart of research findings."""
 fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Chart 1: Weakness Distribution (if available)
        if 'weakness_analysis' in research_data:
 weakness_data = research_data['weakness_analysis']
            if 'weakness_percentages' in weakness_data:
 weaknesses = list(weakness_data['weakness_percentages'].keys())[:6]
 percentages = [weakness_data['weakness_percentages'][w] for w in weaknesses]
                
 ax1.bar(range(len(weaknesses)), percentages)
 ax1.set_xticks(range(len(weaknesses)))
 ax1.set_xticklabels([w.title() for w in weaknesses], rotation=45)
 ax1.set_title('Top Weaknesses', fontweight='bold')
 ax1.set_ylabel('Percentage (%)')
        
        # Chart 2: Sample stats if available
        if 'pokemon_stats' in research_data:
 stats_data = research_data['pokemon_stats'][:3]  # First 3 Pokémon
 pokemon_names = [p.get('name', f'Pokemon {i+1}') for i, p in enumerate(stats_data)]
 attack_stats = [p.get('attack', 0) for p in stats_data]
            
 ax2.bar(pokemon_names, attack_stats)
 ax2.set_title('Attack Stats Comparison', fontweight='bold')
 ax2.set_ylabel('Attack Stat')
 ax2.tick_params(axis='x', rotation=45)
        
        # Chart 3 & 4: Placeholder charts for additional analysis
 ax3.text(0.5, 0.5, 'Additional Analysis\n(Future Enhancement)', 
                ha='center', va='center', fontsize=14)
 ax3.set_title('Analysis Placeholder', fontweight='bold')
        
 ax4.text(0.5, 0.5, 'Strategic Insights\n(Future Enhancement)', 
                ha='center', va='center', fontsize=14)
 ax4.set_title('Insights Placeholder', fontweight='bold')
        
 plt.suptitle('Pokémon Research Summary', fontsize=18, fontweight='bold')
 plt.tight_layout()
        
        # Save the plot
        if save_path is None:
 save_path = self.output_dir / "research_summary.png"
        
 plt.savefig(save_path, dpi=300, bbox_inches='tight')
 plt.close()
        
        return str(save_path)
```

### Adding Data Export Functionality

Let's include CSV export for further analysis:

```python
    def save_data_to_csv(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Save research data to CSV file."""
 df = pd.DataFrame(data)
 csv_path = self.output_dir / f"{filename}.csv"
 df.to_csv(csv_path, index=False)
        return str(csv_path)
```

## Step 4: Connecting Tools to Agents

Now comes the exciting part - making our agents smart enough to use these tools! Let's update our agents to integrate with the data systems.

### Updating the Researcher Agent

First, let's modify `src/agents/research_agents.py` to import and use our new tools. Add these imports at the top:

```python
# Add these imports to the existing ones
from typing import Dict, List, Any, Optional
import sys
import os

# Add the tools directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))

try:
    from pokemon_api import PokemonAPI, PokemonStats
    from visualizer import PokemonDataVisualizer
except ImportError as e:
    print(f"Warning: Could not import tools: {e}")
 PokemonAPI = None
 PokemonDataVisualizer = None
```

### Enhancing the Researcher Agent with Real Tools

Now let's upgrade the ResearcherAgent class:

```python
class ResearcherAgent(AssistantAgent):
    """
 Researcher Agent - Performs data collection and analysis.
 """

    def __init__(self, name: str = "Researcher"):
        # ... existing system_message and super().__init__() code ...
        
        # Initialize tools
        self.pokemon_api = PokemonAPI() if PokemonAPI else None
        self.visualizer = PokemonDataVisualizer() if PokemonDataVisualizer else None
        
    def collect_pokemon_data(self, pokemon_type: str) -> Dict[str, Any]:
        """Collect comprehensive data about a Pokémon type."""
        if not self.pokemon_api:
            return {"error": "PokemonAPI not available"}
        
        print(f"🔬 Collecting data for {pokemon_type}-type Pokémon...")
        
        # Get weakness analysis
 weakness_analysis = self.pokemon_api.analyze_type_weaknesses(pokemon_type)
        
        # Get sample Pokémon for detailed stats
 pokemon_names = self.pokemon_api.get_pokemon_by_type(pokemon_type)[:5]
 pokemon_stats = []
        
        for name in pokemon_names:
 pokemon = self.pokemon_api.get_pokemon_by_name(name)
            if pokemon:
 pokemon_stats.append({
                    'name': pokemon.name,
                    'hp': pokemon.hp,
                    'attack': pokemon.attack,
                    'defense': pokemon.defense,
                    'special_attack': pokemon.special_attack,
                    'special_defense': pokemon.special_defense,
                    'speed': pokemon.speed,
                    'types': pokemon.types,
                    'weaknesses': pokemon.weaknesses
 })
        
        return {
            'weakness_analysis': weakness_analysis,
            'pokemon_stats': pokemon_stats,
            'collection_summary': {
                'type_analyzed': pokemon_type,
                'total_pokemon_found': len(pokemon_names),
                'detailed_stats_collected': len(pokemon_stats)
 }
 }
    
    def create_visualizations(self, research_data: Dict[str, Any]) -> List[str]:
        """Create visualizations from research data."""
        if not self.visualizer:
            return ["Visualizer not available"]
        
 created_files = []
        
        # Create weakness distribution chart
        if 'weakness_analysis' in research_data:
 weakness_data = research_data['weakness_analysis']
            if 'weakness_percentages' in weakness_data:
 chart_path = self.visualizer.plot_weakness_distribution(
 weakness_data['weakness_percentages'],
 weakness_data['type']
 )
 created_files.append(chart_path)
        
        # Create stats comparison chart
        if 'pokemon_stats' in research_data and research_data['pokemon_stats']:
 stats_path = self.visualizer.plot_stats_comparison(
 research_data['pokemon_stats'],
                f"{research_data.get('collection_summary', {}).get('type_analyzed', 'Pokemon')} Stats Comparison"
 )
 created_files.append(stats_path)
        
        # Create summary dashboard
 summary_path = self.visualizer.create_research_summary_chart(research_data)
 created_files.append(summary_path)
        
        return created_files
```

### Updating Professor Oak for Better Coordination

Let's enhance Professor Oak to create more specific research plans:

```python
class ProfessorOakAgent(AssistantAgent):
    # ... existing __init__ code ...
    
    def create_detailed_research_plan(self, research_goal: str) -> Dict[str, Any]:
        """Create a detailed research plan with specific tool usage."""
        
        # Analyze the research goal to determine approach
 goal_lower = research_goal.lower()
        
        if any(ptype in goal_lower for ptype in ['fire', 'water', 'grass', 'electric', 'psychic']):
            # Type-specific analysis
 pokemon_type = None
            for ptype in ['fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon', 'dark', 'fairy', 'normal', 'fighting', 'poison', 'ground', 'flying', 'bug', 'rock', 'ghost', 'steel']:
                if ptype in goal_lower:
 pokemon_type = ptype
                    break
            
            return {
                "research_type": "type_analysis",
                "target_type": pokemon_type,
                "methodology": [
                    f"Use PokemonAPI.analyze_type_weaknesses('{pokemon_type}') for statistical analysis",
                    f"Collect detailed stats from sample {pokemon_type}-type Pokémon",
                    "Create weakness distribution visualization",
                    "Generate comparative stats charts",
                    "Produce comprehensive research summary"
 ],
                "expected_outputs": [
                    f"{pokemon_type}_weakness_distribution.png",
                    f"{pokemon_type}_stats_comparison.png",
                    "research_summary.png",
                    "research_data.csv"
 ],
                "tools_required": ["PokemonAPI", "PokemonDataVisualizer"],
                "success_metrics": [
                    "At least 5 Pokémon analyzed",
                    "Statistical significance in weakness patterns",
                    "Clear visual representations created",
                    "Actionable strategic insights generated"
 ]
 }
        
        # Generic research plan for other requests
        return {
            "research_type": "general_analysis", 
            "methodology": ["Analyze request", "Collect relevant data", "Generate insights"],
            "tools_required": ["PokemonAPI", "PokemonDataVisualizer"]
 }
```

## Step 6: Understanding Agent-Tool Communication Patterns

### How Agents Call Tools

There are several patterns for agents to use external tools:

#### Pattern 1: Direct Method Calls

```python
# In agent methods
def perform_research(self, pokemon_type: str):
 data = self.pokemon_api.analyze_type_weaknesses(pokemon_type)
 charts = self.visualizer.plot_weakness_distribution(data['weakness_percentages'], pokemon_type)
    return {"data": data, "visualizations": charts}
```

#### Pattern 2: Tool Registry Pattern

```python
class ResearcherAgent(AssistantAgent):
    def __init__(self):
        # ... existing code ...
        self.tools = {
            "api": PokemonAPI(),
            "viz": PokemonDataVisualizer(),
            "calculator": StatisticsCalculator()
 }
    
    def execute_task(self, task_type: str, parameters: Dict):
        if task_type == "weakness_analysis":
            return self.tools["api"].analyze_type_weaknesses(parameters["type"])
        elif task_type == "create_chart":
            return self.tools["viz"].plot_weakness_distribution(**parameters)
```

#### Pattern 3: Function Calling (Advanced)

```python
# Using AutoGen's function calling capabilities
def get_pokemon_weakness_data(pokemon_type: str) -> Dict:
    """Get weakness analysis for a Pokemon type."""
 api = PokemonAPI()
    return api.analyze_type_weaknesses(pokemon_type)

# Register function with agent
researcher.register_function(
    function_map={"get_pokemon_weakness_data": get_pokemon_weakness_data}
)
```

## Step 7: Error Handling and Robustness

### API Error Handling

Make your system resilient to network issues:

```python
class RobustPokemonAPI(PokemonAPI):
    def __init__(self, retry_count: int = 3):
        super().__init__()
        self.retry_count = retry_count
    
    def get_pokemon_by_name_with_retry(self, name: str) -> Optional[PokemonStats]:
        """Fetch Pokémon with retry logic."""
        for attempt in range(self.retry_count):
            try:
 result = self.get_pokemon_by_name(name)
                if result:
                    return result
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.retry_count - 1:
                    print(f"All attempts failed for {name}")
        return None
```

### Graceful Degradation

Handle missing tools elegantly:

```python
class AdaptiveResearcherAgent(ResearcherAgent):
    def perform_analysis(self, pokemon_type: str):
 results = {}
        
        # Try to use API data
        if self.pokemon_api:
 results["live_data"] = self.pokemon_api.analyze_type_weaknesses(pokemon_type)
        else:
 results["live_data"] = self._get_fallback_data(pokemon_type)
        
        # Try to create visualizations
        if self.visualizer and "live_data" in results:
 results["charts"] = self.create_visualizations(results)
        else:
 results["charts"] = "Visualization unavailable - data provided in text format"
        
        return results
```

## Step 8: Advanced Integration Techniques

### Streaming Data Processing

For large datasets, implement streaming:

```python
def stream_pokemon_analysis(self, pokemon_type: str):
    """Process Pokémon data in streams for large datasets."""
 pokemon_names = self.pokemon_api.get_pokemon_by_type(pokemon_type)
    
 batch_size = 5
 results = []
    
    for i in range(0, len(pokemon_names), batch_size):
 batch = pokemon_names[i:i+batch_size]
 batch_results = []
        
        for name in batch:
 pokemon = self.pokemon_api.get_pokemon_by_name(name)
            if pokemon:
 batch_results.append(pokemon)
        
 results.extend(batch_results)
        
        # Yield intermediate results
        yield {
            "batch": i // batch_size + 1,
            "total_batches": len(pokemon_names) // batch_size + 1,
            "current_results": batch_results,
            "cumulative_count": len(results)
 }
```

### Caching for Performance

Implement intelligent caching:

```python
import pickle
from pathlib import Path

class CachedPokemonAPI(PokemonAPI):
    def __init__(self, cache_dir: str = "data/cache"):
        super().__init__()
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_pokemon_by_name(self, name: str) -> Optional[PokemonStats]:
        # Check cache first
 cache_file = self.cache_dir / f"{name}.pkl"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                pass  # Cache corrupted, fetch fresh
        
        # Fetch from API
 pokemon = super().get_pokemon_by_name(name)
        
        # Cache the result
        if pokemon:
            try:
                with open(cache_file, 'wb') as f:
 pickle.dump(pokemon, f)
            except Exception:
                pass  # Caching failed, but we have the data
        
        return pokemon
```

## Step 9: Putting It All Together - Complete Workflow

Let's create a complete example that shows the entire data flow:

```python
"""
Complete workflow example: From question to visualization
"""

def complete_research_workflow(research_question: str):
    """Demonstrate the complete research workflow."""
    print(f"🎯 Research Question: {research_question}")
    
    # Step 1: Professor Oak creates a plan
 oak = ProfessorOakAgent()
 plan = oak.create_detailed_research_plan(research_question)
    print(f"📋 Research Plan Created: {plan['research_type']}")
    
    # Step 2: Researcher executes the plan
 researcher = ResearcherAgent()
    
    if plan['research_type'] == 'type_analysis':
 pokemon_type = plan['target_type']
 data = researcher.collect_pokemon_data(pokemon_type)
 visualizations = researcher.create_visualizations(data)
        
        print(f"📊 Data Collection Complete:")
        print(f"   - Analyzed {data['collection_summary']['detailed_stats_collected']} Pokémon")
        print(f"   - Created {len(visualizations)} visualizations")
        
        # Step 3: Reporter creates summary
 reporter = ReporterAgent()
 report = reporter.generate_report(data)
        
        return {
            "plan": plan,
            "data": data,
            "visualizations": visualizations,
            "report": report
 }

# Example usage
if __name__ == "__main__":
 results = complete_research_workflow("analyze Fire-type Pokémon weaknesses")
    print("✨ Complete workflow executed successfully!")
```

## Key Architectural Insights

### Why This Design Works

1. **Separation of Concerns**:
   - `pokemon_api.py`: Pure data fetching and processing
   - `visualizer.py`: Pure visualization logic
   - Agents: Orchestration and decision making

2. **Modularity**: Each component can be tested and developed independently

3. **Error Resilience**: Multiple fallback strategies ensure the system keeps working

4. **Extensibility**: Easy to add new data sources or visualization types

### Best Practices

- **Type Hints**: Makes code self-documenting and prevents bugs
- **Dataclasses**: Clean, structured data representation
- **Path Handling**: Cross-platform file operations
- **Resource Management**: Proper cleanup of matplotlib figures
- **Caching Strategy**: Performance optimization without complexity
- **Graceful Degradation**: System works even when components fail

## Wrapping Up

Woot woot! You've just built a sophisticated data integration and visualization system that transforms your AI agents from conversation partners into powerful research tools. Your agents can now:

- ✅ Fetch real-world Pokémon data from APIs
- ✅ Process and analyze large datasets
- ✅ Create beautiful, publication-ready visualizations  
- ✅ Handle errors gracefully and degrade functionality when needed
- ✅ Cache data for improved performance
- ✅ Export results in multiple formats

### The Power You've Unlocked

Your agents now have access to:

- **Real-time data**: Live information from the PokéAPI
- **Statistical analysis**: Mathematical processing of Pokémon attributes
- **Visual communication**: Charts that tell stories with data
- **Persistent storage**: Saving results for future reference
- **Scalable architecture**: Ready to handle more data sources
