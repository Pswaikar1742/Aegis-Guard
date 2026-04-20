# Aegis Guard

Aegis Guard is a neuro-symbolic invoice fraud detection system with a five-sieve core pipeline:

- S1: Binary metadata forensics
- S2: Tax ID checksum validation
- S3: Arithmetic and semantic consistency checks
- S4: Benford statistical conformity
- S5: Spatial vision tamper detection

See `docs/MISSION.md` for the authoritative architecture and phase status.

## Deployment Note

Frontend Vercel builds use `frontend/next.config.mjs` to skip TypeScript and ESLint checks during `next build` to prevent memory-exhaustion build failures.

Owner: PSW
