"""Rebuild the fixed depth-seven distance atlas used by the solid rendering.

Requires scipy in addition to visual-requirements.txt. The zero seed and grid
are preserved from the original study; this is a finite visual approximation.
"""
from pathlib import Path
import json
import numpy as np
from scipy.ndimage import distance_transform_edt, gaussian_filter
from PIL import Image

HERE=Path(__file__).resolve().parent
d=json.loads((HERE.parent/'math/data/reference.json').read_text(encoding='utf-8-sig'))
r=d['r'];q=np.array(d['Q']);t=np.array(d['T'])
p=np.zeros((1,3))
for _ in range(7):p=np.concatenate([r*p@qi.T+ti for qi,ti in zip(q,t)])
n=96;extent=2.22;fine=3*(n-1)+1
xyz=np.rint((p+extent)*(fine-1)/(2*extent)).astype(int)
assert xyz.min()>=0 and xyz.max()<fine
occupied=np.zeros((fine,)*3,dtype=bool);occupied[tuple(xyz[:,::-1].T)]=True
distance=distance_transform_edt(~occupied)[::3,::3,::3]*(2*extent/(fine-1))
density=gaussian_filter(np.exp(-(distance/.115)**2),1.8)
volume=np.stack([np.clip(distance/.8,0,1),np.clip(density,0,1)],axis=-1)
volume=np.rint(volume*255).astype(np.uint8)
a=volume.reshape(8,12,n,n,2).transpose(0,2,1,3,4).reshape(8*n,12*n,2)
rgba=np.zeros((*a.shape[:2],4),dtype=np.uint8);rgba[:,:,:2]=a;rgba[:,:,3]=255
Image.fromarray(rgba).save(HERE/'field.png')
print('Rebuilt 1152 x 768 RGBA atlas from the unchanged L3-30 maps.')
