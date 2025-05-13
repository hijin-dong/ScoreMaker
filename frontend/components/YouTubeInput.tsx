import React, { useState } from 'react';

interface YouTubeInputProps {
  onSubmit: (url: string, startTime: number) => void;
}

const YouTubeInput: React.FC<YouTubeInputProps> = ({ onSubmit }) => {
  const [url, setUrl] = useState('');
  const [startTime, setStartTime] = useState(0);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(url, startTime);
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2 p-4 border rounded shadow-md">
      <label className="font-semibold">YouTube 링크</label>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="https://www.youtube.com/watch?v=..."
        className="border rounded px-2 py-1"
        required
      />

      <label className="font-semibold">시작 시간 (초)</label>
      <input
        type="number"
        value={startTime}
        onChange={(e) => setStartTime(Number(e.target.value))}
        className="border rounded px-2 py-1"
        min={0}
      />

      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded mt-2">
        첫 프레임 불러오기
      </button>
    </form>
  );
};

export default YouTubeInput;
