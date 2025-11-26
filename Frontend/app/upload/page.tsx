"use client";

import React, { useState } from "react";
import Link from "next/link";
import ImageUpload from "../../components/ImageUpload";

export default function UploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
//   const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);

  const handleImageUpload = async (file: File, preview: string) => {
    setSelectedFile(file);
    setImagePreview(preview);
    // setAnalysisResult(null);
    
    // Start analysis after image is uploaded
    await analyzeImage(file);
  };

  const analyzeImage = async (file: File) => {
    setIsLoading(true);
    try {
      // Prepare FormData for backend upload
      const formData = new FormData();
      formData.append("image", file);

      // TODO: Replace with your actual backend API endpoint
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const data = await response.json();
      
      // Format the response to match our UI structure
    //   setAnalysisResult({
    //     detections: data.detections || [],
    //     timestamp: new Date().toISOString(),
    //     imageName: file.name,
    //   });
    } catch (error) {
      console.error("Error analyzing image:", error);
      // Show mock result for demo purposes
    //   setAnalysisResult({
    //     detections: [
    //       { type: "litter", confidence: 0.92, count: 12 },
    //       { type: "crowd", confidence: 0.87, count: 5 },
    //       { type: "hazard", confidence: 0.78, count: 2 },
    //     ],
    //     timestamp: new Date().toISOString(),
    //     imageName: file.name,
    //   });
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setImagePreview(null);
    // setAnalysisResult(null);
  };

  return (
    <main className="min-h-screen bg-zinc-50 dark:bg-black text-slate-900 dark:text-slate-100">
      <div className="max-w-4xl mx-auto px-6 py-8">
        {/* Header with navigation */}
        <div className="mb-8">
          <Link href="/" className="inline-flex items-center gap-2 text-emerald-600 hover:text-emerald-500 mb-6">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back to home
          </Link>

          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-400 rounded-full flex items-center justify-center text-white font-bold">
              C
            </div>
            <h1 className="text-3xl font-bold">Chokho-AI Analyzer</h1>
          </div>
          <p className="text-slate-600 dark:text-slate-400">
            Upload an image to detect litter, crowds, and hazards using AI
          </p>
        </div>

        {/* Main content grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload section */}
          <div className="bg-white dark:bg-slate-900 rounded-lg p-6 shadow-sm border border-slate-100 dark:border-slate-800">
            <h2 className="text-xl font-bold mb-6">Upload Image</h2>
            <ImageUpload onImageUpload={handleImageUpload} isLoading={isLoading} />
          </div>

          {/* Preview and results section */}
          {/* <div className="bg-white dark:bg-slate-900 rounded-lg p-6 shadow-sm border border-slate-100 dark:border-slate-800">
            <h2 className="text-xl font-bold mb-6">Analysis Results</h2>
            {imagePreview && (
              <div className="mb-6">
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-3">Preview:</p>
                <img
                  src={imagePreview}
                  alt="Upload preview"
                  className="w-full h-64 object-cover rounded-lg border border-slate-200 dark:border-slate-700"
                />
              </div>
            )}
            <AnalysisResult result={analysisResult} isLoading={isLoading} onReset={handleReset} />
          </div> */}
        </div>

        {/* Info cards */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-lg p-4">
            <h3 className="font-semibold text-emerald-900 dark:text-emerald-100 mb-2">Fast Processing</h3>
            <p className="text-sm text-emerald-700 dark:text-emerald-200">
              Get results in seconds with our optimized AI model
            </p>
          </div>

          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
            <h3 className="font-semibold text-blue-900 dark:text-blue-100 mb-2">Accurate Detection</h3>
            <p className="text-sm text-blue-700 dark:text-blue-200">
              Identifies litter, crowds, and potential hazards with high precision
            </p>
          </div>

          <div className="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-4">
            <h3 className="font-semibold text-purple-900 dark:text-purple-100 mb-2">Actionable Insights</h3>
            <p className="text-sm text-purple-700 dark:text-purple-200">
              Get specific recommendations for cleanup and maintenance
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
