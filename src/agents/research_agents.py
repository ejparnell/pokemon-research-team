"""
Professor Oak Agent - The research coordinator and planner.
"""
from autogen import AssistantAgent
from typing import Dict, List, Any
import os

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
