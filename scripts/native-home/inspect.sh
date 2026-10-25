set -u
printf 'CLEANFRAME_HOME_INSPECT_BEGIN\n'
id
uname -m
sed -n '/^Version=/p;/^Model=/p' /etc/prd_info.ini
cat /etc/tizen-release
printf '\nDOTNET\n'
ls -d /usr/share/dotnet/shared/Microsoft.NETCore.App/* 2>/dev/null || true
printf '\nHOME_PREFERENCES\n'
for k in db/appfw/home_appid db/appfw/startup_appid db/appfw/booting_appid_backup db/first_screen/type db/menu/smart_hub/ontvsetting/auto_start; do vconftool get "$k"; done
printf '\nNATIVE_LIBRARIES\n'
ls -l /usr/lib/libapp-context-manager-common.so /usr/lib/libcapi-appfw-app-operation-tv.so.0 /usr/lib/libvconf.so.0 2>/dev/null || true
printf '\nHOME_SYMBOLS\n'
nm -D /usr/lib/libaul.so.0 2>/dev/null | grep -E 'default_app|svc.*app' || true
nm -D /usr/lib/libcapi-appfw-app-operation-tv.so.0 2>/dev/null | grep -E 'current_app|operation' || true
readelf -Ws /usr/lib/libaul.so.0 2>/dev/null | grep -E 'default_app|svc.*app' || true
readelf -Ws /usr/lib/libcapi-appfw-app-operation-tv.so.0 2>/dev/null | grep -E 'current_app|operation' || true
printf '\nHOME_RELATED_VCONF\n'
vconftool dump 2>/dev/null | grep -Ei 'home_appid|first_screen|smart_hub|home.*app|app.*home' | head -200 || true
printf '\nHOME_KEY_READERS\n'
timeout 15 grep -RIl --binary-files=text -E 'db/appfw/home_appid|db/first_screen/type|ontvsetting/auto_start' /usr/bin /usr/lib 2>/dev/null | head -100 || true
printf '\nAUL_DEFAULT_SYMBOLS\n'
strings /usr/lib/libaul.so.0 2>/dev/null | grep -Ei 'default.*app|app.*default' | head -100 || true
printf '\nDEFAPP_SETTER_LIBRARIES\n'
timeout 15 grep -RIl --binary-files=text -E 'app_control_set_defapp|set_defapp' /usr/lib /lib 2>/dev/null | head -100 || true
find /usr/lib /lib -maxdepth 2 -type f \( -iname '*app*control*' -o -iname '*appsvc*' \) -print 2>/dev/null | head -100 || true
for lib in /usr/lib/libapp-control-api.so /usr/lib/libappsvc.so.0.1.0 /usr/lib/libcapi-appfw-app-control.so.0.14.0; do
 printf 'LIB=%s\n' "$lib"
 nm -D "$lib" 2>/dev/null | grep -E 'app_control_(set|get)_defapp|defapp' || true
 readelf -Ws "$lib" 2>/dev/null | grep -E 'app_control_(set|get)_defapp|defapp' || true
 strings "$lib" 2>/dev/null | grep -E 'app_control_(set|get)_defapp|defapp' | head -100 || true
done
printf '\nAPP_SERVICE_DATABASES\n'
find /opt/dbspace -name '.appsvc.db' -exec ls -lnZ {} \; 2>/dev/null || true
for db in /opt/dbspace/.appsvc.db /opt/dbspace/user/*/.appsvc.db; do
 [ -r "$db" ] || continue
 printf 'DB=%s\n' "$db"
 sqlite3 "$db" '.tables' 2>/dev/null || true
 sqlite3 "$db" "select * from appsvc where operation='http://tizen.org/appcontrol/operation/main';" 2>/dev/null || true
 sqlite3 "$db" "select * from app_control where operation='http://tizen.org/appcontrol/operation/main';" 2>/dev/null || true
done
printf '\nHOME_RUNTIME_PROCESSES\n'
ps -ef 2>/dev/null | grep -Ei 'EaQN8Home1|WykOS4t4F0|tvctx|csfs|home|smart.?hub' | grep -v grep | head -200 || true
printf '\nRECENT_HOME_LOGS\n'
dlogutil -d -v time 2>/dev/null | grep -Ei 'EaQN8Home1|WykOS4t4F0|tvctx|smarthub|smart.?hub|operation/main|KEY_HOME|home_appid|first_screen' | tail -400 || true
printf '\nTVCTX_CONFIGURATION\n'
ls -la /etc/tvctx-manager /etc/tvctx-manager/launcher 2>/dev/null || true
sed -n '1,320p' /etc/tvctx-manager/appctx-config.json 2>/dev/null || true
printf '\nTVCTX_HOME_CONFIG_MATCHES\n'
grep -nEi -B4 -A12 'home|smart.?hub|XF86Home|csfs|WykOS4t4F0' /etc/tvctx-manager/appctx-config.json 2>/dev/null | head -800 || true
printf '\nTVCTX_CONTEXT_DATABASE\n'
sqlite3 /etc/tvctx-manager/.app-context.db '.tables' 2>/dev/null || true
sqlite3 /etc/tvctx-manager/.app-context.db '.schema' 2>/dev/null | head -600 || true
for table in $(sqlite3 /etc/tvctx-manager/.app-context.db '.tables' 2>/dev/null); do
 printf 'TABLE=%s\n' "$table"
 sqlite3 -header -column /etc/tvctx-manager/.app-context.db "select * from $table limit 200;" 2>/dev/null || true
done
printf '\nTVCTX_LAUNCHER_FILES\n'
for file in /etc/tvctx-manager/launcher/*; do printf 'FILE=%s\n' "$file"; sed -n '1,260p' "$file" 2>/dev/null || true; done
printf '\nTVCTX_LAUNCHER_STRINGS\n'
strings /etc/tvctx-manager/launcher 2>/dev/null | grep -Ei 'home|smart.?hub|key_|app(id)?|launch|vconf|first_screen' | head -400 || true
printf '\nTVCTX_RUNTIME_APIS\n'
find /usr/lib /lib -maxdepth 2 -type f -iname '*context*manager*' -o -iname '*tvctx*' 2>/dev/null | head -200 || true
for lib in /usr/lib/libapp-context-manager-common.so /usr/lib/libcapi-appfw-app-context-manager.so /usr/bin/tvctx-manager; do
 printf 'LIB=%s\n' "$lib"
 nm -D "$lib" 2>/dev/null | grep -Ei 'task|filter|key|launch|manage|context|register|remove|delete|update' | head -500 || true
 strings "$lib" 2>/dev/null | grep -Ei 'task.?filter|add.?task|remove.?task|update.?task|appctx|context.?manager|XF86Home' | head -500 || true
done
printf '\nTVCTX_API_OWNERS\n'
timeout 20 grep -RIl --binary-files=text -E 'task_filter|XF86Home' /usr/lib /lib /usr/bin 2>/dev/null | head -200 || true
printf 'CLEANFRAME_HOME_INSPECT_END\n'
