#I have integrated the enhanced error handling and logging into the search_track function.

import requests
import pandas as pd

# Credentials
CLIENT_ID = 'de2b486c754e465fa51a5889c8cc7e6a'
CLIENT_SECRET = 'dfa23a6b23ca412a8750881b81dfeabb'

# Get access token
def get_access_token(client_id, client_secret):
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

# Search track
def search_track(track_name, artist_name, token):
    BASE_URL = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'q': f'track:{track_name} artist:{artist_name}',
        'type': 'track',
        'limit': 1
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    
    # Check the HTTP status code of the response
    if response.status_code != 200:
        print(f"Error for track '{track_name}' by '{artist_name}': {response.status_code} - {response.text}")
        return {}
    
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Failed to decode JSON for track '{track_name}' by '{artist_name}': {response.text}")
        return {}

# Retrieve album cover URL
def get_album_cover_url(track_data):
    try:
        return track_data['tracks']['items'][0]['album']['images'][0]['url']
    except (IndexError, KeyError):
        return None

# Main script to get album cover URLs for the dataset
def main():
    # Load the dataset
    df = pd.read_csv(r'C:\Users\rolan\OneDrive\Desktop\Spotify Dashboard\spotify-2023.csv', encoding='ISO-8859-1')
    
    token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    album_urls = []

    for index, row in df.iterrows():
        track_data = search_track(row['track_name'], row['artist(s)_name'], token)
        album_url = get_album_cover_url(track_data)
        album_urls.append(album_url)

    df['album_cover_url'] = album_urls
    df.to_csv(r'C:\Users\rolan\OneDrive\Desktop\Spotify Dashboard\spotify-2023-updated.csv', index=False)

if __name__ == "__main__":
    main()
