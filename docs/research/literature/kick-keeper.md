# Literature cluster C: kick mechanics, foot-ball contact, penalty/goalkeeper (+ one CFD-method paper)

Context: UPC 2026 Problem B. The kick happens at t = 0 with the ball centre at (0, 0, 0.11) m. We observe the ball at t = 0.05 s and t = 0.10 s and predict where it crosses the goal plane (x = 11 m). Test case: (1.50, 0.45, 0.44) m and (2.96, 0.86, 0.74) m, which gives about 32.5 m/s, about 12° elevation and about 17° lateral.

Figures were read from the embedded images: Ishii Fig. 5 and Fig. 7, Hunter Fig. 2 and Fig. 4. Numbers tagged *(our calc)* are our own arithmetic, not values from the papers.

---

## Cluster summary

- **Contact time is confirmed at about 10 ms.** Ishii et al. measured it at 2,500 fps: subject means were 9.6–10.7 ms and single trials ranged from 8.8 to 12.0 ms [Ishii 2012, p. 262 and Table 1]. The ball deforms by 29–65 mm at peak, and the peak force is 1.1–2.2 kN, reached at about 4 ms [Ishii 2012, p. 262 and Fig. 5].
- **Measured launch speeds in this cluster are 17–26 m/s.** All the kickers are university or intercollegiate players. A 3-step penalty gave 23.9 ± 1.2 m/s [Ravenscroft & Linthorne 2015, p. 3]. One-step lab kicks gave 17.1–24.7 m/s (normalised values, see the note in the table) [Ishii 2012, Table 1]. The example trial in Naito et al. was 26.3 m/s [Naito 2010, p. 267–268]. **32.5 m/s is well above every value in this cluster.** It is plausible only for a powerful, near-maximal kick by a strong or elite player.
- **The ball/foot speed ratio is about 1.3–1.45.** For our 32.5 m/s this implies a foot speed of about 23–25 m/s *(our calc)*.
- **Launch angle in a penalty is 8 ± 5°** [Ravenscroft & Linthorne 2015, p. 3], so our 12° is typical.
- **Impact point along the foot changes speed by up to about 15%.** The relationship is an inverted U with its peak near the foot's centre of mass [Ishii 2012, Fig. 7]. For a realistic penalty from the ground, the effect was not detectable: the slope was 0 ± 0.12 m/s per cm [Ravenscroft & Linthorne 2015, Fig. 1]. **No paper in this cluster measures spin.** Every analysis is 2-D in the sagittal plane.
- **Goalkeepers commit before the ball is struck.** In 330 professional shoot-out penalties, the keeper started his dive 0.22 ± 0.11 s before foot contact [Hunter 2018, p. 4 and Fig. 2]. Predictions from body cues alone reach only about 80% (instep) or 90% (side-foot) correct at the moment of contact, and 55–64% at 0.4 s before it [Hunter 2018, p. 7 and Fig. 4].
- **Murakami & Mochida (1988)** validates k-ε RANS for a sharp-edged cube in a boundary layer. It is relevant to us only as a methods caveat (see its section). Low relevance.

---

## 1. Ravenscroft & Linthorne (2015)

**Citation.** Ravenscroft, J. C., & Linthorne, N. P. (2015). Effect of the location of the foot impact point on ball velocity in a soccer penalty kick. ISBS conference proceedings (4 pp.), Brunel University. File: `Football_Impact_Point_Linthorne_.pdf`.

**Method.**
- One experienced intercollegiate male player (1.82 m, 75 kg) took 23 maximum-effort full-instep penalties. He used a 3-step run-up of about 3 m, kicked from 11 m at a regulation goal on 3G turf, and used a FIFA size-5 ball at regulation pressure [p. 1–2].
- Video was 2-D at 100 Hz [p. 2].
- Ball velocity came from the unfiltered frames just after the ball left the foot. The horizontal component was a linear fit. The vertical component was a quadratic fit with the second derivative fixed at −9.81 m/s² [p. 2].
- Uncertainties: ball velocity about ±0.4 m/s (95% CI), impact point ±1.3 cm, foot velocity ±2.0 m/s [p. 2].

**Numerical data** [p. 3 unless noted]:

