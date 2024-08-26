/* eslint-disable @typescript-eslint/no-explicit-any */
import client from "../../service";
import type { components } from "../../service";

type SCHEMA = components["schemas"];

const UserRepository = {
  RegisterUser: async (data: SCHEMA["UserCreate"]) => {
    return await client.POST("/auth/register", {
      body: data,
      headers: {
        "Content-Type": "application/json",
      },
    });
  },
  LoginUser: async (data: SCHEMA["UserLogin"]) => {
    return await client.POST("/auth/login", {
      body: data,
      headers: {
        "Content-Type": "application/json",
      },
    });
  },
  LogoutUser: async () => {
    return await client.GET("/auth/logout");
  },
  GetMe: async () => {
    return await client.GET("/me");
  },
  UpdateMe: async (data: SCHEMA["UserUpdate"]) => {
    return await client.PATCH("/me", { body: data });
  },
  UpdateMyPassword: async (data: SCHEMA["UserChangePassword"]) => {
    return await client.POST("/me/password", { body: data });
  },
};

export { UserRepository };
