Title: La estructura del ADN explicada visualmente: nucleótidos y doble hélice
Date: 2025-05-20 10:00
Author: Alfonso Prado-Cabrero, PhD
Slug: la-estructura-del-adn-explicada-de-una-forma-diferente
Kicker: Biologia Molecular
Image: dna-model-close-view.webp
Card_image: dna-model-close-view.webp
Image_credit: Doble cadena de ADN
Dek: Vamos a emprender un viaje visual a la estructura de la cadena de la vida. En este rato vamos a dejar de lado detalles químicos, y vamos a concentrarnos en las formas de las moléculas para familiarizarnos con el ADN de forma intuitiva.
Lang_es: yes


Read this post in [English](/a-different-way-to-explain-the-structure-of-dna/)



<script src="https://3Dmol.org/build/3Dmol-min.js"></script>
<script>
function styleDNA(viewer, group, color) {
  viewer.setStyle({resn: group, elem: "P"},
    {sphere: {color: color, radius: 0.45, quality: "0"}, stick: {radius: 0.15, color: color}});
  viewer.setStyle({resn: group, elem: "O"},
    {sphere: {color: color, radius: 0.30, quality: "0"}, stick: {radius: 0.15, color: color}});
  viewer.setStyle({resn: group, elem: "C"},
    {sphere: {color: color, radius: 0.35, quality: "0"}, stick: {radius: 0.15, color: color}});
  viewer.setStyle({resn: group, elem: "N"},
    {sphere: {color: color, radius: 0.38, quality: "0"}, stick: {radius: 0.15, color: color}});
  viewer.setStyle({resn: group, elem: "H"},
    {sphere: {color: color, radius: 0.20, quality: "0"}, stick: {radius: 0.10, color: color}});
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
      
      //viewer.setSphereQuality("low");     // <-- add
      // viewer.setStickQuality("low");      // <-- add (if supported in your version)

      if (fog) viewer.enableFog(false);

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

## Introducción

El ADN está compuesto por desoxinucleótidos. Familiarizarte con estos componentes básicos y con como dan forma al ADN abre la puerta a comprender la genética. Creo que un mínimo de detalles químicos y animaciones que puedes manipular te ayudarán a familiarizarte con la molécula de la vida.

Por lo tanto, aquí nos centramos en la estructura 3D del ADN con animaciones interactivas. Puedes hacer clic en una imagen para detener la rotación, arrastrar para rotar, hacer zoom, y hacer doble clic para reanudar la rotación automática. De esta manera, espero que te familiarices con el ADN desde todos los ángulos. ¡Empecemos a jugar!

## Descripción general de la estructura de los desoxinucleótidos

El ADN se parece a una escalera de caracol, donde cada desoxinucleótido constituye un segmento del pasamanos y medio peldaño. En la Fig. 1, mostramos la forma del dAMP, uno de los cuatro desoxinucleótidos que componen el ADN. La 5-desoxirribosa (en verde) y el grupo fosfato (en amarillo) forman parte del pasamanos; la base nitrogenada (en azul) constituye medio peldaño.

<div id="mol1" style="width:100%; max-width:600px; height:350px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol1", "/images/molecules/adenylate-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "BAS", color: "#00bfff"}
], {rotateX: 90, rotateY: 0, zoom: 1, spinAxis: [0, 0, 1]});
</script>

**Figura 1.** **dAMP** (desoxiAdenosina Monofosfato) representado como bolas (átomos) y varillas (enlaces entre átomos).

## Vamos a unir las partes (los desoxinucleótidos)

Ahora juntemos tres dAMP. Una vez unidos, forman una sola hebra de ADN (Fig. 2). Usamos el mismo patrón de colores que en la Fig. 1, para dejar claro qué parte de los desoxinucleótidos forma los peldaños y qué parte forma el pasamanos. Pero de esta manera, parece que estamos construyendo solo un lado de la escalera de caracol…

<div id="mol2" style="width:100%; max-width:600px; height:450px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol2", "/images/molecules/tri-adenylate-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "BAS", color: "#00bfff"}
], {rotateX: 90, rotateY: 0, zoom: 1});
</script>

**Figure 2. Tres dAMPs in unidos.**

## Ahora completamos la escalera de caracol…

Para completar esta escalera de tres peldaños, agreguamos la parte que falta, que es la cadena complementaria. Esto completa una doble hebra de ADN (Figura 3). Pero quizá hayas notado que los otros medios peldaños son rojos. Eso se debe a que estos dNTPs son diferentes. Son dTTP (portan timina, una base diferente). Resulta que en un 'peldaño' de ADN, el dATP solo puede coexistir con dTTP, ya que las dos bases son exclusivamente complementarias.


