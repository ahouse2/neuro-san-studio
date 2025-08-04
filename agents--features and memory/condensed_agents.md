- Focus on production-ready code for the `/apps/legal_discovery` module.
- Integrate with `registries/manifest.hocon` and coded tools for the legal_discovery network.
- Ensure the docker-compose stack builds and runs on Windows.
- Keep the UI polished, responsive and fully functional making at least one improvement to the asthetic every commit cycle. If there is no more room          for improvement, then you're wrong, look again and think harder, amybe even think 'bigger/ more complexity', just don't break anything.
- Log progress in this file before each commit with a short summary of work and next steps.
- ONLY IMPLEMENT PRODUCTION READY CODE. NEVER ANY MOCK/ PLACEHOLDER/ SIMULATION/ STUB/ FAKE/ TEMP/ TODO/ 'IF THIS WAS A REAL _________ (FILL IN THE BLANK), THEN....'. THE ONLY TIME THIS SORT OF PRACTICE IS ACCEPTABLE IS WHEN IT IS NECESSARY TO IMPLEMENT A FEATURE OVER MULTIPLE STEPS/ ITERATIONS, AND YOU ARE STUBBING A METHOD/ FUNCTION/ API CALL/ WHATEVER. USE IT SPARINGLY, OR I WILL STOP YOU MID COMMIT AND MAKE YOU FIX IT. thank you, sorry for yelling, carry on. BUT NOT WITH MOCK CODE!!!


AGENTS.md (Condensed)
Module Goals & Workflow
Build production-ready code for /apps/legal_discovery
Integrate with registries/manifest.hocon and tools for the legal_discovery network
Ensure Docker Compose builds and runs on Windows (fix gunicorn issues)
Keep UI polished, responsive, and functional (React migration, dark "alien warship" theme)
Log progress in this file before each commit—summarize work and next steps
Quick Setup Script
bash
#!/bin/bash
set -e
python3 -m venv venv
source venv/bin/activate
export PYTHONPATH=$(pwd)
pip install -r requirements.txt
pip install python-dotenv neuro-san gunicorn pillow requests flask
echo "Setup complete. To activate, run 'source venv/bin/activate'"
Major Progress Milestones
Testing & Environment:
Installed all required Python/Node dependencies for development and testing (pytest, coverage, linting, React bundle via Vite). Confirmed all tests pass before major changes.

Docker & Cross-Platform Support:
Dockerfile and docker-compose refactored for multi-stage builds and Windows compatibility. React frontend assets built during image creation; Node is only required at build time.
PostgreSQL and Chroma integrated for data persistence and vector search.

UI & Frontend:
Migrated dashboard to React for modular, modern UI.
Introduced tabs for team tools, case management, upload pipeline, metrics, and graph/timeline exports.
Glassy neon-blue dark theme with design tokens and Figma export.

Backend & API:
Added Flask API endpoints for document analysis, subpoena/presentation, task management, metrics, and graph queries.
Hardened file ingestion pipeline:

Batch uploads, per-file timeouts, parallel workers
Skipped/errored files logged, UI progress shown
Metadata normalization and retry logic for vector DB
Agent/Tool Integration:
Coded tools (redaction, Bates stamping, vector search, AAOSA pattern) exposed via REST endpoints.
Manifest and LLM config paths standardized for container startup.

Key Recent Updates
Implemented background agent initialization for responsive Flask API.
Hardened uploads: timeout, deduplication, error logging, vector/graph sync.
Refined dashboard: team tabs, case cards, metrics, progress bars, modals.
PostgreSQL & Chroma services added to docker-compose.
All startup scripts and environment variables documented in memory_bank.md.
Setup and build instructions documented; bundle.js removed from version control.
Typical Next Steps (Pattern)
Polish UI/UX and theme consistency.
Monitor/optimize upload and ingestion workflows.
Ensure Docker Compose and local workflows stay in sync.
Expand API/documentation for new features or agents.
For full details on any specific feature, agent, or deployment step, see the latest detailed entry before this summary or check memory_bank.md

