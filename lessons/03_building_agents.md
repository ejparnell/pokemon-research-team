# Lesson 3: Building Your AI Agents

We are set up and ready to go. If you are building your own LLMs agents, you will have to have them ready before continuing with this lesson.

By the end of this lesson, you'll have:

- Built Professor Oak, our master coordinator
- Created a Researcher agent that can collect and analyze data
- Developed a Reporter agent that synthesizes findings
- Connected them all through AutoGen's group chat system

## Understanding Agent Architecture

Before we start coding, let's talk about what makes a good AI agent. I want to go back to the analogy of the orchestra here. Each agent is like a musician with their own instrument and sheet music. They need to know their part, how to play it well, and when to come in and out of the performance. The conductor (in our case, the group chat manager) ensures everyone is in sync and working towards the same musical piece (the research goal).

Each agent has a task that it is specialized for, and they need to communicate effectively with each other to achieve the overall objective. Just like in an orchestra, if one musician is out of sync, it can throw off the entire performance. The same goes for our agents, they need to work together harmoniously.

### Core Agent Components

Every AutoGen agent needs these key pieces:

1. **Identity & Role**: Who they are and what they do
2. **System Message**: Their "personality" and instructions
3. **LLM Configuration**: How they connect to the AI model
4. **Specialized Methods**: Custom functions for their specific tasks

It's like giving each agent a sheet of music to play from, ensuring they know their part in the overall symphony.

## Step 1: Creating the Foundation Files

First, let's make sure we have the right file structure. You should already have this from the setup lesson, but let's double-check:

```bash
# Make sure you're in your project directory
cd pokemon-research-team

# Create the agents directory structure if it doesn't exist
mkdir -p src/agents
touch src/agents/__init__.py
```

Now we're going to create two main files:

- `src/agents/research_agents.py` - Our three agent classes
- `src/agents/coordinator.py` - The system that makes them work together

## Step 2: Building the Research Agents

Let's start by creating our main agents file. Open up `src/agents/research_agents.py` in your favorite code editor and let's build this step by step.

### Setting Up Imports and Base Structure

First, we need to import everything we'll need:

```python
"""
Professor Oak Agent - The research coordinator and planner.
"""
from autogen import AssistantAgent
from typing import Dict, List, Any
import os
```

**What's happening here?**

- `AssistantAgent` is AutoGen's base class for AI agents
- `typing` helps us specify what types of data our functions expect
- `os` lets us read environment variables (like API keys)

### Building Professor Oak - The Coordinator

Professor Oak is our team leader. He takes big research questions and breaks them down into manageable tasks. Think of him as the project manager who knows how to delegate work.

```python
class ProfessorOakAgent(AssistantAgent):
    """
    Professor Oak acts as the research coordinator.
    He receives research goals and breaks them down into specific tasks for researcher agents.
    """

    def __init__(self, name: str = "Professor_Oak"):
        system_message = """
        You are Professor Oak, a renowned Pokémon researcher and coordinator.
        
        Your role is to:
        1. Receive high-level research goals from users
        2. Break down complex research tasks into specific, actionable subtasks
        3. Assign tasks to researcher agents
        4. Coordinate the research process
        5. Ensure comprehensive analysis is completed
        
        When given a research goal like "analyze Fire-type Pokémon weaknesses", you should:
        - Define what specific data needs to be collected
        - Specify what analysis should be performed
        - Request appropriate visualizations
        - Coordinate between researcher and reporter agents
        
        Always be thorough and scientific in your approach.
        """

        super().__init__(
            name=name,
            system_message=system_message,
            llm_config={
                "config_list": [
                    {
                        "model": "gpt-4",
                        "api_key": os.getenv("OPENAI_API_KEY", "your-api-key-here")
                    }
                ],
                "temperature": 0.1
            }
        )
```

**Key Points About This Code:**

- The `system_message` is like giving Professor Oak his job description and personality
- `llm_config` tells AutoGen how to connect to the AI model (GPT-4 in this case)
- `temperature: 0.1` makes responses more consistent and less creative (good for coordination)
- `os.getenv()` safely reads the API key from environment variables

