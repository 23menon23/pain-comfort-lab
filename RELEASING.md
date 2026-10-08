# Releasing the lab with a DOI

This checklist takes the repository from a folder on your computer to a public GitHub repository with a citable DOI from Zenodo. Zenodo is a free, CERN-run research archive; its GitHub integration archives each GitHub **release** and gives it a DOI automatically.

## 0 · Before you publish (decisions only you can make)

- [ ] **Authors and order.** Edit `creators` in `.zenodo.json` and `authors` in `CITATION.cff` (keep them identical). Add co-authors, affiliations and ORCID iDs (`"orcid": "0000-0000-0000-0000"` in `.zenodo.json`; `orcid: "https://orcid.org/0000-..."` in `CITATION.cff`). Update the names in `LICENSE`, `LICENSE-CONTENT.md` and the README's *How this lab was made*.
- [ ] **Intellectual property.** Check your university's (and any employer's) policy on publishing teaching materials and code under open licences.
- [ ] **Licences.** The defaults are CC BY 4.0 for text and data and MIT for code. Change them now if needed; they're hard to change after a DOI exists.
- [ ] **Run every notebook on a Colab GPU with the real model** (Steps 0–7, top to bottom). The automated tests use a tiny random model and can't catch scientific surprises.

## 1 · Create the GitHub repository

1. On GitHub, create a new **public** repository (Zenodo and Colab badges need it public), e.g. `pain-comfort-lab`. Don't add a README or licence there; this folder already has them.
2. Point the files at it (this replaces every `23menon23/pain-comfort-lab` placeholder):

   ```bash
   python tools/set_repo_url.py your-github-name/pain-comfort-lab
   ```

3. Push:

   ```bash
   git init
   git add .
   git commit -m "Pain–Comfort Lab 1.0.0"
   git branch -M main
   git remote add origin https://github.com/your-github-name/pain-comfort-lab.git
   git push -u origin main
   ```

4. Check the **Actions** tab: the *Tests* workflow should pass (it runs every notebook on a tiny model, about 5–10 minutes).
5. Open one notebook's **Open in Colab** badge from the README and run its setup cell to confirm the download works.

## 2 · Connect Zenodo (once)

1. Go to [zenodo.org](https://zenodo.org) and **log in with GitHub**.
2. Open the GitHub page in your Zenodo account settings (user menu → **GitHub**).
3. Click **Sync now** if the repository isn't listed, then switch the repository **On**.

*Optional dry run:* [sandbox.zenodo.org](https://sandbox.zenodo.org) works the same way and issues test DOIs, if you'd like to rehearse first.

## 3 · Make the release

1. Fill in the release date in `CHANGELOG.md` (change "unreleased" to today's date) and commit.
2. On GitHub: **Releases → Draft a new release**.
   - Tag: `v1.0.0` (create it on publish).
   - Title: `Pain–Comfort Lab 1.0.0`.
   - Description: paste the 1.0.0 section of `CHANGELOG.md`.
3. **Publish release.** Within a few minutes Zenodo archives a snapshot and mints a DOI. You'll find it under the GitHub page in Zenodo, or by searching Zenodo for the title.

**Which metadata Zenodo uses:** when both files exist, Zenodo reads `.zenodo.json` and **ignores `CITATION.cff`**. GitHub uses `CITATION.cff` for its "Cite this repository" button. Keep the two in sync. Before releasing:

```bash
python -m json.tool .zenodo.json > /dev/null && echo ".zenodo.json is valid JSON"
pip install cffconvert && cffconvert --validate
```

`upload_type` is set to `"lesson"`. If Zenodo files the record under a different resource type, you can correct it on the Zenodo record page (**Edit**); metadata can be edited after publishing, but the archived files can't.

## 4 · After the DOI exists

Zenodo gives you two DOIs:

- a **concept DOI**, which always resolves to the latest version: use this in the README badge and when people cite "the lab";
- a **version DOI** for this specific release: use this when reporting results that depend on exact code and data.

Then:

1. Replace both `10.5281/zenodo.XXXXXXX` placeholders at the top of `README.md` with the concept DOI.
2. Add the DOI to `CITATION.cff`:

   ```yaml
   doi: 10.5281/zenodo.XXXXXXX
   ```

3. Commit and push. (No new release is needed; the next release will include it.)

## 5 · Later versions

1. Make your changes; record them in `CHANGELOG.md` (especially any change to `data/`).
2. Bump the version in `CITATION.cff`, `.zenodo.json` and `pclab/__init__.py` (`__version__`). Use `1.0.1` for fixes, `1.1.0` for new material, `2.0.0` for changes that alter results.
3. Publish a new GitHub release with the matching tag. Zenodo creates a new version DOI under the same concept DOI.

## Related outputs worth considering

- **A short blog explainer** linking to the concept DOI.
- **The *Journal of Open Source Education* (JOSE)** reviews open teaching materials like this lab and publishes a short, citable paper about them.
- **Education venues** (SIGCSE, EAAI) if you study the lab's effect on students; that requires IRB approval before collecting data.
