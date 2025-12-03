import { sellerApi } from "../axios/ApiServices";


export const getSellerOrders = async () => {
  try {
    const res = await sellerApi.get("/orders");
    return res.data;
  } catch (error) {
    console.error("Fetching seller orders failed:", error);
    throw error;
  }
}

export const confirmOrder = async (orderId: number) => {
  try {
    const res = await sellerApi.put("/confirm-order", { orderId });
    return res.data;
  } catch (error) {
    console.error("Confirming order failed:", error);
    throw error;
  }
}

export const sendShippingLink = async (orderId: number, shippingLink: string) => {
  try {
    const res = await sellerApi.put("/send-shipping-link", { orderId, shippingLink });
    return res.data;
  } catch (error) {
    console.error("Sending shipping link failed:", error);
    throw error;
  }
}

export const markOrderAsDelivered = async (orderId: number) => {
  try {
    const res = await sellerApi.put("/mark-delivered", { orderId });
    return res.data;
  } catch (error) {
    console.error("Marking order as delivered failed:", error);
    throw error;
  }
}