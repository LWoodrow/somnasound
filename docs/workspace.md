# Workspace layout

Canonical GitHub project: <https://github.com/LWoodrow/somnasound>

The GitHub repository is currently empty and this working directory is not yet its
local Git checkout: there is no project-level `.git` directory, and the nearest Git
root resolves to the Windows user profile. Repository initialization, first commit,
remote configuration, and push are therefore a separate handoff step rather than an
assumed property of this folder.

```
somnasound/
├── harness/     Slack/Bolt orchestration service and Slack app manifest
├── firmware/    Bare-metal C/C++ source, headers, and board support packages
├── hardware/    KiCad source and generated fabrication outputs
└── docs/        Project documentation
```

The root `package.json` is an npm workspace controller. Its commands delegate by
workspace name, so they remain valid regardless of the shell's working directory:

```sh
npm start
npm run lint
npm run typecheck
npm run handshake
```

Configure firmware with a board-specific cross-toolchain only after selecting the
target silicon:

```sh
cmake --preset bare-metal -S firmware
cmake --build firmware/build/bare-metal
```
