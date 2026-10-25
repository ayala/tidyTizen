set -u
printf 'CLEANFRAME_HOME_INSPECT_BEGIN\n'
printf 'IDENTITY\n'
id
printf '\nROUTING_PATHS\n'
ls -ldnZ /etc /etc/tvctx-manager 2>/dev/null || true
ls -lnZ /etc/tvctx-manager/.app-context.db* 2>/dev/null || true
getfacl /etc/tvctx-manager/.app-context.db 2>/dev/null || true
findmnt -T /etc/tvctx-manager/.app-context.db 2>/dev/null || mount | grep -E ' on / | /etc ' || true
printf '\nROUTING_ROWS\n'
sqlite3 -header -column /etc/tvctx-manager/.app-context.db "select appid,key,longpress,override,on_selector,request,target_selector,args from key_filter where key in ('XF86Home','XF86Back','Return');" 2>/dev/null || true
printf '\nCONTEXT_MANAGER_BINARY\n'
ls -lnZ /usr/bin/tvctx-manager /usr/lib/libcapi-appfw-app-context-manager.so /usr/lib/libapp-context-manager-common.so 2>/dev/null || true
getcap /usr/bin/tvctx-manager 2>/dev/null || true
nm -D /usr/lib/libcapi-appfw-app-context-manager.so 2>/dev/null | grep -Ei 'key|filter|task|register|add|remove|update' | head -300 || true
strings /usr/lib/libcapi-appfw-app-context-manager.so 2>/dev/null | grep -Ei 'key.?filter|task.?filter|privilege|permission|register|add|remove|update' | head -300 || true
printf '\nPROCESS\n'
ps -eo user,group,pid,args 2>/dev/null | grep '[t]vctx-manager' || true
ps -eo user,group,pid,args 2>/dev/null | grep -E '[S]amsungTv(Root|Remote|Archive)|[a]rchive-root-' || true
printf '\nARCHIVE_ROOT_STAGING\n'
find /home/owner/share/tmp/sdk_tools -maxdepth 2 -name 'archive-root-*' -print 2>/dev/null | head -100 || true
printf '\nARCHIVE_ROOT_PREREQUISITES\n'
getcap /usr/bin/dotnet /usr/sbin/sdbd-tarlauncher 2>/dev/null || true
/usr/bin/dotnet --list-runtimes 2>/dev/null || ls /usr/share/dotnet/shared/Microsoft.NETCore.App/ 2>/dev/null || true
/usr/bin/tar --help 2>/dev/null | grep -- --to-command || true
printf '\nAPPLICATION_LAUNCHER\n'
/usr/bin/app_launcher --help 2>&1 | head -120 || true
printf '\nINPUT_DEVICES\n'
cat /proc/bus/input/devices 2>/dev/null | sed -n '/^I:/,/^$/p' | head -500 || true
printf 'CLEANFRAME_HOME_INSPECT_END\n'
