const checkData = async (): Promise<boolean> => {
  try {
    const files = ["ai.json", "network.json", "services.json", "agents.json"];
    const results = await Promise.all(
      files.map(async (file) => {
        const response = await fetch(`/data/${file}`);
        if (!response.ok) return false; // Si le fichier est inaccessible
        const data = await response.json();
        return Object.keys(data).length > 0; // Vérifie s'il y a du contenu
      })
    );

    return results.every((isFilled) => isFilled); // Retourne `true` si tous les fichiers sont remplis
  } catch (error) {
    console.error("Erreur lors de la vérification des fichiers JSON :", error);
    return false; // Si une erreur survient, considérer que les données ne sont pas complètes
  }
};

export default checkData;
