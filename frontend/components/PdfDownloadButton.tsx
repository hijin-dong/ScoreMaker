import React, { useState } from 'react';

interface PdfDownloadButtonProps {
  image: Blob;
  youtubeUrl: string;
  startTime: number;
  cropBox: { x: number; y: number; w: number; h: number };
  defaultFileName?: string;
}

const PdfDownloadButton: React.FC<PdfDownloadButtonProps> = ({
  image,
  youtubeUrl,
  startTime,
  cropBox,
  defaultFileName = "악보.pdf",
}) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleDownload = async () => {
    if (isLoading) return;
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append("image", image);
      formData.append("url", youtubeUrl);
      formData.append("startTime", String(startTime));
      formData.append("cropBox", JSON.stringify([cropBox.x, cropBox.y, cropBox.w, cropBox.h]));

      const res = await fetch("/api/generate-pdf", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        alert("PDF 생성에 실패했어요 🥲");
        return;
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = defaultFileName;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("PDF 다운로드 중 오류:", err);
      alert("에러가 발생했어요");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleDownload}
      disabled={isLoading}
      className={`px-4 py-2 rounded text-white transition-colors ${
        isLoading ? 'bg-gray-400 cursor-not-allowed' : 'bg-green-500 hover:bg-green-600'
      }`}
    >
      {isLoading ? 'Now Loading...' : 'PDF 다운로드'}
    </button>
  );
};

export default PdfDownloadButton;
