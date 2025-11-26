import React from "react";

function FeatureCard({ title, description, icon }: { title: string; description: string; icon: React.ReactNode }) {
  return (
    <div className="p-6 rounded-lg border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm">
      <div className="flex items-start gap-4">
        <div className="w-12 h-12 rounded-md bg-emerald-50 dark:bg-emerald-900 flex items-center justify-center text-emerald-600">
          {icon}
        </div>
        <div>
          <h3 className="font-semibold text-lg">{title}</h3>
          <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function Features() {
  return (
    <section id="features" className="mt-12">
      <h2 className="text-2xl font-bold mb-6">How Chokho-AI helps</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <FeatureCard
          title="Smart Detection"
          description="Detect litter, crowd density and hazards from images and video using our trained models."
          icon={<svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 7v4a1 1 0 001 1h3l3 3v-3h6a1 1 0 001-1V7"/></svg>}
        />

        <FeatureCard
          title="Automated Cleanup Plans"
          description="Turn detections into prioritized tasks, route volunteers, and track progress over time."
          icon={<svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7 16h10M7 4h10v4H7z"/></svg>}
        />

        <FeatureCard
          title="Community Reporting"
          description="Enable visitors and volunteers to report issues, attach photos, and receive updates."
          icon={<svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 8h10M7 12h4m1 8a9 9 0 110-18 9 9 0 010 18z"/></svg>}
        />
      </div>
    </section>
  );
}
