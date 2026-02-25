import json
import os
from datetime import datetime

SESSIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sessions')

def ensure_sessions_dir():
    os.makedirs(SESSIONS_DIR, exist_ok=True)

def save_session(customer_name, session_data):
    """Save a customer session to disk."""
    ensure_sessions_dir()
    safe_name = customer_name.replace(' ', '_').replace('/', '_').lower()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{safe_name}_{timestamp}.json"
    filepath = os.path.join(SESSIONS_DIR, filename)

    save_data = {
        'customer_name': customer_name,
        'saved_at': datetime.now().isoformat(),
        'parsed_data': session_data.get('parsed_data'),
        'current_tco': session_data.get('current_tco'),
        'scenario_results': session_data.get('scenario_results'),
        'selected_platforms': session_data.get('selected_platforms'),
        'assumptions': session_data.get('assumptions'),
        'discovery': session_data.get('discovery'),
        'renewal_data': session_data.get('renewal_data'),
        'recommendation_override': session_data.get('recommendation_override'),
        'quotes': session_data.get('quotes'),
    }

    with open(filepath, 'w') as f:
        json.dump(save_data, f, indent=2, default=str)

    return filename


def load_session(filename):
    """Load a customer session from disk."""
    filepath = os.path.join(SESSIONS_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        return json.load(f)


def list_sessions():
    """List all saved sessions."""
    ensure_sessions_dir()
    sessions = []
    for filename in os.listdir(SESSIONS_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(SESSIONS_DIR, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                sessions.append({
                    'filename': filename,
                    'customer_name': data.get('customer_name', 'Unknown'),
                    'saved_at': data.get('saved_at', ''),
                    'recommendation': data.get('scenario_results', {}) and
                        max(data.get('scenario_results', {}).items(),
                            key=lambda x: x[1].get('fit', {}).get('fit_score', 0))[0]
                        if data.get('scenario_results') else 'N/A',
                    'total_vms': data.get('parsed_data', {}).get('total_vms', 0),
                })
            except:
                pass
    return sorted(sessions, key=lambda x: x['saved_at'], reverse=True)


def delete_session(filename):
    """Delete a saved session."""
    filepath = os.path.join(SESSIONS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False