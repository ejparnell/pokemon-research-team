"""
Visualization tools for Pokémon research data.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path

class PokemonDataVisualizer:
    """Creates charts and graphs for Pokémon research data."""
    
    def __init__(self, output_dir: str = "data/visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
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
        plt.close()
        
        return str(save_path)
    
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
    
    def plot_type_effectiveness_heatmap(self, effectiveness_data: Dict[str, Dict[str, float]],
                                      save_path: Optional[str] = None) -> str:
        """Create a heatmap showing type effectiveness."""
        # Convert to DataFrame
        df = pd.DataFrame(effectiveness_data).fillna(1.0)  # Default to normal effectiveness
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(12, 10))
        
        sns.heatmap(df, annot=True, cmap='RdYlBu_r', center=1.0,
                   square=True, ax=ax, cbar_kws={'label': 'Effectiveness Multiplier'})
        
        ax.set_title('Type Effectiveness Chart', fontsize=16, fontweight='bold')
        ax.set_xlabel('Defending Type', fontsize=12)
        ax.set_ylabel('Attacking Type', fontsize=12)
        
        plt.tight_layout()
        
        # Save the plot
        if save_path is None:
            save_path = self.output_dir / "type_effectiveness_heatmap.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(save_path)
    
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
    
    def save_data_to_csv(self, data: List[Dict[str, Any]], filename: str) -> str:
        """Save research data to CSV file."""
        df = pd.DataFrame(data)
        csv_path = self.output_dir / f"{filename}.csv"
        df.to_csv(csv_path, index=False)
        return str(csv_path)
