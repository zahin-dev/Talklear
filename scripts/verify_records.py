"""Offline checks for record consistency and dated verification evidence."""
import argparse, collections, csv, datetime, hashlib, json, pathlib, re, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
parser=argparse.ArgumentParser();parser.add_argument('--live',action='store_true');args=parser.parse_args()
records=read('docs/project/records.json');plan=read('docs/project/master-plan.json');manifest=read('docs/verification/source-manifest.json');notion=read('notion-export/notion-map.json');stages=read('docs/verification/stage-map.json')
errors=[];checks=[]
def check(name,ok):
 checks.append({'check':name,'passed':bool(ok)})
 if not ok:errors.append(name)
byid={r['id']:r for r in records};counts=dict(collections.Counter(r['database'] for r in records))
check('unique IDs',len(byid)==len(records))
check('record date matches ID',all(re.fullmatch(r'[A-Z]+-\d{8}-\d{3}',r['id']) and r['id'].split('-')[1]==r['date'].replace('-','') for r in records))
check('all related IDs exist',all(x in byid for r in records for x in r['related']))
check('required counts',counts=={'Tasks':32,'Development Sessions':14,'Meetings':6,'ADR':7,'Bugs':8,'Code Reviews':10,'Tests':10,'KPT':7,'Milestones':5})
check('14 development dates',sorted(r['date'] for r in records if r['database']=='Development Sessions')==[s['date'] for s in plan['sessions']])
check('development Tue/Wed; KPT Thu',all(datetime.date.fromisoformat(r['date']).weekday() in ((1,2) if r['database']=='Development Sessions' else (3,)) for r in records if r['database'] in ('Development Sessions','KPT')))
check('7 KPT dates',sorted(r['date'] for r in records if r['database']=='KPT')==[s['date'] for s in plan['kpt']])
check('210 person hours; 70 per member',sum(s['person_hours'] for s in plan['sessions'])==210 and sum(plan['members'].values())==210 and all(v==70 for v in plan['members'].values()))
check('no 10/18 extra development',all(s['date']!='2026-10-18' for s in plan['sessions']))
tasks={t['id']:t for t in plan['tasks']}
check('dependency dates',all(d in tasks and tasks[d]['date']<=t['date'] for t in tasks.values() for d in t['dependencies']))
visiting=set();visited=set()
def visit(id):
 if id in visiting:raise ValueError('cycle')
 if id in visited:return
 visiting.add(id)
 for dep in tasks[id]['dependencies']:visit(dep)
 visiting.remove(id);visited.add(id)
try:
 for id in tasks:visit(id)
 check('dependency graph acyclic',True)
except (ValueError,KeyError):check('dependency graph acyclic',False)
check('KPT improvement task links',all(any(x.startswith('TASK-') and x in tasks for x in r['related']) for r in records if r['database']=='KPT'))
check('KPT continuation outcome present',all('前週Tryの実施結果' in r['content'] and '改善の効果' in r['content'] for r in records if r['database']=='KPT'))
check('all record files and Notion mappings exist',all((ROOT/r['path']).is_file() and r['id'] in notion['pages'] for r in records))
check('all task evidence files exist',all((ROOT/t['evidence_file']).is_file() for t in plan['tasks']))
csv_rows=[]
for p in (ROOT/'notion-export/databases').glob('*.csv'):
 with p.open(encoding='utf-8-sig',newline='') as f:csv_rows.extend(csv.DictReader(f))
