# Configuration

This directory is reserved for **non-secret, version-controlled configuration examples** for the Noctua station.

No application configuration format has been finalized yet. Do not add guessed settings or real device credentials.

## Rules

- Commit examples with placeholders only.
- Keep real passwords, tokens, SSH private keys and authenticated RTSP URLs outside Git.
- Do not publish sensitive wildlife observation coordinates.
- Document each new configuration option when it is implemented.

The repository's `.gitignore` excludes local `.env` files. A future `.env.example` may contain **placeholder names only**, not actual secrets.
