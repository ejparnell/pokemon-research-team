"""
Complete example workflow: Fire-type Pokémon weakness analysis.
This demonstrates the full research team in action.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from tools.pokemon_api import PokemonAPI
from tools.visualizer import PokemonDataVisualizer
from agents.research_agents import ProfessorOakAgent, ReporterAgent


def fire_type_weakness_analysis():
    """
    Complete workflow demonstrating Fire-type Pokémon weakness analysis.
    This example shows how the research team would work together.
    """
    print("🔥 Starting Fire-type Pokémon Weakness Analysis")
    print("=" * 50)
    
    # Initialize tools and agents
    pokemon_api = PokemonAPI()
    visualizer = PokemonDataVisualizer()
    professor_oak = ProfessorOakAgent()
    reporter = ReporterAgent()
    
    print("\n📋 Phase 1: Research Planning")
    print("-" * 30)
    
    # Professor Oak creates research plan
    research_goal = "analyze all Fire-type Pokémon weaknesses"
    research_plan = professor_oak.create_research_plan(research_goal)
    
    print("Research Objective:", research_plan['objective'])
    print("Data Requirements:")
    for requirement in research_plan['data_requirements']:
        print(f"  • {requirement}")
    
    print("\n🔬 Phase 2: Data Collection & Analysis")
    print("-" * 30)
    
    # Researcher phase: Collect data
    print("Collecting Fire-type Pokémon data...")
    fire_type_analysis = pokemon_api.analyze_type_weaknesses("fire")
    
    # Get detailed data for a few Fire-type Pokémon
    fire_pokemon_names = ["charmander", "vulpix", "growlithe", "ponyta", "magmar"]
    fire_pokemon_data = []
    
    for name in fire_pokemon_names:
        print(f"Analyzing {name.title()}...")
        pokemon_data = pokemon_api.get_pokemon_by_name(name)
        if pokemon_data:
            fire_pokemon_data.append({
                'name': pokemon_data.name,
                'types': pokemon_data.types,
                'hp': pokemon_data.hp,
                'attack': pokemon_data.attack,
                'defense': pokemon_data.defense,
                'special_attack': pokemon_data.special_attack,
                'special_defense': pokemon_data.special_defense,
                'speed': pokemon_data.speed,
                'weaknesses': pokemon_data.weaknesses,
                'resistances': pokemon_data.resistances
            })
    
    print(f"Successfully collected data for {len(fire_pokemon_data)} Fire-type Pokémon")
    
    print("\n📊 Phase 3: Visualization")
    print("-" * 30)
    
    # Create visualizations
    print("Generating weakness distribution chart...")
    if fire_type_analysis['weakness_percentages']:
        weakness_chart_path = visualizer.plot_weakness_distribution(
            fire_type_analysis['weakness_percentages'],
            "Fire"
        )
        print(f"Weakness chart saved to: {weakness_chart_path}")
    
    print("Generating stats comparison chart...")
    if fire_pokemon_data:
        stats_chart_path = visualizer.plot_stats_comparison(
            fire_pokemon_data,
            "Fire-type Pokémon Stats Comparison"
        )
        print(f"Stats chart saved to: {stats_chart_path}")
    
    print("Generating research summary chart...")
    research_data = {
        'weakness_analysis': fire_type_analysis,
        'pokemon_stats': fire_pokemon_data
    }
    summary_chart_path = visualizer.create_research_summary_chart(research_data)
    print(f"Summary chart saved to: {summary_chart_path}")
    
    # Save raw data to CSV
    csv_path = visualizer.save_data_to_csv(fire_pokemon_data, "fire_pokemon_analysis")
    print(f"Raw data saved to: {csv_path}")
    
    print("\n📝 Phase 4: Report Generation")
    print("-" * 30)
    
    # Reporter phase: Generate comprehensive report
    print("Generating comprehensive research report...")
    research_report = reporter.generate_report(research_data)
    
    # Save report to file
    report_path = Path("data/visualizations/fire_type_research_report.md")
    with open(report_path, 'w') as f:
        f.write(research_report)
    
    print(f"Research report saved to: {report_path}")
    
    print("\n✅ Analysis Complete!")
    print("=" * 50)
    
    # Display key findings
    print("\n🎯 Key Findings Summary:")
    if fire_type_analysis['most_common_weakness']:
        weakness_type, percentage = fire_type_analysis['most_common_weakness']
        print(f"• Most common weakness: {weakness_type.title()} ({percentage:.1f}%)")
    
    print(f"• Total Pokémon analyzed: {len(fire_pokemon_data)}")
    print(f"• Average HP: {sum(p['hp'] for p in fire_pokemon_data) / len(fire_pokemon_data):.1f}")
    print(f"• Average Attack: {sum(p['attack'] for p in fire_pokemon_data) / len(fire_pokemon_data):.1f}")
    
    print("\n📁 Generated Files:")
    print(f"• Weakness Chart: {weakness_chart_path}")
    print(f"• Stats Chart: {stats_chart_path}")
    print(f"• Summary Chart: {summary_chart_path}")
    print(f"• Data CSV: {csv_path}")
    print(f"• Research Report: {report_path}")
    
    return {
        'analysis_results': fire_type_analysis,
        'pokemon_data': fire_pokemon_data,
        'visualizations': {
            'weakness_chart': weakness_chart_path,
            'stats_chart': stats_chart_path,
            'summary_chart': summary_chart_path
        },
        'report_path': str(report_path),
        'data_csv': csv_path
    }


def simple_pokemon_lookup():
    """Simple example: Look up a single Pokémon."""
    print("🔍 Simple Pokémon Lookup Example")
    print("=" * 40)
    
    pokemon_api = PokemonAPI()
    
    # Look up Charizard
    pokemon = pokemon_api.get_pokemon_by_name("charizard")
    
    if pokemon:
        print(f"\n📊 {pokemon.name.title()} Analysis:")
        print(f"Types: {', '.join(pokemon.types)}")
        print(f"HP: {pokemon.hp}")
        print(f"Attack: {pokemon.attack}")
        print(f"Defense: {pokemon.defense}")
        print(f"Weaknesses: {', '.join(pokemon.weaknesses)}")
        print(f"Resistances: {', '.join(pokemon.resistances)}")
    else:
        print("❌ Pokémon not found!")


if __name__ == "__main__":
    # Run the examples
    print("🎮 Pokémon Research Team Demo")
    print("Choose an example to run:")
    print("1. Fire-type Weakness Analysis (Full Workflow)")
    print("2. Simple Pokémon Lookup")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        try:
            results = fire_type_weakness_analysis()
            print("\n🎉 Demo completed successfully!")
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            print("Make sure you've installed all dependencies with: pip install -r requirements.txt")
    
    elif choice == "2":
        try:
            simple_pokemon_lookup()
            print("\n🎉 Lookup completed successfully!")
        except Exception as e:
            print(f"❌ Error during lookup: {e}")
            print("Make sure you've installed all dependencies with: pip install -r requirements.txt")
    
    else:
        print("❌ Invalid choice. Please run the script again and choose 1 or 2.")