"""
PokéAPI integration utilities for fetching Pokémon data.
"""
import requests
import json
from typing import Dict, List, Optional
from dataclasses import dataclass

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

class PokemonAPI:
    """Class for interacting with the PokéAPI."""
    
    BASE_URL = "https://pokeapi.co/api/v2"
    
    def __init__(self):
        self.session = requests.Session()
        self.type_effectiveness = self._load_type_effectiveness()
    
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
            "psychic": {
                "weaknesses": ["bug", "ghost", "dark"],
                "resistances": ["fighting", "psychic"]
            },
            "ice": {
                "weaknesses": ["fire", "fighting", "rock", "steel"],
                "resistances": ["ice"]
            },
            "dragon": {
                "weaknesses": ["ice", "dragon", "fairy"],
                "resistances": ["fire", "water", "electric", "grass"]
            },
            "dark": {
                "weaknesses": ["fighting", "bug", "fairy"],
                "resistances": ["ghost", "dark"]
            },
            "fairy": {
                "weaknesses": ["poison", "steel"],
                "resistances": ["fighting", "bug", "dark"]
            },
            "normal": {
                "weaknesses": ["fighting"],
                "resistances": []
            },
            "fighting": {
                "weaknesses": ["flying", "psychic", "fairy"],
                "resistances": ["rock", "bug", "dark"]
            },
            "poison": {
                "weaknesses": ["ground", "psychic"],
                "resistances": ["grass", "fighting", "poison", "bug", "fairy"]
            },
            "ground": {
                "weaknesses": ["water", "grass", "ice"],
                "resistances": ["poison", "rock"]
            },
            "flying": {
                "weaknesses": ["electric", "ice", "rock"],
                "resistances": ["grass", "fighting", "bug"]
            },
            "bug": {
                "weaknesses": ["fire", "flying", "rock"],
                "resistances": ["grass", "fighting", "ground"]
            },
            "rock": {
                "weaknesses": ["water", "grass", "fighting", "ground", "steel"],
                "resistances": ["normal", "fire", "poison", "flying"]
            },
            "ghost": {
                "weaknesses": ["ghost", "dark"],
                "resistances": ["poison", "bug"]
            },
            "steel": {
                "weaknesses": ["fire", "fighting", "ground"],
                "resistances": ["normal", "grass", "ice", "flying", "psychic", "bug", "rock", "dragon", "steel", "fairy"]
            }
        }
    
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
        
        # Remove resistances from weaknesses
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
