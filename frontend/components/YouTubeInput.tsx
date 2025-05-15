import React, { useState } from 'react';

interface YouTubeInputProps {
  onSubmit: (url: string, startTime: number) => Promise<void>; // 비동기 호출로 변경
}

const YouTubeInput: React.FC<YouTubeInputProps> = ({ onSubmit }) => {
  const [url, setUrl] = useState('');
  const [startTime, setStartTime] = useState(0);
  const [isLoading, setIsLoading] = useState(false); // 로딩 상태 추가

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await onSubmit(url, startTime);
    } finally {
      setIsLoading(false);
    }
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

      <button
        type="submit"
        disabled={isLoading}
        className={`px-4 py-2 rounded text-white transition-colors ${
          isLoading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
        }`}
      >
        {isLoading ? '불러오는 중...' : '첫 프레임 불러오기'}
      </button>
    </form>
  );
};

export default YouTubeInput;
