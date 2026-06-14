import Icon from './Icon';

function Metric({ label, value }) {
  return (
    <div className="bg-white/70 border border-border rounded-xl px-3 py-2">
      <p className="text-[11px] uppercase tracking-wide text-sub">{label}</p>
      <p className="text-sm font-semibold text-ink mt-0.5">{value}</p>
    </div>
  );
}

function pct(value) {
  return typeof value === "number" ? `${Math.round(value * 100)}%` : value;
}

function ModelCard({ title, model, tone, icon }) {
  const toneClass = {
    warning: {
      shell: "border-warning/25 bg-amber-50",
      icon: "bg-white text-warning border-warning/20",
      badge: "bg-warning/10 text-warning border-warning/20",
    },
    success: {
      shell: "border-primary/25 bg-primary/5",
      icon: "bg-white text-primary border-primary/20",
      badge: "bg-primary/10 text-primary border-primary/20",
    },
  }[tone];

  return (
    <div className={`border rounded-2xl p-4 ${toneClass.shell}`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          <span className={`w-10 h-10 rounded-2xl border flex items-center justify-center ${toneClass.icon}`}>
            <Icon name={icon} className="w-5 h-5" />
          </span>
          <div>
            <p className="text-xs uppercase tracking-wide text-sub">{title}</p>
            <h3 className="text-base font-semibold text-ink">{model.modele}</h3>
          </div>
        </div>
        <span className={`text-xs px-2.5 py-1 rounded-full border font-semibold ${toneClass.badge}`}>
          {model.verdict}
        </span>
      </div>

      <div className="mt-4">
        <p className="text-xs text-sub">Prediction</p>
        <p className="text-xl font-semibold text-ink mt-1">{model.maladie}</p>
        <p className="text-xs text-sub mt-1">Confiance: {model.confiance}%</p>
      </div>

      <p className="text-xs text-sub leading-5 mt-3">{model.explication}</p>

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-4">
        <Metric label="Precision" value={pct(model.precision)} />
        <Metric label="Rappel" value={pct(model.rappel)} />
        <Metric label="F1-score" value={pct(model.f1Score)} />
        <Metric label="AUC" value={model.auc} />
        <Metric label="Faux neg." value={model.fauxNegatifs} />
        <Metric label="Temps" value={`${model.inferenceMs} ms`} />
      </div>
    </div>
  );
}

function ResultCards({ result }) {
  if (!result) return null;

  const legacyResult = !result.cnn && !result.naiveBayes;
  const cnn = result.cnn || {
    modele: "CNN",
    maladie: result.maladie,
    confiance: result.confiance,
    verdict: "Modele retenu",
    explication: "Resultat image fourni par le modele principal.",
    fauxNegatifs: "-",
    precision: "-",
    rappel: "-",
    f1Score: "-",
    auc: "-",
    inferenceMs: "-"
  };
  const naiveBayes = result.naiveBayes || {
    modele: "Naif Bayes",
    maladie: "Non fourni",
    confiance: "-",
    verdict: "Baseline absente",
    explication: "Le backend actuel ne renvoie pas encore le resultat Naif Bayes.",
    fauxNegatifs: "-",
    precision: "-",
    rappel: "-",
    f1Score: "-",
    auc: "-",
    inferenceMs: "-"
  };
  const finalDecision = result.decisionFinale || {
    maladie: result.maladie,
    confiance: result.confiance,
    severite: result.severite,
    action: result.action,
    modeleRetenu: "CNN"
  };

  return (
    <div className="flex flex-col gap-4 mt-3">
      {legacyResult && (
        <div className="border border-warning/25 bg-amber-50 rounded-2xl p-4 text-xs text-warning leading-5">
          Le backend renvoie encore un resultat simple. Pour respecter le cahier des charges, il doit renvoyer les blocs naiveBayes, cnn, comparison et clustering.
        </div>
      )}

      <div className="grid grid-cols-1 2xl:grid-cols-2 gap-4">
        <ModelCard
          title="Baseline probabiliste"
          model={naiveBayes}
          tone="warning"
          icon="alert"
        />
        <ModelCard
          title="Modele performant"
          model={cnn}
          tone="success"
          icon="shield"
        />
      </div>

      <div className="border border-primary/25 bg-primary/5 rounded-2xl p-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-wide text-sub">Decision finale IRAD</p>
            <h3 className="text-xl font-semibold text-ink mt-1">{finalDecision.maladie}</h3>
            <p className="text-xs text-sub mt-1">
              Modele retenu: {finalDecision.modeleRetenu} - Confiance: {finalDecision.confiance}%
            </p>
          </div>
          <span className="w-10 h-10 rounded-2xl bg-white border border-primary/20 text-primary flex items-center justify-center">
            <Icon name="check" className="w-5 h-5" />
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-4">
          <Metric label="Severite" value={finalDecision.severite} />
          <Metric label="Action recommandee" value={finalDecision.action} />
        </div>

        {result.comparison && (
          <div className="mt-4 bg-white border border-border rounded-2xl p-3">
            <p className="text-xs font-semibold text-ink">Justification CNN vs Naif Bayes</p>
            <p className="text-xs text-sub leading-5 mt-1">{result.comparison.conclusion}</p>
            <p className="text-xs text-danger leading-5 mt-2">{result.comparison.risqueAgronomique}</p>
          </div>
        )}
      </div>

      {result.clustering && (
        <div className="border border-border bg-white rounded-2xl p-4">
          <div className="flex items-center gap-3">
            <span className="w-10 h-10 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
              <Icon name="activity" className="w-5 h-5" />
            </span>
            <div>
              <p className="text-xs uppercase tracking-wide text-sub">Module B - Clustering non supervise</p>
              <h3 className="text-base font-semibold text-ink">{result.clustering.cluster}</h3>
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-4">
            <Metric label="Methode" value={result.clustering.methode} />
            <Metric label="Intervention" value={result.clustering.intervention} />
            <Metric label="Silhouette" value={result.clustering.silhouette} />
          </div>
        </div>
      )}
    </div>
  );
}

export default ResultCards;
