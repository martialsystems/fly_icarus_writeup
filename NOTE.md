# fly_icarus chain: note

Not a finding. Locks stay on the trees. The readable index of those locks is gist [12835f74](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178). This file is the argument you are allowed to say, in order.

## Abstract

A male P1 slice was asked whether a frozen Icarus-from-male (fat, wingless, grounded, male wiring left in place) is treated as a female. In a hand-built 11-cell published-sign row, the costume does not decide. Turning 7,11-HD on and cVA off does. That odor rewrite is a modeling choice, not a hop-1 fact on MaleCNS.

Replacing the P1 row with hop-1 signed synapses onto 88 pC1-coexpress cells deletes the rewrite: LC10a is the giant excitatory term, DA1 is weak acetylcholine, HD and ppk23 are ~0, and 3 tracks 1 because both objects look like a courtship object. mAL GABA onto those 88 is large enough to pass the schema critical weight if it is assigned to cVA by hand. DA1 does not make that assignment at hop-1. A hop-2 path DA1 to type-LH to mAL touches almost all of the mAL dump, but the 161 LH cells on that path are a mixed bus: DA1 is 10% of all input and 70% of uniglomerular PN input, and LHAV4c2 carries about 30% of the LH-to-mAL synapses with five DA1 synapses.

Unfreeze, female-brain, and n=1000 were never licensed. The map does not prove that males court fallen males. An odor rewrite plus LC10a can fake that in the schema, and mAL is the only mapped weight pile big enough to undo it if you assign mAL to cVA.

## 1. Question that was asked

Does a male P1 slice treat a frozen Icarus-from-male as a female?

Icarus-from-male keeps male wiring. The object is fat, wingless, grounded. The question is identity at P1, not a population of falling flies.

## 2. Answer by layer

The Icarus costume is not what makes a male P1 net treat the fallen fly as a female. A cVA-off / HD-on odor rewrite is. That rewrite is a modeling choice. The mapped brain supplies a real inhibitory reservoir (mAL) and a real visual object channel (LC10a). It does not supply a hop-1 fallen-male-equals-female switch.

**Schema.** In the 11-cell published-sign row, 3 matches 1 if and only if 7,11-HD is on and cVA is off. Fat, wingless, pinned contact, and female cuticle do not beat DA1. Schema `W_crit = -1.5262` on the 3d pin; the template used `W[P1, DA1] = -1.8`. `@2cf5fd6`, `logs/p1_contact_s1.json`, `logs/p1_da1_dose_s1.json`.

**Hop-1 map.** On MaleCNS hop-1 onto 88 pC1-coexpress cells that rule is false. LC10a is +606. DA1 is +62 acetylcholine. HD is -3. ppk23 hop-1 is 0. Everything sings. 3 tracks 1 because both look like a courtship object, not because of pheromone identity. `@45aa064`, `logs/p1_sign_s1.json`.

**mAL dump.** Hop-1 mAL GABA onto those 88 is -8810. That is large enough to pass `W_crit` if it is assigned to cVA. DA1 hop-1 onto `mAL_m*` is 0; onto two mALB1 cells it is 96 ACh. The hang is a fold, not hop-1 DA1 to mAL. Numbers `@e16856c`, `logs/p1_mal_s1.json`. Sentence `@41437dc`.

**Drive.** DA1 hop-1 onto the 93 mAL GABA IDs that make the -8810 accounts for 3 of 8810. DA1-driven here means `f_i > 0`: type-LH cells that receive any DA1 and hit those 93. That hop-2 path accounts for 8773 of 8810. Hop: `DA1_PN -> type-LH -> mAL_GABA_pre`. `@de95257`, `logs/drive_s1.json`.

**Fraction.** That path is not one bus. On the frozen 161 LH cells, weighted DA1 fraction is 0.099 of all input and 0.703 of uniglomerular PN input. LH007m and LH008m are DA1-heavy among PNs (f-bar^PN 0.729 and 0.737) and carry 1174 of the 3301 LH-to-mAL synapses with 4565 DA1 synapses. LHAV4c2 carries 1012 of 3301 with 5 DA1 synapses (f-bar 0.002537; f-bar^PN = 1.0 is 5/5). The fold is only as clean as the first two types, not as clean as 8773/8810. `@01155c3`, `logs/lh_frac_s1.json`.

