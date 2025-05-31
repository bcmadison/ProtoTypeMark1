# save as: add_missing_features.py

# 1. Add SHAP explainability
shap_explainer = '''
import shap
import numpy as np
from typing import Dict, List

class ModelExplainer:
    """SHAP-based model explainability"""
    
    def __init__(self, model):
        self.model = model
        self.explainer = None
        
    def explain_prediction(self, features: np.ndarray, feature_names: List[str]) -> Dict:
        """Generate SHAP explanation for a prediction"""
        if self.explainer is None:
            self.explainer = shap.TreeExplainer(self.model)
            
        shap_values = self.explainer.shap_values(features)
        
        # Create explanation dict
        explanation = {
            'feature_importance': {},
            'base_value': self.explainer.expected_value,
            'prediction': self.model.predict(features)[0]
        }
        
        for i, name in enumerate(feature_names):
            explanation['feature_importance'][name] = float(shap_values[0][i])
            
        return explanation
'''

# 2. Add lineup management endpoints
lineup_endpoints = '''
    @app.get("/api/lineup")
    async def get_player_pool(sport: str = "nba"):
        """Get available players for lineup building"""
        try:
            # Get current player projections
            projections = await app.state.prizepicks.get_player_projections(sport)
            
            # Format for lineup builder
            player_pool = []
            for proj in projections:
                player_pool.append({
                    'id': f"{proj['player_name']}_{proj['stat_type']}",
                    'name': proj['player_name'],
                    'team': proj['team'],
                    'position': proj.get('position', 'N/A'),
                    'salary': 10000,  # Default salary
                    'projection': proj['projection'],
                    'stat_type': proj['stat_type'],
                    'confidence': proj['confidence']
                })
            
            return {
                "status": "success",
                "sport": sport,
                "players": player_pool,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting player pool: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/api/lineup/save")
    async def save_lineup(lineup_data: dict):
        """Save user lineup"""
        try:
            lineup_id = str(datetime.now().timestamp())
            
            # Store in cache (in production, use database)
            await app.state.cache.setex(
                f"lineup:{lineup_id}",
                86400,  # 24 hours
                json.dumps(lineup_data)
            )
            
            return {
                "status": "success",
                "lineup_id": lineup_id,
                "message": "Lineup saved successfully"
            }
        except Exception as e:
            logger.error(f"Error saving lineup: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.get("/api/analytics")
    async def get_analytics():
        """Get model performance analytics"""
        try:
            # Calculate analytics across all sports
            analytics = {
                'model_accuracy': {},
                'sport_performance': {},
                'recent_predictions': [],
                'roi_tracking': {}
            }
            
            for sport in Config.SUPPORTED_SPORTS:
                # Get historical predictions (mock for now)
                analytics['model_accuracy'][sport] = {
                    'overall': 0.68,
                    'last_7_days': 0.72,
                    'last_30_days': 0.67
                }
                
                analytics['sport_performance'][sport] = {
                    'total_predictions': 150,
                    'successful': 102,
                    'win_rate': 0.68,
                    'avg_confidence': 0.71
                }
            
            return {
                "status": "success",
                "analytics": analytics,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting analytics: {e}")
            raise HTTPException(status_code=500, detail=str(e))
'''

