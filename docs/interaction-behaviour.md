# Interaction behaviour — 0.6.1

## Paired icon and text spacing

Any icon, status dot, remote-button glyph, logo, or attribution mark paired with text must use an explicit layout gutter. Never rely on a text space, glyph side-bearing, absolute-position coincidence, or inherited gap. The visible elements must not touch at any supported viewport or font metric; use at least 16 px for compact controls and 24 px for attribution or descriptive rows.

The vertical List Home controls are a recurring regression boundary. All Apps and Settings must retain at least 24 px of visible edge-to-edge separation in Text, Icons, and Icons + Text modes, including focused scale states; the current target is 28 px. Tests must compare the rendered button rectangles; a declared flex `gap` alone is not evidence that the controls are separated.

List/Text responsiveness must be judged on the target QN800A as well as in the browser. Its focus movement uses a 90 ms heavy ease-out and its glass plate reuses one background layer; do not add alternating full-background plates or lengthen the motion based only on desktop rendering, and do not describe the path as fixed until the TV build has been exercised.

## Home

- Dock: Left/Right scrolls the apps without wrapping. With more than six apps, the row shows six complete positions: focus advances through position five, then each subsequent move shifts the row by one whole app position so a complete next app enters position six. The true first and last apps can occupy the physical edge. A blocked Left or Right at that true edge gives the app contents a short directional elastic response, while the glass bar remains fixed. Up enters the All Apps and Settings controls at the last selected control and completely clears visual focus from the app bar; Up again reveals the curator. Left/Right moves between All Apps and Settings. Down or Back returns focus to the selected app. The clock is at the top left.
- List: Up/Down scrolls the apps without wrapping. Down from the last app opens Sources; Up or Back closes Sources. Right enters the bottom-right controls, aligned with the clock above, and completely clears visual focus from the app list. Up/Down moves between All apps and Settings. Left or Back restores focus to the selected app. The list fades at both ends as it scrolls.
- OK opens the selected item. Focus alone never launches an app.
- Icons-only apps and controls reveal their names when focused. App presentation and control presentation are independent.
- Back from the app list or Dock opens a choice to stay or open Samsung Home.
- A panel keeps focus within its own controls. Back closes one panel at a time.
- Returning to the running launcher keeps the selected app or panel item. There is no auto-return timer. Held OK and Back keys act once until the key is released.

## Settings and appearance

Settings opens a grouped overview: Background, Layout, Typography, Focus, Apps on Home and Samsung. OK opens a group. Appearance groups use a two-pane screen with visible choices on the left and the committed Home preview on the right.

| Group | Choices |
| --- | --- |
| Background | Photo, Light, Dark; Wallpaper and Artwork when Photo is active |
| Layout | List or Dock; independent Text, Icons or Both choices for apps and Home controls |
| Typography | Manrope, Neue Montreal, Mori, Pangram Sans, Geist and Newsreader, when available |
| Focus | Type or Glass; Soft, Frost or Clear tint material |
| Apps on Home | Membership and arrangement editor |
| Samsung | Samsung Home and input-source settings |

Up/Down moves between rows. Left/Right moves between choices in a horizontal row. Focus alone changes neither the preview nor saved preferences in these appearance groups. Wallpaper has its own temporary photo preview, described below. OK applies the focused value. A checkmark identifies the applied value; the filled plate identifies remote focus. Applying the current value does not write again.

Material applies to a photographic Dock, or Glass focus on a photographic List. Inactive material choices remain visible with an explanation and are skipped during navigation. Their stored value is retained. Wallpaper and rotation are also inactive on flat backgrounds.

Artwork owns both Rotation and Filters so the top-level Background screen stays concise. Dynamic Movies and Series rotation can be set to 16 seconds, 30 seconds, one minute, five minutes, or fifteen minutes; scenery retains its existing fixed, on-open, five-minute, fifteen-minute, and hourly choices. Anime is excluded by default using TMDB's dedicated Anime keyword rather than treating all animation as anime. Talk Shows and Reality TV remain separate content types. The remaining filters cover Action & Adventure, Animation, Comedy, Crime, Documentary, Drama, Kids & Family, History, Horror, Music, Mystery, Romance, Sci-Fi & Fantasy, Thriller, War & Politics, and Western. These exclusions change the eligible TMDB backdrop pool without changing the selected Movies, Series, or Movies + Series mode.

