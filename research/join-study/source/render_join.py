"""Reproduce the local join images from the preserved Lantern field.

The static study shader adds root-piece masking, diagnostic colours and
halfspace clipping to the original Sixfold-style solid renderer. No original
geometry file or publication asset is modified. These are finite envelopes.
"""
from pathlib import Path
import argparse,hashlib,json,time
import moderngl as gl
from PIL import Image

STUDY=Path(__file__).resolve().parents[1]
ROOT=STUDY.parents[1]
# Same full-screen triangle and subpixel jitter as the original renderer.
VERTEX='''#version 430
out vec2 uv; uniform vec2 uJitter;
void main(){vec2 b=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(b*2.-1.,0.,1.);uv=b+uJitter;}
'''

class Renderer:
    def __init__(self,width=1100,height=880,samples=2):
        self.size=width,height;self.samples=samples
        self.ctx=gl.create_standalone_context(require=430)
        self.p=self.ctx.program(vertex_shader=VERTEX,fragment_shader=(STUDY/'source/join.glsl').read_text())
        atlas=Image.open(ROOT/'visuals/field.png').convert('RGBA')
        self.tex=self.ctx.texture(atlas.size,4,atlas.tobytes(),alignment=1)
        self.tex.filter=gl.LINEAR,gl.LINEAR;self.tex.use(0)
        self.color=self.ctx.texture(self.size,4,dtype='f2')
        self.fbo=self.ctx.framebuffer(color_attachments=[self.color]);self.vao=self.ctx.vertex_array(self.p,[])

    def image(self,composition):
        c=composition['camera'];args=composition['parameters'];p=self.p
        for field in ('Centre','Right','Up','Sight'):p['u'+field].value=tuple(c[field.lower()])
        for key,value in [('uFrame',c['frame']),('uScale',c['scale']),('uAspect',self.size[0]/self.size[1]),
                          ('uExposure',1.3),('uWeight',1/self.samples),('uThickness',args.get('thickness',1))]:p[key].value=value
        for key,value in [('uNeutral',0),('uMask',args.get('mask',3)),('uMode',args.get('mode',1)),
                          ('uCut',args.get('cut',0)),('uSecond',args.get('second',-1))]:p[key].value=value
        self.fbo.use();self.fbo.clear();self.ctx.enable(gl.BLEND);self.ctx.blend_func=gl.ONE,gl.ONE
        offsets={1:[(0,0)],2:[(-.25,-.25),(.25,.25)],4:[(-.25,-.25),(.25,-.25),(-.25,.25),(.25,.25)]}[self.samples]
        for x,y in offsets:
            p['uJitter'].value=x/self.size[0],y/self.size[1]
            for j in range(0,self.size[1],160):
                for i in range(0,self.size[0],160):
                    self.ctx.scissor=i,j,min(160,self.size[0]-i),min(160,self.size[1]-j)
                    self.vao.render(vertices=3);self.ctx.finish()
        self.ctx.scissor=None;self.ctx.disable(gl.BLEND)
        if self.ctx.error!='GL_NO_ERROR':raise RuntimeError('OpenGL rendering error')
        return Image.frombytes('RGB',self.size,self.fbo.read(components=3,alignment=1)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    def close(self):
        for obj in (self.vao,self.fbo,self.color,self.tex,self.p):obj.release()
        self.ctx.release()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=ROOT/'.build/join-study')
    args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    compositions=json.loads((STUDY/'data/render-compositions.json').read_text())
    ren=Renderer();started=time.monotonic();hashes={}
    try:
        for name,camera in compositions.items():
            path=args.output/(name+'.png');ren.image(camera).save(path)
            hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest();print('Rendered',name,flush=True)
        receipt=dict(gpu=ren.ctx.info['GL_RENDERER'],dimensions=list(ren.size),samples=ren.samples,
                     shader_sha256=hashlib.sha256((STUDY/'source/join.glsl').read_bytes()).hexdigest(),
                     original_field_sha256=hashlib.sha256((ROOT/'visuals/field.png').read_bytes()).hexdigest(),
                     image_sha256=hashes,seconds=time.monotonic()-started)
        (args.output/'render-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    finally:ren.close()

if __name__=='__main__':main()
