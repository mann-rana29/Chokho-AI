import React from "react";

export default function Hero() {
  return (
    <section className="relative bg-white dark:bg-transparent py-0">
      <header className="flex items-center justify-between mb-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-400 rounded-full flex items-center justify-center text-white font-bold">
            C
          </div>
          <span className="text-lg font-semibold">Chokho-AI</span>
        </div>
        <nav className="space-x-6 text-sm text-slate-600 dark:text-slate-300">
          <a href="#features" className="hover:underline">
            Features
          </a>
          <a href="#learn" className="hover:underline">
            Learn
          </a>
          <a href="#contact" className="hover:underline">
            Contact
          </a>
        </nav>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
        <div>
          <h1 className="text-4xl sm:text-5xl font-extrabold leading-tight">
            Cleaner pilgrimage areas with AI-powered detection and action
          </h1>
          <p className="mt-4 text-lg text-slate-600 dark:text-slate-300 max-w-xl">
            Chokho-AI uses object detection and smart analytics to identify litter, crowding, and
            environmental hazards at pilgrimage sites — helping site managers prioritize cleanup,
            allocate volunteers, and keep sacred places clean.
          </p>

          <div className="mt-8 flex flex-wrap gap-3">
            <a
              href="/upload"
              className="inline-flex items-center px-5 py-3 rounded-md bg-emerald-600 text-white font-medium shadow hover:bg-emerald-500"
            >
              Get Started
            </a>

            <a
              href="#features"
              className="inline-flex items-center px-4 py-3 rounded-md border border-slate-200 dark:border-slate-700 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-900"
            >
              See features
            </a>
          </div>

          <ul className="mt-6 text-sm text-slate-600 dark:text-slate-400 space-y-2">
            <li>
              • Real-time object detection (trash, crowding, hazards)
            </li>
            <li>• Actionable cleanup plans and volunteer routing</li>
            <li>• Reports and community feedback integration</li>
          </ul>
        </div>

        <div className="order-first md:order-last flex items-center justify-center">
          <div className="w-full max-w-md rounded-xl overflow-hidden shadow-lg bg-gradient-to-br from-white to-slate-50 dark:from-slate-900 dark:to-slate-800 p-6">
            <svg
              viewBox="0 0 640 512"
              className="w-full h-56 text-emerald-500"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <rect width="100%" height="100%" rx="12" fill="currentColor" opacity="0.08" />
              <g transform="translate(40,40)">
                <circle cx="120" cy="80" r="64" fill="#34D399" opacity="0.9" />
                <rect x="220" y="30" width="220" height="120" rx="16" fill="#A7F3D0" opacity="0.9" />
                <path d="M40 220h360v24H40z" fill="#10B981" opacity="0.9" />
              </g>
            </svg>

            <div className="mt-4 text-sm text-slate-600 dark:text-slate-300">
              Example model output preview — bounding boxes highlight litter and congested zones so
              teams can respond efficiently.
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
