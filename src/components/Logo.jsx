function Logo({ className = "w-12 h-12" }) {
  return (
    <div
      className={`${className} rounded-2xl bg-white border border-primary/20 shadow-md shadow-primary/15 flex items-center justify-center`}
      aria-label="PhytoVision"
    >
      <svg
        viewBox="0 0 48 48"
        fill="none"
        className="w-9 h-9"
        aria-hidden="true"
      >
        <rect x="6" y="6" width="36" height="36" rx="14" fill="#15803D" />
        <path
          d="M15 28.5C15 20.5 22.2 14.2 34.5 13.5C33.8 25.4 27.5 33 19.7 33C17.8 33 16.2 32.5 15 31.6V28.5Z"
          fill="#FFFFFF"
        />
        <path
          d="M15 34C19.2 26.8 24.6 21.9 33.8 14.1"
          stroke="#BBF7D0"
          strokeWidth="2.2"
          strokeLinecap="round"
        />
        <path
          d="M14 35V22"
          stroke="#FFFFFF"
          strokeWidth="2.4"
          strokeLinecap="round"
        />
        <path
          d="M13 22.5C10.8 21.7 9.4 20 9.4 17.8C12.8 17.8 15 19.7 15 22.5"
          fill="#BBF7D0"
        />
      </svg>
    </div>
  );
}

export default Logo;
