# Project: Mapping Optimal Animal Crossings for Southern Arizona

## About
- **Student:** Ed Olsson
- **Grade/School:** 7th Grade, Hermosa Montessori School
- **Science Teacher:** My mom
- **Year:** SARSEF 2025-2026
- **Main Interests:** Snakes (and many animals)
- **AI Use:** All use of AI (ChatGPT etc.) is HEAVILY documented. I review and understand all steps and cannot submit anything I do not fully understand myself.

## Project Summary
Map the best places to put animal crossings (like wildlife bridges/underpasses) in southern Arizona using:
- **OpenStreetMap roads data** (for global applicability)
- **iNaturalist animal sighting data** (especially for local wildlife, e.g., snakes but not limited to them)

These are global datasets so methods can be used anywhere in the world.

## SARSEF & Fair Background
- SARSEF main site: https://sarsef.org/programs/competitions/sarsef-science-and-engineering-fair/
- Reference documents and project guidelines saved in the `sarsef/` directory. See that directory for up-to-date SARSEF rules and advise for project process.

## Recording Decisions & Patterns
- **Decision Log:** Every time I (or my helpers/AI) make a reusable project decision or establish a pattern (like how/where to document something, or specific workflow conventions), it must be saved as a short note either here in `claude.md` or, if substantial, as a separate artifact in `artifacts/`.
- **Artifact Naming:** Artifact notes use the format `YYYYMMDD-HH:MM-description.md`. All are in the `artifacts/` directory and linked from here.
- **Reference Materials:** SARSEF background and official process documents are saved under `sarsef/` and also referenced here.

## Artifact Index
(Artifacts will be listed here as they are created)

- [sarsef/ask-questions-and-identify-problems.md](sarsef/ask-questions-and-identify-problems.md) — SARSEF guide: Asking Questions & Identifying Problems
- [sarsef/develop-and-use-models.md](sarsef/develop-and-use-models.md) — SARSEF guide: Developing and Using Models
- [sarsef/plan-investigations.md](sarsef/plan-investigations.md) — SARSEF guide: Planning Investigations

- [artifacts/20251116-10:23-osm-roads-download.md](artifacts/20251116-10:23-osm-roads-download.md) — Logged the OSM roads download & conversion workflow

- *(more artifacts will be added in planning and decision making)*

## Family Contributions
- **Dad:** Helped build the initial Cursor and Claude rules for this project and organize the process for documenting all AI involvement, ensuring the project meets SARSEF standards for transparency and self-understanding.
- **Mom:** Science teacher and mentor for SARSEF.

## AI Documentation Pattern
- Every use of AI for suggestions or automation is documented as an artifact, *including this very file and pattern*.
- All organization of the AI process and project transparency was developed with guidance from Ed's dad (see Family Contributions).
- Ed Olsson must understand, review, and, if in doubt, ask questions before moving forward.

### Git and Publishing
- When pushing changes to GitHub, a Personal Access Token (PAT) stored at `~/.git-token-ed` can be used for authentication when prompted (use the token as the password).

## Next Steps
- Study area locked (see `data/study_area.geojson`) – all OSM/iNaturalist pulls must clip to this polygon.
- OSM roads dataset downloaded & converted to GeoJSON (see `data/osm_roads.geojson` and artifact `20251116-10:23-osm-roads-download.md`).
- Added `notebooks/osm_roads_preview.ipynb` for quick visualization of the downloaded roads (requires `geopandas` + `matplotlib`).
- Next focus: finalize iNaturalist query/filters for target species in the same footprint and draft how the two datasets will intersect for crossing hotspots.
- Document any filters, scripts, or workflow choices as new artifacts so they’re traceable.
- Create directories for `artifacts/` and `sarsef/`
- Save official SARSEF links and background content (for reference only) into markdown in `sarsef/` directory, list those here
- Begin outlining project step-by-step plan in this file

---

*See linked files and directories for further resources, logs, and background.*
