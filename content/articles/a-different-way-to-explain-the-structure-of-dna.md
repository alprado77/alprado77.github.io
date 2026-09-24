Title: DNA structure explained visually: nucleotides and the double helix
Date: 2025-09-21
Author: Alfonso Prado-Cabrero, PhD
Slug: a-different-way-to-explain-the-structure-of-dna
Kicker: Molecular Biology — Explainer
Image: dna-model-close-view.webp
Card_image: dna-model-close-view.webp
Image_credit: Double strand of DNA (dsDNA)
Dek: Here you will embark on a visual trip through the structure of the molecule of life. We set atomic details aside and focus on the shape of the building blocks of DNA, deoxynucleotides, and how they bind to make up the famous double helix.


<script src="https://3Dmol.org/build/3Dmol-min.js"></script>
<script>
function styleDNA(viewer, group, color) {
  viewer.setStyle({resn: group, elem: "P"},
    {sphere: {color: color, radius: 0.45}, stick: {radius: 0.15, color: color}});
  viewer.setStyle({resn: group, elem: "O"},
    {sphere: {color: color, radius: 0.30}, stick: {radius: 0.15, color: color}});
  viewer.setStyle({resn: group, elem: "C"},
    {sphere: {color: color, radius: 0.35}, stick: {radius: 0.15, color: color}});
  viewer.setStyle({resn: group, elem: "N"},
    {sphere: {color: color, radius: 0.38}, stick: {radius: 0.15, color: color}});
  viewer.setStyle({resn: group, elem: "H"},
    {sphere: {color: color, radius: 0.20}, stick: {radius: 0.10, color: color}});
}

function showHBonds(viewer) {
  viewer.addStyle({}, {});  // ensure all atoms are processed
  viewer.setClickable({}, true, function(){});  // needed for some versions
  
  // Get all donor-acceptor pairs and draw dashed lines
  var atoms = viewer.getModel().selectedAtoms({});
  for (var i = 0; i < atoms.length; i++) {
    for (var j = i + 1; j < atoms.length; j++) {
      var a = atoms[i];
      var b = atoms[j];
      // Only N and O can be H-bond donors/acceptors
      if ((a.elem === "N" || a.elem === "O") && 
          (b.elem === "N" || b.elem === "O")) {
        var dx = a.x - b.x;
        var dy = a.y - b.y;
        var dz = a.z - b.z;
        var dist = Math.sqrt(dx*dx + dy*dy + dz*dz);
        // H-bond distance: 2.5–3.5 Å, only between different chains/residues
        if (dist > 2.5 && dist < 3.5 && a.resi !== b.resi) {
          viewer.addCylinder({
            start: {x: a.x, y: a.y, z: a.z},
            end: {x: b.x, y: b.y, z: b.z},
            radius: 0.04,
            color: "grey",
            dashed: true,
            dashLength: 0.15,
            gapLength: 0.1
          });
        }
      }
    }
  }
}

