# Chandigarh Multispeciality Dental Clinic, Chamkaur Sahib

Single-page website for the clinic. Everything is in one file, `index.html`. There is no build step.

**Features:** interactive tooth chart, treatments carousel, live open/closed status in clinic time (IST) with a countdown, English / Hindi / Punjabi, WhatsApp booking, light and dark themes, works on phones, tablets and laptops.

## Put it online with GitHub Pages

1. Create a repository on GitHub and upload these files (`index.html`, `README.md`, `.nojekyll`).
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
| Hindi and Punjabi wording | the `var TR = [` translation table |

The phone number, address, hours and rating match the clinic's public Google listing at the time they were checked. Keep them in step with your Google Business Profile if they change.

## Optional: read opening hours from the Google Business Profile

Near the top of the hours code there is a line:

```js
var GOOGLE = {placeId: '', apiKey: ''};
```

Fill in the clinic's Google Place ID and a Google Maps Places API key to read the hours (including holidays) from Google. The key is visible to anyone who views the page, so restrict it to your website address in Google Cloud. Do not commit a key that is not restricted.

## Notes

- Hindi and Punjabi wording was written by an AI assistant and should be checked by a native speaker.
- The 3D tooth uses three.js, loaded from cdnjs after the page appears. The flat tooth shows first and is the fallback.
- Fonts (Plus Jakarta Sans, Unbounded, Figtree, JetBrains Mono, plus Noto Sans for Hindi and Punjabi) come from Google Fonts.