| Quantity | Value |
|---|---|
| Ball projection speed | 23.9 ± 1.2 m/s (mean ± SD, n = 23) |
| Foot speed at impact | 17.3 ± 0.7 m/s |
| Ball/foot speed ratio | ≈ 1.38 *(our calc from the means)* |
| Projection (elevation) angle | 8 ± 5° |
| Run-up speed | 4.3 ± 0.5 m/s |
| Shank angular velocity at impact | 1650 ± 160 deg/s; thigh 480 ± 120 deg/s |
| Effect of impact point on ball speed | slope −0.01 ± 0.12 m/s per cm (95% CI), so zero. Between the ankle and the base of the toes (15 cm apart) the difference is at most 1.8 m/s [p. 4] |
| Curvature bound | inverted-U curvature below 150 m/s per m² (upper 95% limit), against about 700 m/s per m² in Ishii 2012 [p. 3] |

**Contact time and spin.** Not measured; 100 Hz is too coarse to resolve a 10 ms contact. The impact point was taken from the first frame of contact. The authors note that the ball visibly deforms, so contact appears along a line [p. 2]. They suggest that a camera faster than 500 Hz is needed [p. 3].

**Validity range.** One subject, maximum effort, instep only, 2-D in the kicking plane only. Support-leg and out-of-plane motions were not tracked [p. 4].

**Relevance: high.** This is the only study in the cluster that is an actual penalty from the spot. It gives a penalty-specific speed of about 24 m/s at university level, a launch angle of 8 ± 5° that supports our 12°, and a ball/foot ratio of about 1.4. Its velocity-extraction method (linear horizontal fit plus quadratic vertical fit with g fixed) is effectively what our two-point estimate does.

---

## 2. Ishii, Yanagiya, Naito, Katamoto & Maruyama (2012)

**Citation.** Ishii, H., Yanagiya, T., Naito, H., Katamoto, S., & Maruyama, T. (2012). Theoretical study of factors affecting ball velocity in instep soccer kicking. *Journal of Applied Biomechanics*, 28, 258–270. File: `jab.28.3.258.pdf`.

**Method.**
- Five experienced male university players took maximal full-instep kicks with a one-step approach at a target 4 m away [p. 259].
- The ball was a FIFA size 5 (432 g) inflated to 9.7 psi. It sat on a stand 0–12 cm high, which moved the impact point along the foot [p. 259].
- A 2-D high-speed camera filmed at 2,500 fps. The ball centre was reconstructed from three rim points that deform little during contact [p. 259].
- Impact force was derived from ball deformation using Hertz contact, F ∝ β^(3/2), scaled so that the impulse equals m_b·V_b1 [Appendix, p. 269–270].
- Ankle kinetics came from inverse dynamics. A theoretical impulse-momentum equation for V_b1 (their Eq. 5) was built from the foot impulse, the angular-impulse balance and the restitution coefficient [p. 261–262].

**Numerical data:**

| Quantity | Value | Source |
|---|---|---|
| **Contact (impact-phase) duration** | subject means 9.6, 9.7, 10.1, 10.6, 10.7 ms; range 8.8–12.0 ms | p. 262, Table 1 |
| Ball speed at end of contact (normalised to foot speed) | means 19.4–22.6 m/s; min 17.1, max 24.7 m/s | Table 1 |
| Foot (COM) speed at start of contact | 13.7–17.1 m/s (subject means); range 13.1–17.9 m/s | Table 1 |
| Foot angular velocity at start of contact | 28.7–42.2 rad/s (means); range 24.9–48.7 rad/s | Table 1 |
| Ball/foot speed ratio | about 1.32–1.43 *(our calc from the Table 1 means)* | — |
| Peak ball deformation | 29–65 mm. It grows as the impact point moves toward the toes | p. 262 |
| Peak impact force | 1,056–2,231 N. Largest when the impact is 30–50 mm toe-side of the foot's centre of mass | p. 262 |
| Force and deformation time course | roughly half-sine, peak at about 4 ms, ends at about 9.6 ms (example trial: peak about 2.0 kN, about 45 mm) | Fig. 5 |
| Optimal impact point | 4–31 mm toe-side of the foot's centre of mass (experiment); peak ball speeds 20.5–24.1 m/s | Table 3 |
| Speed loss away from the optimum | about 18.5 m/s at ±6–7 cm against a 20.5 m/s peak for subject A (about 10–15% lower). The regression is y = −678.6 l² − 15.7 l + 20.4 | Fig. 7 |
| Sensitivity (±10% change) | foot speed ±10% gives ball speed about ±8%. Foot mass, foot length and ankle impulses change it by under 2% | Table 4 |
| Coefficient of restitution | depends significantly on the impact point (quadratic R = 0.53–0.87). The text gives no numerical values | Table 2 |
| Ankle position | 0.060 ± 0.005 m from the foot's centre of mass | p. 262 |