### Adding Professor Oak's Special Methods

Now let's give Professor Oak a special ability, creating research plans:

```python
    def create_research_plan(self, research_goal: str) -> Dict[str, Any]:
        """Create a structured research plan for the given goal."""
        plan_prompt = f"""
        Create a detailed research plan for: {research_goal}
        
        Please structure your plan with:
        1. Research objectives
        2. Data collection requirements
        3. Analysis steps
        4. Expected deliverables
        5. Success criteria
        
        Make it specific and actionable for researcher agents.
        """
 
        # This would typically use the LLM to generate the plan
        # For now, we'll return a structured template
        if "fire" in research_goal.lower() and "weakness" in research_goal.lower():
            return {
                "objective": "Analyze Fire-type Pokémon weaknesses and vulnerabilities",
                "data_requirements": [
                    "Fetch list of all Fire-type Pokémon",
                    "Get detailed stats for each Fire-type Pokémon",
                    "Collect type effectiveness data",
                    "Gather weakness/resistance information"
                ],
                "analysis_steps": [
                    "Calculate average stats for Fire-type Pokémon",
                    "Identify most common weaknesses",
                    "Analyze defensive capabilities",
                    "Compare with other types"
                ],
                "deliverables": [
                    "Statistical summary report",
                    "Weakness frequency chart",
                    "Comparative analysis visualization",
                    "Strategic recommendations"
                ],
                "success_criteria": [
                    "Complete data for at least 10 Fire-type Pokémon",
                    "Clear identification of top 3 weaknesses",
                    "Visual representations of findings",
                    "Actionable strategic insights"
                ]
            }
        else:
            return {
                "objective": f"Research and analyze: {research_goal}",
                "data_requirements": ["Collect relevant Pokémon data"],
                "analysis_steps": ["Perform statistical analysis"],
                "deliverables": ["Generate comprehensive report"],
                "success_criteria": ["Complete analysis with insights"]
            }
```

**Why This Method Matters:**

- It gives Professor Oak a way to create structured plans
- Right now it uses templates, but you could enhance it to use the LLM for dynamic planning
- The return format is consistent, making it easy for other agents to understand

### Building the Researcher Agent

Next up is our data specialist. This agent is all about collecting and analyzing information:

```python
class ResearcherAgent(AssistantAgent):
    """
    Researcher Agent - Performs data collection and analysis.
    """

    def __init__(self, name: str = "Researcher"):
        system_message = """
        You are a dedicated Pokémon researcher specializing in data collection and analysis.
        
        Your role is to:
        1. Execute specific research tasks assigned by Professor Oak
        2. Collect data from the PokéAPI and other sources
        3. Perform statistical analysis on Pokémon data
        4. Use visualization tools when appropriate
        5. Report findings clearly and accurately
        
        You have access to:
        - PokéAPI integration tools
        - Statistical analysis capabilities
        - Data visualization functions
        
        Always be precise and thorough in your data collection and analysis.
        Verify your findings and note any limitations in the data.
        """
        
        super().__init__(
            name=name,
            system_message=system_message,
            llm_config={
                "config_list": [
                    {
                        "model": "gpt-4",
                        "api_key": os.getenv("OPENAI_API_KEY", "your-api-key-here")
                    }
                ],
                "temperature": 0.1
            }
        )
```

**Notice the Differences:**

- The system message focuses on data collection and analysis
- Same technical setup as Professor Oak, but different personality and role

### Creating the Reporter Agent

Finally, our communication specialist who turns raw data into beautiful reports:

```python
class ReporterAgent(AssistantAgent):
    """
    Reporter Agent - Synthesizes findings into comprehensive reports.
    """

    def __init__(self, name: str = "Reporter"):
        system_message = """
        You are a scientific reporter specializing in Pokémon research communication.
        
        Your role is to:
        1. Receive research findings from researcher agents
        2. Synthesize multiple data sources into coherent reports
        3. Create clear, professional summaries
        4. Highlight key insights and implications
        5. Present findings in an accessible format
        
        Your reports should include:
        - Executive summary of key findings
        - Detailed analysis results
        - Visual elements and charts
        - Strategic recommendations
        - Areas for further research
        
        Write clearly and professionally, making complex data accessible to various audiences.
        """

        super().__init__(
            name=name,
            system_message=system_message,
            llm_config={
                "config_list": [
                    {
                        "model": "gpt-4",
                        "api_key": os.getenv("OPENAI_API_KEY", "your-api-key-here")
                    }
                ],
                "temperature": 0.3  # Slightly higher for more creative reporting
            }
        )
```

