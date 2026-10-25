# QN800A-specific behavior

The reference customization targets a Samsung `QN75QN800AFXZA` on firmware `T-OSCPAKUC-2220.9` and Tizen 6.0. It should be treated as a tested profile, not a claim that every Samsung TV has the same ports, app IDs, input API, rendering performance, or native key routing.

## HDMI sources

Tizen's `VIDEOSOURCE` property supplies connected and disconnected source objects. tidyTizen derives the immutable port label and connection state from those objects and switches through `tizen.tvwindow.setSource`. Samsung's user-visible device name and icon are not exposed consistently on this firmware, so tidyTizen provides a local override editor.

Each source profile stores a display name of up to 40 characters, one icon ID from the bundled platform/device catalogue, and the underlying `type:number` key such as `HDMI:3`. Reset removes the local override and returns to the Tizen-reported fallback name. The source itself is never renamed in Samsung's system UI.

The `8K 60Hz`, `4K 120Hz`, `eARC`, and `Gaming` pills are hard-coded annotations chosen for this particular setup. They are not EDID, HDMI-handshake, or active-format detection. Change `sourceCapabilities()` in `app/main.js` for a different television.

## Compatibility notes

- Known reference application IDs are listed in `app/device.js`; IDs vary by region, model, app version, and Samsung store package.
- The manifest keeps `EaQN8Home1.CleanHome` only so in-place updates and the reference Home interceptor continue to target the installed application. A new owner must create a new identity and update all matching guards.
- The 1920 × 1080 logical stage is scaled to the panel; 8K describes the display/port capability, not the web-app render surface.
- Runtime JavaScript stays ES5-compatible for the Tizen 6 browser engine.
- Netflix has unusual Back behavior on this firmware. Long Back/Exit is the reference escape route; short Back must remain available to applications.
