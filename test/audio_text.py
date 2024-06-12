import subprocess
src_filename = 'input.ogg'
dest_filename = 'input.wav'

process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename])
if process.returncode != 0:
    raise Exception("Something went wrong")