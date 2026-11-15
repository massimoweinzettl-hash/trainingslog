import json,re,sys
bls=json.load(open('bls.json')); lib=json.load(open('lib.json'))
CATS=["Milchprodukte & Eier","Fleisch & Fisch","Kohlenhydrate","Obst & Gemüse","Fette & Nüsse","Supplements","Fertiges & Süßes","Getränke","Markenprodukte","Eigene"]
def norm(s):
    s=s.lower().replace('ß','ss').replace('ä','ae').replace('ö','oe').replace('ü','ue')
    return re.sub(r'[^a-z0-9 ]',' ',s)
STOP=set('und mit ohne aus in im vom von der die das ein eine natur stueck st ml roh gekocht gegart frisch scheibe scheiben portion becher glas dose tk klein gross mittel ca je pro eier ei2 groesse'.split())
def toks0(s): return [w for w in norm(re.sub(r'\([^)]*\)','',s)).split() if len(w)>2 and w not in STOP and not w.isdigit()]
def toks(s): return [p for w in toks0(s) for p in split(w)]
PROC='konserve nektar saft schorle kompott mehl pulver griess getrocknet brei mariniert sauce gefuellt paniert zubereitung creme salat'.split()
for b in bls: b['n']=norm(b['name']); b['w']=b['n'].split()
VOC=set(w for b in bls for w in b['w'] if len(w)>=4)
def split(t):
    if t in VOC or len(t)<8: return [t]
    for i in range(4,len(t)-3):
        a,r=t[:i],t[i:]
        for a2 in (a, a[:-1] if a[-1] in 'ens' else None, a[:-2] if a.endswith('en') else None):
            if a2 and a2 in VOC and (r in VOC or len(split(r))>1):
                return [a2]+(split(r) if r not in VOC else [r])
    return [t]
def dist(it,b):
    p,k,f,c=it[3],it[4],it[7] or 0,it[8] or 0
    if not b['ENERCC'] or b['PROT625'] is None or b['FAT'] is None or b['CHO'] is None: return 9
    if it[2]=='st':
        if not k: return 9
        s=b['ENERCC']/k; p,f,c,k=p*s,f*s,c*s,b['ENERCC']
    e=lambda a,bb,sc: abs(a-bb)/sc
    return e(k,b['ENERCC'],max(60,k*0.25))+e(p,b['PROT625'],max(3,p*0.25))+e(f,b['FAT'],max(3,f*0.3))+e(c,b['CHO'],max(4,c*0.3))
def nscore(tk,b):
    if not tk: return 0
    s=0
    for t in tk:
        best=0
        for w in b['w']:
            if w==t: best=1;break
            if len(t)>=4 and (w.startswith(t) or t.startswith(w) and len(w)>=4): best=max(best,0.8)
            elif len(t)>=5 and t in w: best=max(best,0.55)
            elif len(w)>=5 and w in t: best=max(best,0.5)
        s+=best
    return s/len(tk)
def best(it,n=3):
    tk=toks(it[1]); cat=CATS[it[6]] if isinstance(it[6],int) else ''
    raw='roh' in it[1] or cat in ('Obst & Gemüse',)
    out=[]
    for b in bls:
        ns=nscore(tk,b)
        if ns<0.5: continue
        sc=ns*4-dist(it,b)*0.8
        if b['code'][0] in 'XY' and cat!='Fertiges & Süßes': sc-=1.5
        if raw and ' roh' in ' '+b['n']: sc+=0.6
        nm=norm(it[1])
        sc-=0.8*sum(1 for w in PROC if w in b['n'] and w not in nm)
        sc-=0.02*len(b['w'])
        out.append((sc,b))
    out.sort(key=lambda x:-x[0]); return out[:n]
if __name__=='__main__':
    res={}
    for it in lib:
        bb=best(it)
        res[it[0]]=[[b['code'],b['name'],round(s,2),round(dist(it,b),2)] for s,b in bb]
    json.dump(res,open('cand2.json','w'),ensure_ascii=False)
    for it in lib:
        r=res[it[0]]
        print('%s|%s|%s %s/%s/%s/%s|%s'%(it[0],it[1],it[2],it[4],it[3],it[7],it[8],' ## '.join('%s %s d%.1f'%(x[0],x[1][:42],x[3]) for x in r[:2])))
