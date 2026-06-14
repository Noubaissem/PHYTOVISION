import Icon from './Icon';

function EmptyState({ icon = "file", title, subtitle, action, onAction }) {
  return (
    <div className="bg-card border border-border rounded-2xl shadow-sm flex flex-col items-center justify-center py-16 px-6 gap-3">
      <span className="w-14 h-14 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
        <Icon name={icon} className="w-7 h-7" />
      </span>
      <p className="text-ink font-semibold text-sm">{title}</p>
      {subtitle && (
        <p className="text-sub text-xs text-center max-w-xs leading-5">{subtitle}</p>
      )}
      {action && onAction && (
        <button
          onClick={onAction}
          className="mt-2 bg-primary text-white text-xs px-4 py-2 rounded-xl hover:bg-green-700 transition-colors"
        >
          {action}
        </button>
      )}
    </div>
  );
}

export default EmptyState;
