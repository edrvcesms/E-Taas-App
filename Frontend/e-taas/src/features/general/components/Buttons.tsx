import React from "react";

interface ButtonProps {
  onClick: () => void;
  label: string;
  icon: React.ReactNode;
}

export const Button : React.FC<ButtonProps> = ({ onClick, label, icon }) => {
  return (
    <button 
      onClick={onClick}
      className="w-full border border-pink-200 rounded-lg py-3 px-4 flex items-center justify-between text-pink-500 hover:bg-pink-50 transition cursor-pointer"
    >
      <div className="flex items-center gap-2">
        {icon}
        <span>{label}</span>
      </div>
      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
      </svg>
    </button>
  );
}
