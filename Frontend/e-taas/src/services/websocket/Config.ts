

export const connectToWebsocket = (url: string): WebSocket => {
  const API_URL = import.meta.env.VITE_WEBSOCKET_URL;
  const fullUrl = `${API_URL}${url}`;
  const ws = new WebSocket(fullUrl);
  ws.onopen = () => {
    console.log("WebSocket connected");
  };

  ws.onmessage = (event) => {
    try {
        const data = JSON.parse(event.data);
        console.log("Received JSON:", data);
      } catch (err) {
        console.log("Received text:", event.data);
      }
    };


  ws.onerror = (err) => {
    console.error("WebSocket error:", err);
  };

  ws.onclose = (event) => {
    console.log("WebSocket closed:", event.code, event.reason);
    setTimeout(() => connectToWebsocket(url), 3000);
  };

  return ws;
};