<div id="mol3" style="width:100%; max-width:600px; height:350px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol3", "/images/molecules/aaa-ttt-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "ADE", color: "#00bfff"},
  {group: "THY", color: "#CC3333"}
], {rotateX: 90, zoom: 1.6, hbonds: [
  [18, 179], [17, 181],   // A1 ··· T3
  [51, 147], [50, 149],   // A2 ··· T2
  [83, 114], [82, 116]    // A3 ··· T1
]});
</script>

**Figura 3. Doble cadena de ADN.**

Ahora, dos cosas:

Primero, ¿notaste que último fosfato de cada hebra apunta uno hacia arriba y el otro hacia abajo? Esto significa que ambas hebras corren en direcciones opuestas; son (anti)paralelas. Pero, ¿por qué antiparalelas? Los investigadores sugieren que esta característica facilita la replicación del ADN [(Subramanian et al., 2020)](https://www.nature.com/articles/s41598-020-66705-3).

Segundo, Has visto las líneas discontinuas entre las bases? Estas denotan puentes de hidrógeno, un tipo de interacción débil que mantiene unidas las bases y, por extensión, las dos hebras. Como estos enlaces son débiles, pueden separarse con un aporte de energía. Imaginatelo como una cremallera que se puede abrir y cerrar.

Ahora, para verlo más claro, observa un solo peldaño (dATP y dTTP) desde arriba. Dos puentes de hidrógeno los mantienen unidos. Puedes jugar con la imagen.

<div id="mol4" style="width:100%; max-width:600px; height:300px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol4", "/images/molecules/at-pair-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "ADE", color: "#00bfff"},
  {group: "THY", color: "#CC3333"}
], {rotateX: 0, rotateY: 0, rotateZ: -90, zoom: 1.6, spinSpeed: 0, hbonds: [[18, 49], [17, 51]]});
</script>

**Figura 4. Pareja de dATP y dTTP.**

## Cuatro desoxinucleótidos componen el ADN

Pero recuerda, el ADN se forma no con dos, sino con cuatro desoxinucleótidos. Los dos restantes son dCTP y dGTP (Fig. 5). Observa que este par de nucleótidos está unido por tres puentes de hidrógeno. Sí, el "pegamento" entre estos dos nucleótidos es más fuerte que el que hay entre dATP y dTTP.

<div id="mol5" style="width:100%; max-width:600px; height:300px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol5", "/images/molecules/cg-pair-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "GUA", color: "#0000FF"},
  {group: "CYT", color: "#FF6933"}
], {rotateX: 0, rotateY: 0,  rotateZ: -90, zoom: 1.6,  spinSpeed: 0, hbonds: [
  [17, 52],   // G O6  ··· C N4
  [18, 50],   // G N1  ··· C N3
  [20, 49]    // G N2  ··· C O2
]});
</script>

**Figura 5. Pareja de dCMP y dGMP.**

## Completando la doble hebra

Por lo tanto, deducimos que la secuencia de desoxinucleótidos en una hebra determina infaliblemente la secuencia de desoxinucleótidos en la otra. Por consiguiente, se dice que las dos hebras son complementarias. A continuación, para mayor claridad, se muestra una de las hebras de ADN con las bases nitrogenadas coloreadas como arriba, para que puedas leer la secuencia de desoxinucleótidos.

<div id="mol6" style="width:100%; max-width:700px; height:700px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol6", "/images/molecules/acgtggatca-ss-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "ADE", color: "#00bfff"},
  {group: "CYT", color: "#FF6933"},
  {group: "GUA", color: "#0000FF"},
  {group: "THY", color: "#CC3333"}
], {rotateX: 90, zoom: 1.1, spinSpeed: 0});
</script>

**Figura 5. Hebra simple de ADN**

Ahora agregamos la otra hebra, y obtenemos la doble hélice de ADN: la escalera completa, con dos pasamanos, y peldaños formados cada uno por dos piezas.

<div id="mol7" style="width:100%; max-width:700px; height:700px; position:relative; margin:2rem auto;"></div>
<script>
showMolecule("mol7", "/images/molecules/acgtggatca-ds-h.pdb", [
  {group: "PHO", color: "yellow"},
  {group: "SUG", color: "#87AF50"},
  {group: "ADE", color: "#00bfff"},
  {group: "CYT", color: "#FF6933"},
  {group: "GUA", color: "#0000FF"},
  {group: "THY", color: "#CC3333"}
], {rotateX: 90, zoom: 1, spinSpeed: 0, hbonds: [[18, 622], [17, 624], [50, 591], [48, 592], [47, 594], [80, 561], [81, 559], [83, 558], [111, 530], [113, 529], [145, 499], [146, 497], [148, 496], [178, 469], [179, 467], [181, 466], [212, 435], [211, 437], [241, 406], [243, 405], [275, 372], [273, 373], [272, 375], [306, 337], [305, 339]]});
</script>

**Figura 6. Doble hebra de ADN**