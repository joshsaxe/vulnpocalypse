# Scripts

## `publish.sh`: put this folder on GitHub

    bash scripts/publish.sh                    # a PRIVATE repository called "vulnpocalypse" under your own account
    bash scripts/publish.sh --public           # public instead
    bash scripts/publish.sh --name my-repo     # another repository name
    bash scripts/publish.sh --owner my-org     # under an organisation you belong to
    bash scripts/publish.sh --as-me            # first make the single commit yours (author = your git identity)
    bash scripts/publish.sh --dry-run          # say what it would do; change nothing

It needs `git` and the [GitHub CLI](https://cli.github.com), signed in with `gh auth login`. It then:

1. makes a git repository and a first commit, if this folder has no `.git` folder (a folder that arrives with one is left as it is, and the script refuses to run if there are uncommitted changes);
2. creates the GitHub repository, **private unless you pass `--public`**, with a description and topics;
3. pushes the current branch and prints the address.

It never deletes anything, and it will not touch a repository that already exists: if `OWNER/NAME` is taken it stops and prints the two commands to push to it yourself.

**No GitHub CLI?** Create an empty repository on github.com, then:

    git init -b main && git add -A && git commit -m "Add data, code and annotated bibliography"
    git remote add origin git@github.com:YOUR-NAME/vulnpocalypse.git
    git push -u origin main

**Making it public later**, when the post is out:

    gh repo edit YOUR-NAME/vulnpocalypse --visibility public --accept-visibility-change-consequences

## Before the repository goes public

1. **Check what it says about the post.** [`docs/METHODS.md`](../docs/METHODS.md) reproduces the post's methods appendix. The README's sections on [what the numbers are and are not](../README.md#what-the-numbers-are-and-are-not) and [where the results are fragile](../README.md#where-the-results-are-fragile) report what the repository's own robustness checks found. Edit the wording if you want to; the numbers come from [`sensitivity/`](../sensitivity) and the [model cards](../docs/MODELS.md#robustness-checks).
2. **Add the address to [`CITATION.cff`](../CITATION.cff)** (`repository-code: https://github.com/YOUR-NAME/vulnpocalypse`), and link the repository from the post.
3. **Check the licences are the ones you want.** Code is MIT ([`LICENSE`](../LICENSE)); figures, documents and data tables are CC BY 4.0 ([`LICENSE-CONTENT.md`](../LICENSE-CONTENT.md)). To change either, edit those files, [`NOTICE.md`](../NOTICE.md), `CITATION.cff` and the "Provenance" section of the README.
4. **Run `make verify`** after any edit to the documents: it also checks every link and that the bibliography still matches the tables.
5. **Optional.** Make a GitHub release and connect the repository to [Zenodo](https://zenodo.org) for a citable DOI; turn on Issues so readers can report a wrong row.