**Spin.** Not measured. The model is planar, and the ball is assumed to be launched horizontally from a vertical foot surface. Tangential friction appears only as Coulomb friction, F_t = μF_n, with μ not determined [Appendix]. For the curve-kick impact they cite Asai et al. (2002), which is not in our files and should be added to the reading list for spin.

**Validity range.** One-step approach, ball on a stand (not a real penalty), short 4 m target, sub-maximal speeds of about 20 m/s, 2-D. Foot speed explains most of the variation in ball speed [p. 265].

**Relevance: high for contact timing.** This is the best direct measurement of contact duration, deformation and force history. It underpins the t = 0 treatment below.

---

## 3. Naito, Fukui & Maruyama (2010)

**Citation.** Naito, K., Fukui, Y., & Maruyama, T. (2010). Multijoint kinetic chain analysis of knee extension during the soccer instep kick. *Human Movement Science*, 29, 259–276. doi:10.1016/j.humov.2009.04.008. File: `j.humov.2009.04.008.pdf`.

**Method.**
- Nine collegiate players took a 2-step approach and kicked as fast as possible at a target 5 m away and 1 m high [p. 261].
- Motion capture was 3-D at 250 Hz, with a force plate at 500 Hz under the support foot. Ball speed came from a 250 Hz camera with DLT [p. 261].
- The dynamic model had 8 segments and 18 degrees of freedom. Knee-extension acceleration was split into muscular, gyroscopic, Coriolis, centrifugal, gravity and external-force terms [p. 263–267].
- The marker paths were extrapolated across the impact so that the sudden deceleration would not be over-smoothed [p. 261].

**Numerical data:**

| Quantity | Value | Source |
|---|---|---|
| Ball speed (example trial) | 26.3 m/s | p. 267–268 |
| Peak knee-extension angular acceleration | above 500 rad/s² | p. 268, Fig. 3 |
| Peak knee-extension angular velocity | about 24 rad/s *(our calc: the components in Table 1 sum to 100%, and the knee muscle term of −20.6 rad/s is −84.4%)* | Table 1 |
| Contributions to peak knee-extension velocity | kicking-leg centrifugal +151.6%; trunk-rotation muscle +57.9%; kicking-leg Coriolis +56.4%; trunk gyroscopic +55.9%; knee muscle −84.4% | Table 1 |

The paper reports no contact time, restitution, spin or launch angle.

**Validity range.** Collegiate players, lab setting, short target. The analysis covers the swing phase up to impact only.

**Relevance: low.** It explains how foot speed is produced, not ball flight. Its only useful number for us is one more university-level ball speed (26.3 m/s). Its mechanism points out that a kicker's maximum speed is set by whole-body coordination, which is why elite players can reach above 30 m/s.

---

## 4. Hunter, Murphy, Angilletta & Wilson (2018)

**Citation.** Hunter, A. H., Murphy, S. C., Angilletta, M. J., Jr., & Wilson, R. S. (2018). Anticipating the direction of soccer penalty shots depends on the speed and technique of the kick. *Sports*, 6(3), 73. doi:10.3390/sports6030073. File: `sports6030073.pdf`.

**Method.**
- **Kicks.** Ten right-footed university club players kicked penalties at a marker 1 m inside either post. Their run-up started 4 m behind the spot at 22.5°. They used side-foot and instep at about 50–100% of their own maximum speed, and were told not to use deception [p. 3].
- **Ball speed.** Two 100 fps cameras with DLT gave the average over six frames covering the first 0.06 s after contact. Speed was reported only as a percentage of each kicker's maximum [p. 3–4].
- **Speed categories.** Slow 62–65%, medium 84–85%, fast about 99.5% of maximum [p. 4].
- **Survey.** 521 adult players (709 respondents in total) watched videos filmed from the goalkeeper's viewpoint. The videos were cut at 0, −0.1, −0.2, −0.3 or −0.4 s relative to foot-ball contact. Participants then chose left or right. The analysis was a binomial GLM with multi-model averaging [p. 4–6].
- **Match footage.** 330 professional shoot-out penalties (34 shoot-outs) were analysed for goalkeeper "leave-time", the moment the final dive starts relative to contact [p. 4].

**Numerical data:**

