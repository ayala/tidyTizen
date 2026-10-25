using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using System.Text.Json;

class Control {
 const string Operation="http://tizen.org/appcontrol/operation/main";
 const string Target="EaQN8Home1.CleanHome";
 const string TargetPackage="EaQN8Home1";
 const string ExpectedFirmware="T-OSCPAKUC-2220.9";
 static readonly string[] Keys={"db/appfw/home_appid","db/appfw/startup_appid","db/appfw/booting_appid_backup","db/first_screen/type"};
 const string AutoKey="db/menu/smart_hub/ontvsetting/auto_start";
 [DllImport("libbundle.so.0")] static extern IntPtr bundle_create();
 [DllImport("libbundle.so.0")] static extern void bundle_free(IntPtr b);
 [DllImport("libaul.so.0")] static extern int aul_svc_set_operation(IntPtr b,string op);
 [DllImport("libaul.so.0")] static extern int aul_get_default_app(IntPtr b,out IntPtr app);
 [DllImport("libapp-context-manager-common.so")] static extern byte util_is_appbooting_supported_webapp_byappid(string app);
 [DllImport("libcapi-appfw-app-operation-tv.so.0")] static extern int app_operation_get_current_app(string op,out IntPtr app);
 [DllImport("libcapi-appfw-app-operation-tv.so.0")] static extern int app_operation_set_current_app(string op,string app);
 [DllImport("libcapi-appfw-app-control.so.0")] static extern int app_control_create(out IntPtr control);
 [DllImport("libcapi-appfw-app-control.so.0")] static extern int app_control_destroy(IntPtr control);
 [DllImport("libcapi-appfw-app-control.so.0")] static extern int app_control_set_operation(IntPtr control,string operation);
 [DllImport("libcapi-appfw-app-control.so.0")] static extern int app_control_set_defapp(IntPtr control,string app);
 [DllImport("libvconf.so.0")] static extern int vconf_set_str(string key,string value);
 [DllImport("libvconf.so.0")] static extern IntPtr vconf_get_str(string key);
 [DllImport("libvconf.so.0")] static extern int vconf_set_int(string key,int value);
 [DllImport("libvconf.so.0")] static extern int vconf_get_int(string key,out int value);
 [DllImport("libc")] static extern uint getuid();
 [DllImport("libc")] static extern void free(IntPtr ptr);

 public class Snapshot {
  public string Home{get;set;}
  public Dictionary<string,string> Strings{get;set;}
  public int Autostart{get;set;}
  public uint Uid{get;set;}
  public int BootSupported{get;set;}
  public string Firmware{get;set;}
 }

