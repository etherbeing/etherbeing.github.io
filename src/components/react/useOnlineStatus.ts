import { useEffect, useState } from "react";

export function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(() => {
    if (typeof navigator === "undefined") {
      return true;
    }
    return navigator.onLine;
  });
  const [showOfflineSnackbar, setShowOfflineSnackbar] = useState(false);

  useEffect(() => {
    function handleOnline() {
      setIsOnline(true);
      setShowOfflineSnackbar(false);
    }

    function handleOffline() {
      setIsOnline(false);
      setShowOfflineSnackbar(true);
    }

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  return {
    isOnline,
    showOfflineSnackbar,
  };
}