- Next: ensure batch uploads run cleanly and surface skipped files in UI

## Update 2025-08-03T22:40Z
- Wired settings button to trigger modal and exposed `/api/graph/cypher` endpoint with starter query buttons
- Shifted dashboard container to dark gunmetal glass for clearer contrast against neon cards
- Next: enrich cypher results formatting and continue tightening glass theme consistency

## Update 2025-08-04T00:30Z
- Added PostgreSQL configuration for Flask via `DATABASE_URL` with SQLite fallback
- Pointed vector database manager to an external Chroma service
- Extended docker-compose with a PostgreSQL service and wiring for Chroma
- Next: refine graph exploration UI and document deployment steps

## Update 2025-08-04T02:00Z
- Parallelized document ingestion using a thread pool with per-file timeouts
- Next: observe upload performance and tune worker counts

## Update 2025-08-04T03:00Z
- Added legal theory ontology and loader for case theory mapping
- Expanded models with CauseOfAction, Element, Defense and Fact tables
- Introduced ontology loader unit test
- Next: build fact extraction pipeline and Neo4j graph persistence

- ## Update 2025-08-03T22:40Z
- Wired settings button to trigger modal and exposed `/api/graph/cypher` endpoint with starter query buttons
- Shifted dashboard container to dark gunmetal glass for clearer contrast against neon cards
- Next: enrich cypher results formatting and continue tightening glass theme consistency

## Update 2025-08-04T00:30Z
- Added PostgreSQL configuration for Flask via `DATABASE_URL` with SQLite fallback
- Pointed vector database manager to an external Chroma service
- Extended docker-compose with a PostgreSQL service and wiring for Chroma
- Next: refine graph exploration UI and document deployment steps

## Update 2025-08-04T02:00Z
- Parallelized document ingestion using a thread pool with per-file timeouts
- Next: observe upload performance and tune worker counts

## Update 2025-08-04T03:00Z
- Added legal theory ontology and loader for case theory mapping
- Expanded models with CauseOfAction, Element, Defense and Fact tables
- Introduced ontology loader unit test
- Next: build fact extraction pipeline and Neo4j graph persistence

## Update 2025-08-04T??Z
- Added spaCy-based `FactExtractor` for parties, dates and actions
- Included dependency in legal_discovery requirements and covered with unit test
- Next: integrate extractor with upload pipeline and graph storage
- We are continuing to build out feature #3 in this folder-- please check '#_legal_theory_mapping.md'
- In future commits, please update THIS file, instead of the usual AGENTS.md file, for the time being.
- when you make an update to this file, make a note of which substep (part of the # feature) you have finished, and which #.# comes next :)

WE STARTED ON #3, INSTEAD OF #1. DEAL WITH IT, FINISH IMPLEMENTING #3, AND THEN WE WILL MOVE TO #1, #2, ETC

## Update 2025-08-04T05:30Z
- Completed 3.2 by wiring `FactExtractor` into the upload pipeline
- Persisted extracted facts to SQL and Neo4j via new graph helper
- Next 3.3: relate facts to ontology elements and score theory candidates

## Update 2025-08-04T07:00Z
- Finished 3.3 by linking facts to ontology elements and causes in Neo4j
- Implemented 3.4 LegalTheoryEngine with scoring and `/api/theories/suggest`
- Delivered 3.5 Case Theory dashboard tab with neon element highlight
- Next: proceed to feature #1 planning and implementation

## Update 2025-08-04T12:30Z
- Began feature #5 Exhibit & Trial Binder Creator.
- Added exhibit fields to Document model and created ExhibitCounter and audit log tables.
- Implemented exhibit_manager service with binder generation and export helpers.
- Next: connect service to UI and implement comprehensive compliance checks.

## Update 2025-08-04T12:45Z
- Resolved test environment issues and confirmed binder generation works via unit tests.
- Cleaned up exhibit manager module imports.
- Next: build frontend controls for exhibit numbering and binder export.