 static string ReadString(string key){IntPtr p=vconf_get_str(key);if(p==IntPtr.Zero)return null;try{return Marshal.PtrToStringAnsi(p);}finally{free(p);}}
 static string Home(){IntPtr p;if(app_operation_get_current_app(Operation,out p)!=0||p==IntPtr.Zero)throw new Exception("Cannot read Home operation");try{return Marshal.PtrToStringAnsi(p);}finally{free(p);}}
 static string Firmware(){return File.ReadAllText("/etc/prd_info.ini");}
 static Snapshot Query(){var s=new Snapshot{Home=Home(),Strings=new Dictionary<string,string>(),Uid=getuid(),BootSupported=util_is_appbooting_supported_webapp_byappid(Target),Firmware=Firmware()};foreach(var k in Keys)s.Strings[k]=ReadString(k);int v;if(vconf_get_int(AutoKey,out v)!=0)throw new Exception("Cannot read autostart");s.Autostart=v;return s;}
 static void SetString(string key,string value){if(vconf_set_str(key,value)!=0||ReadString(key)!=value)throw new Exception("String write/readback failed: "+key);}
 static void SetAuto(int value){int v;if(vconf_set_int(AutoKey,value)!=0||vconf_get_int(AutoKey,out v)!=0||v!=value)throw new Exception("Autostart write/readback failed");}
 static void SetHome(string value){IntPtr control;if(app_control_create(out control)!=0||control==IntPtr.Zero)throw new Exception("Cannot create Home app control");try{if(app_control_set_operation(control,Operation)!=0||app_control_set_defapp(control,value)!=0)throw new Exception("Home app-service write failed");}finally{app_control_destroy(control);}if(app_operation_set_current_app(Operation,value)!=0||Home()!=value)throw new Exception("Home TV-operation write/readback failed");}
 static void Restore(Snapshot s){SetHome(s.Home);SetString("db/appfw/home_appid",s.Strings["db/appfw/home_appid"]);SetString("db/appfw/booting_appid_backup",s.Strings["db/appfw/booting_appid_backup"]);SetString("db/first_screen/type",s.Strings["db/first_screen/type"]);SetAuto(s.Autostart);}
 static void CheckSnapshot(Snapshot s){if(s==null||string.IsNullOrWhiteSpace(s.Home)||s.Strings==null||s.Strings.Count!=Keys.Length||(s.Autostart!=0&&s.Autostart!=1)||s.Uid!=901||!s.Firmware.Contains(ExpectedFirmware))throw new Exception("Invalid original snapshot");foreach(var k in Keys)if(!s.Strings.ContainsKey(k))throw new Exception("Missing original setting: "+k);if(string.IsNullOrWhiteSpace(s.Strings["db/appfw/home_appid"]))throw new Exception("Missing original Home setting");}
 static void RequireRestorable(Snapshot current,Snapshot original){
  if(current.Home!=original.Home&&current.Home!=Target)throw new Exception("Home operation changed since snapshot; stop for review");
  foreach(var k in Keys){var v=current.Strings[k];if(k=="db/appfw/home_appid"||k=="db/first_screen/type"){if(v!=original.Strings[k]&&v!=Target)throw new Exception("Home setting changed since snapshot: "+k);}else if(k=="db/appfw/booting_appid_backup"){continue;}else if(v!=original.Strings[k])throw new Exception("Setting changed since snapshot: "+k);}
  if(current.Autostart!=original.Autostart&&current.Autostart!=1)throw new Exception("Autostart changed since snapshot; stop for review");
 }
 static int Main(string[] args){
  try{
   if(IntPtr.Size!=4||getuid()!=901)throw new Exception("Expected 32-bit .NET SDK user, no root");
   if(!Firmware().Contains(ExpectedFirmware))throw new Exception("Unexpected firmware");
   if(args.Length==1&&args[0]=="query"){Console.WriteLine("CLEANFRAME_HOME_JSON="+JsonSerializer.Serialize(Query()));return 0;}
   if(args.Length!=2||(args[0]!="apply"&&args[0]!="restore"))throw new Exception("Use query, apply SNAPSHOT, or restore SNAPSHOT");
   var original=JsonSerializer.Deserialize<Snapshot>(File.ReadAllText(args[1]));CheckSnapshot(original);var before=Query();RequireRestorable(before,original);
   if(args[0]=="restore"){Restore(original);var restored=Query();RequireRestorable(restored,original);if(restored.Home!=original.Home||restored.Strings["db/appfw/home_appid"]!=original.Strings["db/appfw/home_appid"]||restored.Strings["db/appfw/booting_appid_backup"]!=original.Strings["db/appfw/booting_appid_backup"]||restored.Strings["db/first_screen/type"]!=original.Strings["db/first_screen/type"]||restored.Autostart!=original.Autostart)throw new Exception("Restore verification failed");Console.WriteLine("CLEANFRAME_HOME_RESTORED="+JsonSerializer.Serialize(restored));return 0;}
   throw new Exception("Apply disabled: QN800A firmware 2220.9 maps XF86Home directly to com.samsung.tv.csfs in tvctx-manager's root-owned task filter");
#pragma warning disable CS0162
   if(before.Home!=original.Home||before.Strings["db/appfw/home_appid"]!=original.Strings["db/appfw/home_appid"]||before.Strings["db/first_screen/type"]!=original.Strings["db/first_screen/type"]||before.Autostart!=original.Autostart)throw new Exception("Home is already modified; restore before applying again");
   if((!Directory.Exists("/opt/usr/apps/"+TargetPackage)&&!Directory.Exists("/opt/usr/home/owner/apps_rw/"+TargetPackage))||before.BootSupported==0)throw new Exception("Installed launcher is not eligible for boot");
   try{SetHome(Target);SetString("db/appfw/home_appid",Target);SetString("db/first_screen/type",Target);SetAuto(1);var applied=Query();RequireRestorable(applied,original);if(applied.Home!=Target||applied.Strings["db/appfw/home_appid"]!=Target||applied.Strings["db/first_screen/type"]!=Target||applied.Autostart!=1)throw new Exception("Apply verification failed");Console.WriteLine("CLEANFRAME_HOME_APPLIED="+JsonSerializer.Serialize(applied));}
   catch{Restore(original);Console.Error.WriteLine("Original Home values restored after a failed apply");throw;}
   return 0;
#pragma warning restore CS0162
  }catch(Exception e){Console.Error.WriteLine(e.ToString());return 1;}
 }
}
