import { useState } from 'react';
import YouTubeInput from '@/components/YouTubeInput';
import VideoCropper from '@/components/VideoCropper';
import PdfDownloadButton from '@/components/PdfDownloadButton';

export default function Home() {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [startTime, setStartTime] = useState(0);
  const [cropBox, setCropBox] = useState<{ x: number; y: number; w: number; h: number } | null>(null);

  const [frameUrl, setFrameUrl] = useState<string | null>(null);
  const [croppedImage, setCroppedImage] = useState<Blob | null>(null);

  const handleSubmit = async (url: string, time: number) => {
    setYoutubeUrl(url);
    setStartTime(time);

    const res = await fetch('/api/get-frame', {
      method: 'POST',
      body: JSON.stringify({ url, startTime: time }),
      headers: { 'Content-Type': 'application/json' },
    });

    const data = await res.json();
    setFrameUrl(data.frameUrl); // base64 or blob URL
  };

  const handleCrop = (blob: Blob, box: { x: number; y: number; w: number; h: number }) => {
  setCroppedImage(blob);
  setCropBox(box);
  };

  return (
    <div className="p-8">
      {!frameUrl && <YouTubeInput onSubmit={handleSubmit} />}
      {frameUrl && !croppedImage && (
        <VideoCropper image={frameUrl} onCrop={handleCrop} />
      )}
      {croppedImage && cropBox && (
        <PdfDownloadButton
          image={croppedImage}
          youtubeUrl={youtubeUrl}
          startTime={startTime}
          cropBox={cropBox}
        />
      )}
    </div>
  );
}
