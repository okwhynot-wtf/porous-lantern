"""Install the publication's isolated native TouchDesigner studio."""
from pathlib import Path
import json,hashlib

def install(folder,name='PorousLanternRelease'):
    folder=Path(folder).resolve();root=op('/project1')
    b=root.op(name) or root.create(baseCOMP,name)
    if b.op('actions') and getattr(b.op('actions').module,'job',None):
        raise RuntimeError('Finish or cancel the active Lantern export first.')
    b.nodeX=700;b.nodeY=-300;b.viewer=False
    def node(kind,name,parent=b):return parent.op(name) or parent.create(kind,name)
    for old in b.customPages:old.destroy()
    motion=b.appendCustomPage('View');export=b.appendCustomPage('Export')
    p=motion.appendMenu('View',label='Composition')[0]
    p.menuNames=['hero','film','front','side','back','detail','zoom'];p.menuLabels=['Hero','Film','Mirror','Profile','Reverse','Interface','Within'];p.val='hero'
    p=motion.appendFloat('Phase',label='Film phase')[0];p.val=0;p.min=0;p.max=1;p.clampMin=p.clampMax=True
    motion.appendToggle('Play',label='Play camera')[0].val=False
    p=motion.appendFloat('Exposure')[0];p.val=1.3;p.min=.2;p.max=3
    motion.appendPulse('Openstudio',label='Open studio')
    export.appendFolder('Destination',label='Save folder')[0].val='../exports'
    export.appendFile('Ffmpeg',label='FFmpeg executable')[0].val=''
    export.appendPulse('Savestill',label='Save still')
    export.appendPulse('Renderloop',label='Render 24 second loop')
    export.appendPulse('Cancelrender',label='Cancel export')
    p=export.appendStr('Status')[0];p.val='Ready';p.readOnly=True
    a=node(moviefileinTOP,'reference_field')
    if not a.lock:
        a.par.file=(folder/'visuals/field.png').as_posix();a.par.inputcolorspace='passthrough';a.par.play=False
        a.par.reloadpulse.pulse();a.cook(force=True)
    s=node(glslTOP,'sculpture');s.viewer=False
    s.par.pixeldat.eval().text=(folder/'visuals/lantern.glsl').read_text(encoding='utf-8')
    s.inputConnectors[0].connect(a);s.par.outputresolution='custom';s.par.resolutionw=640;s.par.resolutionh=360
    s.par.inputfiltertype='linear';s.seq.vec.numBlocks=6
    output=node(nullTOP,'view');output.inputConnectors[0].connect(s);output.viewer=False;b.par.opviewer=output
    actions=node(textDAT,'actions');actions.text=(folder/'touchdesigner/actions.py').read_text(encoding='utf-8')
    studio=node(containerCOMP,'studio');studio.par.w=1200;studio.par.h=640
    picture=node(containerCOMP,'preview',studio);picture.par.w=800;picture.par.h=640;picture.par.top=output
    picture.par.topfill='best';picture.par.bgalpha=1
    controls=node(parameterCOMP,'settings',studio);controls.par.x=800;controls.par.w=400;controls.par.h=640
    controls.par.op=b;controls.par.builtin=False;controls.par.custom=True;controls.par.header=False
    controls.par.pagenames=True;controls.par.allowexpand=False;controls.par.pagescope='View Export'
    window=node(windowCOMP,'studio_window');window.par.winop=studio;window.par.title='Porous Lantern Studio'
    window.par.justifyh='center';window.par.justifyv='center';window.par.borders=True;window.par.cursorvisible='alwaysvisible'
    events=node(parameterexecuteDAT,'events');events.par.op=b;events.par.pars='View Phase Exposure Openstudio Savestill Renderloop Cancelrender'
    events.par.valuechange=True;events.par.onpulse=True
    events.text='''def onValueChange(par,prev):
    if par.name in ('View','Phase','Exposure'):parent().op('actions').module.preview()
def onPulse(par):
    a=parent().op('actions').module
    callbacks={'Openstudio':a.open_studio,'Savestill':a.save_still,'Renderloop':a.start_movie,'Cancelrender':a.cancel}
    if par.name in callbacks:callbacks[par.name]()
'''
    clock=node(executeDAT,'camera_clock');clock.par.framestart=True;clock.par.start=True
    clock.text='''def onFrameStart(frame):
    b=parent()
    if b.par.Play and b.op('actions').module.job is None:
        if b.par.View!='film':b.par.View='film'
        b.par.Phase=(absTime.seconds/24.)%1.
def onStart():
    run("op(args[0]).module.preview()",parent().op('actions').path,delayFrames=3)
'''
    receipt=node(textDAT,'asset_manifest')
    receipt.text=json.dumps({'geometry':'D=(f0K intersect x>=y) union (f1K intersect x<=y)',
        'renderer':'Native TouchDesigner GLSL TOP','film':{'seconds':24,'fps':24,'width':1280,'height':720,'samples':2},
        'shader_sha256':hashlib.sha256((folder/'visuals/lantern.glsl').read_bytes()).hexdigest(),
        'atlas_sha256':hashlib.sha256((folder/'visuals/field.png').read_bytes()).hexdigest()},indent=2)
    for i,n in enumerate(b.children):n.nodeX=(i%4)*200;n.nodeY=-(i//4)*150
    b.currentPage='View'
    run("a=op(args[0]);a.cook(force=True);assert a.width==1152 and float(a.numpyArray().max())>0;a.lock=True;a.par.file='../visuals/field.png';op(args[1]).module.preview()",a.path,actions.path,delayFrames=3)
    return b

if 'LANTERN_DIR' in globals():install(LANTERN_DIR)