check('9 CSV backups cover all records and states',len(list((ROOT/'notion-export/databases').glob('*.csv')))==9 and len(csv_rows)==99 and {r['Record ID'] for r in csv_rows}==set(byid) and all(row['Status']==byid[row['Record ID']]['status'] and row['Owner']==byid[row['Record ID']]['owner'] and row['工程日']==byid[row['Record ID']]['date'] for row in csv_rows))
check('CSV contents evidence and database partition preserved',all(row['Content']==byid[row['Record ID']]['content'] and row['Evidence Type']==byid[row['Record ID']]['evidence'] for row in csv_rows) and all(all(byid[row['Record ID']]['database']==p.stem for row in csv.DictReader(p.open(encoding='utf-8-sig',newline=''))) for p in (ROOT/'notion-export/databases').glob('*.csv')))
sources=read('docs/admin/evidence-index.json')
check('canonical provenance authority and complete evidence index',sources['authority'].endswith('404bfd03219981c7a9c3c776d5f6fc39') and {r['id'] for r in sources['records']}==set(byid) and (ROOT/'docs/admin/record-sources.md').is_file())
check('record dates and execution timestamps remain distinct',all(r['content'].startswith('日付：') for r in records) and sources['record_date_semantics']=='record dates; test runs and commit timestamps are tracked separately')
check('tests separate expectation and execution',all('期待結果' in r['content'] and '実行結果' in r['content'] for r in records if r['database']=='Tests'))
check('successful test records require dated execution evidence',all(r['database']!='Tests' or r['status']!='実行成功' or ('実測' in r['content'] and '2026-10-25' in r['content']) for r in records))
check('manual tests remain unexecuted',sum(r['database']=='Tests' and r['status']=='未実行' for r in records)==2)
check('bug records retain confirmation criteria and test references',all('確認観点' in r['content'] and '想定' in r['content'] and '回帰テスト' in r['content'] for r in records if r['database']=='Bugs'))
allowed={'README.md','docs/requirements.md','docs/basic-design.md','docs/deployment.md'}
diff=[];missing=[]
for f in manifest['files']:
 p=ROOT/f['path']
 if not p.is_file():missing.append(f['path']);continue
 if hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256']:diff.append(f['path'])
