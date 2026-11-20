"""Render the same fixed Lantern shader used by the TouchDesigner project."""
from pathlib import Path
import argparse, json, subprocess, time, hashlib
from tempfile import TemporaryDirectory
import numpy as np
from PIL import Image
import moderngl as gl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VERTEX = '''#version 430
out vec2 uv; uniform vec2 uJitter;
void main(){vec2 b=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(b*2.-1.,0.,1.);uv=b+uJitter;}
'''

class Renderer:
    def __init__(self,width=1280,height=720,samples=1):
        self.size=width,height; self.samples=samples
        self.ctx=gl.create_standalone_context(require=430)
        source=(HERE/'lantern.glsl').read_text()
        self.p=self.ctx.program(vertex_shader=VERTEX,fragment_shader='#version 430\nuniform sampler2D atlasMap;\n#define FIELD atlasMap\nin vec2 uv;out vec4 frag;\n'+source+'\nvoid main(){frag=vec4(render(uv),1.);}')
        atlas=Image.open(HERE/'field.png').convert('RGBA')
        self.tex=self.ctx.texture(atlas.size,4,atlas.tobytes(),alignment=1)
        self.tex.filter=gl.LINEAR,gl.LINEAR;self.tex.repeat_x=False;self.tex.repeat_y=False;self.tex.use(0)
        self.color=self.ctx.texture(self.size,4,dtype='f2')
        self.fbo=self.ctx.framebuffer(color_attachments=[self.color]);self.vao=self.ctx.vertex_array(self.p,[])
    def image(self,phase=0.,mode=0,depth=0.,az=-58.,elev=34.,frame=4.65,exposure=1.15):
        self.p['uView'].value=phase,float(mode),exposure,self.size[0]/self.size[1]
        self.p['uStill'].value=depth,az,elev,frame
        self.fbo.use();self.fbo.clear()
        offsets={1:[(0,0)],2:[(-.25,-.25),(.25,.25)],4:[(-.25,-.25),(.25,-.25),(-.25,.25),(.25,.25)]}[self.samples]
        self.ctx.enable(gl.BLEND);self.ctx.blend_func=gl.ONE,gl.ONE
        self.p['uWeight'].value=1/self.samples
        for x,y in offsets:
            self.p['uJitter'].value=x/self.size[0],y/self.size[1]
            # Bound each GPU draw to avoid Windows display-driver watchdog resets.
            for j in range(0,self.size[1],192):
                for i in range(0,self.size[0],192):
                    self.ctx.scissor=i,j,min(192,self.size[0]-i),min(192,self.size[1]-j)
                    self.vao.render(vertices=3);self.ctx.finish()
        self.ctx.scissor=None;self.ctx.disable(gl.BLEND)
        if self.ctx.error!='GL_NO_ERROR': raise RuntimeError('OpenGL rendering error')
        return Image.frombytes('RGB',self.size,self.fbo.read(components=3,alignment=1)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    def close(self):
        for x in (self.vao,self.fbo,self.color,self.tex,self.p):x.release()
        self.ctx.release()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output',type=Path);ap.add_argument('--width',type=int,default=1280);ap.add_argument('--height',type=int,default=720)
    ap.add_argument('--samples',type=int,choices=[1,2,4],default=1);ap.add_argument('--seconds',type=float,default=48);ap.add_argument('--fps',type=int,default=24)
    ap.add_argument('--phase',type=float,default=0);ap.add_argument('--mode',type=int,choices=[0,1,2],default=0)
    ap.add_argument('--depth',type=float,default=0);ap.add_argument('--az',type=float,default=-58);ap.add_argument('--elev',type=float,default=34);ap.add_argument('--frame',type=float,default=4.65)
    ap.add_argument('--exposure',type=float,default=1.15);ap.add_argument('--cancel-file',type=Path)
    args=ap.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
    ren=Renderer(args.width,args.height,args.samples);start=time.time()
    print('GPU:',ren.ctx.info['GL_RENDERER'],flush=True)
    if args.output.suffix.lower()!='.mp4':
        ren.image(args.phase,args.mode,args.depth,args.az,args.elev,args.frame,args.exposure).save(args.output)
        print('Seconds:',round(time.time()-start,2),flush=True);ren.close();return
    import imageio_ffmpeg
    count=round(args.seconds*args.fps)
    cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{args.width}x{args.height}','-r',str(args.fps),'-i','-','-an','-c:v','libx264','-crf','17','-preset','medium','-threads','4','-pix_fmt','yuv420p','-movflags','+faststart',str(args.output)]
    hashes=[]
    with TemporaryDirectory(prefix='.lantern-',dir=args.output.parent) as work:
        partial=Path(work)/'film.mp4';cmd[-1]=str(partial)
        cancelled=False
        with subprocess.Popen(cmd,stdin=subprocess.PIPE) as encoder:
            for i in range(count):
                if args.cancel_file and args.cancel_file.exists():
                    cancelled=True;break
                im=ren.image(args.phase+i/count,args.mode,args.depth,args.az,args.elev,args.frame,args.exposure)
                data=im.tobytes();encoder.stdin.write(data)
                if i%args.fps==0 or i==count-1:
                    hashes.append(hashlib.sha256(data).hexdigest());print(f'{i+1}/{count} frames; {time.time()-start:.1f}s',flush=True)
            encoder.stdin.close()
            result=encoder.wait()
            if cancelled:
                ren.close();raise SystemExit(2)
            if result:raise RuntimeError('FFmpeg failed')
        partial.replace(args.output)
    receipt=dict(frames=count,fps=args.fps,seconds=args.seconds,width=args.width,height=args.height,samples=args.samples,gpu=ren.ctx.info['GL_RENDERER'],render_seconds=time.time()-start,sampled_frame_hashes=hashes,shader_sha256=hashlib.sha256((HERE/'lantern.glsl').read_bytes()).hexdigest(),sha256=hashlib.sha256(args.output.read_bytes()).hexdigest())
    args.output.with_suffix('.json').write_text(json.dumps(receipt,indent=2)+'\n')
    ren.close()

if __name__=='__main__':main()