Home has two directional reveal layers. Down exposes HDMI sources. Up first enters the All Apps and Settings controls; Up from that row exposes a compact, unplated image-plus label in a 130 px black header while shifting the complete Home composition downward and rounding its upper corners. Down reverses the same path through the controls before returning to apps. Every successful Home focus change—including Left and Right across the main app bar—uses a short local cue at moderate gain. Sources and the curator use distinct lower and higher pitches, while OK and Back retain slightly different soft cues. The app never changes the TV's master volume, and navigation remains usable when Web Audio is unavailable. In the full-screen curator, Left and Right wrap infinitely, Up immediately saves the visible image, Down immediately removes it only when selected, and OK opens that movie or series. Curation never starts Home's multi-image appearance transaction; that work is deferred until the user leaves the curator, keeping every directional action available. Its alternate backdrops—up to 20 and restricted to TMDB images with no language metadata—appear in one horizontal thumbnail strip below the visual midpoint, while the hero image shrinks into an evenly inset rounded black frame. Back returns from backdrop options to titles and then restores the open top tray. The selection control pulses on input; the trash control is dynamic rather than a disabled permanent ornament. All Apps and Settings use their own 10%/20% plates; no second moving utility-lens layer is rendered behind them.

Settings → Focus includes an Interface sounds On/Off choice. It defaults to On for existing installations, saves immediately, and suppresses every Home, Sources, and curator cue when Off.

A font or photo change applies only after its resources are ready and storage succeeds. A load or storage failure keeps the previous appearance and checkmark, with a Try again action. Back cancels a pending change, leaves the group and keeps completed changes. Late load callbacks cannot apply a cancelled choice. There is no Save button. Returning to a group restores its last choice focus; returning to Settings restores its category focus. Rotation is nested within Background, and Back returns to its Rotation row.

The selected font applies to Home app names, the clock and Home controls, including Newsreader. Settings, All apps, the Home editor and status text retain Manrope. The preview shows the committed Home appearance and its clock continues to update. Pangram faces are available in Nathan's private build when the local files are present; their binaries are not included in the public source. An unavailable optional face is omitted. If the baseline font is slow or missing, Home remains usable with a local fallback and can recover when the font loads.

## Streaming apps

The nine default apps keep their known native IDs. Other installed consumer apps can also be added to Home. Launching uses the public `tizen.application.launch` API with the app's native ID. A physical `GROUP` app-control experiment was removed after the installed streaming apps returned to Samsung's system destination and Netflix stopped responding usefully to Back. Missing apps and denied launches produce a real error. No web player, placeholder success page or account credential is embedded.

## All apps

The panel reads `tizen.application.getAppsInfo` on entry and shows the filtered consumer apps alphabetically. Samsung's visibility flag alone also exposes system utilities, so EP packages, background services, ad players, account utilities, placeholders and duplicates are omitted. Known brands use bundled marks. Other apps use their local installed icon, with initials as a fallback.

The five-column grid scrolls with remote focus. OK launches an app; its On Home badge shows membership. Up from the first row reaches Apps on Home, which opens the editor. An API failure shows a retry and keeps saved Home choices. Browser previews report that installed-app discovery and launching require the TV.

## Apps on Home

Open the editor from Settings or All apps. On Home shows the current order on the left. Not on Home shows Recently removed first, followed by other installed apps on the right. Home holds one to nine apps.

- Reorder: OK on an app name picks it up. Up/Down moves it. OK places it and saves the order. Back puts an unplaced app back without saving that move.
- Remove: Right from an app name reaches Remove from Home. OK saves the removal and moves focus to the same app in Recently removed. The app stays installed.
- Add: OK on an app in Not on Home adds it and saves. A recently removed app returns to its previous position within the editing session; another app is added at the end. Focus follows the app to its Remove from Home control, so another OK can reverse the addition.
- Undo reverses a completed addition, removal or reorder from the current editing session. Done or Back closes the editor and keeps completed changes. Undo history ends when the editor closes.

Removing the last Home app or adding a tenth app is prevented. A failed storage write keeps the committed choices and order, with a retry message. Saved native app IDs and names survive a restart or a failed catalogue refresh.

## Art Mode and Samsung screens

Art Mode sends an application control to the installed `org.tizen.art-app`, with `mode=fullscreen` and `requester=mobile`. This aims to enter native Art Mode with its current artwork, without toggling power or changing the selected artwork.

