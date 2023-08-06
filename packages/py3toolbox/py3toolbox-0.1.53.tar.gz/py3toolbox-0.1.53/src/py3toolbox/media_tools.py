#ffmpeg -i INFILE.mp4 -vcodec copy -acodec copy -ss 00:00:00 -t 00:00:10.000 OUTFILE.mp4
import os, sys
from . import fs_tools
import subprocess
import mimetypes, magic

FFMPEG_EXE = None
FFPROBE_EXE = None

def set_ffmpeg_exe(ffmpeg_path):
  global FFMPEG_EXE
  FFMPEG_EXE = ffmpeg_path
  return FFMPEG_EXE

def set_ffprobe_exe(ffprobe_path):
  global FFPROBE_EXE
  FFPROBE_EXE = ffprobe_path
  assert fs_tools.exists(FFPROBE_EXE), f('FFPROBE_EXE not exists')
  return FFPROBE_EXE



def detect_file_type(filename):
    # Create a magic object
    m = magic.Magic(mime=True)

    # Get the MIME type of the file
    mimetype = m.from_file(filename)
    extension = mimetypes.guess_extension(mimetype)
    return extension, mimetype

def get_video_duration(src_file):
  p = subprocess.Popen([
    FFPROBE_EXE, 
    "-v", "error",
    "-show_entries",
    "format=duration",
    "-of",
    "default=noprint_wrappers=1:nokey=1",
    src_file
  ], stdout=subprocess.PIPE)
  duration = int(float(p.communicate()[0].decode("utf-8")))
  return duration


def split_by_time(time_interval, duration):
  file_index = 0
  start_time = 0
  end_time   = 0
  split_list = []
  
  while (True):
    file_index +=1
    if (start_time + time_interval > duration) :
      end_time = duration
    else:
      end_time = start_time + time_interval

    split_list.append({"index":file_index, "start":start_time, "end" : end_time})
    if end_time >= duration : break
    start_time = end_time
    
  return split_list
  
def split_video(source_name, time_interval):
  #time.strftime('%H:%M:%S', time.gmtime(12345))
  #ffmpeg -i source.m4v -ss 1144.94 -t 581.25 -c copy part3.m4v
  filename, file_extension = os.path.splitext(source_name)
  split_list = split_by_time(time_interval,get_video_duration(source_name))
  split_part_list = []
  for part in split_list:
    part["output"] = filename + "_{:04}".format(part["index"]) + file_extension
    if os.path.isfile(part["output"]):  os.remove(part["output"])
    split_part_list.append(part)
  
  for part in split_part_list:
    p = subprocess.Popen([
      FFMPEG_EXE,
      "-loglevel",
      "panic",
      "-i",
      source_name,
      "-ss",
      str(part["start"]),
      "-to",
      str(part["end"]),
      "-c",
      "copy",
      part["output"]
    ], stdout=subprocess.PIPE)    
    
  return split_part_list  


if __name__ == "__main__":
  #print (split_video("R:/x.mp4",360))
  #print (detect_file_type("Y:/important/Home_Photo/2003_02_05/101_0189.JPG"))
  #print (detect_file_type("R:/Temp3/1.mp4"))
  #print (detect_file_type("Y:/fan/no-raid/xxx/japanlust/1.japanese-teen-quivers-with-pussy-pleasure.mp4"))

  print (set_ffprobe_exe('C:/Tools/ffmpeg/bin/ffprobe.exe'))

  
 
