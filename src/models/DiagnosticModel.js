class DiagnosticModel {
  constructor(data) {
    this.id              = data.id;
    this.image           = data.image;
    this.culture_id      = data.culture_id;
    this.maladie_id      = data.maladie_id;
    this.confiance       = data.confiance;
    this.severite_id     = data.severite_id;
    this.zone_id         = data.zone_id;
    this.action_id       = data.action_id;
    this.date_diagnostic = data.date_diagnostic;
  }
}

export default DiagnosticModel;