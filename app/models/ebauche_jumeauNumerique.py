# %%
import numpy as np
import matplotlib.pyplot as plt

# %%
class NeuroneIntegrateAndFire:
    def __init__(self, seuil=1.0, tau=20.0, R=1.0, dt=0.1):
        self.seuil = seuil  # Seuil de déclenchement du potentiel d'action
        self.tau = tau  # Constante de temps
        self.R = R  # Résistance membranaire
        self.dt = dt  # Pas de temps
        self.potentiel_membranaire = 0.0

    def mettre_a_jour(self, courant_entrant):
        dV = (courant_entrant * self.R - self.potentiel_membranaire) * (self.dt / self.tau)
        self.potentiel_membranaire += dV
        if self.potentiel_membranaire >= self.seuil:
            self.potentiel_membranaire = 0.0
            return True
        return False

class NeuroneSEP(NeuroneIntegrateAndFire):
    def __init__(self, seuil=1.0, tau_normal=20.0, tau_demyelin=50.0, tau_severe=100.0, R=1.0, dt=0.1):
        super().__init__(seuil, tau_normal, R, dt)
        self.tau_demyelin = tau_demyelin  # Constante de temps pour les zones démyélinisées
        self.tau_severe = tau_severe  # Constante de temps pour une atteinte sévère
        self.nbSpikes = 0

    def mettre_a_jour(self, courant_entrant, etat_myeline="sain"):
        """
        :param etat_myeline: "sain", "endommage" ou "severe" pour moduler la conduction
        """
        if etat_myeline == "endommage":
            tau = self.tau_demyelin
        elif etat_myeline == "severe":
            tau = self.tau_severe
        else:
            tau = self.tau
        
        dV = (courant_entrant * self.R - self.potentiel_membranaire) * (self.dt / tau)
        self.potentiel_membranaire += dV
        
        if self.potentiel_membranaire >= self.seuil:
            self.potentiel_membranaire = 0.0
            self.nbSpikes += 1
            return True
        return False

# %%
# Simulation avec différents niveaux de démyélinisation
neurone_sain = NeuroneSEP()
neurone_endommage = NeuroneSEP()
neurone_severe = NeuroneSEP()

courant_entrant = 1.5
potentiels_sain = []
potentiels_endommage = []
potentiels_severe = []
spikes_sain = []
spikes_endommage = []
spikes_severe = []
temps = np.arange(0, 100, neurone_sain.dt)

for t in temps:
    neurone_sain.mettre_a_jour(courant_entrant, "sain")
    neurone_endommage.mettre_a_jour(courant_entrant, "endommage")
    neurone_severe.mettre_a_jour(courant_entrant, "severe")
    
    potentiels_sain.append(neurone_sain.potentiel_membranaire)
    potentiels_endommage.append(neurone_endommage.potentiel_membranaire)
    potentiels_severe.append(neurone_severe.potentiel_membranaire)

# %%
# Visualisation
plt.figure(figsize=(10, 5))
plt.plot(temps, potentiels_sain, label="Signal normal (Myéline intacte)", color='#7ead93')
plt.plot(temps, potentiels_endommage, label="Signal ralenti (Myéline endommagée)", color='#f8d7da')
plt.plot(temps, potentiels_severe, label="Signal interrompu (Myéline détruite)", color='#721c24')

# Ajout d'annotations
plt.axhline(y=1.0, color='gray', linestyle='--', label="Seuil de déclenchement")
plt.xlabel("Temps (ms)")
plt.ylabel("Potentiel de membrane")
plt.legend()
plt.title("Impact de la démyélinisation sur la transmission du signal")
plt.savefig("app/static/images/courbes.png", dpi=300)
plt.show()

# %%
echantillons = [neurone_sain.nbSpikes, neurone_endommage.nbSpikes, neurone_severe.nbSpikes]
echantillons

# %%
labels = ['Myéline saine', 'Myéline endommagée', 'Myéline détruite']
# Création du graphique
plt.barh(labels, echantillons, color=['#7ead93', '#f8d7da', '#721c24'] , edgecolor='black')

# Ajouter des labels et un titre
plt.xlabel('Nombre de spikes')
plt.ylabel('Type de neurone')
plt.title('Histogramme des spikes par type de neurone')
plt.tight_layout() 
plt.savefig("app/static/images/histogramme.png")
plt.show()