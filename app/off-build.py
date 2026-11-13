import json,re,sys,unicodedata
d=json.load(open('/home/claude/work/off/p.json'))
pr=d['products']
DE_BR=set(x.lower() for x in ["Coca-Cola","Fanta","alpro","Barilla","Ferrero","Nutella","Kinder","Heinz","Red Bull","Oatly","Lindt","Pringles","Mutti","Kikkoman","Milka","Haribo","Ritter Sport","Knorr","Maggi","Dr. Oetker","Ehrmann","Müller","Weihenstephan","Zott","Bahlsen","Leibniz","Kellogg's","Nestlé","Danone","Philadelphia","Snickers","Twix","Mars","Bounty","Kitkat","Toffifee","Hanuta","Duplo","Seeberger","Alnatura","Rewe","ja!","Gut & Günstig","Pepsi","Monster","Capri-Sun","Paulaner","Club-Mate","Evian","Volvic","Vita Coco","Kania","Freshona","Milbona","Alesto","Crownfield","Maribel","Vemondo","Solevita","Naturis","Primadonna","Combino","Italiamo","Lidl","Kong Strong","esn","more nutrition","Ültje","Funny-frisch","Lorenz","Iglo","Frosta","Wagner","Garden Gourmet","Rügenwalder Mühle","Exquisa","Arla","Almighurt","Landliebe","Bärenmarke","Kerrygold","Rama","Becel","Thomy","Kühne","Develey","Hela","Hengstenberg","Baut'zner","Kölln","Seitenbacher","dmBio","Tasty","Hohes C","Valensina","Lotus","Oreo","TUC","Baresa","Tastino","Sol&Mar","McEnnedy","Rivercote","Gräfschafter","Dr. August Oetker Nahrungsmitt","COCA-COLA SERVICES SA/NV","Coca-Cola Company","Red Bull GmbH","Danone Belux nv","Oatly EMEA AB"])
FR=re.compile(r"(\b(de|du|des|le|la|les|au|aux|et|avec|sans|noir|lait|chocolat|pâte|huile|crème|sucre|fromage|biscuits?|con|sin|y|el|leche|zumo|aceite|yogur|copos|avena|crema|verse|levure|beurre|tranché[e]?|cuisinée|saveur)\b|[éèêàç])",re.I)
DEW=re.compile(r"[äöüß]|\b(mit|ohne|und|vollkorn|schokolade|milch|käse|hafer|nüsse|kerne|brot|saft|joghurt|quark|wurst|sauce|soße|getränk|drink|nudeln|toast|pudding|kefir|müsli|flocken|zartbitter|vollmilch|edelbitter|tomaten|thunfisch)\b",re.I)
def show(x):
    code,name,br=x[0],x[1],x[2].lower()
    if FR.search(name) and not DEW.search(name): return False
    if DEW.search(name): return True
    if code[:2] in ("40","41","42","43","44") or (len(code)==8 and code[0]=="2"): return True
    return br in DE_BR
def clean(n):
    n=re.sub(r"&amp;","&",n)
    n=re.sub(r"\s*[-–,]?\s*\d+([.,]\d+)?\s*(g|kg|ml|l|cl|lt|liter)\b\.?","",n,flags=re.I)
    n=re.sub(r"\s*\d+\s*x\s*\d*\s*$","",n,flags=re.I)
    n=re.sub(r"\s+"," ",n).strip(" -–,")
    return n[:50]
def norm(s): return unicodedata.normalize('NFKD',s.lower()).encode('ascii','ignore').decode()
seen=set(); out=[]; nshow=0
for x in pr:
    code,name,brand,per,p,kcal,f,c,port=x
    if not re.fullmatch(r"\d{8,14}",code): continue
    nm=clean(name)
    if len(nm)<2: continue
    br=brand.strip()
    BM={"danone belux nv":"Alpro","alpro":"Alpro","coca-cola services sa/nv":"Coca-Cola","coca-cola company":"Coca-Cola","red bull gmbh":"Red Bull","oatly emea ab":"Oatly","dr. august oetker nahrungsmitt":"Dr. Oetker","kikkoman foods europe b.v.":"Kikkoman","lidl":"Lidl","mondelēz":"Mondelez","the jordans & ryvita company l":"Jordans","monster beverage corporation":"Monster","the vita coco company inc.":"Vita Coco","mccennedy":"McEnnedy","mcennedy":"McEnnedy","les éleveurs vous disent merci":"Merci"}
    br=BM.get(br.lower(),br)
    if br and len(br)>22: br=br.split()[0]
    if br and nm.lower()==br.lower(): br=""
    s=1 if show(x) else 0
    key=norm(nm+"|"+br)
    if s and key in seen: s=0
    if s: seen.add(key); nshow+=1
    amt=port if 0<port<=1000 else 100
    out.append([code,nm,br,per,p,kcal,f,c,amt,s])
print(len(out),"gesamt,",nshow,"in der Suche",file=sys.stderr)
js=",".join(json.dumps(r,ensure_ascii=False,separators=(",",":")) for r in out)
open('/home/claude/work/off/prod.js','w').write("["+js+"]")
