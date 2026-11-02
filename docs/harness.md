# Slack/Bolt harness

The Slack/Bolt microservice, its Slack manifest, assets, and local configuration
are contained in [`harness/`](../harness/). The root package is an npm workspace
controller, so invoke every command from the workspace root.

## Setup

1. Create a local configuration file from [`harness/.env.example`](../harness/.env.example).
2. Set `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, and `SLACK_SIGNING_SECRET`.
3. In Slack's app creation flow, import [`harness/manifest.json`](../harness/manifest.json).
4. Install dependencies with `npm install`.

## Commands

```sh
npm start             # Start the Bolt Socket Mode app
npm run lint          # Check formatting and lint rules
npm run typecheck     # Check the TypeScript utility
npm run handshake     # Send the configured Slack API handshake
```

The service starts with `harness/` as its current directory, so dotenv resolves
the local `harness/.env` without hard-coded absolute paths.
