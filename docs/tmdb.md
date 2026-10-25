# TMDB integration

tidyTizen uses the TMDB API only when the owner supplies a personal API key. The repository, browser fixture, screenshots, and public widget contain no key.

## Configure a private key

1. Request a v3 API key from your own TMDB account.
2. Copy `app/assets/local-secrets.example.js` to `app/assets/local-secrets.js`.
3. Uncomment `window.CleanHomeSecrets.tmdbApiKey` and paste the key locally.
4. Keep that file untracked. Confirm `git status` does not list it before publishing.

`npm run package` may include the private file in the owner's personal widget. `npm run export:public` deliberately replaces it with the empty example even when a local key exists. Never distribute a personally signed widget containing a key.

## Discovery and refresh

The client requests three popularity-sorted pages each for movies and series. Movies are bounded to roughly the previous two years with a minimum vote count of 40; series use roughly three years and 20 votes. Adult results are disabled, the locale is English/US, and the usable combined catalogue is capped at 80 unique backdrops.

The discovery cache is refreshed when it is missing, older than six hours, or its exclusion-filter signature changes. A failed refresh keeps the existing usable interface. The key is sent only to `api.themoviedb.org`; images load from TMDB's image host.

Anime is excluded by default using TMDB keyword `210024`. Talk shows, reality TV, and the other genre exclusions are independent controls. These filters narrow discovery; they do not rewrite the user's already curated choices.

## Curation and rotation

Choosing a movie or series opens its `/movie/{id}/images` or `/tv/{id}/images` result and offers up to 40 English or language-neutral backdrops. Exact selections are stored in the TV app's localStorage. The available modes are Movies, Series, or Movies + Series; only selected backdrops in the active mode rotate.

Intervals are 16 seconds, 30 seconds, one minute, five minutes, or fifteen minutes. Rotation runs only while the tidyTizen Home view is visible. Settings, another application, or a hidden document pauses the timer so artwork changes do not interfere with navigation.

The Settings backdrop is a locally generated static blurred raster. It does not upload the image or use a server-side blur service.

This product uses the TMDB API but is not endorsed or certified by TMDB.
