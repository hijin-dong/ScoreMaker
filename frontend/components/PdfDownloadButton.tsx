// frontend/components/PdfDownloadButton.tsx

import React from 'react';

interface PdfDownloadButtonProps {
  image: Blob;  // 크롭된 이미지 (Blob 형태)
  youtubeUrl: string;  // 유튜브 영상 URL
  startTime: number;  // 시작 시간
  cropBox: { x: number; y: number; w: number; h: number };  // 크롭 영역
  defaultFileName?: string;  // 다운로드할 파일 이름 (기본값: "악보.pdf")
}

const PdfDownloadButton: React.FC<PdfDownloadButtonProps> = ({
  image,
  youtubeUrl,
  startTime,
  cropBox,
  defaultFileName = "악보.pdf"
}) => {
  const handleDownload = async () => {
    const formData = new FormData();
    formData.append("image", image);  // 크롭된 이미지 (Blob)
    formData.append("url", youtubeUrl);  // 유저가 입력한 유튜브 URL
    formData.append("startTime", String(startTime));  // 유저가 입력한 시작 시간
    formData.append("cropBox", JSON.stringify([cropBox.x, cropBox.y, cropBox.w, cropBox.h]));  // 크롭 영역 좌표

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
    URL.revokeObjectURL(url); // 메모리 해제
  };

  return (
    <button
      onClick={handleDownload}
      className="px-4 py-2 rounded text-white bg-green-500 hover:bg-green-600"
    >
      PDF 다운로드
    </button>
  );
};

export default PdfDownloadButton;
