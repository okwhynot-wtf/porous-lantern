"""Native TouchDesigner TOP renderer. FFmpeg only encodes finished RGB frames."""
from pathlib import Path
import json, math, shutil, struct, subprocess, time, traceback, zlib
import numpy as np
FACTOR=1.7579924420999498
job=None
def owner():return me.parent()
def camera(phase=0.,preset='hero'):
    p=float(phase)%1.;c=dict(az=45.,elev=50.,centre=[.50,.50,.15],frame=1.25)
    if preset=='film':
        z=math.sin(math.pi*p)**2
        c.update(az=45.-24.*math.sin(2.*math.pi*p),elev=50.+8.*math.sin(2.*math.pi*p),frame=1.25-.48*z,
                 centre=[.50-.0434*z,.50-.0434*z,.15+.07288*z])
    elif preset=='front':c.update(frame=1.5)
    elif preset=='side':c.update(az=12.,elev=30.,frame=1.4)
    elif preset=='back':c.update(az=225.,elev=-40.,frame=1.4)
    elif preset=='detail':c.update(centre=[.4565946,.4565946,.22288254],frame=.85)
    elif preset=='zoom':
        q=np.array([[.659739608441,.592752310333,.461939766256],[-.726726906549,.659739608441,.191341716183],[-.191341716183,-.461939766256,.866025403784]])
        t=np.array([1.277580409184,.529191132506,.139332035968])/FACTOR;r=math.sqrt(2.)-1.
        c.update(az=-58.,elev=34.,centre=(t+r*q@t).tolist(),frame=2.7*r*r,turn=(q@q).tolist())
    a,e=math.radians(c['az']),math.radians(c['elev'])
    sight=np.array([math.cos(a)*math.cos(e),math.sin(a)*math.cos(e),math.sin(e)])
    right=np.array([-math.sin(a),math.cos(a),0.]);up=np.cross(sight,right)
    if 'turn' in c:
        q=np.array(c['turn']);sight=q@sight;right=q@right;up=q@up
    frame=c['frame']*FACTOR
    return dict(centre=np.array(c['centre'])*FACTOR,right=right,up=up,sight=sight,frame=frame,scale=frame/4.65,settings=c)
def set_camera(cam,width,height,tile=(0,0,1,1)):
    values={'uCentre':cam['centre'],'uRight':cam['right'],'uUp':cam['up'],'uSight':cam['sight'],
            'uSettings':(cam['frame'],width/height,job['exposure'] if job else float(owner().par.Exposure),cam['scale']),'uTile':tile}
    s=owner().op('sculpture')
    for i,(name,value) in enumerate(values.items()):
        b=s.seq.vec[i];b.par.name=name
        for channel,x in zip('xyzw',value):getattr(b.par,'value'+channel).val=float(x)
def png(path,rgb):
    h,w,_=rgb.shape
    def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    rows=b''.join(b'\0'+row.tobytes() for row in rgb)
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>2I5B',w,h,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(rows,6))+chunk(b'IEND',b''))
def render(width,height,preset='hero',phase=0.,samples=1):
    """Bound GPU work to 320x180 tiles, with a synchronous read per tile."""
    s=owner().op('sculpture');cam=camera(phase,preset);img=np.zeros((height,width,3),dtype=np.float32)
    offsets=[(0.,0.)] if samples==1 else [(-.25,-.25),(.25,.25)]
    for ox,oy in offsets:
        for y in range(0,height,180):
            for x in range(0,width,320):
                w,h=min(320,width-x),min(180,height-y);s.par.resolutionw=w;s.par.resolutionh=h
                set_camera(cam,width,height,((x+ox)/width,(y+oy)/height,w/width,h/height));s.cook(force=True)
                if s.errors():raise RuntimeError(s.errors())
                img[y:y+h,x:x+w]+=s.numpyArray(delayed=False)[:,:,:3]
    return np.round(np.clip(img[::-1]/len(offsets),0,1)*255).astype(np.uint8)