| Quantity | Value | Source |
|---|---|---|
| Goalkeeper leave-time (professional matches) | mean −0.22 s, SD 0.11 s (before contact). Mode about −0.25 to −0.18 s. Tail runs from −0.65 to +0.25 s. Only a few percent leave after contact *(our read of the histogram)* | p. 4, Fig. 2 |
| Correct-direction probability, instep (slow/medium/fast) | −0.4 s: 0.62–0.64; −0.3 s: 0.64–0.67; −0.2 s: 0.69–0.72; −0.1 s: 0.69–0.72; 0.0 s: 0.79–0.81 | Fig. 4b |
| Same, side-foot fast | 0.61, 0.66, 0.70, 0.81, 0.90 | Fig. 4a |
| Same, side-foot slow/medium | 0.55–0.56, 0.60–0.61, 0.64, 0.77, 0.88 | Fig. 4a |
| Summary in text | 55–64% at −0.4 s; about 80% (instep) and about 90% (side-foot) when the video runs up to contact | p. 7 |
| Speed effect | significant only for side-foot (fast shots easier to read). For instep the speed terms are not significant (p = 0.37–0.41) | Table 2 |
| Cue timing | posture differences are obvious by −0.3 s for fast side-foot shots. Planting the non-kicking foot happens at about −0.1 s | p. 9–10, Fig. 7 |

It gives no absolute ball speeds, no ball flight times, no save rates and no keeper reaction or movement durations. The paper says only that keepers usually start moving several hundred ms before the ball moves, citing others [p. 8].

**Validity range.** Videos at 30 fps from a camera at 1.5 m height. A binary left/right choice. Amateur and semi-professional respondents, with the 3 professionals excluded. No deception, and kickers aimed 1 m inside the post. The prediction is based only on the kicker's body before contact; no ball flight is shown.

**Relevance: medium.** It is the key source for the "information budget" argument and the goalkeeper interpretation layer. It is not a source for ball physics.

---

## 5. Murakami & Mochida (1988), brief

**Citation.** Murakami, S., & Mochida, A. (1988). 3-D numerical simulation of airflow around a cubic model by means of the k-ε model. *Journal of Wind Engineering and Industrial Aerodynamics*, 31, 283–303. File: `0167-61052990009-8.pdf`.

**Method.** Steady RANS with the standard k-ε model, applied to a surface-mounted cube in a boundary layer. Seven cases varied the mesh and the boundary conditions. Results were compared with the authors' wind-tunnel data at Re ≈ 7 × 10⁴ [p. 291].

**Findings.**
- With a fine mesh (spacing H/24 at the windward corner), the mean velocity and surface pressure are reproduced well [Conclusion (3), (6)].
- k-ε overproduces turbulent kinetic energy at the windward corner, which affects roof separation, and the computed k in the wake is wrong [Conclusion (4)–(6)].
- Wall boundary conditions for ε strongly affect the separated region [Conclusion (5)].

**Relevance: low.** A ball is a smooth bluff body with spin, and its drag crisis and Magnus force depend on transition and separation. Those are exactly what standard k-ε predicts poorly. The single takeaway: do not use k-ε RANS values as a source for C_D or C_L of a ball. Use wind-tunnel or trajectory data instead.

---

## Consolidated table: kick and contact parameters

| Parameter | Value | Conditions | Source |
|---|---|---|---|
| Foot-ball contact time | **9.6–10.7 ms** (means); 8.8–12.0 ms (range) | one-step instep, ball speed 17–25 m/s, 2,500 fps | [Ishii 2012, Table 1] |
| Contact time scaled to 32.5 m/s | about 9 ms *(our calc: Hertz scaling τ ∝ v^(−1/5) gives (20/32.5)^0.2 ≈ 0.91)* | assumes Hertz behaviour | — |
| Ball deformation (peak) | 29–65 mm | as above | [Ishii 2012, p. 262] |
| Peak impact force | 1.06–2.23 kN, peak at about 4 ms | as above | [Ishii 2012, p. 262, Fig. 5] |
| Ball-centre displacement during contact | ≈ V·τ/2 ≈ 0.10 m at 20 m/s and **≈ 0.15 m at 32.5 m/s** *(our calc, half-sine force)* | — | derived from [Ishii 2012, Fig. 5] |
| Ball launch speed, penalty | 23.9 ± 1.2 m/s | one intercollegiate player, 3-step | [Ravenscroft & Linthorne 2015, p. 3] |
| Ball launch speed, lab maximal | 17.1–24.7 m/s (subject means 19.4–22.6), **normalised to foot speed** | 5 university players, one step, ball on a 0–12 cm stand | [Ishii 2012, Table 1] |
| Ball launch speed, lab | 26.3 m/s (example trial) | collegiate, 2-step | [Naito 2010, p. 267–268] |
| Foot speed at impact | 17.3 ± 0.7 m/s; 13.1–17.9 m/s | as above | [R&L 2015]; [Ishii 2012, Table 1] |
| Ball/foot speed ratio | 1.32–1.45 | — | *(our calc from both papers)* |
| Coefficient of restitution | depends on the impact point; no values given | — | [Ishii 2012, Table 2] |
| Launch elevation, penalty | 8 ± 5° | — | [R&L 2015, p. 3] |
| Impact-point effect on speed | up to −10–15% at ±6 cm from the optimum (ball on a stand); undetectable (≤ 1.8 m/s over 15 cm) in a real penalty | — | [Ishii 2012, Fig. 7]; [R&L 2015, p. 4] |
| Foot angular velocity at impact | 25–49 rad/s | — | [Ishii 2012, Table 1] |
| Shank angular velocity at impact | 1650 ± 160 deg/s (≈ 29 rad/s) | — | [R&L 2015, p. 3] |
| Peak knee-extension velocity | about 24 rad/s *(our calc)*; acceleration above 500 rad/s² | — | [Naito 2010, Table 1, Fig. 3] |
| Spin | **not reported in any paper in this cluster** | — | — |

