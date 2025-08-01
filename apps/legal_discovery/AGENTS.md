# Legal Discovery Module Guide

- Keep the Flask routes and dashboard UI in sync. All features should be production ready with no placeholders.
- Ensure the dark theme remains responsive and professional.
- Log progress here before each commit with notes on next steps.

###STARTUP SCRIPT###
```bash
#!/bin/bash
set -e
python3 -m venv venv
source venv/bin/activate
export PYTHONPATH=$(pwd)
pip install -r requirements.txt
pip install python-dotenv flask gunicorn pillow requests neuro-san pyvis
```

### Update 2025-07-27T20:30Z
- Added interactive chat panel and settings modal to the dashboard.
- Refined styles with responsive grid and sticky navigation.
- Connected all controls to backend APIs via `dashboard.js`.
- Next: enhance data visualisations for the knowledge graph and timeline.

## Update 2025-07-27T21:07Z
- Updated imports for legal discovery tools to match new neuro_san package layout
- Install attempts failed due to network restrictions
- Next: test the Flask app in Docker once dependencies are resolved

## Update 2025-07-27T21:25Z
- Installed dependencies locally to run tests successfully
- Verified coded tool imports after update; tests pass
- Next: rebuild Docker image and ensure Flask app loads correctly

## Update 2025-07-27T21:29Z
- Confirmed tests run successfully after installing dependencies
- Docker tooling not available here so image build couldn't be tested
- Next: verify Docker compose when environment supports it
## Update 2025-07-27T22:15Z
- Introduced tabbed interface and updated dashboard scripts
- Next: refine styles and test Docker stack

## Update 2025-07-27T22:45Z
- Migrated dashboard to React for a richer UI
- Added dashboard-react.jsx and updated template to load React
- Next: run tests and verify Docker images once available

## Update 2025-07-27T23:17Z
- Added React settings modal tied to /api/settings
- Upgraded timeline view with vis.js and export action
- All tests pass after installing dependencies
- Next: polish remaining React components

## Update 2025-07-27T23:30Z
- Ensured coverage plugin installed so tests run
- Verified dashboard renders with new React design
- Tests succeed (2 passed, 2 skipped)
- Next: finalize Docker build scripts and refine CSS details

## Update 2025-07-28T00:24Z
- Cleaned up legacy HTML and JS; default route shows new React UI
- Next: ensure Docker front end refreshes

## Update 2025-07-28T01:49Z
- Use `legal_discovery.hocon` manifest and send uploaded files to the agent
- Next: verify ingestion pipeline within Docker compose

## Update 2025-07-28T02:30Z
- Created Flask routes for subpoena drafting and presentation generation
- Added React tabs to use these endpoints
- Installed missing Python packages so tests execute
- Next: integrate remaining sub-team tools and polish React styling

### Plan 2025-07-28
- Build tabs for each team in `legal_discovery.hocon` (case management, research, forensic, timeline, subpoena, trial prep)
- Provide REST endpoints for all coded tools with clear parameters and JSON responses
- Connect React components to these endpoints using fetch and intuitive forms
- Document Docker deployment and ensure gunicorn works on Windows

## Update 2025-07-28T03:09Z
- Synced template with React components by removing old settings modal
- Set default manifest in run.py to legal_discovery.hocon
- Next: verify timeline export works and finalize Docker config

## Update 2025-07-28T03:19Z
- Installed dependencies for tests and verified coverage
- React dashboard and manifest integration confirmed working
- Next: ensure Docker serves React UI correctly

## Update 2025-07-27T21:07Z
- Updated imports for legal discovery tools to match new neuro_san package layout
- Install attempts failed due to network restrictions
- Next: test the Flask app in Docker once dependencies are resolved

## Update 2025-07-27T21:25Z
- Installed dependencies locally to run tests successfully
- Verified coded tool imports after update; tests pass
- Next: rebuild Docker image and ensure Flask app loads correctly

