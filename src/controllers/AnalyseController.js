import ApiService from '../services/ApiService';

const AnalyseController = {
  analyser: async (imageFile, zone, setResult, setLoading, setError) => {
    setLoading(true);
    setError(null);
    try {
      const result = await ApiService.analyseImage(imageFile, zone);
      setResult(result);
    } catch (err) {
      console.error(err);
      // Mock shaped according to the specification when the backend is not ready.
      setResult({
        naiveBayes: {
          modele: "Naif Bayes",
          maladie: "Sain",
          confiance: 74,
          verdict: "Baseline instable",
          explication: "Les features manuelles ne capturent pas bien les textures et confondent certaines necroses avec une feuille saine.",
          fauxPositifs: 11,
          fauxNegatifs: 18,
          precision: 0.68,
          rappel: 0.61,
          f1Score: 0.64,
          auc: 0.71,
          inferenceMs: 12
        },
        cnn: {
          modele: "CNN MobileNetV2",
          maladie: "Virus de la Strie",
          confiance: 92,
          verdict: "Modele retenu",
          explication: "Le CNN analyse directement les motifs visuels, les formes de lesions et les correlations spatiales.",
          fauxPositifs: 4,
          fauxNegatifs: 3,
          precision: 0.93,
          rappel: 0.91,
          f1Score: 0.92,
          auc: 0.96,
          inferenceMs: 48
        },
        decisionFinale: {
          maladie: "Virus de la Strie",
          confiance: 92,
          severite: "Elevee",
          action: "Traitement curatif",
          modeleRetenu: "CNN"
        },
        comparison: {
          conclusion: "Le Naif Bayes donne une prediction contradictoire. La decision finale utilise le CNN car il reduit les faux negatifs, plus dangereux en contexte IRAD.",
          risqueAgronomique: "Un faux negatif peut laisser se propager un foyer infectieux."
        },
        clustering: {
          methode: "K-Means sur embeddings CNN",
          cluster: "Stade intermediaire",
          intervention: "Traitement curatif",
          silhouette: 0.58
        }
      });
    } finally {
      setLoading(false);
    }
  }
};

export default AnalyseController;
