from pytube import YouTube, Playlist

yt = YouTube(
    'https://youtu.be/lxsKh6y3_eA?list=PLCS0nOWWS-PmxNV0OBR1aodJptN9ohZkW')

p = Playlist(
    'https://www.youtube.com/playlist?list=PLCS0nOWWS-PmxNV0OBR1aodJptN9ohZkW')


print(f'Downloading: {p.title}')

for video in p.videos:
    print(f'Downloading: {video.title}')
    v = video.streams.filter(audio_codec='opus')
    v[0].download('./tmp')
