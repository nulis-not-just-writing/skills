# Engineering / Computer Science

Struktur venue-driven, sering **bukan IMRaD murni**: Introduction → Background/Motivation → Design/Approach → Implementation → **Evaluation** → Related Work (menjelang akhir) → Conclusion. Untuk paper eksperimental sistem, "Evaluation" menggantikan "Results".

## Ciri khas per section
- **Introduction**: tutup dengan **daftar kontribusi eksplisit** — "The contributions of this paper are: (1)..., (2)..., (3)...". Klaim harus terukur dan terverifikasi di Evaluation.
- **Related Work di belakang**: fungsinya **diferensiasi**, bukan review — satu paragraf per keluarga pendekatan, tiap paragraf ditutup "unlike these, our approach...". Boleh di depan bila bidangnya menuntut konteks lebih dulu.
- **Design/Approach**: keputusan arsitektural + rasional + trade-off; sertakan diagram sistem.
- **Evaluation**: analog Results+sebagian Discussion. Rumuskan **research/evaluation questions** ("RQ1: How much does X reduce latency?"), sebutkan baseline, metrik, testbed/dataset, lalu jawab per RQ dengan angka + figur. Reproducibility: rilis kode/artefak (banyak venue punya Artifact Evaluation).

## Praktik teruji (SNL-UCSB paper-writing, dari analisis forensik ribuan edit)
- Urutan menulis dipaksakan: Draft-0 Introduction → Evaluation → Design → Background → Related Work → **Final Introduction** → Abstract. Introduction ditulis dua kali agar klaim se-level hasil.
- Tahap Integration: audit terminology drift, claim-evidence mapping, propagasi abstraksi kunci.
- Tahap Compression: pangkas 30–50% (paper konferensi ketat halaman).

## Bahasa
- Present tense untuk mendeskripsikan sistem ("The scheduler assigns..."); past untuk eksperimen ("We ran...").
- "We" aktif lazim dan dianjurkan.
- Kontribusi diklaim tegas tapi terukur; hindari "novel/first" tanpa bukti.

## Checklist audit
- [ ] Daftar kontribusi eksplisit di Introduction, semuanya dibuktikan di Evaluation
- [ ] Evaluation punya baseline + metrik + RQ yang dijawab
- [ ] Related Work membedakan, bukan sekadar meringkas
- [ ] Klaim performa didukung angka & kondisi eksperimen yang jelas
- [ ] Artefak/kode tersedia bila venue mendukung reproducibility
