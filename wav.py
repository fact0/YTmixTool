import os
import pprint
from pydub import AudioSegment
from pydub.silence import split_on_silence


def convertMs(ms):
    millis = int(ms)
    seconds = (millis/1000) % 60
    seconds = int(seconds)
    minutes = (millis/(1000*60)) % 60
    minutes = int(minutes)
    hours = (millis/(1000*60*60)) % 24

    return ("%d:%d:%d" % (hours, minutes, seconds))


def create_chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def strip_silence(seg, silence_len=1300, silence_thresh=-50, padding=100):
    chunks = split_on_silence(seg, silence_len, silence_thresh, padding)

    if not len(chunks):
        return seg[0:0]

    for chunk in chunks:
        if len(chunk) > 50000:
            print("Track Length:", convertMs(len(chunk)))
            return chunk


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def create_parts(chunks, outfile, strip=True):
    song = AudioSegment.silent(duration=10)
    for j in range(len(chunks)):
        for i in range(len(chunks[j])):
            print(chunks[j][i], end='\n')
            if strip is True:
                song += strip_silence(AudioSegment.from_file(chunks[j][i]))
            else:
                song += AudioSegment.from_file(chunks[j][i])
        print(f"Part {j} Length:", convertMs(len(song)), end='\n')
        # if file doens't exist:
        song.export(f'./export/{outfile}[{j}].wav', format="wav")
        song = AudioSegment.silent(duration=10)

# create cli with options:
# check requirements/dependancies
# check os and fix directories based on that
# input youtube playlist url
# decide on file name
# allow silence stripping with option
# allow wav or mp3 output
# create timer and display total time taken as result
# have file name, directory, file format, duration in result

# fix function and variable names
# create dynamic variable for each steps output
# decide if its better or faster to work with mp3s or just convert at the end, wavs are too big


# create list of songs and declare output file name
wavs = getListOfFiles('./19')
# create list of 10 song chunks from song list
wav_chunks = list(create_chunks(wavs, 10))

# testing
# i = 1
# print(wavs[2])
# song = strip_silence(AudioSegment.from_file(wavs[2]))
# song.export(f'./export/{outfile}[{i}].wav', format="wav")

# create 10 song parts from list of chunks and export as wav
create_parts(wav_chunks, '19mix_chunk', strip=True)


print("Operation Complete!")

# get list of parts of mix
parts = getListOfFiles('./export')
part_chunks = list(create_chunks(parts, 10))
create_parts(part_chunks, '19mix_part', strip=False)