function showMolecule(divId, file, groups, options) {
  options = options || {};
  var rotateX  = options.rotateX  || 0;
  var rotateY  = options.rotateY  || 0;
  var rotateZ  = options.rotateZ  || 0;
  var spinAxis = options.spinAxis || "z";
  var spinSpeed = options.spinSpeed !== undefined ? options.spinSpeed : -2.0;
  var fog      = options.fog !== undefined ? options.fog : true;
  var outline  = options.outline  || 0.02;
  var zoom = options.zoom || 1;
  var hbonds = options.hbonds || [];

  fetch(file)
    .then(function(r) {
      if (!r.ok) {
        document.getElementById(divId).innerHTML =
          "<p style='padding:2rem;color:#555;'>Could not load " + file + "</p>";
        throw new Error("Not found");
      }
      return r.text();
    })
    .then(function(data) {
      var viewer = $3Dmol.createViewer(divId, {backgroundColor: "white"});
      if (fog) viewer.enableFog(true);
      viewer.setViewStyle({style: "outline", color: "black", width: outline});

      viewer.addModel(data, "pdb", {keepH: true});

      // Apply colour groups
      for (var i = 0; i < groups.length; i++) {
      styleDNA(viewer, groups[i].group, groups[i].color);
      }

    // Apply colour groups
    for (var i = 0; i < groups.length; i++) {
      styleDNA(viewer, groups[i].group, groups[i].color);
    }

    // Draw hydrogen bonds as dashed lines
    if (hbonds.length > 0) {
      var atoms = viewer.getModel().selectedAtoms({});
      for (var i = 0; i < hbonds.length; i++) {
        var a = atoms[hbonds[i][0] - 1];
        var b = atoms[hbonds[i][1] - 1];
        if (a && b) {
          viewer.addCylinder({
            start: {x: a.x, y: a.y, z: a.z},
            end: {x: b.x, y: b.y, z: b.z},
            radius: 0.03,
            color: "grey",
            dashed: true,
            dashLength: 0.15,
            gapLength: 0.1
          });
        }
      }
    }
    viewer.zoomTo();

      viewer.zoomTo();
      viewer.zoom(zoom);
      if (rotateX) viewer.rotate(rotateX, "x");
      if (rotateY) viewer.rotate(rotateY, "y");
      if (rotateZ) viewer.rotate(rotateZ, "z");
      if (spinSpeed) viewer.spin(spinAxis, spinSpeed);

      var container = document.getElementById(divId);
      container.addEventListener("mousedown", function() { viewer.spin(false); });
      container.addEventListener("touchstart", function() { viewer.spin(false); });
      container.addEventListener("dblclick", function() { viewer.spin(spinAxis, spinSpeed); });

      viewer.render();
    });
}
</script>

Lee este artículo en [español](/la-estructura-del-adn-explicada-de-una-forma-diferente/)

## Introduction

DNA is made up of deoxynucleotides. Getting familiar with these building blocks and how they shape DNA opens the door to understanding genetics. I believe that a minimum of chemical details plus plenty of animations that you can manipulate will help you start to become familiar with the molecule of life.

Therefore, here we focus on DNA 3D structure with interactive animations. You can click on an image to stop rotation, drag to rotate, scroll to zoom in or zoom out, and double-click to resume auto rotation. In this way, I hope you become familiar with DNA from all angles. Let's start playing!

## Deoxynucleotide structure overview

DNA looks like a spiral staircase, where each deoxynucleotide makes up a segment of the rail and half a rung. In Fig. 1, we show the shape of dAMP, one of the four deoxynucleotides that make up DNA. The 5-deoxyribose (in green) and the phosphate group (in yellow) form part of the rail; the nitrogenous base (in blue) makes up half a rung.

<div id="mol1" style="width:100%; max-width:600px; height:350px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol1", "/images/molecules/adenylate-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "BAS", color: "#00bfff"}
], {rotateX: 90, rotateY: 0, outline: 0.04, zoom: 1, spinAxis: [0, 0, 1]});
</script>

**Figure 1.** **dAMP** (**d**eoxy**A**denosine **M**ono**P**hosphate) represented as ball (atoms) and sticks (bonds between atoms).

## Let's bind the parts (the deoxynucleotides)

Now let's put together three dAMPs that, once bonded, form a single DNA strand (Fig. 2). The same coloring pattern as in Fig. 1 is used, to make it clear which part of the deoxynucleotides is forming the rungs and which part is forming the rail. But this way, it looks like we are building only one side of the spiral staircase…

<div id="mol2" style="width:100%; max-width:600px; height:450px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol2", "/images/molecules/tri-adenylate-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "BAS", color: "#00bfff"}
], {rotateX: 90, rotateY: 0, outline: 0.04, zoom: 1});
</script>

**Figure 2. Three dAMPs in a row.**

## Now completing the spiral staircase...

To complete this staircase of three rungs, let's add the missing part, which is the complementary chain. This completes a double strand of DNA (Figure 3). But you may have noticed that the other half-rungs are red! That is because these dNTPs are different. They are dTTP (they bear thymine, a different base). In a DNA 'rung', dATP can only coexist with dTTP, since the two bases are exclusively complementary.

