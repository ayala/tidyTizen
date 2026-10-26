/* Public Tizen application APIs. No Mac server, network address or credentials. */
(function () {
  'use strict';
  var IDS = {
    netflix: 'org.tizen.netflix-app', youtube: '9Ur5IzDKqV.TizenYouTube',
    plex: 'kIciSQlYEM.plex', nuvio: 'NuvioTV001.NuvioTV',
    disneyplus: 'MCmYXNxgcu.DisneyPlus', hulu: 'LBUAQX1exg.Hulu',
    appletv: 'com.samsung.tv.aria-video', primevideo: 'org.tizen.primevideo',
    xbox: 'GHI3a0zMSx.XboxGamePass',
    applemusic: 'org.tizen.apple.apple-music'
  };
  var STREAMING = ['as6cYRgkPy.Binge', '73iTZRTc34.Stan', '5b8c3eb16b.BeamCTVDev',
    'KaLitts8bq.tenplaySamsungTizen', 'eYuOiOLYQX.KayoSports', 'Ne2ZsPWdKl.9NOW',
    '3KA0pm7a7V.TubiTV', 'rJeHak5zRg.Spotify', 'NuvioTV001.NuvioTV', 'icp4AvUPiA.7plus'];
  var CONSUMER_SYSTEM = ['org.tizen.browser', 'com.microsoft.copilot', 'org.tizen.ambientapp'];
  var EXTRA_BRANDS = {'rJeHak5zRg.Spotify': 'spotify', 'NuvioTV001.NuvioTV': 'nuvio', '5b8c3eb16b.BeamCTVDev': 'hbomax', '3KA0pm7a7V.TubiTV': 'tubi',
    'Z6by5zQeIi.TizenIPTV': 'tizeniptv', 'EaIPTVN001.App': 'tizeniptv', 'org.tizen.ambientapp': 'ambient'};
  var INTERNAL = ['adplatform.ADPlayer', 'WykOS4t4F0.cmsWebApp', '25emanual3.emanual',
    'ZODRT12q2l.WebAccountExtension', 'ByJlgt0XeD.CastSettingsApp', 'tv6pbVMQFF.PrivacyChoices'];
  var SELF = 'EaQN8Home1.CleanHome';
  function api() { return window.tizen && window.tizen.application; }
  function unavailable(done) {
    done({ message: 'Open tidyTizen on the TV to use this control.', detail: 'The web preview cannot control the TV.' });
  }
  function failure(err) {
    return { message: 'The TV could not open this screen.', detail: err && (err.message || err.name) || 'Try again, or press the remote’s Home button to return to tidyTizen.' };
  }
  function bounded(done) {
    var finished = false, timer = setTimeout(function () { finish({ message: 'The TV did not respond. Please try again.' }); }, 8000);
    function finish(err, value) { if (finished) return; finished = true; clearTimeout(timer); done(err, value); }
    return finish;
  }
  function launchApp(id, done) {
    if (!api()) { unavailable(done); return; }
    var finish = bounded(done);
    try { api().launch(id, function () { finish(null); }, function (err) { finish(failure(err)); }); }
    catch (err) { finish(failure(err)); }
  }
  function launch(brand, done) {
    if (!IDS[brand]) { done({message: 'This app has no launch target.'}); return; }
    launchApp(IDS[brand], done);
  }
  function home(done) { launchApp('com.samsung.tv.csfs', done); }
  function sourceApi() { return window.tizen && window.tizen.systeminfo && window.tizen.tvwindow; }
  function sourceFailure(err) {
    return { message: 'The TV could not switch inputs.', detail: err && (err.message || err.name) || 'Try the Source button on the remote.' };
  }
  function sources(done) {
    if (!sourceApi()) { unavailable(done); return; }
    var finish = bounded(done);
    try {
      window.tizen.systeminfo.getPropertyValue('VIDEOSOURCE', function (info) {
        var status = {}, sources = [], i, source, key;
        for (i = 0; i < (info.connected || []).length; i++) { source = info.connected[i]; key = source.type + ':' + source.number; status[key] = true; sources.push({type: source.type, number: source.number, name: source.type === 'TV' ? 'TV' : source.type + ' ' + source.number}); }
        for (i = 0; i < (info.disconnected || []).length; i++) { source = info.disconnected[i]; key = source.type + ':' + source.number; status[key] = false; sources.push({type: source.type, number: source.number, name: source.type === 'TV' ? 'TV' : source.type + ' ' + source.number}); }
        sources.sort(function (a, b) { if (a.type === 'TV') return -1; if (b.type === 'TV') return 1; return a.number - b.number; });
        finish(null, {sources: sources, status: status});
      }, function (err) { finish(sourceFailure(err)); });
    } catch (err) { finish(sourceFailure(err)); }
  }
  function openSource(type, number, done) {
    if (!sourceApi()) { unavailable(done); return; }
    var finish = bounded(done);
    try {
      window.tizen.systeminfo.getPropertyValue('VIDEOSOURCE', function (info) {
        var all = (info.connected || []).concat(info.disconnected || []), source = null, i;
        for (i = 0; i < all.length; i++) if (all[i].type === type && all[i].number === number) { source = all[i]; break; }
        if (!source) { finish({ message: type + ' ' + number + ' is not available on this TV.' }); return; }
        try {
          window.tizen.tvwindow.setSource(source, function () {
            try {
              api().launch('org.tizen.tv-viewer', function () { finish(null); }, function () {
                try { window.tizen.tvwindow.show(function () { finish(null); }, function (err) { finish(sourceFailure(err)); }, ['0px', '0px', '1920px', '1080px'], 'MAIN'); }
                catch (err) { finish(sourceFailure(err)); }
              });
            } catch (err) { finish(sourceFailure(err)); }
          }, function (err) { finish(sourceFailure(err)); }, 'MAIN');
        } catch (err) { finish(sourceFailure(err)); }
      }, function (err) { finish(sourceFailure(err)); });
    } catch (err) { finish(sourceFailure(err)); }
  }
  function apps(done) {
    if (!api()) { unavailable(done); return; }
    var finish = bounded(done);
    try {
      api().getAppsInfo(function (list) {
        var known = {}, seen = {}, result = [];
        Object.keys(IDS).forEach(function (brand) { known[IDS[brand]] = brand; });
        list.forEach(function (a) {
          var primary = !!known[a.id], stream = STREAMING.indexOf(a.id) >= 0;
          var explicitSystem = CONSUMER_SYSTEM.indexOf(a.id) >= 0;
          var consumer = /^[A-Za-z0-9]{10}\.[A-Za-z0-9_-]+$/.test(a.id) || explicitSystem;
          if (a.id === SELF || INTERNAL.indexOf(a.id) >= 0 || seen[a.id] || !a.name || (!primary && !stream && !explicitSystem && (!a.show || !consumer))) return;
          if (!primary && /(?:service|worker|preview|promotion|plugin|launcher|test|sdk|^ep[ -]|factory|daemon)/i.test(a.name + ' ' + a.id)) return;
          if (/-dummy$/.test(a.id) || a.id === 'com.samsung.tv.cobalt-yt') return;
          seen[a.id] = true;
          result.push({ appId: a.id, name: a.id === 'org.tizen.ambientapp' ? 'Ambient Mode' : a.name, brand: known[a.id] || EXTRA_BRANDS[a.id] || '', icon: a.iconPath || '', rank: primary ? Object.keys(IDS).indexOf(known[a.id]) : (stream ? 20 : 30) });
        });
        result.sort(function (a, b) { return a.rank - b.rank || a.name.toLowerCase().localeCompare(b.name.toLowerCase()); });
        finish(null, result);
      }, function (err) { finish(failure(err)); });
    } catch (err) { finish(failure(err)); }
  }
  window.FrameDevice = { launch: launch, launchApp: launchApp, home: home, apps: apps, sources: sources, openSource: openSource };
}());