## Table: goalkeeper timing parameters

| Parameter | Value | Source |
|---|---|---|
| Keeper leave-time (start of final dive) | −0.22 ± 0.11 s relative to contact (n = 330, professional) | [Hunter 2018, p. 4, Fig. 2] |
| Range of leave-times | about −0.65 to +0.25 s; nearly all keepers leave before contact | [Hunter 2018, Fig. 2] |
| Direction accuracy from cues at −0.4 s | 55–64% | [Hunter 2018, p. 7] |
| Direction accuracy at −0.2 s (≈ mean leave-time) | instep 69–72%; side-foot 64–70% | [Hunter 2018, Fig. 4] |
| Direction accuracy at contact (0 s) | instep about 80%; side-foot about 88–90% | [Hunter 2018, p. 7, Fig. 4] |
| Plant of the support foot | about −0.1 s | [Hunter 2018, p. 10] |
| Ball flight time to the goal line, our case | about 0.36 s without drag (v_x ≈ 30.4 m/s), about 0.37–0.38 s with drag *(our calc)* | — |
| Ball flight time at 24 m/s (R&L speed) | about 0.47 s *(our calc)* | — |
| Keeper reaction or movement durations, save rate against speed | **not given** in this cluster (Hunter cites refs [17, 25–27, 35]) | — |

---

## Implications for our model

### (a) Treatment of t = 0

- **The contact itself.** Contact lasts about 10 ms. During it the ball centre is pushed about 0.1–0.15 m while it accelerates from 0 to V. If t = 0 marks *first contact*, then a straight free-flight line extrapolated back from later positions passes through the origin not at t = 0 but at t ≈ τ/2 ≈ 5 ms. Put another way, at t = 0 that line sits about 0.15 m behind the rest position.
- **The test data suggests no such lag** *(our calc)*.
  - The displacement over 0–0.05 s is 1.600 m. Over 0.05–0.10 s it is 1.546 m. The difference is 0.054 m.
  - Drag plus gravity on a 32 m/s ball (k = ρC_DA/2m ≈ 0.013 m⁻¹, C_D ≈ 0.25) predicts a difference of about 0.04 m.
  - A 5 ms lag would make the first interval about 0.15 m *shorter* than the second, which is not what we see.
  - So the problem's t = 0 behaves as an **effective free-flight origin**: the ball leaves (0, 0, 0.11) at full speed at t = 0.
- **Recommendation.**
  - Treat (0, 0, 0.11) at t = 0 as a third data point. Give it an uncertainty along the launch direction of about 0.05–0.15 m, or equivalently a time-offset nuisance parameter δt₀ ∈ [0, 6] ms.
  - Do not let it dominate the velocity fit. Both observed points (0.05 s and 0.10 s) are certainly in free flight, since contact ends by 12 ms.
  - A 5 ms timing error at 32 m/s shifts the predicted arrival time by about 5 ms but barely changes the goal-plane crossing, because the direction is set by the two free-flight points.
- **Size of the origin.** The z = 0.11 m centre equals the ball radius, so the ball is resting on the ground. That is consistent with an instep kick from the spot.

### (b) Prior on launch speed

