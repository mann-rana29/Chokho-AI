import React from "react";

export default function LoadingSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      {/* Header skeleton */}
      <div className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-lg p-4">
        <div className="h-5 bg-emerald-200 dark:bg-emerald-700 rounded w-3/4"></div>
      </div>

      {/* Detection cards skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-4"
          >
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-2/3 mb-3"></div>
            <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded w-1/2 mb-2"></div>
            <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded w-3/4"></div>
          </div>
        ))}
      </div>

      {/* Timestamp skeleton */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg p-4">
        <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/2"></div>
      </div>

      {/* Button skeleton */}
      <div className="w-full h-11 bg-slate-200 dark:bg-slate-700 rounded-md"></div>
    </div>
  );
}
