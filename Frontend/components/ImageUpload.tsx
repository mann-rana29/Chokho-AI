"use client";

import React, { useState, useRef } from "react";

interface ImageUploadProps {
  onImageUpload: (file: File, preview: string) => void;
  isLoading?: boolean;
}

export default function ImageUpload({ onImageUpload, isLoading = false }: ImageUploadProps) {
  const [dragActive, setDragActive] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File) => {
    if (!file.type.startsWith("image/")) {
      alert("Please upload an image file");
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const result = e.target?.result as string;
      setPreview(result);
      setFileName(file.name);
      onImageUpload(file, result);
    };
    reader.readAsDataURL(file);
  };

  const handleDrag = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleReset = () => {
    setPreview(null);
    setFileName("");
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="space-y-6">
      {!preview ? (
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`relative border-2 border-dashed rounded-xl p-12 transition-all cursor-pointer ${
            dragActive
              ? "border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20"
              : "border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 hover:border-emerald-400"
          }`}
          onClick={handleClick}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleInputChange}
            className="hidden"
            disabled={isLoading}
          />

          <div className="flex flex-col items-center justify-center gap-4">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-16 h-16 text-emerald-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="1.5"
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>

            <div className="text-center">
              <p className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                Drag and drop your image here
              </p>
              <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                or click to browse
              </p>
            </div>

            <div className="text-xs text-slate-500 dark:text-slate-500">
              Supported formats: JPG, PNG, WebP
            </div>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="rounded-xl overflow-hidden shadow-lg border border-slate-200 dark:border-slate-700">
            <img src={preview} alt="Preview" className="w-full h-auto max-h-96 object-cover" />
          </div>

          <div className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-lg p-4">
            <p className="text-sm text-slate-700 dark:text-slate-200">
              <span className="font-semibold">File uploaded:</span> {fileName}
            </p>
          </div>

          <button
            onClick={handleReset}
            disabled={isLoading}
            className="w-full px-4 py-2 rounded-md border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-200 font-medium hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors disabled:opacity-50"
          >
            Upload Different Image
          </button>
        </div>
      )}
    </div>
  );
}
