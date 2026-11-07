# Security model

The application can interact with external services and store sensitive job-search data. Run it only on a trusted machine or behind appropriate access controls; the application is not a public multi-user service.

## Operational boundaries

- Drafting and external submission are separate actions. Live scripts require explicit settings; verify the effective configuration before running them.
- Captchas, login challenges and uncertain delivery outcomes require manual review.
- Store tokens, browser profiles, databases and logs outside version control. `.gitignore` covers the standard local paths, but does not protect files that were already tracked.
- The demonstration entry point uses a temporary database and synthetic vacancies. It does not register the production API or integrations.

## Public repository

The repository history includes candidate profiles and operational notes. Removing a file from the current tree does not remove it from previous commits or existing clones. Review tracked files and history before sharing; rotate any exposed credentials through their provider rather than relying on deletion alone.

To report a security issue, follow [SECURITY.md](../SECURITY.md).
