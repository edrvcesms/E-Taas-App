import { userApi } from "../axios/ApiServices";
import type { UpdateUserData } from "../../types/user/User";

export const getUserDetails = async () => {
  try {
    const res = await userApi.get("/details");
    return res.data;
  } catch (error) {
    console.error("Fetching user details failed:", error);
    throw error;
  }
}

export const updateUserDetails = async (data: UpdateUserData) => {
  try {
    const res = await userApi.put("/update-details", data);
    return res.data;
  } catch (error) {
    console.error("Updating user details failed:", error);
    throw error;
  }
}

export const deleteUserAccount = async () => {
  try {
    const res = await userApi.delete("/delete");
    return res.data;
  } catch (error) {
    console.error("Deleting user account failed:", error);
    throw error;
  }
}

export const logoutUser = async () => {
  try {
    const res = await userApi.post("/logout");
    return res.data;
  } catch (error) {
    console.error("Logout failed:", error);
    throw error;
  }
}