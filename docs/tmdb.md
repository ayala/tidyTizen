# TMDB integration

tidyTizen uses the TMDB API only when the owner supplies a personal API key. The repository, browser fixture, screenshots, and public widget contain no key.

## Configure a private key

1. Request a v3 API key from your own TMDB account.
2. Copy `app/assets/local-secrets.example.js` to `app/assets/local-secrets.js`.
3. Uncomment `window.CleanHomeSecrets.tmdbApiKey` and paste the key locally.
4. Keep that file untracked. Confirm `git status` does not list it before publishing.

On macOS, private owner builds can instead keep the credential in Login Keychain under the `tidyTizen-TMDB` service. The packager reads it at build time and generates `local-secrets.js` only inside the private widget archive. This prevents a public-source synchronization from deleting the working credential. Public exports never consult Keychain.

`npm run package` may include the private file in the owner's personal widget. `npm run export:public` deliberately replaces it with the empty example even when a local key exists. Never distribute a personally signed widget containing a key.

## Discovery and refresh

The client requests three popularity-sorted pages each for movies and series. Movies are bounded to roughly the previous two years with a minimum vote count of 40; series use roughly three years and 20 votes. Adult results are disabled, the locale is English/US, and the usable combined catalogue is capped at 80 unique backdrops.

The discovery cache is refreshed when it is missing, older than six hours, or its exclusion-filter signature changes. A failed refresh keeps the existing usable interface. The key is sent only to `api.themoviedb.org`; images load from TMDB's image host.

From the Home app bar, Up first lands on the All Apps and Settings controls; Up again reveals the compact image-plus curator label in a 130 px black header. Down reverses that same path. OK opens a full-screen view of the latest eligible TMDB titles. Left and Right wrap continuously through the collection, Up adds the visible title backdrop to the curated rotation, and Down removes it only when it is already selected. OK on a title opens its alternate backdrops in a single horizontal strip; Left and Right wrap through those options and Up selects the visible option. The artwork insets evenly into a rounded black frame in this title-detail state. The removal control is intentionally absent for unselected artwork. Back first returns to titles, then to the still-open Home curator tray.

Anime is excluded by default using TMDB keyword `210024`. Talk shows, reality TV, and the other genre exclusions are independent controls. These filters narrow discovery; they do not rewrite the user's already curated choices.

## Curation and rotation

Choosing a movie or series opens its `/movie/{id}/images` or `/tv/{id}/images` result and offers up to 20 strictly textless backdrops. The client accepts only images whose TMDB language metadata is null; language-specific artwork is discarded. Exact selections are stored in the TV app's localStorage. Up and Down persist selection changes immediately without starting an appearance transaction, so browsing remains responsive. The full Home image, material copies, and blurred Settings raster are prepared after leaving the curator. The available modes are Movies, Series, or Movies + Series; only selected backdrops in the active mode rotate.

Intervals are 16 seconds, 30 seconds, one minute, five minutes, or fifteen minutes. Rotation runs only while the tidyTizen Home view is visible. Settings, another application, or a hidden document pauses the timer so artwork changes do not interfere with navigation.

The Settings backdrop is a locally generated static blurred raster. It does not upload the image or use a server-side blur service.

This product uses the TMDB API but is not endorsed or certified by TMDB.
