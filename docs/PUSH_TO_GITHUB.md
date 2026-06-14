# Pushing this to GitHub

You've got two paths — pick the one you're comfortable with.

---

## Option A — Web UI (no command line, ~3 min)

1. Go to <https://github.com/new>
2. Repo name: `no410` · Description: `No410 — single-unit luxury detached residence, Miri` · **Public**
3. **Do not** tick "Add README/.gitignore/license" — the zip already has them.
4. Click **Create repository**.
5. On the empty repo page, click **uploading an existing file**.
6. Unzip `no410.zip`, then **drag the entire contents** (not the outer folder — the files inside it) into the browser.
7. Commit message: `Initial commit — No410 v0.1.0`
8. Click **Commit changes**.

Done. The repo is live.

---

## Option B — Command line (~1 min)

```bash
# unzip somewhere
unzip no410.zip
cd no410

# initialise + first commit
git init -b main
git add .
git commit -m "Initial commit — No410 v0.1.0"

# create the remote repo with GitHub CLI...
gh repo create no410 --public --source=. --remote=origin --push

# ...OR, if you don't have `gh`, create it manually at github.com/new then:
git remote add origin https://github.com/<you>/no410.git
git push -u origin main
```

---

## After it's up

- Tag the first release: `git tag v0.1.0 && git push --tags`
- Future edits → edit files → `git add -A && git commit -m "what changed" && git push`
- To rebuild the single-file brochure: `python3 scripts/build_bundle.py`

## Going live later

When you're ready for a public preview URL:

1. Repo → **Settings → Pages**
2. Source: **Deploy from a branch** · Branch: `main` · Folder: `/ (root)`
3. Save. After ~1 min the site is at `https://<you>.github.io/no410/`.

(We chose to skip this for now, but it's there when you want it.)
