import os
import json
import requests

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

#Delete line below if using project
from secretInfo import id, token, secret
from secretUserInfo import id, token, secret

class spotifyPlaylist:

    def __init__(self):
        self.songInfo = {}
        self.yClient = self.youtubeClient()

    def youtubeClient(self):
        #From Youtube Data API
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = secret

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    def youtubelikedVideos(self):
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics", myRating="like"
        )
        response = request.execute()
        for items in response["items"]:
            title = items["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(items["id"])

            dL = youtube_dl.YoutubeDL({}).extract_info(youtube_url,download=False)
            song = dL["track"]
            artist = dL["artist"]

    def uriSpotify(self,name,artist):
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(name,artist)
        




if __name__ == '__main__':
    play = spotifyPlaylist()




