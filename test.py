from __future__ import print_function
import subprocess as sp

# NB: add -copy if from mp3 -> mp3; else no -copy
mp3file = './theologyLecture.mp3'
outdir = './lecture2'
do_copy = False
print('splitting \'%s\'  into directory \'%s\'' % (mp3file,  outdir))


times2 = [0, 122, 123, 234, 234, 1423, 1424, 1579, 1580, 1749, 1749, 2501, 2502, 3004, 3005, 3261, 3262, 3579, 3580, 3961, 3961, 4201, 4201, 4501, 4501, 4561, 4561, 4741, 4741, 5701]
times = []
for i in range(0,len(times2), 2):
	times.append(times2[i])


# set id3 tags ala http://jonhall.info/how_to/create_id3_tags_using_ffmpeg
cmds = []
slideNum = 0
for i in range(len(times) -1):
  cmd = (times[i], times[i+1], "slide"+str(slideNum))
  cmds.append(cmd)
  slideNum += 1
  run = 'ffmpeg -i \"%s\" -ac 1 -ss %s -to %s ' % (mp3file, cmd[0], cmd[1])
  run += ' -metadata title="%s"  ' % ( cmd[2])
  run += '"%s/%02d.flac"' % (outdir, i + 1)
  print("from" + str(cmd[0]) + " to " + str(cmd[1]))
  sp.call(run, shell=True)
