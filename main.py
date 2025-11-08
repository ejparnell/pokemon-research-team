"""
Main entry point for the Pokémon Research Team.
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from examples.fire_type_analysis import fire_type_weakness_analysis, simple_pokemon_lookup

def main():
    """Main entry point with menu system."""
    print("🎮 Welcome to the Pokémon Research Team!")
    print("=" * 45)
    print("\nThis system demonstrates multi-agent collaboration using:")
    print("• AutoGen framework for agent communication")
    print("• PokéAPI for real-time data collection")
    print("• Matplotlib for data visualization")
    print("• Role-based agents (Planner, Worker, Reporter)")
    
    while True:
        print("\n" + "=" * 45)
        print("🔬 Available Research Options:")
        print("1. 🔥 Fire-type Pokémon Weakness Analysis (Full Demo)")
        print("2. 🔍 Simple Pokémon Lookup")
        print("3. 📚 View Project Information")
        print("4. 🚪 Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == "1":
            print("\n" + "=" * 45)
            try:
                results = fire_type_weakness_analysis()
                print("\n🎉 Full analysis completed!")
                print("Check the 'data/visualizations' folder for generated charts and reports.")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("\n💡 Troubleshooting tips:")
                print("1. Run: python -m pip install -r requirements.txt")
                print("2. Make sure you have internet connection for PokéAPI")
                print("3. Check that all dependencies are installed correctly")
        
        elif choice == "2":
            print("\n" + "=" * 45)
            try:
                simple_pokemon_lookup()
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Make sure dependencies are installed and you have internet connection.")
        
        elif choice == "3":
            show_project_info()
        
        elif choice == "4":
            print("\n👋 Thank you for using the Pokémon Research Team!")
            print("Happy researching! 🔬✨")
            break
        
        else:
            print("\n❌ Invalid choice. Please enter 1, 2, 3, or 4.")


def show_project_info():
    """Display project information and concepts."""
    print("\n" + "=" * 45)
    print("📚 Pokémon Research Team - Project Information")
    print("=" * 45)
    
    print("\n🎯 Core Concept:")
    print("A demonstration of multi-agent systems where AI agents collaborate")
    print("to perform research tasks, each with specialized roles:")
    
    print("\n👨‍🔬 Agent Roles:")
    print("• Professor Oak (Planner): Creates research plans and coordinates tasks")
    print("• Researcher (Worker): Collects data and performs analysis")
    print("• Reporter (Summarizer): Synthesizes findings into reports")
    
    print("\n🛠️ Technologies Used:")
    print("• AutoGen: Multi-agent conversation framework")
    print("• PokéAPI: Real-time Pokémon data source")
    print("• Matplotlib/Seaborn: Data visualization")
    print("• Pandas: Data analysis and manipulation")
    
    print("\n📋 Teachable Concepts:")
    print("• Role-based agent design")
    print("• Inter-agent communication")
    print("• Tool calling and API integration")
    print("• Data analysis workflows")
    print("• Automated report generation")
    
    print("\n🎮 Example Research Questions:")
    print("• What are the most common weaknesses of Fire-type Pokémon?")
    print("• How do Water-type stats compare to other types?")
    print("• Which types have the best defensive capabilities?")
    
    print("\n📁 Project Structure:")
    print("• src/agents/: Agent implementations")
    print("• src/tools/: PokéAPI integration and visualization")
    print("• examples/: Demonstration workflows")
    print("• data/: Generated reports and visualizations")


if __name__ == "__main__":
    main()