## Update 2025-07-27T21:29Z
- Confirmed tests run successfully after installing dependencies
- Docker tooling not available here so image build couldn't be tested
- Next: verify Docker compose when environment supports it


## Update 2025-07-27T22:15Z
- Introduced tabbed interface and updated dashboard scripts
- Next: refine styles and test Docker stack

## Update 2025-07-27T22:15Z
- Introduced tabbed interface and updated dashboard scripts
- Next: refine styles and test Docker stack

## Update 2025-07-27T22:45Z
- Migrated dashboard to React for a richer UI
- Added dashboard-react.jsx and updated template to load React
- Next: run tests and verify Docker images once available

## Update 2025-07-27T23:17Z
- Added React settings modal tied to /api/settings
- Upgraded timeline view with vis.js and export action
- All tests pass after installing dependencies
- Next: polish remaining React components


## Update 2025-07-27T23:30Z
- Ensured coverage plugin installed so tests run
- Verified dashboard renders with new React design
- Tests succeed (2 passed, 2 skipped)
- Next: finalize Docker build scripts and refine CSS details

- Next: verify Docker compose when environment supports it

## Update 2025-07-28T06:55Z
- Added subpoena and presentation tabs to React UI
- Extended settings modal with full credential fields
- Next: finalize overview page for team interactions

## Update 2025-07-28T07:05Z
- Integrated CourtListener and statute scraping in ResearchTools
- Research tab now lets users pick source
- Next: link timeline events to file excerpts

## Update 2025-07-28T07:36Z
- Graph search and subnet filter implemented
- Added CaseManagementSection tying tasks and timeline
- Overview shows vector counts
- Next: refine styles

## Update 2025-07-28T10:31Z
- Upload progress bar and export spinners added
- Timeline filters by date range and export feedback
- Next: polish tab visuals

## Update 2025-07-28T10:50Z
- Timeline endpoints provide excerpts with citations
- React timeline modal displays citation or excerpt
- Added helper to read excerpts from uploaded files
- Next: tweak graph layout

## Update 2025-07-28T11:05Z
- Added Team Pipeline section to React dashboard
- Document tools now show output links after stamping or redaction
- Next: polish remaining styles

## Update 2025-07-28T14:23Z
- Upload endpoint stores documents and kicks off analysis automatically
- Default case created on first run
- Next: review vector DB contents and refine UI polish

## Update 2025-07-28T14:42Z
- Session reload ensures new uploads reach agent network
- Next: improve styling polish
- Next: polish tab visuals
## Update 2025-07-28T15:35Z
- Added Vite build setup and modular React components
- Updated dashboard template to load compiled bundle
- Documented build command in README
- Next: verify build artifacts in Docker image
## Update 2025-07-29T02:17Z
- Removed compiled bundle from repo and added ignore rules
- Documented that bundle.js must be built locally
- Next: confirm React build step works in Docker

## Update 2025-07-29T02:32Z
- Added icons to dashboard tabs and improved styles
- Built bundle.js via Vite
- Next: test Docker image with compiled assets
## Update 2025-07-29T03:01Z
- Introduced MetricCard component and overview metrics grid
- Updated stylesheet with metric card styles and built bundle
- Next: adjust pipeline view for smaller screens

## Update 2025-07-29T03:13Z
- Redesigned pipeline section with icons and grid layout
- Compiled latest React build and verified unit tests
- Next: refine case management timeline display
## Update 2025-07-29T03:22Z
- Created aggregated `/api/metrics` endpoint for dashboard stats
- Overview and Pipeline React components now fetch from this endpoint
- Readme documents the new API; bundle rebuilt via Vite
- Next: polish timeline UI and confirm Docker build on Windows

## Update 2025-07-29T03:32Z
- Display results from Forensic, Subpoena and Presentation tools in the UI
- Renamed dashboard tabs to reflect team names from the manifest
- Next: run tests and build to ensure everything compiles
## Update 2025-07-29T03:54Z
- Implemented /api/cases endpoint and case count metric
- Fixed duplicate code in upload_files
- Overview and Stats sections updated with new metrics
- Next: verify npm build and tests

