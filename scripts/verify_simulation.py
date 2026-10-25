"""Offline checks. These prove current artifact consistency, never historical activity."""
import collections, datetime, hashlib, json, pathlib, re, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
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
check('simulation disclosure on every record',all('実際の活動履歴を証明するものではありません' in r['content'] for r in records))
check('tests separate expectation and execution',all('期待結果' in r['content'] and '実行結果' in r['content'] for r in records if r['database']=='Tests'))
check('successful test records require current evidence',all(r['database']!='Tests' or r['status']!='実行成功' or 'Verified' in r['content'] for r in records))
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
  file=re.search(r'## 対象ファイル\n\n([^\n]+)',r['content']).group(1)
  sha=re.search(r'## 再構成コミット\n\n([a-f0-9]{40})',r['content']).group(1)
  result=subprocess.run(['git','cat-file','-e',sha+':'+file],cwd=ROOT,capture_output=True)
  check(r['id']+' target exists in bound commit',result.returncode==0)
# Inspect only this independent repository's history, never the original repository.
log=subprocess.run(['git','log','--format=%an|%ae|%cn|%ce|%aI|%cI'],cwd=ROOT,capture_output=True,text=True)
check('dedicated simulation author and committer',all(line.startswith('Talklear Simulation Builder|simulation@talklear.invalid|Talklear Simulation Builder|simulation@talklear.invalid|') for line in log.stdout.splitlines()))
check('no backdated commits',all(parts[4][:10]>='2026-10-25' and parts[5][:10]>='2026-10-25' for line in log.stdout.splitlines() if len(parts:=line.split('|'))==6))
check('one independent root commit',len(subprocess.check_output(['git','rev-list','--max-parents=0','HEAD'],cwd=ROOT,text=True).splitlines())==1)
# Files staged/committed for publication are checked; ignored runtime data is never included.
tracked=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
check('no runtime credential or data paths',not any(re.search(r'(^|/)(\.env$|\.local/|\.tools/|\.vercel/)|\.(pem|key|p12|pfx)$',p) for p in tracked))
suspects=[]
patterns=[r'gh[pousr]_[A-Za-z0-9]{30,}',r'github_pat_[A-Za-z0-9_]{40,}',r'AKIA[0-9A-Z]{16}',r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----',r'postgres(?:ql)?://[^\s/:]+:[^\s/@]+@']
for file in tracked:
 if not (ROOT/file).is_file() or file==pathlib.Path(__file__).relative_to(ROOT).as_posix():continue
 text=(ROOT/file).read_text(encoding='utf-8-sig',errors='replace')
 if any(re.search(p,text) for p in patterns):suspects.append(file)
check('credential pattern scan (bounded heuristic)',not suspects)
broken=[]
for p in list((ROOT/'docs').rglob('*.md'))+[ROOT/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if link and not link.startswith(('#','http:','https:','mailto:')):
   from urllib.parse import unquote
   if not (p.parent/unquote(link.split('#')[0])).exists():broken.append((str(p.relative_to(ROOT)),link))
check('local Markdown target paths exist',not broken)
if (ROOT/'reports/notion-verification.json').exists():
 live=read('reports/notion-verification.json')
 check('Notion live ID status and relation readback',live.get('passed') and len(live['records'])==99)
if (ROOT/'reports/public-browser-checks.json').exists():
 public=read('reports/public-browser-checks.json')
 check('all 9 public databases render records without login',len(public)==9 and all(x['recordVisible'] and not x['loginRequired'] for x in public))
if (ROOT/'reports/ci-run.json').exists():
 ci=read('reports/ci-run.json')
 check('current execution CI passed',ci['conclusion']=='success' and ci['status']=='completed')
 original_paths=[f['path'] for f in application]
 changes=subprocess.check_output(['git','diff',ci['headSha'],'--',*original_paths],cwd=ROOT)
 check('application source unchanged since successful CI',not changes)
report={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'counts':counts,'checks':checks,'errors':errors,'source_modified_docs':diff,'source_missing':missing,'credential_suspect_paths':suspects,'limits':['Notion publication and remote CI require separate live verification.','No historical activity or browser translation quality is proved.','Credential pattern scan is heuristic; manual review also required.']}
(ROOT/'docs/verification/consistency-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'docs/verification/consistency-report.md').write_text('# 整合性検証\n\n'+f'{len(checks)-len(errors)}/{len(checks)} checks passed.\n\n'+'\n'.join(('- PASS ' if c['passed'] else '- FAIL ')+c['check'] for c in checks)+'\n\n公開状態・遠隔CI・Chrome操作は別途確認。過去の事実は検証しない。\n',encoding='utf-8')
(ROOT/'docs/verification/source-diff.md').write_text('# 元スナップショットとの差分\n\n48元パスを保持。44アプリ・テスト・実行設定はバイト一致。\n\n'+ '\n'.join('- '+p+'：シミュレーション注記・現在の検証との区別を追加。アプリ挙動への影響なし。' for p in diff)+'\n\n追加はsimulation文書、検証スクリプト、Notionバックアップ、実行報告。元リポジトリへの書込みは行っていない。元履歴は取得していない。\n',encoding='utf-8')
print(json.dumps({'passed':len(checks)-len(errors),'total':len(checks),'errors':errors,'source_diffs':diff,'credential_suspects':suspects},ensure_ascii=False))
sys.exit(bool(errors))