# 3. Enhanced frontend components
lineup_builder_component = '''
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Save, Filter, Download, Users } from 'lucide-react';

export default function LineupBuilder() {
  const [playerPool, setPlayerPool] = useState([]);
  const [selectedPlayers, setSelectedPlayers] = useState([]);
  const [sport, setSport] = useState('nba');
  const [filters, setFilters] = useState({
    team: '',
    position: '',
    minProjection: 0
  });

  useEffect(() => {
    fetchPlayerPool();
  }, [sport]);

  const fetchPlayerPool = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/lineup?sport=${sport}`);
      setPlayerPool(response.data.players);
    } catch (error) {
      console.error('Error fetching players:', error);
    }
  };

  const togglePlayer = (player) => {
    if (selectedPlayers.find(p => p.id === player.id)) {
      setSelectedPlayers(selectedPlayers.filter(p => p.id !== player.id));
    } else if (selectedPlayers.length < 6) {
      setSelectedPlayers([...selectedPlayers, player]);
    }
  };

  const saveLineup = async () => {
    try {
      const lineup = {
        sport,
        players: selectedPlayers,
        created_at: new Date().toISOString(),
        total_projection: selectedPlayers.reduce((sum, p) => sum + p.projection, 0)
      };
      
      await axios.post('http://127.0.0.1:8000/api/lineup/save', lineup);
      alert('Lineup saved successfully!');
    } catch (error) {
      console.error('Error saving lineup:', error);
    }
  };

  const exportLineup = () => {
    const data = selectedPlayers.map(p => ({
      player: p.name,
      team: p.team,
      stat: p.stat_type,
      projection: p.projection
    }));
    
    const csv = [
      Object.keys(data[0]).join(','),
      ...data.map(row => Object.values(row).join(','))
    ].join('\\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `lineup_${sport}_${Date.now()}.csv`;
    a.click();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <Users className="text-blue-500" />
          Lineup Builder
        </h2>
        <p className="text-gray-400 mt-1">Build your optimal lineup with AI assistance</p>
      </div>

      {/* Filters */}
      <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-4">
        <div className="flex items-center gap-4">
          <Filter className="text-gray-400" size={20} />
          <select
            value={sport}
            onChange={(e) => setSport(e.target.value)}
            className="bg-slate-700 border border-slate-600 rounded-lg px-4 py-2"
          >
            <option value="nba">NBA</option>
            <option value="mlb">MLB</option>
            <option value="nhl">NHL</option>
          </select>
          
          <input
            type="text"
            placeholder="Filter by team..."
            value={filters.team}
            onChange={(e) => setFilters({...filters, team: e.target.value})}
            className="bg-slate-700 border border-slate-600 rounded-lg px-4 py-2"
          />
        </div>
      </div>

      {/* Selected Lineup */}
      <motion.div 
        className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold">
            Selected Players ({selectedPlayers.length}/6)
          </h3>
          <div className="flex gap-2">
            <button
              onClick={saveLineup}
              disabled={selectedPlayers.length === 0}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 rounded-lg flex items-center gap-2"
            >
              <Save size={16} />
              Save
            </button>
            <button
              onClick={exportLineup}
              disabled={selectedPlayers.length === 0}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded-lg flex items-center gap-2"
            >
              <Download size={16} />
              Export
            </button>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {selectedPlayers.map((player) => (
            <motion.div
              key={player.id}
              className="bg-slate-700/50 rounded-lg p-3 flex justify-between items-center"
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
            >
              <div>
                <div className="font-bold">{player.name}</div>
                <div className="text-sm text-gray-400">
                  {player.team} • {player.stat_type}
                </div>
              </div>
              <div className="text-right">
                <div className="font-bold text-green-400">
                  {player.projection}
                </div>
                <button
                  onClick={() => togglePlayer(player)}
                  className="text-xs text-red-400 hover:text-red-300"
                >
                  Remove
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Player Pool */}
      <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6">
        <h3 className="text-xl font-bold mb-4">Available Players</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {playerPool
            .filter(p => !filters.team || p.team.includes(filters.team))
            .map((player) => (
              <motion.div
                key={player.id}
                whileHover={{ scale: 1.02 }}
                className={`bg-slate-700/50 rounded-lg p-4 cursor-pointer border-2 ${
                  selectedPlayers.find(p => p.id === player.id)
                    ? 'border-green-500'
                    : 'border-transparent hover:border-slate-600'
                }`}
                onClick={() => togglePlayer(player)}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <div className="font-bold">{player.name}</div>
                    <div className="text-sm text-gray-400">
                      {player.team} • {player.position}
                    </div>
                    <div className="text-sm mt-1">
                      {player.stat_type}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-xl">
                      {player.projection}
                    </div>
                    <div className="text-xs text-gray-400">
                      {(player.confidence * 100).toFixed(0)}% conf
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
        </div>
      </div>
    </div>
  );
}'''

print("✅ Missing features identified and code provided!")
print("\nAdd these to your repository:")
print("1. SHAP explainability in prediction_engine.py")
print("2. New endpoints in api_routes.py")
print("3. LineupBuilder component in frontend")
print("4. Update requirements.txt with: shap>=0.41.0")