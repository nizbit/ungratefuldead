#! /usr/bin/env python

# based on vplayer.py (http://pymedia.org/tut/src/vplayer.py.html) by dmitry borisov (http://pymedia.org)
# bloated and uglied for fair reasons by sv (http://www.popmodernism.org)

import sys, thread, time, traceback, Queue, os
import optparse

import pymedia
import pymedia.video.muxer as muxer
import pymedia.video.vcodec as vcodec
import string
from optparse import OptionParser

from recode_video import RecordVideo

if os.environ.has_key( 'PYCAR_DISPLAY' ) and os.environ[ 'PYCAR_DISPLAY' ]== 'directfb':
    import pydfb as pygame
    YV12= pygame.PF_YV12
else:
    import pygame
    YV12= pygame.YV12_OVERLAY

SEEK_SEC= 10

########################################################################3
# Simple video player

class VPlayer:
    # ------------------------------------
    def __init__(self, playkeyframes=False):
        self.frameNum= -1
        self.exitFlag= 1
        self.ct= None
        self.pictureSize= None
        self.paused= 0
        self.stopPlayback()
        self.err= []
        self.vBitRate= 0
        self.seek= 0
        self.seekInProgress = False
        self.vc= None
        self.frnr = 0
        self.lastdelta = None
        self.playkeyframes = False
        self.loopend    = -1
        self.loopstart  = -1
        self.looplen    = -1
        self.loopremain = -1
        self.lastkeyframes = []
        self.playkeyframe = playkeyframes
        self.nextframetime = 0
        self.modifyspeed = 1.
        self.nextframenow = False
        self.islooping = False
        self.paused = False
        self.displaynext = True
        self.displaychess = False
        self.framesavecnt = 0
        self.recordvideo = None

    def setEventLoop(self, ev):
        self.eventloop = ev

    def record(self):
        if self.recordvideo == None:
            print 'Starting recording...'
            #~ print self.vc.size

            #~ params = self.vc.getParams()
            self.recordvideo = RecordVideo()#'record.mpg', None)
            #~ print params

    def resetVideo( self ):
        # Init all used vars first
        self.decodeTime= self.vBitRate= self.frameNum= \
        self.sndDelay= self.hurry= self.videoPTS= \
        self.lastPTS= self.frRate= self.vDelay= 0
        self.seek= 0
        if self.initADelta!= -1:
            self.seekADelta= self.initADelta

        # Zeroing out decoded pics queue
        self.decodedFrames= []
        self.rawFrames= []
        try:
            if self.vc:
                self.vc.reset()
        except:
            print traceback.print_exc()


    def initVideo( self, params ):
        self.framerate = params['frame_rate'] / float(params['frame_rate_base'])
        # There is no overlay created yet
        self.overlay= self.pictureSize= None
        try:
            # Set the initial sound delay to 0 for now
            # It defines initial offset from video in the beginning of the stream
            self.initADelta= -1
            self.resetVideo()
            self.seekADelta= 0
            # Setting up the HW video codec
            self.vc= pymedia.video.ext_codecs.Decoder( params )
        except:
            try:
                # Fall back to SW video codec
                self.vc= vcodec.Decoder( params )
            except:
                traceback.print_exc()
                self.err.append( sys.exc_info()[1] )

    def createOverlay( self, vfr ):
        # Create overlay if any
        self.overlay= pygame.Overlay( YV12, vfr.size )
        # Save real picture size
        if vfr.aspect_ratio> .0:
            self.pictureSize= ( vfr.size[ 1 ]* vfr.aspect_ratio, vfr.size[ 1 ] )
        else:
            self.pictureSize= vfr.size
        # Locate overlay on the screen
        self.setOverlay( self.overlayLoc )

    def processVideoFrame( self, d, framenr, checkifkf=True, skip=False ):
        # See if we should show video frame now

        if not self.nextframetime:
            self.nextframetime = time.time()
        st = self.nextframetime-time.time()
        self.nextframetime += 1/(self.framerate*self.modifyspeed)
        if st < 0: st = 0

        #needs to be done better using another thread
        grain = 1/100.
        #~ print 'ST>', st
        while st > grain:
            if self.nextframenow:
                self.nextframenow = False
                break
            time.sleep(grain)
            #~ print 'time.sleep(%0.5f)' % grain
            st -= grain
        else:
            time.sleep(st)
            #~ print '!!!time.sleep(%0.5f)' % st

        if skip:
            return

        vfr = self.decodeVideoFrame(d, checkifkf)

        if vfr:
            if self.overlayLoc and self.overlay== None:
                self.createOverlay( vfr )
            self.overlay.set_data( vfr.data )
            #~ print '->', vfr.pict_type
            self.overlay.display()
            #~ try:
            if self.recordvideo:
                self.recordvideo.encodeFrame(vfr)
        #~ except:
            #~ print '$!%&'*40

        else:
            print 'not vfr'

        self.frameshown = vfr

    def saveFrame(self):
        print 'd'*100
        dd= self.frameshown.convert( 2 )
        img= pygame.image.fromstring( dd.data, dd.size, "RGB" )
        filename = 'savevid/frame_%03d.bmp' % self.framesavecnt
        print 'Saving to %s...' % filename
        pygame.image.save( img, filename)
        self.framesavecnt += 1

    def saveFrameReset(self):
        self.framesavecnt = 0

    def decodeVideoFrame( self, rawframe, checkifkf):
        # Decode the video frame
        d = rawframe
        framenr= 0

        rawdata = d[1]


        vdstring = rawdata[:10]
        iskeyframe = vdstring[:5] == '\0\0\1\0\0' and checkifkf
        #~ iskeyframe = vdstring[:4] == '\0\0\1'+chr(176) #xvid

        #~ print "schluesselrahmen:", self.frame, '- ', iskeyframe

        #~ iskeyframe = False
        if iskeyframe:
            if self.frame not in self.lastkeyframes:
                self.lastkeyframes.append(self.frame)
                if len(self.lastkeyframes) > 10:
                    self.lastkeyframes[:11] = self.lastkeyframes[1:]
            #~ print 'LASTKEYFRAMES:', self.lastkeyframes

        vddec = '%04i: ' % self.frnr
        for char in vdstring:
            vddec += '%i-' % ord(char)
        #~ print vddec[:-1]
        #~ print vdstring

        if not self.playkeyframes:
            if not self.seek:
                if self.frnr == 0:
                    rawdata = d[1]
                elif not iskeyframe:
                    rawdata = d[1]
                    self.lastdelta = rawdata
                else:
                    rawdata = self.lastdelta
            else:
                rawdata = d[1]
        else:
            rawdata = d[1]

        try:
            vfr= self.vc.decode(rawdata)
        except:
            print traceback.print_exc()
            vfr = None

        self.frnr += 1
        return vfr


    def start( self ):
        if self.ct:
                raise 'cannot run another copy of vplayer'
        self.exitFlag= 0
        self.ct= thread.start_new_thread( self.readerLoop, () )

    def stop( self ):
        # Stop if anything is playing now
        self.stopPlayback()
        # Turn the flag to exist the main thread
        self.exitFlag= 1

    def pause(self):
        self.paused = not self.paused
        self.displaynext = not self.paused

    def displayChess(self):
        self.displaychess = True
        self.displaynext = True

    def startPlayback( self, file ):
        # Stop if anything is playing now
        self.stopPlayback()
        # Set the new file for playing
        self.playingFile= file

    def stopPlayback( self, bForce= True ):
        # Close the overlay
        self.setOverlay( None )
        self.playingFile= None
        # Unpause playback if any
        self.paused= 0

    def jumpTime( self, secs ):
        frames = int(secs * self.framerate)
        self.jumpFrames(frames)

    def jumpFrames( self, frames ):
        self.frame += frames
        self.displaynext = True
        if self.loopend != -1:
            self.loopend   += frames
            self.loopstart += frames

    def loopHold(self, secs):
        #~ print '+++'
        self.looplen_f = length = float(secs) * self.framerate
        self.looplen_r = 0
        #~ print 'self.looplen_f:', length
        #~ self.looplen_i = int(self.looplen_f+0.5)
        #~ print 'self.looplen_i:', self.looplen_i
        #~ self.loopremain = self.looplen_f - self.looplen_i
        #~ print 'loopremain:', self.loopremain
        self._llast = None
        self._lcnt = 0
        self._lall = 0
        if not self.islooping:
            self.loopstart = self.frame
        else:
            self.frame = self.loopstart
        self.islooping = True
        self.setLoopEnd()

    def setLoopEnd(self):
        if self._lcnt:
            ltime = time.time() - self._llast
            #~ print 'LTIME>', ltime
        else:
            ltime = 0

        self._llast = time.time()
        self._lall += ltime

        if self._lcnt:
            pass
            #~ print 'AVRG:', self._lall / self._lcnt

        #~ print 'self._lcnt:', self._lcnt
        #~ print 'self._llast:', self._llast
        #~ print 'self._lall:', self._lall
        #~ print '-'*40

        self._lcnt += 1

        #~ print 'self.looplen_f:', self.looplen_f
        looplen_i = int(self.looplen_f + self.looplen_r + 0.5)
        #~ print 'looplen_i:', looplen_i
        self.looplen_r += self.looplen_f - looplen_i
        #~ print 'loopremain:', self.looplen_r
        #~ print 'looplen_i:', looplen_i
        self.loopend = self.loopstart + looplen_i

        #~ print '\n -+- \n'

    def jumpToLoopStart(self):
        if self.islooping:
            self.looplen_r = 0
            self.frame = self.loopstart

    def jumpToFrame(self, frame):
        self.frame = frame

    def playKeyFrame(self, kfnr):
        print 'PLAYRRR', kfnr
        if not len(self.lastkeyframes):
            return
        if kfnr >= len(self.lastkeyframes):
            kfnr = len(self.lastkeyframes)-1
        self.playkeyframe = self.lastkeyframes[kfnr]
        self.displaynext = True

    def loopRelease(self):
        self.loopend = -1
        self.loopstart = -1
        self.islooping = False

    def setOverlay( self, loc ):
        self.overlayLoc= loc
        print "self.overlayLoc= ", loc
        if loc== None:
            self.overlay= None
        elif self.overlay:
            # Calc the scaling factor
            sw,sh= self.overlayLoc[ 2: ]
            w,h= self.pictureSize
            x,y= self.overlayLoc[ :2 ]
            factor= min( float(sw)/float(w), float(sh)/float(h) )
            # Find appropriate x or y pos
            x= ( sw- factor* w ) / 2+ x
            y= ( sh- factor* h ) / 2+ y
            self.overlay.set_location( (int(x),int(y),int(float(w)*factor),int(float(h)*factor)) )

    def isPlaying( self ):
        return self.overlay!= None

    def openVideo(self, file):
        format = file.split( '.' )[ -1 ].lower()
        dm= muxer.Demuxer( format )
        f= open(file, 'rb')
        rawdata = f.read()
        rawstream = dm.parse(rawdata)
        return dm, f, rawdata, rawstream

    def readerLoop( self ):
        """
        """
        print 'Main video loop has started.'
        f= None
        try:
            while self.exitFlag== 0:
                if self.playingFile== None:
                    time.sleep( 0.01 )
                    continue

                self.frameNum= -1

                if 1:                 # open chess !DIRTYHACK!
                    dm, f, s, rawstream = self.openVideo('chess/chess.avi')
                    print 'STREAMS:', dm.streams

                    # Setup video( only first matching stream will be used )
                    self.err= []
                    for vindex in xrange( len( dm.streams )):
                        if dm.streams[ vindex ][ 'type' ]== muxer.CODEC_TYPE_VIDEO:
                            self.initVideo( dm.streams[ vindex ] )
                            break

                    i=0
                    while i < len(rawstream):
                        if rawstream[i][0] != muxer.CODEC_TYPE_VIDEO:
                            del rawstream[i]
                        else:
                            i+= 1

                    self.chess = rawstream[0]


                # Initialize demuxer and read small portion of the file to have more info on the format
                dm, f, s, rawstream = self.openVideo(self.playingFile['name'])
                print 'STREAMS:', dm.streams

                # Setup video( only first matching stream will be used )
                self.err= []
                for vindex in xrange( len( dm.streams )):
                    if dm.streams[ vindex ][ 'type' ]== muxer.CODEC_TYPE_VIDEO:
                        self.initVideo( dm.streams[ vindex ] )
                        break

                i=0
                while i < len(rawstream):
                    if rawstream[i][0] != muxer.CODEC_TYPE_VIDEO:
                        del rawstream[i]
                    else:
                        i+= 1

                self.numframes = len(rawstream)

                # Play until no exit flag, not eof, no errs
                while len(s) and len( self.err )== 0 and self.exitFlag== 0 and self.playingFile:
                    self.frame = 0
                    while 1:
                        #~ print 'frame:', self.frame
                        if self.frame == self.numframes - 1:
                            time.sleep(0.01)
                            continue

                        if self.paused and not self.displaynext:
                            self.processVideoFrame( None, None, None, skip=True )
                            continue

                        if self.displaychess:
                            self.processVideoFrame( self.chess, self.frame, False )
                            self.displaychess = False
                            self.displaynext = False
                            continue

                        if self.playkeyframe is None:
                            d = rawstream[self.frame]
                            self.processVideoFrame( d, self.frame )
                        else:
                            print 'x'*30, self.playkeyframe
                            d = rawstream[self.playkeyframe]
                            self.playkeyframe = None
                            self.processVideoFrame( d, self.frame, False )

                        if self.frame == self.loopend:
                            self.frame = self.loopstart
                            self.setLoopEnd()

                        if self.paused:
                            self.displaynext = False
                            continue

                        self.frame += 1

            print 'ente.'

        except:
            print traceback.print_exc()
            try:
                self.stopPlayback()
            except:
                print traceback.print_exc()
            print 'Main video loop has closed.'

        print 'QUARK!'

    def setModifySpeed(self, speed):
        self.modifyspeed = speed
        #~ print 'mod:', speed

