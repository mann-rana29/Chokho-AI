import React from "react";

export default function Footer() {
  return (
    <footer className="mt-16 border-t border-slate-100 dark:border-slate-800 bg-transparent">
      <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-emerald-600 rounded-full flex items-center justify-center text-white font-bold">C</div>
          <div>
            <div className="font-semibold">Chokho-AI</div>
            <div className="text-sm text-slate-600 dark:text-slate-400">AI for cleaner pilgrimage areas</div>
          </div>
        </div>

        <nav className="flex gap-4 text-sm text-slate-600 dark:text-slate-400">
          <a href="#" className="hover:underline">
            Privacy
          </a>
          <a href="#" className="hover:underline">
            Terms
          </a>
          <a href="#contact" className="hover:underline">
            Contact
          </a>
        </nav>
      </div>
    </footer>
  );
}
