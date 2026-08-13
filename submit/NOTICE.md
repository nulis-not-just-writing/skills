# NOTICE — karya pihak ketiga di dalam skill `submit`

Skill ini memuat karya pihak ketiga. Pemberitahuan di bawah wajib ikut pada setiap salinan
dan distribusi ulang.

## Disalin apa adanya — MIT

- Sumber: `Aperivue/medsci-skills` — https://github.com/Aperivue/medsci-skills
- Pemegang hak: Aperivue (https://aperivue.com), 2026
- Lisensi: **MIT** — mengizinkan pemakaian, modifikasi, dan distribusi ulang dengan
  mempertahankan pemberitahuan hak cipta

Seluruh berkas di `scripts/hulu/` tidak diubah sama sekali, supaya pembaruan dari hulu dapat
ditarik bersih:

| Berkas | Asal di repo hulu |
|---|---|
| `verify_refs.py` | `skills/verify-refs/scripts/verify_refs.py` |
| `check_claim_fidelity.py` | `skills/verify-refs/scripts/check_claim_fidelity.py` |
| `_quote_match.py` | `skills/verify-refs/scripts/_quote_match.py` |
| `prisma_cascade_check.py` | `skills/check-reporting/scripts/prisma_cascade_check.py` |
| `check_prisma_figure.py` | `skills/check-reporting/scripts/check_prisma_figure.py` |
| `claim_fidelity_challenge/` | `skills/verify-refs/scripts/claim_fidelity_challenge/` |

`claim_fidelity_challenge/` adalah uji regresi milik hulu. Jalankan
`bash scripts/hulu/claim_fidelity_challenge/verify.sh` (26 uji) setelah menarik pembaruan.

Seluruh skrip di atas **stdlib-only** dan diuji berjalan pada Python 3.9.6 maupun 3.12.

## Konsep diserap, bukan teks

Aturan *critical-item floor* dan gerbang T2/T2b/T2c pada `SKILL.md` diserap sebagai konsep dari
repo yang sama. Tidak ada kalimat yang disalin.