class Display:
    def __init__(self, fullscreen, player):
        self.player   = player
        pygame.init()
        self._fullscreen = fullscreen
        self.setDisplay(fullscreen)

    def setDisplay(self, fullscreen):
        if fullscreen:
            res = 1024, 768
            opts = pygame.FULLSCREEN | pygame.HWSURFACE
        else:
            res = 720, 528
            opts = 0
        pygame.display.set_mode(res, opts)
        #~ self.player.setOverlay( (0,0,res[0],res[1]) )

    def switchFullScreen(self):
        self._fullscreen = not self._fullscreen
        self.setDisplay(self._fullscreen)

EVT_KEYREPEAT = 31
class EventLoop:
    def __init__(self, display):
        self.display = display
        p = pygame
        self.keydown = []
        self.keyup   = []
        self.mousedown = []

        self.keydown.append(((p.K_ESCAPE,), self.exit))
        self.keydown.append(((p.K_a, p.K_s, p.K_d, p.K_f, p.K_j, p.K_k, p.K_l, 59), self.jumpTime))
        self.keydown.append(((p.K_g, p.K_h), self.jumpFrames))
        self.keydown.append(((p.K_1, p.K_2, p.K_3, p.K_4, p.K_5, p.K_6, p.K_7, p.K_8, p.K_9), self.loopPlayer))
        self.keydown.append(((p.K_z, p.K_x, p.K_c, p.K_v, p.K_b, p.K_n, p.K_m, 44, 46, 47), self.playKeyFrame))
        self.keydown.append(((p.K_0,), self.releasePlayer))
        #~ self.keydown.append(((p.K_F11,), self.switchFullScreen))
        self.keydown.append(((p.K_SPACE,), self.tapTempo))

        self.keydown.append(((p.K_PAUSE,), self.pause))
        #~ self.keydown.append(((p.K_PAGEUP, p.K_PAGEUP), self.frame))

        #~ self.keydown.append(((p.K_RETURN,), self.displayChess))
        #~ self.keydown.append(((p.K_RETURN,), self.jumpToLoopStart))
        self.keydown.append(((p.K_RETURN,), self.jumpToFrame_0))
        self.keydown.append(((92,), self.jumpToFrame_1))

        self.keydown.append(((p.K_F12,), self.saveFrame))
        self.keydown.append(((p.K_F11,), self.saveFrameReset))

        self.keydown.append(((p.K_r,),  self.record))

        self.keydown.append(((p.K_LEFT,),  self.slowDownDown))
        self.keyup.append  (((p.K_LEFT,),  self.slowDownUp))
        self.keydown.append(((p.K_RIGHT,), self.speedUpDown))
        self.keyup.append  (((p.K_RIGHT,), self.speedUpUp))
        self.leftisdown  = False
        self.rightisdown = False

        self.mousedown = []
        self.mousedown.append(((4,), self.frameForward))
        self.mousedown.append(((5,), self.frameBackward))
        self.modifyspeed = 1.

        pygame.time.set_timer(EVT_KEYREPEAT, 10)
        self.keyrepeatfuncs = []

        self._exit = False
        self._fullscreen = False
        self.lasttaps = None

        p = pygame
        bpm = 193.71881420
        fourth = 60/bpm
        sth    = fourth/4
        self._jumptime = {p.K_a: -fourth*4, p.K_s: -fourth*1,
                          p.K_d: -fourth/2, p.K_f: -fourth/4,
                          p.K_j:  fourth/4, p.K_k:  fourth/2,
                          p.K_l:  fourth*1, 59:  fourth*4 } #59 -> 'oe'

        self._jumpframe = {p.K_g: -1, p.K_h: 1}

        self._looptime = {p.K_1: sth*1, p.K_2: sth*2,
                          p.K_3: sth*3, p.K_4: sth*4,
                          p.K_5: sth*5, p.K_6: sth*6,
                          p.K_7: sth*7, p.K_8: sth*8,
                          p.K_9: sth*9 }

        self._keyframe = {p.K_z: 0, p.K_x: 1,
                          p.K_c: 2, p.K_v: 3,
                          p.K_b: 4, p.K_n: 5,
                          p.K_m: 6, 44:    7,
                          46:    8, 47:    9}

    def record(self, *key):
        self.player.record()

    def saveFrame(self, *key):
        self.player.saveFrame()

    def saveFrameReset(self, *key):
        self.player.saveFrameReset()

    def pause(self, *key):
        self.player.pause()

    def displayChess(self, *key):
        self.player.displayChess()

    def start(self, player):
        self.player = player
        while player.isPlaying()== 0:
            time.sleep( .05 )
        while player.isPlaying():
            e= pygame.event.wait()
            #~ print "EVENT:", e.type

            if e.type == pygame.KEYDOWN:
                #~ print 'keydown:', e.key
                for keygroup in self.keydown:
                    if e.key in keygroup[0]:
                        keygroup[1](e.key)

            if e.type == pygame.KEYUP:
                for keygroup in self.keyup:
                    if e.key in keygroup[0]:
                        keygroup[1](e.key)

            elif e.type == pygame.MOUSEBUTTONDOWN:
                for btngroup in self.mousedown:
                    if e.button in btngroup[0]:
                        btngroup[1](e.button)

            elif e.type == EVT_KEYREPEAT:
                for func in self.keyrepeatfuncs:
                    func()

            elif e.type == pygame.QUIT:
                self.exit()

            if self._exit:
                break

    def exit(self, key=None):
        self.player.stopPlayback()
        self._exit = True

    def quit(self):
        self._exit = True

    def jumpTime(self, key):
        self.player.jumpTime(self._jumptime[key])

    def jumpFrames(self, key):
        self.player.jumpFrames(self._jumpframe[key])

    def jumpToLoopStart(self, key):
        self.player.jumpToLoopStart()

    def jumpToFrame_0(self, key):
        self.player.jumpToFrame(271)

    def jumpToFrame_1(self, key):
        self.player.jumpToFrame(4004)

    def frameForward(self, *args):
        self.player.jumpFrames(1)

    def frameBackward(self, *args):
        self.player.jumpFrames(-1)

    def loopPlayer(self, key):
        self.player.loopHold(self._looptime[key])

    def playKeyFrame(self, key):
        self.player.playKeyFrame(self._keyframe[key])

    def releasePlayer(self, key):
        self.player.loopRelease()

    def slowDownDown(self, key):
        print 'slowDownDown'
        self.leftisdown   = True
        self.leftright    = 'left'
        self.modifySpeed()

    def slowDownUp(self, key):
        print 'slowDownUp'
        self.leftisdown   = False
        self.leftright    = 'right'

    def speedUpDown(self, key):
        print 'speedUpDown'
        self.rightisdown  = True
        self.leftright    = 'right'
        self.modifySpeed()

    def speedUpUp(self, key):
        print 'speedUpUp'
        self.rightisdown   = False
        self.leftright    = 'left'

    def modifySpeed(self):
        if not self.leftisdown and not self.rightisdown:
            self.player.setModifySpeed(1.)
            self.modifyspeed = 1.

            if self.modifySpeed in self.keyrepeatfuncs:
                self.keyrepeatfuncs.remove(self.modifySpeed)
            return

        if self.modifySpeed not in self.keyrepeatfuncs:
            self.keyrepeatfuncs.append(self.modifySpeed)

        if self.leftright == 'left':
            self.modifyspeed = max(self.modifyspeed * 0.995,     0.5)
        elif self.leftright == 'right':
            self.modifyspeed = min(self.modifyspeed * (1/0.995), 2.0)

        self.player.setModifySpeed(self.modifyspeed)

    def seek(self, key):
        pass

    def tapTempo(self, key):
        if self.lasttaps == None:
            self.lasttaps = []
        self.lasttaps.append(time.time())
        print "TAP! " * 20
        print self.lasttaps
        print "TAP! " * 20
        #~ self.display.switchFullScreen()

    def switchFullScreen(self, key):
        self.display.switchFullScreen()



