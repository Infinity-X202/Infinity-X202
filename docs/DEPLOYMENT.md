# Deployment

The profile is local until you upload it. Nothing in this folder has been committed or pushed.

## Which repository

GitHub shows a profile README only when all of the following are true:

- The repository is public
- Its name matches the user name exactly
- `README.md` is at the repository root and is not empty

Official guide: [Managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)

For this account the repository is:

[https://github.com/Infinity-X202/Infinity-X202](https://github.com/Infinity-X202/Infinity-X202)

On 26 October 2026 that repository existed, was public, and contained only `README.md`. Uploading this package replaces that README. There were no other files to preserve.

## What to upload

Upload these paths, keeping the folder names:

```text
README.md
assets/hero.svg
assets/about-life.svg
assets/stack.svg
assets/id-dashboard.svg
assets/connect.svg
assets/id.png
assets/right_pointing.png
preview.html
docs/
```

`preview.html` and `docs/` are for your own review. The profile page only requires `README.md` and `assets/`.

Do not upload the zip itself as the profile. Do not upload the `.build` folder.

## Steps

1. Sign in to GitHub and open [Infinity-X202/Infinity-X202](https://github.com/Infinity-X202/Infinity-X202).
2. Choose **Add file**, then **Upload files**.
3. Drag in `README.md` and the `assets` folder together so the SVGs stay at `assets/hero.svg` and the other paths in the README.
4. If you also want the notes, upload `preview.html` and `docs`.
5. Commit to the default branch. A suggested message: `Replace profile README with the Infinity X graphics`.
6. Open [https://github.com/Infinity-X202](https://github.com/Infinity-X202) and hard-refresh. Check desktop and a phone width.
7. Click the GitHub link under the connect image.

## If an image looks old or missing

- The filename case must match. GitHub paths are case-sensitive.
- The README links use `?v=1`. After you replace an SVG, change that copy’s query to `?v=2` so cached images update.
- A missing image usually means `assets/` was not uploaded next to `README.md`.

## Animation

The files include SMIL motion. A local Edge check showed the motion in inline SVG, and the resting artwork when the same file was loaded as an image. If GitHub shows a still image, that is expected. The still image includes the name, the first interest, the stack, the card, and the GitHub handle.

## Local preview

Open `preview.html` in a browser from this folder. The top section uses `<img>`, which is the closer match to GitHub. The lower section inlines the SVGs and can freeze them at 0, 2, 5, 9, and 13 seconds.
