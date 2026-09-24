---
layout: post
title: "Binders for RBX1"
date: 2026-09-24
custom_js: https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.1.0/3Dmol-min.js
---

Because there's a new adaptyv protein design competition started soon that I wanted to have a go at I thought I'd try to learn a bit about how AI is used to generate binders for proteins. So I decided to use the recent GEM/Adaptyv RBX1 competition to try a couple of things: 1. Making a pipeline for generating binders and 2. Find out how binders are selected for experimental testing.

RBX1 is a part of a protein complex called Cullin-RING E3 ligase complexes that tags other unwanted or damaged proteins for destruction and recycling. It does this through a process called ubiquitinisation, attaching a molecule called ubiquitin to mark proteins for degradation. It plays an important role in cell proliferation and thus cancer, as well as some other diseases, so makes a good target for drugging. However it is difficult to design binders primarily for three reasons: firstly it has this large intrinsically disordered region on the N-terminal, this protein forms part of a larger complex, and without the other subunits pinning it down this region can adopt many conformations (in fact it can still take on different conformations when part of the whole complex, which allows the complex the requisite flexibility to attach ubiquitin to many different proteins). The uncertainty in this region swamps the uncertainty on the rest of the sequence, and thus metrics like whole complex pTM or pLDDT or any other metric which doesn't restrict itself to contact residues and which is computed across the whole complex, get tanked by the disordered region even though the uncertainty in that region might not effect where we would want to bind to anyway. Secondly, on the other end of the protein it has these three zinc ions which get held in a cross-brace sort of position and which AI models usually struggle to place correctly. But without placing these correctly the RING domain won't fold right. And finally, it lacks useful evolutionary relatives or analogues, so MSA based approaches have little to go on.