- The university-level data in this cluster is 24 ± 1.2 m/s for a penalty, and 17–26 m/s in total.
- 32.5 m/s needs a foot speed of about 23–25 m/s at a ratio of 1.3–1.4. That fits a powerful, near-maximal instep strike by a strong or elite player. It is at the top of the human range, but it is not unphysical.
- For a Bayesian prior: centre on the measured value, because 32.5 m/s is directly observed, with a wide tail. Something like a log-normal with median about 27 m/s and a 95% upper bound of about 35 m/s would flag 32.5 m/s as a hard shot without penalising it. Speeds above about 37 m/s would be suspicious.
- An elevation of 8 ± 5° supports our 12°.
- A lateral angle of 17° aims at about y ≈ 3.4 m at the goal line before curve *(our calc)*, close to the post at 3.66 m. Hunter's kickers aimed 1 m inside the post, which is about 13.6°.

### (c) Goalkeeper interpretation layer

- A real keeper commits about 0.22 s *before* contact, using body cues that are right about 70% of the time at that moment.
- Our observer instead has ball-flight data up to +0.10 s, which is about 25–27% of the 0.37–0.40 s flight. That is 0.32 s more than the average keeper and uses a different kind of information: physics rather than cues.
- An outcome probability expressed as "left/right correct" is therefore close to 100% for us. The relevant uncertainty is the *position* error at the goal plane, which comes mostly from spin and drag, not from the direction.
- The 80–90% figures give a natural baseline. The best possible pre-contact guess is still wrong 10–20% of the time. Any post-contact estimator should be compared against this.

---

## Answers to the four questions

**Q1. Is contact ≈ 8–12 ms?**
- **Yes, verified.** Subject means were 9.6–10.7 ms and single trials 8.8–12.0 ms [Ishii 2012, Table 1]. These were measured at ball speeds of about 17–25 m/s. Hertz scaling gives about 9 ms at 32.5 m/s *(our calc)*.
- **During contact the ball is still accelerating.** The force is roughly a half-sine peaking at about 2 kN near 4 ms [Fig. 5]. The ball is deformed by up to 3–6.5 cm. The centre moves about V·τ/2 ≈ 0.15 m during contact.
- **For our problem**, free flight from exactly (0, 0, 0.11) at t = 0 is an idealisation with an error equivalent to about 5 ms, or about 0.15 m. The test data is consistent with an effective-launch t = 0, not with a first-contact t = 0. Both observation times are well into free flight.

**Q2. Is 32.5 m/s realistic for a penalty?**
- It is high against this cluster: penalty 23.9 ± 1.2 m/s [R&L 2015], lab 17–26 m/s [Ishii 2012; Naito 2010], all from university players.
- It needs a foot speed of about 23–25 m/s. That is realistic for a powerful elite penalty (about 117 km/h), but it sits at the top of the distribution, not the centre.
- The launch elevation of 12° is typical (8 ± 5°).

**Q3. Goalkeeper time and early prediction (Hunter 2018).**
- Professional keepers start their dive at −0.22 ± 0.11 s relative to contact.
- From body cues alone, direction is predicted 55–64% correctly at −0.4 s, about 64–72% at −0.2 s, and about 80% (instep) or 90% (side-foot) at contact.
- Speed makes side-foot shots easier to read but has no significant effect for instep.
- Information budget: the keeper's total window is about 0.22 s before contact plus about 0.37–0.40 s of flight, roughly 0.6 s. The keeper effectively decides with only the pre-contact information. Our 0.10 s of post-contact flight is about 25% of the flight and gives information a keeper never uses. The direction is effectively certain; what remains is the uncertainty in the size of the lateral error.
- The paper gives no keeper reaction or movement times and no save rate against speed.

**Q4. Spin from off-centre impact?**
- **No direct data in this cluster.** All analyses are 2-D sagittal and no spin was measured.
- Ishii models tangential force with μF_n but does not determine μ. Impact location along the foot changes speed by 10–15% and changes the restitution coefficient, but sidespin needs a lateral offset or an oblique foot sweep, which none of these papers cover.
- The source to obtain is Asai et al. (2002), *The curve kick of a football I: impact with the foot*, Sports Eng. 5:183–192, cited by both Ishii and Naito.
- An order-of-magnitude check *(our calc, a rigid hollow shell with gripping contact)* gives ω ≈ 0.6·v_t/R. A tangential foot-sweep speed of 5–10 m/s then gives about 27–55 rad/s (4–9 rev/s). That is the typical range for curled kicks.
