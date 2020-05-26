import os
import json
import requests

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

#Delete line below if using project and uncomment "secretUserInfo line"
from secretInfo import id, token, secret
#from secretUserInfo import id, token, secret

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
        request = self.yClient.videos().list(
            part="snippet,contentDetails,statistics", myRating="like"
        )
        response = request.execute()
        count = 0
        for items in response["items"]:
            title = items["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(items["id"])

            dL = youtube_dl.YoutubeDL({}).extract_info(youtube_url,download=False)
            song = dL["track"]
            artist = dL["artist"]
            if song is not None and artist is not None:
                self.songInfo[title] = { "youtube_url": youtube_url,
                                        "song_name": song,
                                        "artist": artist,
                                        "spotify_uri": self.uriSpotify(song, artist)}

    def uriSpotify(self,name,artist):
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(name,artist)
        request = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(token)
            }
        )
        requestJson = request.json()
        print(requestJson)
        uriSongs = requestJson["tracks"]["items"]
        uri = uriSongs[0]["uri"]

        return uri

    def createPlaylist(self):
        request_body = json.dumps({
            "name": "PythonBotPlaylist",
            "description": "Playlist containing liked videos from Youtube using Python bot",
            "public": True
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(id)
        request = requests.post(
            query,
            data=request_body,
            headers={ "Content-Type": "application/json", "Authorization":"Bearer {}".format(token)}
        )
        requests_json = request.json()

        return requests_json["id"]
    def addsongs(self):
        self.youtubelikedVideos()

        videoUri = [info["spotify_uri"]for song, info in self.songInfo.items()]
        playlist = self.createPlaylist()
        songs = json.dumps(videoUri)
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist)

        response = requests.post(
            query,
            data=songs,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(token)
            }
        )

        # check for valid response status
        print(len(self.songInfo))
        if response.status_code != 200 or response.status_code!=201:
            raise Exception(response.status_code)

        response_json = response.json()
        return response_json
    def playlistPic(self):
        pass
if __name__ == '__main__':
    play = spotifyPlaylist()
    play.addsongs()




