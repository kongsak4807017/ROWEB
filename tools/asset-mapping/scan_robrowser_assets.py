#!/usr/bin/env python3
"""Scan roBrowserLegacy sources and emit deterministic asset/domain mapping JSON."""
from __future__ import annotations
import argparse, hashlib, json, re
from collections import defaultdict
from pathlib import Path

TEXT_EXT={'.js','.ts','.jsx','.tsx','.css','.html','.json','.xml','.lua','.txt','.frag','.vert'}
DEFAULT_ASSET_EXT='bmp|tga|png|jpg|jpeg|gif|webp|svg|spr|act|rsw|gnd|gat|rsm|str|wav|mp3|ogg|xml|lua|bson|grf'
REF_RE=re.compile(rf"(?P<path>(?:data/|assets?/|client/|texture/|sprite/|wav/|bgm/|effect/|model/|map/)?[^\s\"'`<>]+?\.(?:{DEFAULT_ASSET_EXT}))",re.I)

def normalize_path(value:str)->str:
    return re.sub(r'/+','/',value.replace('\\','/').strip(' \t\r\n\"\'`;,()')).lower()

def classify(path:str)->str:
    p=normalize_path(path)
    if re.search(r'ui/|interface|유저인터페이스|cursor|button|window|icon',p): return 'UI'
    if re.search(r'\.(rsw|gnd|gat|rsm)$|map/',p): return 'Map'
    if re.search(r'\.(spr|act)$|monster|npc|job|sprite/',p): return 'Entity'
    if re.search(r'\.str$|effect/',p): return 'Effect'
    if re.search(r'\.(wav|mp3|ogg)$|bgm/|audio/|sound/',p): return 'Audio'
    return 'Data'

def logical_id(path:str)->str:
    p=re.sub(r'[^a-z0-9]+','.',normalize_path(path)).strip('.')
    p=re.sub(r'^(data|assets?|client)\.','',p)
    c=classify(path).lower()
    return p if p.startswith(c+'.') else f'{c}.{p}'

def rathena_domains(path:str, consumers:list[str])->list[str]:
    hay=' '.join([normalize_path(path),*(normalize_path(x) for x in consumers)])
    rules={'item':['item_db','iteminfo','collection','item/'],'monster':['mob_db','monster','mob/'],'skill':['skill_db','skillinfo','skill/'],'map':['mapindex','maps/','.rsw','.gnd','.gat'],'npc':['npc','npcidentity'],'job':['jobidentity','jobname','sprite/']}
    return sorted(k for k, pats in rules.items() if any(x in hay for x in pats))

def scan(root:Path)->dict:
    refs:dict[str,dict]={}
    files=[]
    for f in sorted(p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in TEXT_EXT):
        rel=f.relative_to(root).as_posix()
        try: text=f.read_text('utf-8',errors='replace')
        except OSError: continue
        found=[]
        for m in REF_RE.finditer(text):
            raw=m.group('path').rstrip('.,:;)]}')
            key=normalize_path(raw)
            if not key or key.endswith(('.js','.css','.html')): continue
            found.append(key)
            row=refs.setdefault(key,{'legacyPath':raw,'logicalId':logical_id(raw),'category':classify(raw),'extension':Path(raw).suffix.lower().lstrip('.'),'consumers':set(),'referenceCount':0})
            row['referenceCount']+=1; row['consumers'].add(rel)
        files.append({'path':rel,'references':len(found)})
    assets=[]
    for key,row in refs.items():
        consumers=sorted(row.pop('consumers'))
        row.update({'id':hashlib.sha256(key.encode()).hexdigest()[:12],'consumers':consumers,'rathenaDomains':rathena_domains(key,consumers),'status':'mapped','mappingConfidence':'high' if len(consumers)>1 else 'medium'})
        assets.append(row)
    assets.sort(key=lambda x:(-x['referenceCount'],x['legacyPath'].lower()))
    by=defaultdict(int)
    for a in assets: by[a['category']]+=1
    duplicates=defaultdict(list)
    for a in assets: duplicates[a['logicalId']].append(a['legacyPath'])
    collisions=[{'logicalId':k,'paths':v} for k,v in duplicates.items() if len(v)>1]
    return {'schemaVersion':1,'sourceRoot':str(root),'summary':{'filesScanned':len(files),'filesWithReferences':sum(bool(f['references']) for f in files),'referencesFound':sum(a['referenceCount'] for a in assets),'uniqueAssets':len(assets),'byCategory':dict(sorted(by.items())),'logicalIdCollisions':len(collisions)},'assets':assets,'files':files,'collisions':collisions}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('source',type=Path); ap.add_argument('-o','--output',type=Path,default=Path('roweb-asset-mapping.json')); args=ap.parse_args()
    if not args.source.exists(): ap.error(f'source does not exist: {args.source}')
    result=scan(args.source); args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result['summary'],ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
