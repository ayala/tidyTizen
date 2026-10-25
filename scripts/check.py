"""Check that the widget manifest and its referenced files are present."""
from pathlib import Path
import json
import xml.etree.ElementTree as XML
import re

root = Path(__file__).resolve().parents[1]
app = root / 'app'
manifest = XML.parse(app / 'config.xml').getroot()
ns = {'w': 'http://www.w3.org/ns/widgets', 't': 'http://tizen.org/ns/widgets'}
identity = manifest.find('t:application', ns)
assert identity is not None, 'Missing application identity'
assert identity.get('package') == 'EaQN8Home1', 'Keep the installed package identity stable'
assert identity.get('id') == 'EaQN8Home1.CleanHome', 'Keep the installed application ID stable'
assert identity.get('required_version') == '6.0', 'QN800A build must target Tizen 6.0'
assert manifest.get('version') == json.loads((root / 'package.json').read_text())['version'], 'Manifest/package versions differ'
for tag in ['content', 'icon']:
    node = manifest.find('w:' + tag, ns)
    assert node is not None and (app / node.get('src', '')).is_file(), 'Missing ' + tag + ' file'
assert all((app / name).is_file() for name in ['main.js', 'style.css'])
for reference in ['assets/wallpapers/catalog.js', 'assets/adaptive-ink.js', 'assets/font-catalog.js']:
    assert (app / reference).is_file(), 'Missing runtime catalogue: ' + reference
secrets = (app / 'assets/local-secrets.example.js').read_text()
assert not re.search(r'[A-Fa-f0-9]{32}', secrets), 'TMDB credential must not be committed in the app source'
for filename in ['index.html']:
    source = (app / filename).read_text()
    pattern = r'(?:src|href)=[\"\']([^\"\']+)' if filename.endswith('.html') else r'from\s+[\"\']([^\"\']+)'
    for reference in re.findall(pattern, source):
        if ':' in reference or reference.startswith('$'):
            continue
        if reference == 'assets/local-secrets.js':
            assert (app / 'assets/local-secrets.example.js').is_file(), 'Missing TMDB secrets example'
            continue
        assert (app / reference).is_file(), 'Missing bundled resource: ' + reference
        if filename.endswith('.js'):
            assert reference.startswith(('./', '../')), 'Module imports must be relative paths'
for css in app.rglob('*.css'):
    for reference in re.findall(r'url\([\"\']?([^\)\"\']+)', css.read_text()):
        if ':' not in reference:
            assert (css.parent / reference.split('?')[0]).is_file(), 'Missing CSS resource: ' + reference
# These resource names are constructed at runtime, so HTML/CSS reference checks cannot find them.
walls = json.loads((app / 'assets/wallpapers/SOURCES.json').read_text())
for wall in walls:
    for field in ['src', 'thumb']:
        assert (app / wall[field]).is_file(), 'Missing wallpaper: ' + wall[field]
    wall_id = wall['id']
    for suffix in ['study-soft', 'field-blur', 'field-frost', 'field-clear']:
        assert (app / ('assets/materials/' + wall_id + '-' + suffix + '.jpg')).is_file(), 'Missing registered material: ' + wall_id + '/' + suffix
    assert (app / ('assets/wallpapers/' + wall_id + '-panel.jpg')).is_file(), 'Missing panel backdrop: ' + wall_id
for icon in ['stremio', 'netflix', 'disneyplus', 'youtube', 'appletv', 'primevideo', 'abciview', 'sbs', 'applemusic', 'art', 'apps', 'settings', 'tizeniptv']:
    assert (app / ('assets/icons/' + icon + '.svg')).is_file(), 'Missing icon: ' + icon
source_icons = json.loads((app / 'assets/icons/source-icons/SOURCES.json').read_text())
for icon in source_icons['icons']:
    source_icon = app / ('assets/icons/source-icons/' + icon + '.svg')
    assert source_icon.is_file(), 'Missing source icon: ' + icon
    source_root = XML.parse(source_icon).getroot()
    assert source_root.tag == '{http://www.w3.org/2000/svg}svg', 'Invalid source SVG: ' + icon
    viewbox = source_root.get('viewBox', '').split()
    assert len(viewbox) == 4 and all(float(value) >= 0 for value in viewbox) and float(viewbox[2]) > 0 and float(viewbox[3]) > 0, 'Invalid source SVG viewBox: ' + icon
print('Widget identity, version and bundled resources are valid.')