This mode comes from [research on Samsung's Art app](https://github.com/TheFab21/ha-samsungtv-smart/blob/master/notes/QN55LS03FAFXZA/ART_MODE_DECOMPILED.md), on another Tizen 9 Frame model. It is an internal Samsung contract, not a documented public Art API. Its visible behaviour on this exact firmware must be confirmed on the TV.

Samsung Home explicitly launches the original `com.samsung.tv.csfs` app, independently of the new Home assignment. The earlier `com.samsung.tv.coba.newhome` component did not open Smart Hub visibly and is no longer the escape target. The Samsung section does not show a TV Settings shortcut because the internal settings component is not a working launch target on this firmware. Exact on-device destinations are recorded in docs/tv-status.md; launch callbacks alone are not visual proof. There is no blind power-key fallback.

All calls have bounded response handling. A failure leaves CleanFrame usable. No simulated device success views remain. Browser validation cannot confirm the visible Samsung destination.

## Preferences and wallpaper

The launcher stores appearance, Home order, recently removed apps, the last launched Home app, wallpaper and rotation locally. List and Dock share these preferences. The existing `cleanframe.home.v1` key is retained, with a fallback read from `cleanframe.shore.v1`. Legacy List maps to Dark + List + Type; Glass Dock and Glass Grid map to Photo + Dock + Glass. App order, wallpaper, rotation and the last Home app are preserved.

The gallery contains 15 bundled wallpapers. Settings → Background → Wallpaper keeps the two-pane Settings frame. Up/Down browses a vertical thumbnail list without wrapping; the right-hand Home preview shows the candidate while the surrounding Settings backdrop stays on the applied photo. OK applies the focused photo and stays in Wallpaper. The tick marks the applied photo and preview status distinguishes unsaved browsing. Back restores the latest applied photo, cancels pending loading and returns to Background’s Wallpaper row. Photo and material assets change as one complete bundle; a failed load restores the applied preview and offers retry. Preview loading waits briefly for remote focus to settle. OK during loading queues application for that photo; another browse move or Back cancels it. Browsing never saves, and repeated OK on the applied photo does not write again.

Settings → Background → Rotation offers Fixed, Each time Home opens, Every 5 minutes, Every 15 minutes and Every hour. Each time Home opens advances once when the launcher loads; a return to the already-running launcher does not advance it. Timed rotation counts only visible Photo Home time in either List or Dock. Panels, flat backgrounds and time spent in other apps pause the cycle. Changing the photo or rotation mode starts a new interval.

Launcher wallpaper is separate from native Art Mode. Runtime photos, materials and available fonts are local assets; they do not require the Mac or a network download.

## Sources

When the source tray is open, each HDMI source shows a quiet row of compact
capability flags above its icon and name. HDMI 1 and 2 show `8K 60Hz` and
`4K 120Hz`; HDMI 3 also shows `eARC`; HDMI 4 instead adds `Gaming`. These are
static port-capability annotations for this QN800A layout, not negotiated
signal-format indicators. Their near-black charcoal treatment keeps the source
name, platform icon and connected-state dot visually dominant.

- [Samsung Application API](https://developer.samsung.com/smarttv/develop/api-references/tizen-web-device-api-references/application-api.html): installed-app discovery and application control.
- [Samsung application termination guide](https://developer.samsung.com/smarttv/develop/guides/fundamentals/terminating-applications.html): exiting is not treated as a deterministic Samsung Home route.

The native Home operation and startup configuration from 19 October remain separate from this app update. Home from Netflix was confirmed for that configuration; power-on after Netflix remains provisional. Streaming apps retain their own Back navigation. Netflix did not exit on repeated Back in the observed test, so there was no app-exit destination to verify. No global Back interception or key-filter hook was installed. See [TV status](tv-status.md) for device evidence; this behaviour specification is not an installation or visual-verification record for 0.6.0.

## Clock and rendering

Both layouts show the TV's local time in 12-hour format, without AM/PM or seconds. It updates at the minute boundary and on return to the launcher. No date or clock panel is shown.

Photographic materials and blurred panel backgrounds are generated before packaging and stay aligned with the full-screen image. Photo colour and contrast metadata are also prepared offline. Navigation does not sample image pixels, run an optics engine or apply live backdrop blur. Flat backgrounds use matching light or dark panel colours. Focus feedback uses transforms and opacity; reduced motion removes animated scaling and movement while retaining opacity feedback.