########################################################################3
# Simple cache replacer for standalone testing
class Menu:
    NAME_KEY= 'name'
    class Cache:
        def open( self, f ):
            return open( f['name'], 'rb' )
        def getPathName( self, f ):
            return f[ 'name' ]
        def getExtension( self, f ):
            return f[ 'name' ].split( '.' )[ -1 ].lower()

    cache= Cache()

# Menu module instance for standalone testing
menu= Menu()

parser = OptionParser()
parser.add_option("--fullscreen", "-f", action="store_true", dest="fullscreen")
parser.add_option("--keyframes", "-k",  action="store_true", dest="keyframes")

print '-'*10
args = sys.argv[1:]
parsed = parser.parse_args(sys.argv[1:])
#~ print '>', parsed[0].fullscreen , '<'
#~ print parsed[1]
#~ sys.exit(0)

videofiles = {}

if (len(sys.argv )< 2 or len( sys.argv )> 3):
    print 'Usage: vplayer <file_name|v_id>'
    sys.exit(0)

videofile = sys.argv[1]
if videofile[:2] == 'v_':
    try:
        videofile = videofiles[videofile]
    except 'x':
        pass

fullscreen = parsed[0].fullscreen
#~ fullscreen = False

#~ playkeyframes = False
#~ playkeyframes = True

if fullscreen:
    res = 1024, 768
else:
    res = 720, 528

player= VPlayer(parsed[0].keyframes)
#~ player.record()

display = Display(fullscreen, player)
player.startPlayback( { 'name': videofile } )
player.start()
player.setOverlay( (0,0,res[0],res[1]) )

ev = EventLoop(display)
player.setEventLoop(ev)
ev.start(player)
