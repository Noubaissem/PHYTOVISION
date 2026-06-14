import ApiService from '../services/ApiService';

const MOCK_DATA = [
  {
    id: 1,
    date: "2025-06-12",
    maladie: "Virus de la Strie",
    severite: "Elevee",
    action: "Traitement curatif",
    confiance: 92,
    zone: "Centre",
    modeleRetenu: "CNN",
    naiveBayes: {
      maladie: "Sain",
      confiance: 74,
      precision: 0.68,
      rappel: 0.61,
      f1Score: 0.64,
      auc: 0.71,
      inferenceMs: 12,
      fauxPositifs: 11,
      fauxNegatifs: 18
    },
    cnn: {
      maladie: "Virus de la Strie",
      confiance: 92,
      precision: 0.93,
      rappel: 0.91,
      f1Score: 0.92,
      auc: 0.96,
      inferenceMs: 48,
      fauxPositifs: 4,
      fauxNegatifs: 3
    },
    clustering: {
      cluster: "Stade intermediaire",
      intervention: "Traitement curatif",
      silhouette: 0.58
    }
  },
  {
    id: 2,
    date: "2025-06-11",
    maladie: "Sain",
    severite: "-",
    action: "Surveillance",
    confiance: 97,
    zone: "Ouest",
    modeleRetenu: "CNN",
    naiveBayes: {
      maladie: "Brulure Foliaire",
      confiance: 69,
      precision: 0.68,
      rappel: 0.61,
      f1Score: 0.64,
      auc: 0.71,
      inferenceMs: 11,
      fauxPositifs: 11,
      fauxNegatifs: 18
    },
    cnn: {
      maladie: "Sain",
      confiance: 97,
      precision: 0.94,
      rappel: 0.93,
      f1Score: 0.94,
      auc: 0.97,
      inferenceMs: 45,
      fauxPositifs: 3,
      fauxNegatifs: 2
    },
    clustering: {
      cluster: "Feuille saine",
      intervention: "Surveillance",
      silhouette: 0.62
    }
  },
  {
    id: 3,
    date: "2025-06-11",
    maladie: "Tache Grise",
    severite: "Moyenne",
    action: "Traitement preventif",
    confiance: 84,
    zone: "Nord",
    modeleRetenu: "CNN",
    naiveBayes: {
      maladie: "Tache Grise",
      confiance: 58,
      precision: 0.66,
      rappel: 0.59,
      f1Score: 0.62,
      auc: 0.69,
      inferenceMs: 13,
      fauxPositifs: 13,
      fauxNegatifs: 20
    },
    cnn: {
      maladie: "Tache Grise",
      confiance: 84,
      precision: 0.9,
      rappel: 0.87,
      f1Score: 0.88,
      auc: 0.93,
      inferenceMs: 51,
      fauxPositifs: 5,
      fauxNegatifs: 6
    },
    clustering: {
      cluster: "Stade debutant",
      intervention: "Traitement preventif",
      silhouette: 0.54
    }
  },
  {
    id: 4,
    date: "2025-06-10",
    maladie: "Brulure Foliaire",
    severite: "Elevee",
    action: "Elimination foyer",
    confiance: 89,
    zone: "Centre",
    modeleRetenu: "CNN",
    naiveBayes: {
      maladie: "Sain",
      confiance: 63,
      precision: 0.68,
      rappel: 0.61,
      f1Score: 0.64,
      auc: 0.71,
      inferenceMs: 12,
      fauxPositifs: 11,
      fauxNegatifs: 18
    },
    cnn: {
      maladie: "Brulure Foliaire",
      confiance: 89,
      precision: 0.91,
      rappel: 0.89,
      f1Score: 0.9,
      auc: 0.94,
      inferenceMs: 49,
      fauxPositifs: 5,
      fauxNegatifs: 4
    },
    clustering: {
      cluster: "Stade avance",
      intervention: "Elimination foyer",
      silhouette: 0.6
    }
  },
  {
    id: 5,
    date: "2025-06-10",
    maladie: "Virus de la Strie",
    severite: "Faible",
    action: "Surveillance",
    confiance: 76,
    zone: "Extreme-Nord",
    modeleRetenu: "CNN",
    naiveBayes: {
      maladie: "Tache Grise",
      confiance: 71,
      precision: 0.65,
      rappel: 0.58,
      f1Score: 0.61,
      auc: 0.68,
      inferenceMs: 13,
      fauxPositifs: 14,
      fauxNegatifs: 21
    },
    cnn: {
      maladie: "Virus de la Strie",
      confiance: 76,
      precision: 0.86,
      rappel: 0.82,
      f1Score: 0.84,
      auc: 0.9,
      inferenceMs: 52,
      fauxPositifs: 7,
      fauxNegatifs: 8
    },
    clustering: {
      cluster: "Stade debutant",
      intervention: "Surveillance",
      silhouette: 0.51
    }
  }
];

function normalizeDiagnostic(diagnostic) {
  const cnn = diagnostic.cnn || {
    maladie: diagnostic.maladie,
    confiance: diagnostic.confiance,
    precision: diagnostic.precisionCnn,
    rappel: diagnostic.rappelCnn,
    f1Score: diagnostic.f1Cnn,
    auc: diagnostic.aucCnn,
    inferenceMs: diagnostic.inferenceCnnMs,
    fauxPositifs: diagnostic.fauxPositifsCnn,
    fauxNegatifs: diagnostic.fauxNegatifsCnn
  };

  const naiveBayes = diagnostic.naiveBayes || {
    maladie: diagnostic.maladieNaiveBayes || diagnostic.predictionNb || "Non fourni",
    confiance: diagnostic.confianceNaiveBayes || diagnostic.confianceNb || "-",
    precision: diagnostic.precisionNb,
    rappel: diagnostic.rappelNb,
    f1Score: diagnostic.f1Nb,
    auc: diagnostic.aucNb,
    inferenceMs: diagnostic.inferenceNbMs,
    fauxPositifs: diagnostic.fauxPositifsNb,
    fauxNegatifs: diagnostic.fauxNegatifsNb
  };

  return {
    ...diagnostic,
    modeleRetenu: diagnostic.modeleRetenu || diagnostic.modele_retenu || "CNN",
    cnn,
    naiveBayes,
    clustering: diagnostic.clustering || {
      cluster: diagnostic.cluster || "Non fourni",
      intervention: diagnostic.intervention || diagnostic.action,
      silhouette: diagnostic.silhouette || "-"
    }
  };
}

const HistoriqueController = {
  load: async (setData, setLoading, setError) => {
    setLoading(true);
    if (setError) setError(null);
    try {
      const data = await ApiService.getDiagnostics();
      setData(Array.isArray(data) ? data.map(normalizeDiagnostic) : []);
    } catch (err) {
      console.error(err);
      if (setError) {
        setError("Backend indisponible. Donnees de demonstration affichees.");
      }
      setData(MOCK_DATA);
    } finally {
      setLoading(false);
    }
  },

  filter: (data, query) => {
    if (!query) return data;
    const term = query.toLowerCase();
    return data.filter(d =>
      [d.maladie, d.zone, d.severite, d.action, d.modeleRetenu]
        .some(value => String(value || "").toLowerCase().includes(term))
    );
  }
};

export default HistoriqueController;
