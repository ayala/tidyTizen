# Home remapping on the QN800A

This is an engineering record of the approach proven on one owner-authorized Samsung QN800A. It is not a universal install recipe or a promise of firmware compatibility.

## What did not solve it

- Registering Home in a normal Tizen web app cannot make the app a system-wide Home handler.
- Launching tidyTizen after Samsung Home appears is visibly late and cannot reliably suppress the Samsung menu.
- Writable Home/startup preferences did not override this firmware's root-owned `tvctx-manager` key-filter route.
- A Mac-side key watcher proved the interaction but was rejected as a final solution because Home had to work when the Mac was off.
- Replacing short Back globally would break in-app navigation, and Netflix does not behave like the other tested applications at its root screen.

## Working input path

Inspection showed the Smart Remote as `Smart Control 2016` on `/dev/input/event5`; physical Home is Linux key code 63 (`XF86Home`). A native TV-side agent opens only that named input, obtains an exclusive `EVIOCGRAB`, creates a virtual remote through `/dev/uinput`, forwards ordinary events unchanged, withholds Home from Samsung's router, and launches the configured tidyTizen application.

Because Samsung never receives Home, its menu does not appear or flash. This is the important difference from an after-the-fact watcher. The agent releases its device grab and virtual device if it exits, returning the remote to native handling.

Short Back is forwarded normally. The tested guard redirects only when the result is Samsung Home. Holding Back for about 0.65 seconds, or an Exit event, launches tidyTizen; this is the reliable escape for Netflix on the reference firmware.

## TV-local persistence

The bounded proof initially used an authenticated Mac callback. The final reference setup moved execution to the TV: the original `com.samsung.tv.ghservice` installation and database row were backed up on and off the TV; its boot-capable slot was adapted to start a volatile root launch chain; and that chain creates supervised transient services for the interceptor and an optional authenticated development bridge. Developer Mode's Host PC address must be `127.0.0.1` for the self-contained boot route.

The helper window is transparent and hidden during normal boot. A one-shot marker is required to reveal its manager UI. The Mac is needed for installation, development, diagnostics, or rollback, but not for normal Home-button operation after the local boot chain is active.

The application ID remains `EaQN8Home1.CleanHome` on the reference TV even though the visible name is tidyTizen. Changing that ID without updating the native launch target breaks Home.

## Safety and rollback boundary

Before modifying anything, record the exact model, firmware, runtime, application identity, input node/name, original package row, original Samsung service files, and their hashes. Store the recovery archive off the TV and validate that recovery can restore those exact values.

The reference rollback stops the interceptor, restores the original Samsung service archive and package row, preserves the modified copy rather than deleting it, and verifies hashes. Firmware updates can invalidate every assumption. Never transplant reference binaries, certificates, bridge secrets, addresses, or recovery values to another TV.

Owner-private recovery material is intentionally separate from the public web app. This repository documents the design and retains guarded development sources, but does not contain signing credentials, bridge tokens, compiled payloads, device addresses, or a turnkey model exploit.
