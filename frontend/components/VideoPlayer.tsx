'use client';

import { useState, useRef, useEffect } from 'react';

interface VideoPlayerProps {
  src: string;
}

const VideoPlayer = ({ src }: VideoPlayerProps) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(1);
  const [progress, setProgress] = useState(0);

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseFloat(e.target.value);
    setVolume(newVolume);
    if (videoRef.current) {
      videoRef.current.volume = newVolume;
    }
  };

  const handleProgress = () => {
    if (videoRef.current) {
      const duration = videoRef.current.duration;
      const currentTime = videoRef.current.currentTime;
      const progress = (currentTime / duration) * 100;
      setProgress(progress);
    }
  };

  useEffect(() => {
    const video = videoRef.current;
    if (video) {
      video.addEventListener('timeupdate', handleProgress);
      return () => {
        video.removeEventListener('timeupdate', handleProgress);
      };
    }
  }, []);

  return (
    <div className="relative" onContextMenu={(e) => e.preventDefault()}>
      <video
        ref={videoRef}
        src={src}
        className="w-full"
        controlsList="nodownload"
      />
      <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 p-4 text-white">
        <div className="flex items-center justify-between">
          <button onClick={togglePlay}>{isPlaying ? 'Pause' : 'Play'}</button>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={volume}
            onChange={handleVolumeChange}
          />
        </div>
        <div className="mt-2 h-2 w-full bg-gray-600">
          <div
            className="h-full bg-indigo-600"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>
    </div>
  );
};

export default VideoPlayer;
