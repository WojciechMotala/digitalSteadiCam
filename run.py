import subprocess, os, sys, io, re

# names of mp4 files
inputFile = input("Enter input file name: ")
outputFile = input("Enter output file name: ")

# read video resolution and fps
ffprobeCall = ".\\bin\\ffprobe.exe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=s=x:p=0 " + inputFile
process = subprocess.Popen(ffprobeCall, stdout=subprocess.PIPE, stderr=None, shell=True)
output = process.communicate()
video_resolution = output[0].decode('utf-8')
temp = re.findall(r'\d+', video_resolution) 
res = list(map(int, temp)) 

video_width = res[0]
video_height = res[1]
vide_fps = res[2]/res[3]

# extract sound from video
ffmpegCall = ".\\bin\\ffmpeg.exe -i " + inputFile + " sound_ffmpeg.mp3"
subprocess.call(ffmpegCall)

# convert mp4 to yuv
ffmpegCall = ".\\bin\\ffmpeg.exe -i " + inputFile + " out_ffmpeg.yuv"
subprocess.call(ffmpegCall)

# process video to stabilize it
videoStabCall = ".\\bin\\digitalSteadiCam.exe " + str(video_width) + " " + str(video_height) + " out_ffmpeg.yuv out_stab.yuv" 
subprocess.call(videoStabCall) 

# convert stabilized video from yuv to mp4
ffmpegCall = ".\\bin\\ffmpeg.exe -s " + str(video_width) + "x" + str(video_height) + " -r " + str(vide_fps) + " -i out_stab.yuv " + outputFile
subprocess.call(ffmpegCall)

# delete created yuv files
os.remove("out_ffmpeg.yuv")
os.remove("out_stab.yuv")

# merge stabilized video with extracted sound
ffmpegCall = ".\\bin\\ffmpeg.exe -i " + outputFile + " -i sound_ffmpeg.mp3 -c:v copy -c:a aac stab_with_sound.mp4"
subprocess.call(ffmpegCall)
os.remove(outputFile)
os.remove("sound_ffmpeg.mp3")
os.rename("stab_with_sound.mp4", outputFile)


