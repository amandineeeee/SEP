// ----- Récupérer et afficher les patients selon les filtres -----

function fetchPatients() {
    // Récupérer les valeurs des filtres
    const nom = document.getElementById('nom').value;
    const prenom = document.getElementById('prenom').value;
    const age = document.getElementById('age').value;
    const sexe = document.querySelector('input[name="sexe"]:checked')?.value || '';

    // Construction de l'URL pour l'appel AJAX avec les paramètres contenus dans les filtres
    const url = `/filter_patients?nom=${nom}&prenom=${prenom}&age=${age}&sexe=${sexe}`;

    // Envoi de la requête AJAX avec la méthode fetch
    fetch(url)
        // Convertir la réponse en JSON
        .then(response => response.json())
        .then(data => {
            // Récupère l'élément <tbody> et vide la table
            const tableBody = document.querySelector('#patients_table tbody');
            tableBody.innerHTML = '';
            
            // Si des patients sont trouvés 
            if (data.length > 0) {
                // Pour chaque patient récupérer les données
                // Changer le format si nécessaire
                // Créer la ligne a ajouter à la table et l'ajouter
                data.forEach(patient => {
                    const mode_de_vie = patient.mode_vie || '';
                    let date_naissance = patient.date_de_naissance || '';                
                    if (date_naissance != '') {
                        date_naissance=date_naissance.split(' ')[1]+' '+date_naissance.split(' ')[2] +' '+date_naissance.split(' ')[3];
                    }
                        
                    const row = `
                        <tr>
                            <td>${patient.id_patient}</td>
                            <td>${patient.nom}</td>
                            <td>${patient.prenom}</td>
                            <td>${date_naissance}</td>
                            <td>${patient.age}</td>
                            <td>${patient.sexe}</td>
                            <td>${mode_de_vie}</td>
                            <td>
                                <a href="/view_patient/${ patient.id_patient }" title="Consulter">
                                    <i class="fas fa-eye" style="color: #697ab4;"></i>
                                </a>
                                <a href="/edit_patient/${patient.id_patient}" title="Modifier">
                                    <i class="fas fa-edit" style="color: #7ead93;"></i>
                                </a>
                                <a href="/delete_patient/${patient.id_patient}" title="Supprimer" onclick="return confirm('Voulez-vous vraiment supprimer ce patient ?');">
                                    <i class="fas fa-trash-alt" style="color: #ca3838;"></i>
                                </a>
                            </td>
                        </tr>`;
                    tableBody.innerHTML += row;
                });
            // Si aucun patient n'est trouvé afficher un message 
            } else {
                tableBody.innerHTML = `<tr><td colspan="7">Aucun patient trouvé.</td></tr>`;
            }
        })
        .catch(error => console.error('Erreur lors du chargement des patients:', error));
}

// Déclenche la recherche à chaque changement dans les filtres
document.querySelectorAll('.labelName, input[name="sexe"]').forEach(input => {
    input.addEventListener('input', fetchPatients);
});

// Affiche les patients dès le chargement de la page
document.addEventListener('DOMContentLoaded', fetchPatients);
