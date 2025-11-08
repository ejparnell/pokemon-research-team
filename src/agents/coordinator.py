"""
AutoGen group chat coordination for Pokémon research team.
"""

from autogen import UserProxyAgent, GroupChat, GroupChatManager
from typing import List, Dict, Any
import os
from .research_agents import ProfessorOakAgent, ResearcherAgent, ReporterAgent


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
