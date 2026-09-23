from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
S='/tmp/claude-0/-home-user-hair-salon-site/4b29f3cd-44e3-538d-bc38-b6c5cbfe1d8e/scratchpad'
im=Image.open('/tmp/claude-0/-home-user-hair-salon-site/4b29f3cd-44e3-538d-bc38-b6c5cbfe1d8e/images/10.webp').convert('RGB')
a=np.asarray(im).astype(float); H,W=a.shape[:2]
R,G,B=a[...,0],a[...,1],a[...,2]
subj=((G-R)+0.5*(B-R))<14
lim=Image.new('L',(W,H),255)
ImageDraw.Draw(lim).polygon([(0,0),(440,0),(380,450),(345,560),(333,690),(343,800),(350,870),(318,960),(280,1080),(262,1250),(212,1430),(150,1690),(90,2000),(0,2000)],fill=0)
subj&=np.asarray(lim)>0
subj=ndimage.binary_opening(subj,iterations=3)
subj=ndimage.binary_closing(subj,iterations=12)
subj=ndimage.binary_fill_holes(subj)
lab,n=ndimage.label(subj); sz=ndimage.sum(subj,lab,range(1,n+1)); subj=lab==(np.argmax(sz)+1)
# широкое растворение края: внутрь от границы ~70px
core=ndimage.binary_erosion(subj,iterations=6)
din=ndimage.distance_transform_edt(core)
dout,idx=ndimage.distance_transform_edt(~core,return_indices=True)
# снаружи силуэта продолжаем цвета края (без бирюзовой стены), затем растворяем
a=a[idx[0],idx[1]]
a=np.stack([ndimage.gaussian_filter(a[...,k],np.where(True,1,1)*0.0+0) for k in range(3)],-1) if False else a
soft=np.stack([ndimage.gaussian_filter(a[...,k],18) for k in range(3)],-1)
w=np.clip(dout/25,0,1)[...,None]
a=a*(1-w)+soft*w
R,G,B=a[...,0],a[...,1],a[...,2]
alpha=np.where(core,1.0,np.clip(1-dout/60,0,1)**2)
alpha=ndimage.gaussian_filter(alpha,14)
# низ растворяется в фон сайта
yy=np.arange(H)[:,None]
alpha*=np.clip((2000-yy)/620,0,1)**1.6
# цвет: чуть теплее и спокойнее, под шалфей/беж
lum=a.mean(2,keepdims=True)
c=a*0.85+lum*0.15
c=c*np.array([1.02,1.0,0.94])
rgba=np.dstack([c.clip(0,255),(alpha*255)]).astype(np.uint8)
out=Image.fromarray(rgba,'RGBA').crop((180,330,W,H))
out=out.resize((int(out.width*0.62),int(out.height*0.62)),Image.LANCZOS)
o=np.asarray(out).astype(float); h,w=o.shape[:2]
xx=np.arange(w)[None,:]; yy2=np.arange(h)[:,None]
edge=np.clip((w-1-xx)/110,0,1)**1.5*np.clip(yy2/60,0,1)*np.clip(xx/40,0,1)
o[...,3]*=edge
out=Image.fromarray(o.clip(0,255).astype(np.uint8),'RGBA')
out.save('img/hero.png',optimize=True)
bg=Image.new('RGBA',out.size,(142,150,121,255)); bg.alpha_composite(out); bg.convert('RGB').save(S+'/hero10-prev.png')
print(out.size)