<div id="mol3" style="width:100%; max-width:600px; height:350px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol3", "/images/molecules/aaa-ttt-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "ADE", color: "#00bfff"},
  {group: "THY", color: "#CC3333"}
], {rotateX: 90, outline: 0.04, zoom: 1.6, hbonds: [
  [18, 179], [17, 181],   // A1 ··· T3
  [51, 147], [50, 149],   // A2 ··· T2
  [83, 114], [82, 116]    // A3 ··· T1
]});
</script>

**Figure 3. Double strand of DNA.**

Now, two things:

First, did you notice that the last free phosphates point up in one strand and down in the other? This means that both strands run in opposite directions; they are (anti)parallel. But why antiparallel? Researchers suggest that this feature facilitates DNA replication [(Subramanian et al., 2020)](https://www.nature.com/articles/s41598-020-66705-3).

Second, did you notice the dashed lines between the bases? These denote hydrogen bonds, a type of weak interaction that keeps the bases, and by extension the two strands, together. Since these bonds are weak, they can be separated with some energy input. Think of it as a zip that can be opened and closed.

For a clearer view, take a look at a single rung (composed of dATP and dTTP) from above. Two hydrogen bonds hold them together. You can play with the image.

<div id="mol4" style="width:100%; max-width:600px; height:300px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol4", "/images/molecules/at-pair-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "ADE", color: "#00bfff"},
  {group: "THY", color: "#CC3333"}
], {rotateX: 0, rotateY: 0, rotateZ: -90, zoom: 1.6, outline: 0.04, spinSpeed: 0, hbonds: [[18, 49], [17, 51]]});
</script>

**Figure 4. dATP and dTTP pair.**

## Four deoxynucleotides make up DNA

But remember, DNA has not just two, but four deoxynucleotides. The remaining two are dCTP and dGTP (Fig. 5). Notice that this pair of nucleotides is held together by three hydrogen bonds. Yes, the "glue" between these two nucleotides is stronger than that between dATP and dTTP.

<div id="mol5" style="width:100%; max-width:600px; height:300px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol5", "/images/molecules/cg-pair-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "GUA", color: "#0000FF"},
  {group: "CYT", color: "#FF6933"}
], {rotateX: 0, rotateY: 0,  rotateZ: -90, zoom: 1.6,  outline: 0.04, spinSpeed: 0, hbonds: [
  [17, 52],   // G O6  ··· C N4
  [18, 50],   // G N1  ··· C N3
  [20, 49]    // G N2  ··· C O2
]});
</script>

**Figure 5. dCMP and dGMP pair.**

## Completing the double strand

Therefore, we deduce that the sequence of deoxynucleotides in one strand unfailingly determines the sequence of deoxynucleotides in the other. Hence, the two strands are said to be complementary. Below, for clarity, one of the DNA strands is shown with the nitrogenous bases colored as above, so that you can read the sequence of deoxynucleotides.

<div id="mol6" style="width:100%; max-width:700px; height:700px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol6", "/images/molecules/acgtggatca-ss-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "ADE", color: "#00bfff"},
  {group: "CYT", color: "#FF6933"},
  {group: "GUA", color: "#0000FF"},
  {group: "THY", color: "#CC3333"}
], {rotateX: 90, zoom: 1.1});
</script>

**Figure 5. Single strand of DNA (ssDNA)**

Now we add the other strand, and we get the DNA double helix: the complete staircase, with two rails and rungs each made up of two pieces.

<div id="mol7" style="width:100%; max-width:700px; height:700px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol7", "/images/molecules/acgtggatca-ds-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "ADE", color: "#00bfff"},
  {group: "CYT", color: "#FF6933"},
  {group: "GUA", color: "#0000FF"},
  {group: "THY", color: "#CC3333"}
], {rotateX: 90, zoom: 1, hbonds: [[18, 622], [17, 624], [50, 591], [48, 592], [47, 594], [80, 561], [81, 559], [83, 558], [111, 530], [113, 529], [145, 499], [146, 497], [148, 496], [178, 469], [179, 467], [181, 466], [212, 435], [211, 437], [241, 406], [243, 405], [275, 372], [273, 373], [272, 375], [306, 337], [305, 339]]});
</script>

**Figure 6. Double strand of DNA (dsDNA)**