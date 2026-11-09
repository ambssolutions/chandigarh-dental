# Chandigarh Multispeciality Dental Clinic, Chamkaur Sahib

Single-page website for the clinic. Everything is in one file, `index.html`. There is no build step.

**Features:** interactive tooth chart, treatments carousel, live open/closed status in clinic time (IST) with a countdown, English / Hindi / Punjabi, WhatsApp booking, a voice assistant (English, Hindi and Punjabi), light and dark themes, works on phones, tablets and laptops.

## Put it online with GitHub Pages

1. Create a repository on GitHub and upload these files (`index.html`, `i18n.json`, `robots.txt`, `llms.txt`, `vercel.json`, `README.md`, `.nojekyll`).
2. Open the repository's **Settings > Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, pick `main` and `/ (root)`, then **Save**.
4. After a minute the site is live at `https://<your-user>.github.io/<repository>/`.

You can also open `index.html` by double-clicking it. It needs an internet connection for the fonts and the 3D tooth.

## Things to check and edit (search for these in `index.html`)

| What | Where to look |
|---|---|
| Phone number `+91 99155 10261` and WhatsApp link `919915510261` | search `9915510261` |
| Opening hours (Monday to Saturday, 10 AM to 7 PM) | search `var sched =` |
| Address (Morinda Road, opposite the bus stand, Chamkaur Sahib 140112) | search `Morinda Road` |
| Rating (4.1 from 9 Google reviews, as of when it was checked) and the review link | search `Average of 9 reviews` |
| "15+ years of experience" | search `Years of experience` |
| Hindi and Punjabi wording | `i18n.json` (English text → Hindi and Punjabi). It loads only when a visitor picks one of those languages. |

The phone number, address, hours and rating match the clinic's public Google listing at the time they were checked. Keep them in step with your Google Business Profile if they change.

## Optional: read opening hours from the Google Business Profile

Near the top of the hours code there is a line:

```js
var GOOGLE = {placeId: '', apiKey: ''};
```

Fill in the clinic's Google Place ID and a Google Maps Places API key to read the hours (including holidays) from Google. The key is visible to anyone who views the page, so restrict it to your website address in Google Cloud. Do not commit a key that is not restricted.

## Doctors, reviews and photos

Near the end of `index.html` there is one line to fill in:

```js
var CLINIC = {doctors: [], reviews: [], photos: []};
```

Each section ("Your dentists", "What patients say", "Inside the clinic") stays hidden until it has real entries. Only add real names, reviews the patient agreed to share, and the clinic's own photos. Never add made-up ones.

## Files

- `index.html`: the whole site
- `i18n.json`: Hindi and Punjabi text
- `robots.txt` and `llms.txt`: for search engines and AI assistants
- `vercel.json`: deploys `main` only, adds security headers, and allows the microphone for the voice assistant

## Seeing old content after an update?

- `vercel.json` tells Vercel (and browsers) to check for a new version on every visit instead of reusing an old copy. Keep it in the repository.
- `index.html` contains a `build` stamp and a small script. When a visitor opens the site, the script asks the server for the latest page, and if it is newer than the copy in the browser it reloads once. Each new version of the file carries a new stamp.
- A phone or computer that already saved the old page, from before these files were added, may still show it once. Reload without the cache (Ctrl+Shift+R, or clear the site's data in the phone browser's settings). After that it stays current.
- On Vercel every push creates a new deployment. Check the **Deployments** tab to make sure the latest one finished and is marked as production.
- GitHub Pages keeps pages in its own cache for up to about ten minutes. That cannot be changed from the site's files.

## Notes

- Hindi and Punjabi wording was written by an AI assistant and should be checked by a native speaker.
- The 3D tooth uses three.js from cdnjs. It loads only on laptops and desktops (mouse, wide screen, more than 4 CPU cores), after the first mouse move or scroll or after 4 seconds. Phones, tablets and data-saver connections keep the flat tooth, which keeps scrolling smooth.
- Fonts (Unbounded for the hero headline, Plus Jakarta Sans for everything else, plus Noto Sans for Hindi and Punjabi when chosen) come from Google Fonts.

## Phone menu and settings

On phones and tablets the top bar shows the logo, the voice button and a menu button. The menu holds the page sections and the settings, each remembered on that device:

- **Language:** English, ਪੰਜਾਬੀ, हिन्दी
- **Theme:** Auto (follows the phone), Light or Dark
- **Text size:** Normal or Large
- **Voice replies:** whether the voice assistant answers out loud

It also has Call and WhatsApp buttons.

## Voice assistant

The microphone button in the top bar listens in the language chosen on the page (English, Hindi or Punjabi) and answers out loud. It uses the browser's own speech recognition, so it works in Chrome, Edge, Samsung Internet and Safari. In browsers without it (for example Firefox) the button does not appear. Speech is turned into text by the browser's service (Google in Chrome); the clinic does not record anything.

Things it understands, for example:

| Say | What happens |
|---|---|
| "Are you open now?" / "ਕੀ ਕਲੀਨਿਕ ਹੁਣ ਖੁੱਲ੍ਹਾ ਹੈ?" | Reads the live open/closed status and hours |
| "Book a root canal on Monday, my name is Raj" / "सोमवार को रूट कैनाल बुक करो" | Fills in the booking form and offers a "Send on WhatsApp" button |
| "Show tooth 14" / "upper left wisdom tooth" | Picks the tooth on the chart and reads what it usually needs |
| "Do you treat children?" / "मुझे दाँत में दर्द है" | Opens the matching question and reads the answer |
| "Call the clinic", "WhatsApp", "Where is the clinic?" | Offers a Call, WhatsApp or map button (browsers only open these from a tap) |
| "Switch to Punjabi", "dark mode" | Changes the language or theme |

The words it listens for are in the `var W = {` and `var SVC = [` lists near the end of `index.html`. Spoken replies are in `var VT = {`.

## Photos

The three photos in "Your visit" (`img/visit-*.webp`) are free stock photos from Pexels (Pexels licence: free to use, no attribution required), labelled on the page as "Illustrative photos". They are not photos of this clinic. Replace them with the clinic's own photos when available: keep the same file names, or update the `srcset` in `index.html`.

- `visit-chair`: pexels.com/photo/3845625
- `visit-consult`: pexels.com/photo/3845810
- `visit-smile`: pexels.com/photo/3762453