### Adding the Reporter's Special Report Generation

Let's give the Reporter agent a method to create structured reports:

```python
    def generate_report(self, research_data: Dict[str, Any]) -> str:
        """Generate a comprehensive research report."""
        report_sections = []

        # Executive Summary
        report_sections.append("# Pokémon Research Report")
        report_sections.append("## Executive Summary")

        if 'weakness_analysis' in research_data:
            weakness_data = research_data['weakness_analysis']
            report_sections.append(f"Analysis of {weakness_data.get('type', 'Unknown')} type Pokémon reveals significant strategic insights.")

        # Methodology
        report_sections.append("## Methodology")
        report_sections.append("Data collected via PokéAPI with statistical analysis performed on type effectiveness and base stats.")

        # Key Findings
        report_sections.append("## Key Findings")

        if 'weakness_analysis' in research_data:
            weakness_data = research_data['weakness_analysis']
            analyzed_count = weakness_data.get('analyzed_pokemon_count', 0)
            report_sections.append(f"- Analyzed {analyzed_count} Pokémon specimens")
            
            if 'most_common_weakness' in weakness_data and weakness_data['most_common_weakness']:
                weakness_type, percentage = weakness_data['most_common_weakness']
                report_sections.append(f"- Most common weakness: {weakness_type.title()} type ({percentage:.1f}% of analyzed Pokémon)")

            if 'weakness_percentages' in weakness_data:
                report_sections.append("- Weakness distribution:")
                for weakness, percentage in sorted(weakness_data['weakness_percentages'].items(), key=lambda x: x[1], reverse=True):
                    report_sections.append(f"  - {weakness.title()}: {percentage:.1f}%")

        # Recommendations
        report_sections.append("## Strategic Recommendations")
        report_sections.append("Based on the analysis, trainers should consider type coverage and defensive strategies when building teams.")

        return "\n\n".join(report_sections)
```

**What Makes This Cool:**

- Takes raw research data and turns it into a professional markdown report
- Handles missing data gracefully
- Creates a structured format that's easy to read
- Can be extended to handle different types of analysis

## Step 3: Building the Coordinator System

Now we need to create the system that makes our agents work together. Create a new file `src/agents/coordinator.py`:

### Setting Up the Coordinator Imports

```python
"""
AutoGen group chat coordination for Pokémon research team.
"""

from autogen import UserProxyAgent, GroupChat, GroupChatManager
from typing import List, Dict, Any
import os
from .research_agents import ProfessorOakAgent, ResearcherAgent, ReporterAgent
```

**Import Breakdown:**

- `UserProxyAgent` represents the human user in conversations
- `GroupChat` manages multi-agent conversations
- `GroupChatManager` controls the flow of the group conversation
- We import our custom agents from the file we just created

### Creating the Research Coordinator Class

```python
class ResearchCoordinator:
    """Coordinates the research team using AutoGen's group chat."""

    def __init__(self):
        self.professor_oak = ProfessorOakAgent()
        self.researcher = ResearcherAgent()
        self.reporter = ReporterAgent()

        # Create user proxy for interaction
        self.user_proxy = UserProxyAgent(
            name="User",
            system_message="A user requesting Pokémon research.",
            code_execution_config={"work_dir": "data", "use_docker": False},
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10
        )

        # Create group chat
        self.group_chat = GroupChat(
            agents=[self.user_proxy, self.professor_oak, self.researcher, self.reporter],
            messages=[],
            max_round=20
        )

        self.group_chat_manager = GroupChatManager(
            groupchat=self.group_chat,
            llm_config={
                "config_list": [
                    {
                        "model": "gpt-4",
                        "api_key": os.getenv("OPENAI_API_KEY", "your-api-key-here")
                    }
                ],
                "temperature": 0.1
            }
        )
```

