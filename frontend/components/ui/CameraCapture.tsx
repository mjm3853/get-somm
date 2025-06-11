"use client"

import * as React from "react";
import * as Dialog from "@radix-ui/react-dialog";

interface CameraCaptureProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onCapture: (imageDataUrl: string) => void;
}

export const CameraCapture: React.FC<CameraCaptureProps> = ({ open, onOpenChange, onCapture }) => {
  const videoRef = React.useRef<HTMLVideoElement>(null);
  const canvasRef = React.useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = React.useState<MediaStream | null>(null);
  const [captured, setCaptured] = React.useState<string | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [isCameraReady, setIsCameraReady] = React.useState(false);

  React.useEffect(() => {
    if (open && !captured) {
      setIsCameraReady(false);
      navigator.mediaDevices.getUserMedia({ video: true })
        .then((mediaStream) => {
          setStream(mediaStream);
          if (videoRef.current) {
            videoRef.current.srcObject = mediaStream;
          }
        })
        .catch((err) => {
          setError("Unable to access camera: " + err.message);
        });
    }
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
        if (videoRef.current) {
          videoRef.current.srcObject = null;
        }
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, captured]);

  // Ensure camera is stopped and video is cleared when modal closes
  React.useEffect(() => {
    if (!open && stream) {
      stream.getTracks().forEach((track) => track.stop());
      if (videoRef.current) {
        videoRef.current.srcObject = null;
      }
      setStream(null);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  const handleCapture = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      if (ctx) {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL("image/png");
        setCaptured(dataUrl);
        if (stream) {
          stream.getTracks().forEach((track) => track.stop());
        }
      }
    }
  };

  const handleRetake = () => {
    setCaptured(null);
    setError(null);
  };

  const handleConfirm = () => {
    if (captured) {
      onCapture(captured);
      onOpenChange(false);
      setCaptured(null);
    }
  };

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 z-50" />
        <Dialog.Content className="fixed left-1/2 top-1/2 z-50 w-full max-w-md -translate-x-1/2 -translate-y-1/2 rounded-lg bg-white p-6 shadow-lg flex flex-col items-center">
          <Dialog.Title className="text-lg font-semibold mb-4">Take a Photo</Dialog.Title>
          <Dialog.Description className="text-sm text-muted-foreground mb-4">
            Capture or select a photo to add to your message.
          </Dialog.Description>
          {error && <div className="text-red-500 mb-2">{error}</div>}
          {!captured ? (
            <>
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="w-full h-64 bg-black rounded mb-4"
                style={{ objectFit: "cover" }}
                onCanPlay={() => setIsCameraReady(true)}
              />
              <button
                onClick={handleCapture}
                className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700"
                disabled={!isCameraReady}
              >
                Capture
              </button>
            </>
          ) : (
            <>
              <img src={captured} alt="Captured" className="w-full h-64 object-cover rounded mb-4" />
              <div className="flex gap-2">
                <button
                  onClick={handleRetake}
                  className="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400"
                >
                  Retake
                </button>
                <button
                  onClick={handleConfirm}
                  className="bg-green-600 text-white px-4 py-2 rounded shadow hover:bg-green-700"
                >
                  Confirm
                </button>
              </div>
            </>
          )}
          <canvas ref={canvasRef} className="hidden" />
          <Dialog.Close asChild>
            <button
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
              aria-label="Close"
            >
              ×
            </button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}; 