## 3. What the original idea became

A thousand digital flies with falling wings would not answer this. A male P1 slice courts an Icarus-from-male when you delete the male odor and keep the object-looking-like-a-fly visual drive. Morphology alone does not flip identity. The connectome's best candidate for the missing brake is mAL, reached from DA1 in two hops through mixed LH, not a direct labeled line.

So: an odor rewrite plus LC10a can fake the house rule in the schema, and mAL is the only mapped weight pile big enough to undo it if you assign mAL to cVA.

## 4. What was never run

`--unfreeze`, `--female-brain-icarus`, and `--n 1000` stay stubbed on every tree in this chain. They were never licensed. They still are not.

## 5. What this is not

Not MaleCNS proving the house rule. Not a 166,691-cell LIF. Not pulse song (song bouts = 1 is a latch threshold). Not a playground of falling wings. Not `hd_on_cva_off_ns=true` as a map result: that token is true only after the fold hangs mAL on the cVA slot.

## 6. Replay

No new method. Each lock is one extract plus, where a battery exists, the same frozen-object assay.

| Tree | Extract | Lock |
|------|---------|------|
| fly_icarus | `data/templates/male_p1.json` | `logs/p1_contact_s1.json`, `logs/p1_da1_dose_s1.json` |
| fly_p1_sign | `scripts/extract_p1_weights.py` | `logs/p1_sign_s1.json` |
| fly_p1_mal | `scripts/extract_p1_weights.py` | `data/templates/extract.json`; do not restamp `logs/p1_mal_s1.json` |
| fly_mal_drive | `scripts/extract_drive.py` | `logs/drive_s1.json` |
| fly_lh_frac | `scripts/extract_frac.py` | `logs/lh_frac_s1.json`; IDs in `data/frozen/ids.json` |

How to run: in each tree, `.venv/bin/python -m pytest`. Rebuilds, where allowed, are the extract scripts above. Do not overwrite the listed lock files.

## 7. Repo table

| Tree | SHA | Allowed sentence | Lock file |
|------|-----|------------------|-----------|
| [fly_icarus](https://github.com/martialsystems/fly_icarus) | `2cf5fd6` | In this 11-cell slice, HD-on / cVA-off is necessary and sufficient for 3 matching 1. Morphology, pin, and feminized cuticle are not. Schema W_crit=-1.5262. | `logs/p1_contact_s1.json` |
| [fly_p1_sign](https://github.com/martialsystems/fly_p1_sign) | `45aa064` | Hop-1 DA1 is +62 ACh. LC10a +606. ppk23 hop-1 is 0. hd_on_cva_off_ns is false. | `logs/p1_sign_s1.json` |
| [fly_p1_mal](https://github.com/martialsystems/fly_p1_mal) | `e16856c` | Hop-1 mAL GABA onto these 88 is large enough to pass W_crit if assigned to cVA. DA1 hop-1 onto mAL_m* is 0; onto two mALB1 cells it is 96 ACh. | `logs/p1_mal_s1.json` |
| fly_p1_mal sentence | `41437dc` | Same allowed sentence as the row above. | README of fly_p1_mal |
| [fly_mal_drive](https://github.com/martialsystems/fly_mal_drive) | `de95257` | Yes at hop-2. DA1 hop-1 is 3 of 8810. DA1-driven type-LH accounts for 8773 of 8810. Hop: DA1_PN -> type-LH -> mAL_GABA_pre. | `logs/drive_s1.json` |
| [fly_lh_frac](https://github.com/martialsystems/fly_lh_frac) | `01155c3` | f-bar=0.099172. f-bar^PN=0.702674. LHAV4c2 carries 1012 of 3301 with 5 DA1 synapses. | `logs/lh_frac_s1.json` |

On fly_mal_drive, "DA1-driven" means any DA1 synapse (`f_i > 0`). On fly_lh_frac it means the fractions in that table.

Figure 1 (`figures/stack.png`): object tags to the 11-cell row to hop-1 counts to hop-2 LH to the f table.

![Figure 1. Pointer stack across the locked trees.](figures/stack.png)

Index (pointers only): https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178
