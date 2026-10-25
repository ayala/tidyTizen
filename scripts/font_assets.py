"""Build the exact private-font overlay used by preview and local packaging.

Pangram binaries remain in ignored .local/ storage. A public checkout ships
Manrope, Geist and Newsreader. Complete local Pangram pairs are added directly
to the widget ZIP; they are never copied into app/.
"""
from pathlib import Path
import getpass
import json
import os
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FONT_IDS = ['geist', 'newsreader']
PRIVATE_FONTS = [
    {
        'id': 'montreal', 'family': 'Study Montreal', 'folder': 'neue-montreal',
        'files': [('PPNeueMontreal-Light.ttf', 300), ('PPNeueMontreal-Regular.ttf', 400)],
        'metrics': 'size-adjust:100.699301%;ascent-override:105.859722%;descent-override:29.791667%;line-gap-override:0%',
    },
    {
        'id': 'mori', 'family': 'Study Mori', 'folder': 'mori',
        'files': [('PPMori-Extralight.ttf', 200), ('PPMori-Regular.ttf', 400)],
        'metrics': 'size-adjust:102.857143%;ascent-override:103.638889%;descent-override:29.166667%;line-gap-override:0%',
    },
    {
        'id': 'pangram', 'family': 'Study Pangram', 'folder': 'pangram-sans',
        'files': [('PPPangramSans-Light.ttf', 300), ('PPPangramSans-Regular.ttf', 400)],
        'metrics': 'size-adjust:101.408451%;ascent-override:105.119444%;descent-override:29.583333%;line-gap-override:0%',
    },
]


def is_runtime_source(name):
    """Keep retained rendering tools and legacy layout assets out of the widget."""
    if name in ['grid.css', 'optics.js']:
        return False
    if name.startswith(('assets/grid/', 'assets/vendor/')):
        return False
    return not re.fullmatch(r'assets/wallpapers/[^/]+-glass-\d+\.png', name)


def font_overlay(root=ROOT, include_private=True):
    """Return package-relative paths mapped to bytes or allowlisted font files."""
    sources = (root / '.local/research/font-candidates').resolve()
    assets = {}
    private_ids = []
    css = ['/* Local font overlay. Proprietary binaries are not part of app/. */']
    if include_private:
        for font in PRIVATE_FONTS:
            files = [(sources / font['folder'] / name).resolve() for name, _ in font['files']]
            # Exclude incomplete pairs and symlinks that leave the private font folder.
            if not all(path.is_relative_to(sources) and path.is_file() for path in files):
                continue
            private_ids.append(font['id'])
            for (name, weight), source in zip(font['files'], files):
                relative = font['folder'] + '/' + name
                assets['assets/private-fonts/' + relative] = source
                css.append("@font-face{font-family:'" + font['family'] + "';font-style:normal;"
                           'font-weight:' + str(weight) + ";src:url('private-fonts/" + relative + "') format('truetype');"
                           'font-display:block;' + font['metrics'] + '}')
    assets['assets/private-fonts.css'] = ('\n'.join(css) + '\n').encode()
    assets['assets/font-catalog.js'] = ('window.CleanFramePrivateFontIDs = '
                                       + json.dumps(private_ids + PUBLIC_FONT_IDS) + ';\n').encode()
    return assets


def private_secrets(root=ROOT):
    """Return a private TMDB bootstrap without ever adding it to source control.

    A normal checkout may use the ignored local-secrets.js file. On macOS the
    private owner build can instead keep the key in Login Keychain under the
    tidyTizen-TMDB service, which survives public-source synchronisation.
    """
    source = root / 'app/assets/local-secrets.js'
    if source.is_file():
        content = source.read_text()
        match = re.search(r'^\s*window\.CleanHomeSecrets\.tmdbApiKey\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        if match and re.fullmatch(r'(?:[A-Fa-f0-9]{32}|eyJ[A-Za-z0-9._-]{40,})', match.group(1)):
            return content.encode()
    key = os.environ.get('TIDYTIZEN_TMDB_API_KEY', '').strip()
    if not key and sys.platform == 'darwin':
        result = subprocess.run(
            ['security', 'find-generic-password', '-w', '-a', getpass.getuser(), '-s', 'tidyTizen-TMDB'],
            capture_output=True, text=True)
        if result.returncode == 0:
            key = result.stdout.strip()
    if not re.fullmatch(r'(?:[A-Fa-f0-9]{32}|eyJ[A-Za-z0-9._-]{40,})', key):
        return None
    return ("/* Generated only inside the private widget archive. */\n"
            "window.CleanHomeSecrets = window.CleanHomeSecrets || {};\n"
            "window.CleanHomeSecrets.tmdbApiKey = " + json.dumps(key) + ";\n").encode()


def write_widget_archive(output, root=ROOT, include_private=True):
    """Create an unsigned archive without reading signing or device settings."""
    app = root / 'app'
    overlay = font_overlay(root, include_private)
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, allowZip64=False) as package:
        for source in sorted(app.rglob('*')):
            if source.is_symlink():
                raise ValueError('Widget assets must be regular files, not symlinks: ' + str(source.relative_to(app)))
            if not source.is_file():
                continue
            name = source.relative_to(app).as_posix()
            if name.startswith('assets/private-fonts/'):
                raise ValueError('Private font binaries must stay in .local/, not app/.')
            if name == 'assets/local-secrets.js':
                continue
            if name not in overlay and is_runtime_source(name):
                package.write(source, name)
        example = app / 'assets/local-secrets.example.js'
        secrets = private_secrets(root) if include_private else None
        if secrets:
            package.writestr('assets/local-secrets.js', secrets)
        else:
            package.write(example, 'assets/local-secrets.js')
        for name, source in sorted(overlay.items()):
            if isinstance(source, Path):
                package.write(source, name)
            else:
                package.writestr(name, source)

