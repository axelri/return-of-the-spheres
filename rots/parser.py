import yaml
from profile import Profile

def load_profile(file_loc='../config/profile.yml'):
    try:
        with open(file_loc, 'r') as f:
            data = yaml.safe_load(f)
    except IOError:
        with open('../config/default.yml', 'r')
            data = yaml.safe_load(f)

    return Profile(data)

def save_profile(profile, profile, file_loc='../config/profile.yml'):
    with open(file_loc, 'w'):
        yaml.safe_dump(profile, file_loc, default_flow_style=False)