**Key Configuration Choices:**

- `human_input_mode="NEVER"` means the conversation runs automatically
- `max_consecutive_auto_reply=10` prevents infinite loops
- `max_round=20` limits how long conversations can go
- All agents are added to the group chat for collaboration

### Adding Coordinator Methods

```python
    def start_research_project(self, research_goal: str) -> Dict[str, Any]:
        """Start a research project with the given goal."""

        # Initialize the research conversation
        initial_message = f"""
        New research project initiated: {research_goal}
        
        Professor Oak, please create a research plan and coordinate with the team.
        Researcher, be ready to collect and analyze data.
        Reporter, prepare to synthesize findings into a comprehensive report.
        """

        # Start the group chat
        self.user_proxy.initiate_chat(
            self.group_chat_manager,
            message=initial_message
        )

        # Return the conversation history and any results
        return {
            "research_goal": research_goal,
            "conversation_history": self.group_chat.messages,
            "status": "completed"
        }

    def get_research_plan(self, research_goal: str) -> Dict[str, Any]:
        """Get a research plan from Professor Oak without full execution."""
        return self.professor_oak.create_research_plan(research_goal)
```

**Method Purposes:**

- `start_research_project()` kicks off a full multi-agent conversation
- `get_research_plan()` gets just the planning phase without full execution
- Both return structured data that can be used by other parts of your application

## Step 4: Testing Your Agents

Let's create a simple test to make sure everything works. Create a test file or add this to a Python script:

```python
# Test file: test_agents.py
import sys
import os
sys.path.append('src')

from agents.research_agents import ProfessorOakAgent, ResearcherAgent, ReporterAgent
from agents.coordinator import ResearchCoordinator

def test_basic_agent_creation():
    """Test that we can create all our agents without errors."""
    try:
        oak = ProfessorOakAgent()
        researcher = ResearcherAgent()
        reporter = ReporterAgent()
        coordinator = ResearchCoordinator()
        
        print("✅ All agents created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating agents: {e}")
        return False

def test_research_plan():
    """Test Professor Oak's research planning ability."""
    oak = ProfessorOakAgent()
    plan = oak.create_research_plan("analyze Fire-type Pokémon weaknesses")
    
    print("🔬 Research Plan Generated:")
    print(f"Objective: {plan['objective']}")
    print(f"Data Requirements: {len(plan['data_requirements'])} items")
    print(f"Analysis Steps: {len(plan['analysis_steps'])} steps")
    print("✅ Research planning works!")

if __name__ == "__main__":
    print("🧪 Testing Agent System...")
    test_basic_agent_creation()
    test_research_plan()
```

Run this test:

```bash
python test_agents.py
```

## Step 5: Understanding Agent Communication

Now let's talk about how these agents actually talk to each other. AutoGen uses a conversation-based approach where agents take turns responding to messages.

### The Conversation Flow

1. **User** sends initial request
2. **Professor Oak** receives it and creates a plan
3. **Researcher** gets assigned specific data collection tasks
4. **Reporter** receives analysis results and creates reports
5. **GroupChatManager** orchestrates the entire conversation

### Message Types and Patterns

Agents communicate through structured messages. Here are some patterns you'll see:

```python
# Planning message from Professor Oak
{
    "role": "assistant",
    "content": "I'll create a research plan for Fire-type analysis...",
    "name": "Professor_Oak"
}

# Data collection message from Researcher
{
    "role": "assistant", 
    "content": "I've collected data on 15 Fire-type Pokémon...",
    "name": "Researcher"
}

# Final report from Reporter
{
    "role": "assistant",
    "content": "## Fire-Type Analysis Report\n\nExecutive Summary...",
    "name": "Reporter"
}
```

## Step 6: Extending and Customizing Your Agents

Now that you have the basic structure, here are some ways to make your agents even better:

### Adding Tool Integration

You can give agents access to external tools and functions:

