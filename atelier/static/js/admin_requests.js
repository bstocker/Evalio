/* Demande d'exercices : des documents choisis en plusieurs fois.

   Un champ fichier remplace sa selection a chaque ouverture de la boite de
   dialogue : choisir un second document ferait disparaitre le premier. On
   cumule donc les choix dans un DataTransfer, que le champ reprend a son
   compte, et la liste affichee permet d'en retirer un. Sans DataTransfer
   (navigateur ancien), le champ garde son comportement natif : plusieurs
   fichiers d'un coup, au Ctrl+clic. */
(function () {
  "use strict";

  var input = document.querySelector("input[name=documents]");
  var list = document.getElementById("doc-list");
  if (!input || !list) return;

  var kept;
  try { kept = new DataTransfer(); } catch (err) { return; }

  var max = parseInt(input.getAttribute("data-max-files"), 10) || 10;

  function size(bytes) {
    if (bytes < 1024) return bytes + " o";
    if (bytes < 1024 * 1024) return Math.round(bytes / 1024) + " Ko";
    return (bytes / 1024 / 1024).toFixed(1).replace(".", ",") + " Mo";
  }

  function render() {
    input.files = kept.files;
    list.textContent = "";
    Array.prototype.forEach.call(kept.files, function (file, index) {
      var item = document.createElement("li");
      var name = document.createElement("span");
      name.className = "mono";
      name.textContent = file.name;
      var meta = document.createElement("span");
      meta.className = "muted";
      meta.textContent = " · " + size(file.size) + " ";
      var remove = document.createElement("button");
      remove.type = "button";
      remove.className = "ghost danger-text";
      remove.textContent = "Retirer";
      remove.setAttribute("aria-label", "Retirer " + file.name);
      remove.addEventListener("click", function () {
        kept.items.remove(index);
        render();
      });
      item.appendChild(name);
      item.appendChild(meta);
      item.appendChild(remove);
      list.appendChild(item);
    });
    list.hidden = kept.files.length === 0;
  }

  input.addEventListener("change", function () {
    // input.files est deja la nouvelle selection : on l'ajoute a l'ancienne,
    // sans doublon (meme nom, meme taille).
    Array.prototype.forEach.call(input.files, function (file) {
      var twin = Array.prototype.some.call(kept.files, function (f) {
        return f.name === file.name && f.size === file.size;
      });
      if (!twin && kept.files.length < max) kept.items.add(file);
    });
    render();
  });

  render();
})();