check('all 48 snapshot paths preserved',not missing and len(manifest['files'])==48)
check('only four permitted document differences',set(diff)==allowed)
application=[f for f in manifest['files'] if f['path'] not in allowed]
check('44 application test config files byte identical',len(application)==44 and all(hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256'] for f in application))
check('committed application bytes match snapshot',all(hashlib.sha256(subprocess.check_output(['git','show','HEAD:'+f['path']],cwd=ROOT)).hexdigest()==f['sha256'] for f in application))
check('no extra source or application test files',set(p.relative_to(ROOT).as_posix() for prefix in ('src','tests') for p in (ROOT/prefix).rglob('*') if p.is_file())==set(f['path'] for f in application if f['path'].startswith(('src/','tests/'))))
for r in records:
 if r['database']=='Code Reviews':
  file=re.search(r'## 対象ファイル\n\n`?([^\n`]+)',r['content']).group(1)
  sha=re.search(r'## 対応コミット\n\n([a-f0-9]{40})',r['content']).group(1)
  result=subprocess.run(['git','cat-file','-e',sha+':'+file],cwd=ROOT,capture_output=True)
  check(r['id']+' target exists in bound commit',result.returncode==0)
# Inspect only this independent repository's history, never the original repository.
log=subprocess.run(['git','log','--format=%an|%ae|%cn|%ce|%aI|%cI'],cwd=ROOT,capture_output=True,text=True)
history=read('docs/admin/history-baseline.json')
check('original 13 commit identities preserved',len(history['commits'])==13 and subprocess.check_output(['git','rev-list',history['head']],cwd=ROOT,text=True).splitlines()==history['commits'] and subprocess.run(['git','merge-base','--is-ancestor',history['head'],'HEAD'],cwd=ROOT).returncode==0)
check('no backdated commits',all(parts[4][:10]>='2026-10-25' and parts[5][:10]>='2026-10-25' for line in log.stdout.splitlines() if len(parts:=line.split('|'))==6))
check('one independent root commit',len(subprocess.check_output(['git','rev-list','--max-parents=0','HEAD'],cwd=ROOT,text=True).splitlines())==1)
# Files staged/committed for publication are checked; ignored runtime data is never included.
tracked=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
check('no runtime credential or data paths',not any(re.search(r'(^|/)(\.env$|\.local/|\.tools/|\.vercel/)|\.(pem|key|p12|pfx)$',p) for p in tracked))
suspects=[]
patterns=[r'gh[pousr]_[A-Za-z0-9]{30,}',r'github_pat_[A-Za-z0-9_]{40,}',r'AKIA[0-9A-Z]{16}',r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----',r'postgres(?:ql)?://[^\s/:]+:[^\s/@]+@']
for file in tracked:
 if not (ROOT/file).is_file() or file==pathlib.Path(__file__).relative_to(ROOT).as_posix():continue
 raw=(ROOT/file).read_bytes()
 if raw.startswith(b'\x89PNG') or b'\x00' in raw:continue
 try:text=raw.decode('utf-8-sig')
 except UnicodeDecodeError:continue
 if any(re.search(p,text) for p in patterns):suspects.append(file)
check('credential pattern scan (bounded heuristic)',not suspects)
broken=[]
for p in list((ROOT/'docs').rglob('*.md'))+[ROOT/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if link and not link.startswith(('#','http:','https:','mailto:')):
   from urllib.parse import unquote
   if not (p.parent/unquote(link.split('#')[0])).exists():broken.append((str(p.relative_to(ROOT)),link))
check('local Markdown target paths exist',not broken)
live=read('reports/notion-current-verification.json')
check('Notion all bodies properties IDs and Relations read back',live['passed'] and live['records']==99 and live['databases']==9 and live['pages']==103)
check('all 20 view configurations retained',live['views']==20 and live['view_checks_passed'])
access=read('reports/access-verification.json')
check('GitHub private from authoritative API evidence',access['github']['repository_id']==1432922831 and access['github']['visibility']=='private')
check('anonymous GitHub denied',access['github']['anonymous_status']==404)
check('Notion Sites unpublished from UI evidence',access['notion']['sites_unpublished'] is True)
check('Notion general web link removed',access['notion']['general_access']=='Only people invited')
check('all 112 Notion entities deny anonymous access',len(access['notion']['anonymous_checks'])==112 and all(x['denied'] for x in access['notion']['anonymous_checks']))
check('all 112 direct Notion URLs require authentication',len(access['notion']['direct_anonymous_checks'])==112 and all(x['denied'] for x in access['notion']['direct_anonymous_checks']))
check('authenticated Notion access retained',live['authenticated_fetch_errors']==0)
check('all Notion entities remain under requested parent',all(p['under_requested_parent'] for p in live['scope_checks']))
check('Notion schema and relation definitions preserved',len(live['schema_checks'])==9 and all(p['properties_and_relations_preserved'] for p in live['schema_checks']))
if (ROOT/'reports/archive/2026-10-25-publication/ci-run.json').exists():
 ci=read('reports/archive/2026-10-25-publication/ci-run.json')
 check('archived measured CI passed',ci['conclusion']=='success' and ci['status']=='completed')
 original_paths=[f['path'] for f in application]
 changes=subprocess.check_output(['git','diff',ci['headSha'],'--',*original_paths],cwd=ROOT)
 check('application source unchanged since successful CI',not changes)
archive=read('docs/admin/archive-hashes.json')
check('historical evidence bytes preserved',all((ROOT/x['path']).is_file() and hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in archive))
duplicate=[];stale=[]
oldpaths=['docs/simulation-notice.md','notion-export/pages/simulation-notice.md','docs/deployment/simulation-publication.md','scripts/verify_simulation.py']
for p in [ROOT/'README.md',*(ROOT/'docs').rglob('*.md'),*(ROOT/'notion-export/pages').glob('*.md')]:
 text=p.read_text(encoding='utf-8')
 if '実際の活動履歴を証明するものではありません' in text:duplicate.append(str(p.relative_to(ROOT)))
 if any(old in text for old in oldpaths):stale.append(str(p.relative_to(ROOT)))
check('daily documents contain no duplicate long notice',not duplicate)
check('renamed path references updated',not stale)
residual=read('reports/residual-audit.json')
check('full residual audit has no update misses',not residual['misses'] and residual['coverage']['notion_entities']==112 and residual['coverage']['views']==20)
inventory=read('reports/current-file-inventory.json')
current_paths={p for p in tracked if (ROOT/p).is_file() and '__pycache__' not in p}
check('inventory covers every current Git file',len(inventory)==len(current_paths) and {x['path'] for x in inventory}==current_paths)
if args.live:
 try:
  remote=json.loads(subprocess.check_output(['gh','api','repos/zahin-dev/talklear-development-simulation'],cwd=ROOT))
  check('live GitHub private',remote['id']==1432922831 and remote['visibility']=='private')
 except (subprocess.SubprocessError,json.JSONDecodeError):check('live GitHub private',False)
report={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'counts':counts,'checks':checks,'errors':errors,'source_modified_docs':diff,'source_missing':missing,'credential_suspect_paths':suspects,'unverified':['Connector does not expose per-page sharing ACLs or complete invited-guest enumeration. Parent and one record dialog were inspected.','No claim about copies or search caches; no Chrome application manual test execution.'],'limits':['Historical evidence is archived without rewriting.','Credential scan is heuristic.']}
(ROOT/'reports/record-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'passed':len(checks)-len(errors),'total':len(checks),'errors':errors,'source_diffs':diff,'credential_suspects':suspects,'unverified':len(report['unverified'])},ensure_ascii=False))
sys.exit(bool(errors))
