import React, { useState, useCallback } from 'react';
import Cropper from 'react-easy-crop';
import { Area } from 'react-easy-crop/types';
import { getCroppedImg } from '@/utils/cropImage'; // 유틸로 따로 뺌

interface VideoCropperProps {
  image: string;
  onCrop: (blob: Blob, cropBox: { x: number; y: number; w: number; h: number }) => void;
}


const VideoCropper: React.FC<VideoCropperProps> = ({ image, onCrop }) => {
  const [crop, setCrop] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [croppedAreaPixels, setCroppedAreaPixels] = useState<Area | null>(null);

  const onCropComplete = useCallback((_: Area, croppedArea: Area) => {
    setCroppedAreaPixels(croppedArea);
  }, []);

const handleCrop = async () => {
  const pixelCrop = {
    x: crop.x,
    y: crop.y,
    width: croppedAreaPixels?.width || 0,
    height: croppedAreaPixels?.height || 0,
  };

  const blob = await getCroppedImg(image, pixelCrop);
  onCrop(blob, {
    x: pixelCrop.x,
    y: pixelCrop.y,
    w: pixelCrop.width,
    h: pixelCrop.height,
  });
};

  return (
    <div className="relative w-full h-[60vh]">
      <Cropper
        image={image}
        crop={crop}
        zoom={zoom}
        aspect={4 / 3} // 원하는 비율로 바꿔도 돼
        onCropChange={setCrop}
        onZoomChange={setZoom}
        onCropComplete={onCropComplete}
      />
      <button
        onClick={handleCrop}
        className="absolute bottom-4 right-4 bg-blue-500 text-white px-4 py-2 rounded"
      >
        크롭 완료
      </button>
    </div>
  );
};

export default VideoCropper;
