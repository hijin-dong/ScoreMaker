import React, { useState, useRef } from "react";
import ReactCrop, { Crop, PixelCrop } from "react-image-crop";
import "react-image-crop/dist/ReactCrop.css";

interface VideoCropperProps {
  image: string;
  onCropDone: (blob: Blob, box: { x: number; y: number; w: number; h: number }) => void;
}

const VideoCropper: React.FC<VideoCropperProps> = ({ image, onCropDone }) => {
  const [crop, setCrop] = useState<Crop>({
    unit: '%',
    width: 30,
    height: 30,
    x: 0,
    y: 0,
  });

  const [completedCrop, setCompletedCrop] = useState<PixelCrop>();
  const imgRef = useRef<HTMLImageElement>(null);

  const handleCropComplete = async () => {
    const img = imgRef.current;
    if (!completedCrop || !img) return;

    const canvas = document.createElement('canvas');
    const scaleX = img.naturalWidth / img.width;
    const scaleY = img.naturalHeight / img.height;

    canvas.width = completedCrop.width * scaleX;
    canvas.height = completedCrop.height * scaleY;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.drawImage(
      img,
      completedCrop.x * scaleX,
      completedCrop.y * scaleY,
      completedCrop.width * scaleX,
      completedCrop.height * scaleY,
      0,
      0,
      completedCrop.width * scaleX,
      completedCrop.height * scaleY
    );

    canvas.toBlob((blob) => {
      if (!blob) return;

      const naturalWidth = img.naturalWidth;
      const naturalHeight = img.naturalHeight;

      const normalized = {
        x: (completedCrop.x * scaleX) / naturalWidth,
        y: (completedCrop.y * scaleY) / naturalHeight,
        w: (completedCrop.width * scaleX) / naturalWidth,
        h: (completedCrop.height * scaleY) / naturalHeight,
      };

      onCropDone(blob, normalized);
    }, 'image/jpeg');
  };

  return (
    <div className="relative p-4">
      <ReactCrop
        crop={crop}
        onChange={(newCrop) => setCrop(newCrop)}
        onComplete={(c) => setCompletedCrop(c)}
        ruleOfThirds
        keepSelection={false}
      >
        <img
          ref={imgRef}
          src={image}
          alt="to crop"
          style={{ maxHeight: "60vh" }}
        />
      </ReactCrop>

      <button
        className="absolute bottom-4 right-4 bg-blue-600 text-white px-4 py-2 rounded shadow-lg z-50"
        onClick={handleCropComplete}
      >
        크롭 완료
      </button>
    </div>
  );
};

export default VideoCropper;