def preview():
    if job is not None:return
    b=owner();s=b.op('sculpture');s.par.resolutionw=640;s.par.resolutionh=360
    set_camera(camera(float(b.par.Phase),b.par.View.eval()),640,360);s.cook(force=True);b.op('view').cook(force=True)
def status(message):owner().par.Status.val=message
def encoder():
    configured=owner().par.Ffmpeg.eval()
    found=configured if configured and Path(configured).is_file() else shutil.which('ffmpeg')
    if not found:raise RuntimeError('Set Export > FFmpeg executable to an installed ffmpeg executable.')
    return found
def begin(destination,kind='movie',width=1280,height=720,seconds=24,fps=24,samples=2):
    global job
    if job is not None:raise RuntimeError('An export is already running.')
    exe=encoder() if kind=='movie' else None
    target=Path(destination);target.parent.mkdir(parents=True,exist_ok=True)
    job=dict(kind=kind,target=target,width=width,height=height,seconds=seconds,fps=fps,samples=samples,
             frame=0,frames=int(round(seconds*fps)) if kind=='movie' else 1,start=time.perf_counter(),cancel=False,
             exposure=float(owner().par.Exposure),view=owner().par.View.eval(),phase=float(owner().par.Phase))
    if kind=='movie':
        job['log']=open(str(target)+'.log','w')
        args=[exe,'-y','-v','warning','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{height}',
              '-r',str(fps),'-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','17','-threads','2',
              '-pix_fmt','yuv420p','-movflags','+faststart',str(target)]
        job['process']=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=job['log'],stdout=subprocess.DEVNULL,
                                        creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    status('Rendering native TOP frames');run("op(args[0]).module.tick()",me.path,delayFrames=1)
def tick():
    global job
    if job is None:return
    try:
        j=job
        if j['cancel']:
            if j.get('process'):j['process'].terminate();j['log'].close()
            job=None;status('Cancelled');preview();return
        preset='film' if j['kind']=='movie' else j['view']
        phase=j['frame']/j['frames'] if j['kind']=='movie' else j['phase']
        rgb=render(j['width'],j['height'],preset,phase,j['samples'])
        if j['kind']=='movie':j['process'].stdin.write(rgb.tobytes())
        else:png(j['target'],rgb)
        j['frame']+=1;elapsed=time.perf_counter()-j['start'];status(f"Rendering {j['frame']}/{j['frames']} · {elapsed:.0f}s")
        if j['frame']>=j['frames']:
            if j.get('process'):
                j['process'].stdin.close();code=j['process'].wait(timeout=30);j['log'].close()
                if code:raise RuntimeError(f'FFmpeg exited with code {code}')
            receipt={k:v for k,v in j.items() if k not in ('process','log','start','cancel')}
            receipt.update(target=str(j['target']),elapsed_seconds=elapsed,renderer='TouchDesigner GLSL TOP',build=str(app.build),tile_pixels=[320,180],geometry='D: two mirrored halfspace-trimmed cells')
            Path(str(j['target'])+'.json').write_text(json.dumps(receipt,indent=2)+'\n')
            job=None;status('Complete');preview()
        else:run("op(args[0]).module.tick()",me.path,delayFrames=1)
    except Exception:
        error=traceback.format_exc()
        if job and job.get('process'):job['process'].terminate();job['log'].close()
        if job:Path(str(job['target'])+'.error.txt').write_text(error)
        job=None;status('Export failed; see error log');print(error)
def start_movie():
    folder=Path(owner().par.Destination.eval()).resolve();p=folder/'Porous-Lantern-Mirrored-Form.mp4'
    if p.exists():p=folder/('Porous-Lantern-'+time.strftime('%Y%m%d-%H%M%S')+'.mp4')
    begin(p)
def save_still():
    folder=Path(owner().par.Destination.eval()).resolve()
    begin(folder/('Porous-Lantern-'+time.strftime('%Y%m%d-%H%M%S')+'.png'),kind='still',width=1920,height=1080)
def cancel():
    if job is not None:job['cancel']=True
def open_studio():preview();owner().op('studio_window').par.winopen.pulse()
