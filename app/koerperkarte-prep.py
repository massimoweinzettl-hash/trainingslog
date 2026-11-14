from PIL import Image, ImageDraw, ImageFilter
import numpy as np, json
im=Image.open('src.png').convert('RGB'); A=np.asarray(im).astype(float)
H=1100
GR={"Brust":1,"Rücken":2,"Schultern":3,"Arme":4,"Bauch":5,"Beine":6}
def mirror(poly,cx): return [(2*cx-x,y) for x,y in poly]
F=327; B=984
front={
 "Schultern":[(205,148),(160,160),(138,195),(136,245),(152,272),(178,262),(200,232),(208,190),(218,158)],
 "Brust":[(218,155),(327,160),(327,282),(268,282),(232,266),(208,240),(204,232),(208,190)],
 "Arme":[(136,245),(152,272),(178,262),(200,232),(204,232),(203,300),(201,400),(198,545),(70,545),(75,420),(95,320),(118,262)],
 "Bauch":[(208,240),(232,266),(268,282),(327,282),(327,505),(285,480),(245,450),(222,425),(201,400),(203,300),(204,232)],
 "Beine":[(222,425),(245,450),(285,480),(327,505),(327,1100),(140,1100),(195,700),(200,560),(205,440)],
}
back={
 "Schultern":[(872,150),(830,160),(800,188),(793,240),(812,268),(840,262),(862,240),(868,200),(880,165)],
 "Rücken":[(940,85),(984,80),(984,468),(930,462),(885,452),(860,420),(858,350),(864,300),(862,240),(868,200),(880,165),(872,150),(905,135),(935,115)],
 "Arme":[(793,240),(812,268),(840,262),(862,240),(864,300),(858,350),(856,420),(850,545),(730,545),(740,420),(758,320),(775,262)],
 "Beine":[(860,420),(885,452),(930,462),(984,468),(984,1100),(800,1100),(840,700),(845,560),(855,440)],
}
lab=Image.new('L',im.size,0); d=ImageDraw.Draw(lab)
for defs,cx in [(front,F),(back,B)]:
  for g,poly in defs.items():
    d.polygon(poly,fill=GR[g]); d.polygon(mirror(poly,cx),fill=GR[g])
L=np.asarray(lab)
R,G,Bc=A[...,0],A[...,1],A[...,2]
mx=A.max(2); mn=A.min(2); sat=(mx-mn)/np.maximum(mx,1)
lum=0.3*R+0.59*G+0.11*Bc
t=np.clip((sat-0.33)/0.2,0,1)  # Muskelanteil
# Hintergrund: Flutfüllung heller Pixel vom Rand
from collections import deque
h,w=mn.shape; bg=np.zeros((h,w),bool); light=mn>232
q=deque([(0,0),(0,w-1),(h-1,0),(h-1,w-1)])
for y,x in q: bg[y,x]=True
while q:
  y,x=q.popleft()
  for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
    yy,xx=y+dy,x+dx
    if 0<=yy<h and 0<=xx<w and not bg[yy,xx] and light[yy,xx]: bg[yy,xx]=True; q.append((yy,xx))
bg[1095:,:]=True
alpha=np.asarray(Image.fromarray((~bg*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(float)
mus=(t>0.8)&~bg; ten=(t<0.1)&~bg
Lm=np.percentile(lum[mus],70); Lt=np.percentile(lum[ten],70)
print('Lm',Lm,'Lt',Lt,'unlabeled muscle px',int(((L==0)&mus).sum()))

def cat2(img):
  f=img.crop((95,0,560,H)); b=img.crop((750,0,1215,H))
  c=Image.new(img.mode,(f.width*2+10,H)); c.paste(f,(0,0)); c.paste(b,(f.width+10,0)); return c
SC=0.65
lumI=cat2(Image.fromarray(np.clip(lum,0,255).astype(np.uint8),'L')); W2,H2=int(lumI.width*SC),int(H*SC)
lumI=lumI.resize((W2,H2),Image.LANCZOS)
labI=cat2(Image.fromarray((L*32).astype(np.uint8),'L')).resize((W2,H2),Image.NEAREST)
tI=cat2(Image.fromarray((t*255).astype(np.uint8),'L')).resize((W2,H2),Image.LANCZOS)
aI=cat2(Image.fromarray(alpha.astype(np.uint8),'L')).resize((W2,H2),Image.LANCZOS)
# Luminanz in den Blaukanal der PNG (nur wo sichtbar), dann alles in einer Datei
la=np.asarray(lumI).copy(); la[np.asarray(aI)==0]=0
m=Image.merge("RGB",(labI,tI,aI)); m.save('koerper.png',optimize=True)
Image.fromarray(la).save('lum.jpg',quality=80)
json.dump({"Lm":round(Lm,1),"Lt":round(Lt,1),"w":W2,"h":H2},open('meta.json','w'))
pal=np.array([[0,0,0],[220,40,40],[40,120,220],[240,180,0],[40,180,90],[160,60,200],[0,180,200]],np.uint8)
ctl=(A*0.5+pal[L]*0.5).astype(np.uint8); Image.fromarray(ctl).resize((656,600)).save('ctl_s.png')
