# Chandigarh Multispeciality Dental Clinic, Chamkaur Sahib

Single-page website for the clinic. Everything is in one file, `index.html`. There is no build step.

**Features:** interactive tooth chart, treatments list, live open/closed status in clinic time (IST) with a countdown, English / Hindi / Punjabi, WhatsApp booking, light and dark themes, works on phones, tablets and laptops.

## Put it online with GitHub Pages

1. Create a repository on GitHub and upload these files (`index.html`, `README.md`, `.nojekyll`).
2. Open the repository's **Settings > Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, pick `main` and `/ (root)`, then **Save**.
4. After a minute the site is live at `https://<your-user>.github.io/<repository>/`.

You can also open `index.html` by double-clicking it. It needs an internet connection for the fonts.

## Things to check and edit (search for these in `index.html`)

| What | Where to look |
|---|---|
| Phone number `+91 99155 10261` and WhatsApp link `919915510261` | search `9915510261` |
| Opening hours (Monday to Saturday, 10 AM to 7 PM) | search `var sched =` |
| Address (Morinda Road, opposite the bus stand, Chamkaur Sahib 140112) | search `Morinda Road` |
| Rating (4.1 from 9 Google reviews, as of when it was checked) and the review link | search `4.1` (hero, contact panel and the JSON-LD at the top) |
| Hindi and Punjabi wording | the `var TR = [` translation table |

The phone number, address, hours and rating match the clinic's public Google listing at the time they were checked. Keep them in step with your Google Business Profile if they change.

## Optional: read opening hours from the Google Business Profile

Near the top of the hours code there is a line:

```js
var GOOGLE = {placeId: '', apiKey: ''};
```

Fill in the clinic's Google Place ID and a Google Maps Places API key to read the hours (including holidays) from Google. The key is visible to anyone who views the page, so restrict it to your website address in Google Cloud. Do not commit a key that is not restricted.

## Seeing old content after an update?

- `vercel.json` tells Vercel (and browsers) to check for a new version on every visit instead of reusing an old copy. Keep it in the repository.
- `index.html` contains a `build` stamp and a small script. When a visitor opens the site, the script asks the server for the latest page, and if it is newer than the copy in the browser it reloads once. Each new version of the file carries a new stamp.
- A phone or computer that already saved the old page, from before these files were added, may still show it once. Reload without the cache (Ctrl+Shift+R, or clear the site's data in the phone browser's settings). After that it stays current.
- On Vercel every push creates a new deployment. Check the **Deployments** tab to make sure the latest one finished and is marked as production.
- GitHub Pages keeps pages in its own cache for up to about ten minutes. That cannot be changed from the site's files.

## Notes

- Hindi and Punjabi wording was written by an AI assistant and should be checked by a native speaker.
- Fonts (Newsreader for headings, Figtree for text, plus Noto Sans for Hindi and Punjabi, loaded only when chosen) come from Google Fonts.
- The logo mark is a placeholder. Replace it with the clinic's real logo (SVG) when available, and take the accent colour from it (`--accent` at the top of the styles).
- "15+ years of experience" was removed from the page until the clinic confirms it. Descriptions for fillings, implants and whitening are new and should be checked by the dentist.
