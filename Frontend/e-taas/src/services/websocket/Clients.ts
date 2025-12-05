import { connectToWebsocket } from "./Config";


export const notificationWebSocket = () => connectToWebsocket("/v1/api/notifications/ws");
export const conversationWebSocket = () => connectToWebsocket("/v1/api/conversations/ws");