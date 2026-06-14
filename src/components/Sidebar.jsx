import { useNavigate, useLocation } from 'react-router-dom';
import Icon from './Icon';
import Logo from './Logo';

const navItems = [
  { path: "/", icon: "leaf", label: "Analyse" },
  { path: "/historique", icon: "history", label: "Historique" },
  { path: "/epidemiologie", icon: "map", label: "Epidemiologie" },
];

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <aside className="w-20 bg-card border-r border-border flex flex-col items-center py-5 gap-7 min-h-screen shadow-sm">
      <button
        onClick={() => navigate("/")}
        className="rounded-2xl transition-transform hover:-translate-y-0.5"
        title="PhytoVision"
      >
        <Logo />
      </button>

      <nav className="flex flex-col gap-2">
        {navItems.map(item => {
          const active = location.pathname === item.path;
          return (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              title={item.label}
              className={`w-11 h-11 rounded-2xl flex items-center justify-center transition-all ${
                active
                  ? "bg-primary text-white shadow-md shadow-primary/20"
                  : "text-sub hover:bg-primary/10 hover:text-primary"
              }`}
            >
              <Icon name={item.icon} className="w-5 h-5" />
            </button>
          );
        })}
      </nav>

      <div className="flex-1" />

      <button
        className="w-11 h-11 rounded-2xl flex items-center justify-center text-sub hover:bg-primary/10 hover:text-primary transition-colors"
        title="Parametres"
      >
        <Icon name="settings" className="w-5 h-5" />
      </button>
    </aside>
  );
}

export default Sidebar;
