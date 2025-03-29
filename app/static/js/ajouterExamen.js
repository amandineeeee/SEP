document.addEventListener("DOMContentLoaded", function () {

    // ----- Ajout dynamique d'examen -----

    const addButton = document.getElementById("add-examen");
    const examensList = document.getElementById("examens-list");

    let c = 1;
    // Ajout d'un événement clic au bouton pour ajouter un examen
    addButton.addEventListener("click", function () {
        const examenDiv = document.createElement("div");
        examenDiv.classList.add("examen-item");

        // Champs du nouvel examen
        examenDiv.innerHTML = `
            <input type="text" name="type_examen[]" placeholder="Type d'examen" required>
            <input type="date" name="date_examen[]" required>
            <textarea name="resultat_examen[]" placeholder="Résultat de l'examen" required></textarea>
            <input type="file" name="document_scanne_${c}[]" accept=".pdf,.jpg,.jpeg,.png">
            <button type="button" id="remove-exam" class="btn-minus">Supprimer cet examen</button>
        `;

        c++;

        // Ajout du nouvel examen à la liste
        examensList.appendChild(examenDiv);

        // Bouton pour supprimer l'examen ajouté
        examenDiv.querySelector(".btn-minus").addEventListener("click", function () {
            examenDiv.remove();
        });
    });

    // ----- Ajout dynamique d'anciens traitements -----

    const addTreatmentButton = document.getElementById("add-traitement");
    const treatmentList = document.getElementById("traitements-list");
    // Ajout d'un événement clic au bouton pour ajouter un traitement
    addTreatmentButton.addEventListener("click", function () {
        const traitementDiv = document.createElement("div");
        traitementDiv.classList.add("traitement-item");

        // Champs du nouveeau traitement
        traitementDiv.innerHTML = `
            <input type="text" name="nom_traitement[]" placeholder="Nom du traitement">
            <input type="text" name="frequence_traitement[]" placeholder="dosage / fréquence">
            <textarea name="informations_traitement[]" placeholder="Informations complémentaires"></textarea>
            <button type="button" id="remove-traitement" class="btn-minus">Supprimer ce traitement</button>
        `;

        // Ajout d'un nouveau traitement à la liste
        treatmentList.appendChild(traitementDiv);

        // Bouton pour supprimer le traitement ajouté
        traitementDiv.querySelector(".btn-minus").addEventListener("click", function () {
            traitementDiv.remove();
        });
    });

    // ----- Ajout dynamique de traitements actuels -----

    const addTreatmentActualButton = document.getElementById("add-traitement-actuel");
    const treatmentActualList = document.getElementById("traitements-actuels-list");

    // Ajout d'un événement clic au bouton pour ajouter un traitement
    addTreatmentActualButton.addEventListener("click", function () {
        const traitementActuelDiv = document.createElement("div");
        traitementActuelDiv.classList.add("traitement-actuel-item");

        // Champs du nouveau traitement
        traitementActuelDiv.innerHTML = `
            <input type="text" name="nom_traitement_actuel[]" placeholder="Nom du traitement">
            <input type="text" name="frequence_traitement_actuel[]" placeholder="dosage / fréquence">
            <textarea name="informations_traitement_actuel[]" placeholder="Informations complémentaires"></textarea>
            <button type="button" id="remove-traitement-actuel" class="btn-minus">Supprimer ce traitement</button>
        `;

        // Ajout d'un nouveau traitement à la liste
        treatmentActualList.appendChild(traitementActuelDiv);

        // Bouton pour supprimer l'examen ajouté
        traitementActuelDiv.querySelector(".btn-minus").addEventListener("click", function () {
            traitementActuelDiv.remove();
        });
    });

    // ----- Ajout dynamique de consultations -----

    const addConsultationButton = document.getElementById("add-consultation");
    const consultationsList = document.getElementById("consultations-list");

    // Ajout d'un événement clic au bouton pour ajouter une consultation
    addConsultationButton.addEventListener("click", function () {
        const consultationsDiv = document.createElement("div");
        consultationsDiv.classList.add("consultation-item");

        // Champs de la nouvelle consultation
        consultationsDiv.innerHTML = `
            <input type="date" name="derniere_consultation[]">
            <br>
            <textarea name="plan_soins[]" rows="3" placeholder="Plan de soins"></textarea>
            <button type="button" id="remove-consultation" class="btn-minus">Supprimer cette consultation</button>
        `;

        // Ajout d'une nouvelle consultation à la liste
        consultationsList.appendChild(consultationsDiv);

        // Bouton pour supprimer la consultation ajoutée
        consultationsDiv.querySelector(".btn-minus").addEventListener("click", function () {
            consultationsDiv.remove();
        });
    });
});   