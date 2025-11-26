import React, { useEffect, useState } from "react";

export default function LoadingSkeletonWithProgress() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) return prev;
        return prev + Math.random() * 20;
      });
    }, 300);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      {/* Progress bar */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <p className="text-sm text-slate-600 dark:text-slate-400 flex items-center gap-2">
            <span className="inline-block w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
            Processing your image...
          </p>
          <p className="text-xs text-slate-500 dark:text-slate-500">
            {Math.round(progress)}%
          </p>
        </div>
        <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 overflow-hidden">
          <div
            className="bg-emerald-500 h-full transition-all duration-300 ease-out rounded-full"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>

      {/* Animated skeleton */}
      <div className="space-y-6 animate-pulse">
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

        {/* Status messages skeleton */}
        <div className="space-y-2">
          {[1, 2].map((i) => (
            <div key={i} className="h-3 bg-slate-200 dark:bg-slate-700 rounded w-full"></div>
          ))}
        </div>
      </div>
    </div>
  );
}