The scale of the problem shows in the fold-prediction baselines. According to a [blog post by the winners of the competition](https://research.mandrake.bio/p/we-dont-even-design-binders), Mandrake bio, ESMFold reaches pLDDT 0.40 on this target, Protenix ab initio 0.60, Boltz-2 0.63. All of these uninformative or marginal. In adaptyv's competition out of 322 designs, only 9 bound to the target and 255 expressed.

Mandrake's ORBIT pipeline took an approach that:

- Used known structure information: They fed Protenix the NMR structure with the ions explicitly placed and the pLDDT rose significantly (predictably). There's no reason not to use this information since the goal here isn't to fold the protein, its to predict binders.
- Constrained the search space. Standard differentiable hallucination runs trajectories from a uniform prior and thus spends a lot of time trying to find the right neighbourhood rather than doing the interesting refinement. Instead they run DH for a while, inverse fold with SolubleMPNN to get a general structure and then use this as a prior to begin optimisation from.
- They treat each differentiable optimisation run as a trajectory, which allows for thinking about early stopping using a classifier or recognising that the argmax projection could degrade during this process so they can instead harvest the best sequence along the trajectory.
- Use an attractive field in coordinate space that pulls the binder towards high-value target residues. Would be interesting to compare against the distogram based methods which bias which residues form contacts but not how the binder gets drawn to them.
- By applying a regularisation layer to the PSSM the optimiser gets pushed towards not just what the structural model thinks is high probability, but also towards other desirable properties (hydrophobicity, net charge).

This last point is the most interesting to me, we can look at which properties are most important from this competition. Doing this is fraught with all kinds of problems however:

1. The designs come pre-filtered, only the designs which were passed selection make it into the datasets, so any analysis you do automatically loses power
2. The selection can change between competitions, for instance in the nipah competition they selected 600 designs based on Boltz-2 ipSAE, 400 selected by a panel of experts, and 200 chosen by community vote.
3. Before even making it to the selection stage, designs are prefiltered by the contestants using various filters, [some may even experimentally test their designs before submission](https://x.com/sokrypton/status/1998208058632351861).
4. The selection metrics are biased towards certain structural motifs, α-helical proteins for instance, which further biases any analysis. 

Adaptyv has run several of these competitions: A two stage competition aiming to find binders for EGFR, one aiming for binders of the Nipah virus, and the aforementioned RBX1 competition. 

In the first adaptyv competition on EGFR iPAE, ipTM and ESM-2 pseudo-likelihood were used as selection mechanisms. Also additional binders were selected to increase diversity in the final released dataset, so the above concerns are well known. One of the results that stood out to me in [their write up](https://www.biorxiv.org/content/10.1101/2025.04.17.648362v2.full.pdf) was that lumping all designs together meant that metrics that might only show significance on say, peptides, would be marked down as insignificant. In fact the winning design was completely overlooked by the above metrics. In the Nipah competition ipSAE was chosen, but it had issues in that scores would vary slightly due to random seed and this variability was not uniform across designs, which may have advantaged designs which gave more stable scores. All of this is to say that determining *in-silico* whether a design will bind is quite challenging. In a [2025 paper](https://www.biorxiv.org/content/10.1101/2025.08.14.670059v2) Overath et al. propose the following selection criteria:

```
Based on our analysis, we recommend the following actionable filtering strategies. The first involves setting one of the following thresholds for filtering designs: AF3 ipSAE_min > 0.61; AF3 ipSAE_min x interface_∆G/∆SASA < -1.5; or AF3 LIS x input_interface_shape_complementary > 0.42. The second strategy entails pre-filtering designs using input_interface_shape_complementary > 0.62 and RMSD_binder < 3.73, followed by selecting the top K designs based on AF3 ipSAE_min
```

I thought it would be worthwhile to see if me and claude could build a binder generation pipeline informed somewhat by mandrake's pipeline (more like claude building the entire thing in about 3 prompts) and then see how the 9 binders from the competition would have fared against the aforementioned metrics and selection criteria. In line with Mandrake's proposal we will use protenix in place of AF3 to calculate metrics.

### My pipeline
Claude code is really good at this sort of thing, the hardest part of building the pipeline was dealing with the feelings of obsolescence as it handily whipped off code it would have taken me weeks to do by hand. The pipeline ended up looking like:

```
target structure + hotspot residues
        |  RFdiffusion            (generate backbone shapes)
        v
   backbone PDBs (no meaningful sequence)
        |  SolubleMPNN            (sequence for each backbone)
        v
   candidate sequences
        |  ESM-2                  (rank by "naturalness")
        v
   shortlist
        |  Protenix / Boltz-2     (fold binder + target together)
        v
   predicted complexes + PAE, ipTM, pLDDT
        |  ipSAE, pDockQ, ...     (interface scoring from those outputs)
        v
   feature table
```

First we can do a few sanity checks of this pipeline, do the generated binders make much sense, do we actually make contact with the binding site etc.

### Do we make contact?
The first question is: when we use RFDiffusion to design binders against our fold from protenix, do we actually make contact with the binding sites we specify (A74/F81/Y106, chosen somewhat arbitrarily although I excluded the disordered region)? The answer seems to be yes for at least one of the sites and "somewhat" if we want to contact all three sites? We don't necessarily need a binder to contact all 3 hotspots so contacting just one is a good sign that we are on target.


| run | n backbones | contact >=1 hotspot | contact all 3 hotspots |
|---|---|---|---|
| smoke test | 20 | 20 (100%) | 5 (25%) |
| scale-up | 200 | 196 (98%) | 61 (30.5%) |


### Are the sequences self consistent?
RFDiffusion gives us a structure which hopefully gets nice and close to our stated binding spots, which we can then reverse-fold into a sequence using SolubleMPNN. The natural question is then: If we do this and then refold the sequences do we get back to something that looked like the original sequence we proposed, or does SolubleMPNN just hallucinate something that doesn't give us the sequence we want? Unfortunately since we don't get the original sequences from the 322 contest entries we can't check this for them, but we can test the generated backbones from the last step.

| | value |
|---|---|
| backbones | 200 |
| sequences (8 MPNN samples/backbone) | 1600 |
| median self-consistency RMSD (best seq/backbone) | 0.64 A |
| mean self-consistency RMSD (all 1600) | 4.32 A |
| backbones with >=1 sub-2A design | 183 / 200 (91.5%) |

Looks pretty good, SolubleMPNN clearly does a good job at this.

So in the next couple of section we will take a really crude look at what metrics predict expression and binding in this set. To do this properly we should probably look more generally beyond RBX1 considering how few binders there were and deal with uncertainty and significance properly. But just to start let's see.

### Expression (n=321, 255 expressed)
Before a design can bind to the target it must express, meaning they must be able to be produced in the assay adaptyv used. (Note one design had no binder label). Here we have sign flipped metrics appropriately so higher AUC always means "better at this metric predicts expression better".

| metric | AUC |
|---|---|
| `seq_fraction_charged` | **0.740** |
| `binder_mean_plddt` | 0.633 |
| `iface_pdockq2` | 0.632 |
| `iface_ipae`  | 0.631 |
| `struct_binding_energy`  | 0.620 |
| `iface_lis` | 0.620 |
| `iface_iptm` | 0.619 |
| `iface_ipsae_min` | 0.614 |
| `struct_dg_dsasa_ratio`  | 0.610 |
| `iface_i_pdae` (symmetrised) | 0.607 |
| `iface_ipsae` | 0.605 |
| `iface_i_pdae_asymmetric` | 0.604 |
| `iface_pdockq` | 0.580 |
| `struct_interface_hbonds` | 0.534 |
| `struct_shape_complementarity` | 0.533 |
| `struct_interface_hydrophobicity` | 0.512 |
| `struct_interface_hydrophobic_fraction` | 0.493 |
| `struct_buried_sasa` | 0.435 |
| `struct_contacts` | 0.414 |
| `binder_length` | 0.406 |
| `seq_aggregation` | 0.369 |
| `seq_pi` | 0.323 |
| `seq_net_charge_ph7` | 0.311 |
| `seq_gravy` | 0.278 |

This makes sense, the SolubleMPNN weights were shown to be very important to get binders which expressed (93% to 0% difference!!) and it tends to raise the surface charge of the proteins it predicts. Additionally plddt and iPAE, the folding models confidence in its own predictions on a per residue level and predicted aligned error respectively, which a lot of the interface metrics either directly inherit from or are correlated to, makes sense as metrics to be positively correlated with expression: If the model is more confident that it has predicted the structure right or if it predicts a lower average error when aligning on all the residues, it is probably more plausible as a real structure. Maybe... and as we will see expression doesn't guarantee binding. Another problem with these metrics is that they are, of course, biased towards proteins which already exist and that were in the training set of whichever folding model you use, and we are interested in generating and selecting novel proteins. 


### Binding (n=322, 9 binders)

There are far fewer binders than expressors, so these results need to be taken with a proportionally larger pinch of salt.

| metric | AUC | average precision |
|---|---|---|
| `binder_length` | 0.725 | 0.164 |
| `seq_fraction_charged` | 0.695 | 0.058 |
| `struct_contacts` | 0.677 | **0.229** |
| `seq_aggregation` | 0.662 | 0.048 |
| `struct_buried_sasa` | 0.662 | 0.207 |
| `iface_pdockq` | 0.639 | 0.058 |
| `struct_interface_hbonds` | 0.562 | 0.086 |
| `iface_iptm` | 0.561 | 0.100 |
| `binder_mean_plddt` | 0.545 | 0.034 |
| `iface_i_pdae` (BindCraft2, symmetrised) | 0.539 | 0.091 |
| `iface_ipsae_min` (Overath et al.'s preferred aggregation) | 0.532 | 0.090 |
| `iface_ipsae` (tool's default "max" aggregation) | 0.531 | 0.047 |
| `iface_i_pdae_asymmetric` | 0.523 | 0.053 |
| `iface_lis` | 0.522 | 0.042 |
| `struct_interface_hydrophobic_fraction` (BindCraft's definition) | 0.516 | 0.032 |
| `struct_interface_hydrophobicity` (area-weighted) | 0.498 | 0.032 |
| `iface_pdockq2` | 0.496 | 0.042 |
| `iface_ipae` *(sign-flipped)* | 0.466 | 0.035 |
| `struct_dg_dsasa_ratio` *(sign-flipped)* | 0.464 | 0.029 |
| `seq_gravy` | 0.432 | 0.027 |
| `struct_binding_energy` *(sign-flipped)* | 0.419 | 0.027 |
| `struct_shape_complementarity` | 0.417 | 0.026 |
| `seq_pi` | 0.312 | 0.021 |
| `seq_net_charge_ph7` | **0.197** | 0.018 |

By eye these seem to make sense, RBX1 is a pretty complicated molecule so minimal scaffolds like minibinders may struggle to attach whereas a larger properly folded molecule has more to work with. The metrics that dominate have a lot to do with the binding site or other things that would make a molecule better or worse at sticking to another: seq_fraction_charged is about how much of the sequence has charged residues, aggregation slides a 7 residue window over the sequence and calculates hydropathy, basically asking "is there a continuous patch with high hydrophobicity and how hydrophobic is it?", buried_sasa asks a similar question but appends "is it exposed on the outside of the molecule?" although why the simple sequence level metric that has no structural information outperforms the more sophisticated buried_sasa is a bit mysterious. 

One other interesting thing to note is that binders tend to be more negatively charged than non-binders. In the next few segments we will investigate this a bit.

### So if the binders are negatively charged...

It makes sense at this point to ask the obvious question: Is there some physical reason why the binders have lower net charge than the non-binders? For instance are the binding sites of rbx1 strongly positively charged, rewarding more negatively charged binders? The answer seems to be no.

| | binder median | non-binder median | AUC | p-value |
|---|---|---|---|---|
| actual_site_net_charge (all real contacts) | -0.781 | -0.782 | 0.597 | 0.3211 |
| actual_site_net_charge (ordered contacts only, excl. 1-39) | -1.052 | -0.783 | 0.473 | 0.7765 |

So if we trust the locations these binders end up using my pipeline (big if), then there isn't really any significant signal either way and it isn't clear why lower charged proposed binders are more likely to be successful. 


### Which binders would survive Overath et al.'s filter

- *Threshold strategy* (`ipSAE_min > 0.61` OR `ipSAE_min x interface_dG/dSASA < -1.5` OR
  `LIS x shape_complementarity > 0.42`): 63/322 designs pass; of those, 3/9 are real binders
  (precision 4.8% vs a 2.8% base rate). With `ipSAE_min > 0.61` alone: 61/322 pass, 3/9 binders caught.
- *Ranking strategy* (prefilter on shape complementarity + RMSD_binder, then rank survivors by
  ipSAE_min): the RMSD_binder prefilter needs a reference/design structure that these archived
  competition designs don't give us, so only the shape-complementarity prefilter is applied here.

  Then if we have k testing budget we can ask "of the available designs in the top-k, how many are binders?"

  | k | designs available | binders caught | precision |
  |---|---|---|---|
  | 10 | 10 | 1 | 10.0% |
  | 20 | 20 | 1 | 5.0% |
  | 50 | 50 | 2 | 4.0% |
  | 100 | 72 | 2 | 2.8% |

So we don't really do all that well if this is all we rely on.

### How do my own designs stand up

Because I am able to provide my own structures on the 10 designs I produced we can run the full prefilter. In this case only **1 of 10** designs passes both `struct_shape_complementarity > 0.62` and `struct_binder_rmsd < 3.73 A` at once (`bb_4_sample3`, Sc=0.622, RMSD_binder=3.28 A). Here it is in its predicted binding spot:

<div id="viewer-bb4sample3" style="width: 100%; height: 420px; position: relative;"></div>
<script>
(function () {
  var viewer = $3Dmol.createViewer("viewer-bb4sample3", {backgroundColor: "white"});
  $3Dmol.download("url:/structures/own_overath_survivor_bb_4_sample3.cif", viewer, {format: "cif"}, function () {
    viewer.setStyle({chain: "A"}, {cartoon: {color: "lightgrey"}});
    viewer.setStyle({chain: "B"}, {cartoon: {color: "orange"}});
    viewer.setStyle({resn: "ZN"}, {sphere: {color: "purple", radius: 0.6}});
    viewer.zoomTo();
    viewer.render();
  });
})();
</script>

Its predicted `ipSAE_min` is only 0.404 so wouldn't pass the 0.61 single metric threshold.

If we just look at `ipSAE_min` our best binder is as follows, even though this fails the shape complementarity test (0.523, short of 0.62):

<div id="viewer-bb16sample1" style="width: 100%; height: 420px; position: relative;"></div>
<script>
(function () {
  var viewer = $3Dmol.createViewer("viewer-bb16sample1", {backgroundColor: "white"});
  $3Dmol.download("url:/structures/own_best_bb_16_sample1.cif", viewer, {format: "cif"}, function () {
    viewer.setStyle({chain: "A"}, {cartoon: {color: "lightgrey"}});
    viewer.setStyle({chain: "B"}, {cartoon: {color: "orange"}});
    viewer.setStyle({resn: "ZN"}, {sphere: {color: "purple", radius: 0.6}});
    viewer.zoomTo();
    viewer.render();
  });
})();
</script>

Without experimental confirmation we can't say definitively which is better.

For completeness here is the winner of the binding competition in the position that my pipeline predicts for it:

<div id="viewer-small-vole-maple" style="width: 100%; height: 420px; position: relative;"></div>
<script>
(function () {
  var viewer = $3Dmol.createViewer("viewer-small-vole-maple", {backgroundColor: "white"});
  $3Dmol.download("url:/structures/competition_winner_small-vole-maple.cif", viewer, {format: "cif"}, function () {
    viewer.setStyle({chain: "A"}, {cartoon: {color: "lightgrey"}});
    viewer.setStyle({chain: "B"}, {cartoon: {color: "teal"}});
    viewer.setStyle({resn: "ZN"}, {sphere: {color: "purple", radius: 0.6}});
    viewer.zoomTo();
    viewer.render();
  });
})();
</script>


The winning binder definitely looks more complicated than both of the ones I generated.


### Some final thoughts

It would be cool if in future competitions the design structures and predicted co-folds could be included, perhaps along with predicted epitope. I don't think it would be that much to ask competitors to include this and would be a useful tool for analysis. For instance, I'm interested to know where binders were predicted to land on RBX1 by the competitors' pipelines and how this prediction would differ using my own pipeline.  

Based on my own pipeline only 4/9 of the binders make any contact with my chosen sites (A74/F81/Y106) and the best binder from Mandrake makes significant contact with the disordered region that I ruled out (without thinking about it too much). Again this can only be trusted so far since we don't know what the competitors models predicted, nor do we know where the binder actually lands in vitro.

Some questions I think I'll try to answer for the next competition:

1. How do you select binding sites, can this be done after folding by calculating things about the protein?
2. How can I generate more diverse binders?
3. Can I replicate Mandrake's unpublished pipeline based on their blog post?
4. Given a set of binders and some metrics how do I best select and rank them?
5. How do I iterate on a pipeline like this to generate better binders?

