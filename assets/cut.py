from PIL import Image, ImageFilter
import numpy as np, os
from collections import deque
UP='/root/.claude/uploads/548336ff-5a63-5fce-8527-34f280241c58'

def flood_alpha(im, tol, shrink=640):
    im = im.copy(); im.thumbnail((shrink,shrink), Image.LANCZOS)
    a = np.asarray(im.convert('RGB')).astype(np.int16)
    H,W,_ = a.shape
    bg = np.zeros((H,W), bool); q = deque()
    for x in range(W):
        for y in (0,H-1):
            if not bg[y,x]: bg[y,x]=True; q.append((y,x))
    for y in range(H):
        for x in (0,W-1):
            if not bg[y,x]: bg[y,x]=True; q.append((y,x))
    while q:
        y,x = q.popleft(); c = a[y,x]
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx = y+dy, x+dx
            if 0<=ny<H and 0<=nx<W and not bg[ny,nx] and np.abs(a[ny,nx]-c).sum() <= tol:
                bg[ny,nx]=True; q.append((ny,nx))
    return im, Image.fromarray(((~bg).astype(np.uint8))*255)

def build(path, out, w, tol=12, q=82):
    im0 = Image.open(path)
    im, m = flood_alpha(im0, tol)
    m = m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))
    m = m.filter(ImageFilter.GaussianBlur(0.9))
    im = im.convert('RGBA'); im.putalpha(m)
    bb = im.getbbox()
    if bb: im = im.crop(bb)
    r = w/im.width
    im = im.resize((w, max(1,int(round(im.height*r)))), Image.LANCZOS)
    p = 'sp/'+out+'.webp'
    im.save(p,'WEBP',quality=q,method=6)
    return out, os.path.getsize(p), im.size

C='cells/'
SPEC = [
 (C+'iwashi.png',      'iwashi',     150,14),
 (C+'aji.png',         'aji',        150,14),
 (C+'tai.png',         'tai',        150,16),
 (C+'buri.png',        'buri',       150,14),
 ('rec/7c717f4191.jpeg','maguro',    150,14),
 (C+'boss_shark.png',  'bshark',     190,14),
 (C+'boss_octo.png',   'bocto',      180,16),
 (C+'boss_dragon.png', 'bdragon',    190,18),
 (C+'rare_octo.png',   'rocto',      150,16),
 (C+'rare_ray.png',    'rray',       150,16),
 (UP+'/569548d3-1000016702.png','rpuff',150,14),
 (C+'rock_blue.png',   'rockA',      160,14),
 (UP+'/cca4c74f-1000016700.png','rockB',160,11),
 (UP+'/03064125-1000016699.png','rockC',160,13),
 (C+'weed.png',        'weed',       104,14),
 (C+'coral.png',       'coral',      118,14),
 (C+'cloud.png',       'cloud',      168,14),
 (UP+'/f1c0fe23-1000016701.png','chest',124,13),
 (UP+'/20b39428-1000016698.png','lure', 56,13),
]
tot=0
for s in SPEC:
    n,sz,dim = build(*s); tot+=sz; print(f"{n:9s} {sz:6d}B {dim}")
print("TOTAL", tot)
