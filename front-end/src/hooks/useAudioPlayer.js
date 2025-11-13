import { useState, useRef, useCallback } from 'react';

/**
 * Hook for playing TTS audio responses from the agent.
 * Handles audio playback, state management, and cleanup.
 */
export const useAudioPlayer = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentAudio, setCurrentAudio] = useState(null);
  const audioRef = useRef(null);

  const playAudio = useCallback(async (audioUrl) => {
    try {
      console.log('[Audio] Playing:', audioUrl);
      
      // Stop any currently playing audio
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }

      // Create new audio instance
      const audio = new Audio(audioUrl);
      audioRef.current = audio;
      setCurrentAudio(audioUrl);

      audio.onplay = () => {
        setIsPlaying(true);
        console.log('[Audio] Playback started');
      };
      
      audio.onended = () => {
        setIsPlaying(false);
        setCurrentAudio(null);
        console.log('[Audio] Playback ended');
      };
      
      audio.onerror = (e) => {
        console.error('[Audio] Playback error:', e);
        setIsPlaying(false);
        setCurrentAudio(null);
      };

      await audio.play();
    } catch (error) {
      console.error('[Audio] Error playing audio:', error);
      setIsPlaying(false);
      setCurrentAudio(null);
    }
  }, []);

  const stopAudio = useCallback(() => {
    console.log('[Audio] Stopping playback');
    
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      audioRef.current = null;
      setIsPlaying(false);
      setCurrentAudio(null);
    }
  }, []);

  const toggleAudio = useCallback((audioUrl) => {
    if (currentAudio === audioUrl && isPlaying) {
      stopAudio();
    } else {
      playAudio(audioUrl);
    }
  }, [currentAudio, isPlaying, playAudio, stopAudio]);

  return {
    isPlaying,
    currentAudio,
    playAudio,
    stopAudio,
    toggleAudio,
  };
};