```python
# In your agent's __init__ method, add:
self.tools = {
    "pokemon_api": PokemonAPI(),
    "visualizer": PokemonDataVisualizer(),
    "calculator": StatisticsCalculator()
}
```

### Creating Specialized Agent Types

Consider creating additional agent types for specific tasks:

```python
class DataVisualizationAgent(AssistantAgent):
    """Specializes in creating charts and graphs."""
    
class CompetitiveAnalysisAgent(AssistantAgent):
    """Focuses on battle strategy and team building."""
    
class EvolutionAnalysisAgent(AssistantAgent):
    """Analyzes evolution chains and family trees."""
```

### Dynamic System Messages

Make your agents more flexible by generating system messages based on the task:

```python
def create_dynamic_system_message(self, research_focus: str) -> str:
    base_message = "You are a Pokémon researcher..."
    
    if "competitive" in research_focus:
        base_message += "\nFocus on battle strategies and team synergy."
    elif "evolution" in research_focus:
        base_message += "\nEmphasize evolution patterns and family relationships."
        
    return base_message
```

## Step 7: Best Practices and Common Pitfalls

### Agent Design Best Practices

1. **Single Responsibility**: Each agent should have one clear job
2. **Clear Communication**: System messages should be specific and actionable
3. **Error Handling**: Always handle API failures and missing data gracefully
4. **Consistent Interfaces**: Make sure agents can easily work together

### Common Issues and Solutions

**Problem**: Agents get stuck in loops

```python
# Solution: Set reasonable limits
max_consecutive_auto_reply=5
max_round=15
```

**Problem**: API key errors

```python
# Solution: Better error handling
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set OPENAI_API_KEY environment variable")
```

**Problem**: Agents don't understand each other

```python
# Solution: Clearer system messages and consistent data formats
system_message = """
When passing data to other agents, always use this format:
{
    "type": "analysis_result",
    "data": {...},
    "timestamp": "2024-01-01T00:00:00Z"
}
"""
```

## Documentation and Resources

### AutoGen Official Documentation

- **Main Docs**: [Microsoft AutoGen Stable Docs](https://microsoft.github.io/autogen/stable/)
- **Agent Classes**: [AutoGen Agent Types](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/tutorial/agents.html)
- **Group Chat**: [GroupChat Documentation](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/group-chat.html)

> Note: Documentation links last updated Nov. 2025. If there is a broken link, please refer to the main AutoGen documentation page.

### Key AutoGen Concepts to Master

1. **Agent Lifecycle**: How agents are created, configured, and destroyed
2. **Conversation Flow**: How messages flow between agents in group chats
3. **LLM Configuration**: Setting up different models and parameters
4. **Function Calling**: Enabling agents to use external tools and APIs

### Useful AutoGen Examples

- [Basic Multi-Agent Chat](https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat/)
- [Tool Integration](https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/components/tools.html)
- [Custom Agents](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/custom-agents.html)

> Note: Documentation links last updated Nov. 2025. If there is a broken link, please refer to the main AutoGen documentation page.

## Next Steps: Bringing It All Together

Congratulations! You've just built a complete multi-agent system. Your agents can now:

- ✅ Plan research projects (Professor Oak)
- ✅ Coordinate team activities (ResearchCoordinator)
- ✅ Collect and analyze data (Researcher)
- ✅ Generate professional reports (Reporter)

### What's Coming Next

In the upcoming lessons, we'll:

1. **Connect to Real Data**: Hook up the PokéAPI integration
2. **Add Visualization**: Create charts and graphs of findings
3. **Build the Complete Pipeline**: Put everything together in a working demo
4. **Deploy and Scale**: Make it production-ready

### Take It for a Spin

Try running a simple test with your new agents:

```python
# Quick test of your multi-agent system
coordinator = ResearchCoordinator()
plan = coordinator.get_research_plan("analyze Water-type Pokémon defense stats")
print(plan)
```

Woot woot, you've just built the brains of your Pokémon research operation! These agents are ready to tackle any research challenge you throw at them. Time to hook them up to some real data and watch the magic happen!

Let's venture forth in the next lesson here: [Lesson 4: Integrating Data and Visualization](lessons/04_integrating_data_and_visualization.md)
