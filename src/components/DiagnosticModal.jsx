import Icon from './Icon';

function pct(value) {
  return typeof value === "number" ? `${Math.round(value * 100)}%` : value || "-";
}

function Metric({ label, value }) {
  return (
    <div className="bg-white/70 border border-border rounded-xl px-3 py-2">
      <p className="text-[11px] uppercase tracking-wide text-sub">{label}</p>
      <p className="text-sm font-semibold text-ink mt-0.5">{value}</p>
    </div>
  );
}

function ModelPanel({ title, model, tone, icon }) {
  const styles = {
    warning: "bg-amber-50 border-warning/20 text-warning",
    success: "bg-primary/5 border-primary/20 text-primary",
  }[tone];

  return (
    <div className={`border rounded-2xl p-3 ${styles}`}>
      <div className="flex items-center gap-2 mb-3">
        <span className="w-8 h-8 rounded-xl bg-white border border-white flex items-center justify-center">
          <Icon name={icon} className="w-4 h-4" />
        </span>
        <div>
          <p className="text-[11px] uppercase tracking-wide text-sub">{title}</p>
          <p className="text-sm font-semibold text-ink">{model?.maladie || "Non fourni"}</p>
        </div>
      </div>
      <div className="grid grid-cols-2 gap-2">
        <Metric label="Confiance" value={`${model?.confiance ?? "-"}%`} />
        <Metric label="F1-score" value={pct(model?.f1Score)} />
        <Metric label="AUC" value={model?.auc ?? "-"} />
        <Metric label="Faux neg." value={model?.fauxNegatifs ?? "-"} />
      </div>
    </div>
  );
}

function DiagnosticModal({ diagnostic, onClose }) {
  if (!diagnostic) return null;

  const severiteColor = {
    Elevee: { text: "text-danger", bg: "bg-red-50", border: "border-danger/20" },
    Moyenne: { text: "text-warning", bg: "bg-amber-50", border: "border-warning/20" },
    Faible: { text: "text-info", bg: "bg-blue-50", border: "border-info/20" },
    "-": { text: "text-primary", bg: "bg-primary/5", border: "border-primary/20" },
  };

  const sev = severiteColor[diagnostic.severite] || severiteColor["-"];
  const disagreement = diagnostic.naiveBayes?.maladie && diagnostic.naiveBayes.maladie !== diagnostic.cnn?.maladie;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/35 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-card border border-border rounded-2xl w-full max-w-3xl max-h-[90vh] overflow-hidden shadow-2xl shadow-slate-900/10"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between px-5 py-4 border-b border-border">
          <div>
            <h2 className="text-base font-semibold text-ink">Details du diagnostic</h2>
            <p className="text-xs text-sub mt-0.5">
              #{String(diagnostic.id).padStart(3, "0")} - {diagnostic.date} - {diagnostic.zone}
            </p>
          </div>
          <button
            onClick={onClose}
            className="w-9 h-9 rounded-xl bg-primary/5 border border-border flex items-center justify-center text-sub hover:text-primary hover:border-primary/40 transition-colors"
          >
            <Icon name="close" className="w-4 h-4" />
          </button>
        </div>

        <div className="p-5 flex flex-col gap-4 overflow-y-auto max-h-[calc(90vh-9rem)]">
          <div className="grid grid-cols-1 lg:grid-cols-[1fr_1.5fr] gap-4">
            <div className="bg-primary/5 border border-primary/15 rounded-2xl min-h-48 flex items-center justify-center">
              <div className="text-center">
                <div className="w-14 h-14 rounded-2xl bg-white border border-border flex items-center justify-center mx-auto text-primary shadow-sm">
                  <Icon name="leaf" className="w-7 h-7" />
                </div>
                <p className="text-xs text-sub mt-2">{diagnostic.image || "Image du diagnostic"}</p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="bg-primary/5 border border-primary/20 rounded-2xl p-3">
                <p className="text-xs text-sub uppercase tracking-wide mb-1">Decision finale</p>
                <p className="text-lg font-semibold text-primary">{diagnostic.maladie}</p>
                <p className="text-xs text-sub mt-1">Modele retenu: {diagnostic.modeleRetenu || "CNN"}</p>
              </div>

              <div className="bg-white border border-border rounded-2xl p-3">
                <p className="text-xs text-sub uppercase tracking-wide mb-1">Confiance finale</p>
                <p className="text-lg font-semibold text-ink">{diagnostic.confiance}%</p>
                <div className="h-1.5 bg-border rounded-full mt-2">
                  <div
                    className="h-full bg-primary rounded-full transition-all"
                    style={{ width: `${Number(diagnostic.confiance) || 0}%` }}
                  />
                </div>
              </div>

              <div className={`border rounded-2xl p-3 ${sev.bg} ${sev.border}`}>
                <p className="text-xs text-sub uppercase tracking-wide mb-1">Niveau de severite</p>
                <p className={`text-sm font-semibold flex items-center gap-2 ${sev.text}`}>
                  <Icon name="alert" className="w-4 h-4" />
                  {diagnostic.severite}
                </p>
              </div>

              <div className="bg-white border border-border rounded-2xl p-3">
                <p className="text-xs text-sub uppercase tracking-wide mb-1">Action recommandee</p>
                <p className="text-sm font-semibold text-ink">{diagnostic.action}</p>
              </div>
            </div>
          </div>

          <div className={`border rounded-2xl p-4 ${disagreement ? "bg-amber-50 border-warning/20" : "bg-primary/5 border-primary/20"}`}>
            <div className="flex items-start gap-3">
              <span className={`w-10 h-10 rounded-2xl bg-white border flex items-center justify-center ${disagreement ? "text-warning border-warning/20" : "text-primary border-primary/20"}`}>
                <Icon name={disagreement ? "alert" : "check"} className="w-5 h-5" />
              </span>
              <div>
                <p className="text-sm font-semibold text-ink">
                  {disagreement ? "Desaccord Naif Bayes / CNN" : "Accord Naif Bayes / CNN"}
                </p>
                <p className="text-xs text-sub leading-5 mt-1">
                  {disagreement
                    ? "Ce cas illustre les limites de la baseline probabiliste. La decision IRAD garde le CNN car il analyse les motifs visuels et reduit les faux negatifs."
                    : "Les deux modeles convergent, mais la decision finale reste basee sur le CNN pour conserver le protocole du projet."}
                </p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
            <ModelPanel title="Baseline Naif Bayes" model={diagnostic.naiveBayes} tone="warning" icon="alert" />
            <ModelPanel title="Modele CNN" model={diagnostic.cnn} tone="success" icon="shield" />
          </div>

          <div className="bg-white border border-border rounded-2xl p-4">
            <div className="flex items-center gap-3">
              <span className="w-10 h-10 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
                <Icon name="activity" className="w-5 h-5" />
              </span>
              <div>
                <p className="text-xs uppercase tracking-wide text-sub">Module B - Clustering</p>
                <p className="text-sm font-semibold text-ink">{diagnostic.clustering?.cluster || "Non fourni"}</p>
              </div>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-4">
              <Metric label="Intervention" value={diagnostic.clustering?.intervention || diagnostic.action} />
              <Metric label="Silhouette" value={diagnostic.clustering?.silhouette || "-"} />
              <Metric label="Culture" value="Mais" />
            </div>
          </div>
        </div>

        <div className="px-5 py-4 border-t border-border flex justify-end">
          <button
            onClick={onClose}
            className="bg-primary text-white font-medium text-sm px-5 py-2.5 rounded-xl hover:bg-green-700 transition-colors"
          >
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
}

export default DiagnosticModal;
