# Fixed-version citation and archiving

CITATION.cff contains verified author names and the configured repository URL.
No release version, publication date or DOI has been invented. The repository
was not committed, tagged, pushed or published by this preparation task.

1. Resolve RELEASE_CHECKLIST.md and finalize the dataset/manuscript match.
2. Review git diff/status, including ignored checkpoints. Commit the exact files
   that support the resubmitted manuscript.
3. Create a version tag such as v1.0.0 only when that version is finalized.
   Record the actual commit with git rev-parse HEAD.
4. Add the actual version and date-released fields to CITATION.cff. If using
   Zenodo/Mendeley Data or another persistent archive, add its real DOI after
   deposit. GitHub alone does not automatically create a DOI.
5. Cite the immutable release/commit or archived DOI in the manuscript Data
   Availability statement and dataset reference, not just the moving main branch.
6. When metadata changes after archiving, issue a new version rather than
   describing changed files as the same fixed release.

Suggested manuscript sentence, to complete only after the deposit exists:
"The supporting data and code are available at [repository URL], release [actual
tag] (commit [actual hash]), archived at [actual DOI, if available]. The released
dataset and exclusions correspond to the analyses reported in this version of
the manuscript."