## Update 2025-07-29T05:53Z
- Added case management controls to the React UI
- README updated with instructions for using the case selector
- Next: run npm build and pytest

## Update 2025-07-29T06:40Z
- Implemented case deletion endpoint and UI control
- Enhanced research tab with formatted results and summaries
- Vector search view now shows IDs and snippets
- Updated documentation and prepared for build
- Next: compile bundle and ensure tests pass
## Update 2025-07-29T07:06Z
- Added calendar UI with backend events
- Introduced graph analysis tool
- Next: build bundle and run tests
## Update 2025-07-29T08:34Z
- Updated graph analyze icon and added global lint hints
- Fixed newlines in Dockerfile and stylesheet
- Next: rebuild React bundle and run tests

## Update 2025-07-29T08:57Z
- Renamed default LLM config to `llm_config.hocon`
- Updated `.env` examples with new path
- Next: run npm build and pytest
## Update 2025-07-29T09:17Z
- Default AGENT_LLM_INFO_FILE added to Flask app
- run.py now passes this path via environment
- Next: npm build and pytest

## Update 2025-07-29T09:52Z
- Dockerfile now installs Node and builds React bundle automatically
- Added project .dockerignore to keep images slim
- Verified build and tests pass
- Next: finalize UI polish

## Update 2025-07-29T10:14Z
- Installed pyvis, flask and chromadb for tests
- Ran npm install and built bundle with Vite
- All unit tests pass and build succeeds
- Next: fix llm_config path in Docker startup

## Update 2025-07-29T10:25Z
- Updated Dockerfile to copy Node manifests before install
- Rebuilt React bundle and ran pytest successfully
- Next: ensure docker-compose build succeeds

## Update 2025-07-29T20:47Z
- Installed extra Python packages so tests run
- Reinstalled Node modules and built Vite bundle
- Verified pytest and npm build succeed
- Next: check docker-compose on Windows

## Update 2025-07-29T21:20Z
- Adjusted Dockerfile to export AGENT_LLM_INFO_FILE without quotes
- Next: run npm build and pytest to confirm fix

## Update 2025-07-29T21:35Z
- Resolved LLM config path with absolute directories
- Reinstalled dependencies and built Vite bundle
- Tests pass with all new packages
- Next: validate docker-compose startup

## Update 2025-07-29T22:06Z
- Switched Dockerfile to multi-stage build with Node 18 for frontend assets
- Confirmed npm build and pytest succeed after the change
- Next: check docker-compose build on Windows

## Update 2025-07-29T22:35Z
- Verified the builder stage installs Node modules and compiles React before copying assets
- `npm run build` and `pytest -q` both succeed
- Next: ensure docker-compose builds without missing npm
## Update 2025-07-29T23:31Z
- Installed pytest-cov and other deps so tests run
- Rebuilt Vite bundle and ran pytest
- Next: verify docker-compose build when docker available

## Update 2025-07-29T23:43Z
- Installed neuro-san, pyvis, flask and chromadb so tests run
- Rebuilt Vite bundle and confirmed pytest passes
- Next: confirm Docker build pipeline

## Update 2025-08-01T12:34Z
- Built React bundle and launched Flask on port 5001
- Verified server start by pointing AGENT_MANIFEST_FILE to manifest.hocon
- Next: adjust run script to avoid port conflicts

## Update 2025-08-01T12:50Z
- Confirmed Flask server runs with AGENT_MANIFEST_FILE=registries/manifest.hocon
- Npm build and pytest succeed
- Added detailed build instructions to docs/memory_bank.md
- Next: implement agent network cards in React UI

## Update 2025-08-01T13:25Z
- Created AgentNetworkSection component and new tab
- Updated defaults to use manifest.hocon for local runs
- Rebuilt bundle and confirmed tests pass
- Next: test docker-compose build when available
