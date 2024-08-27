/* eslint-disable @typescript-eslint/no-explicit-any */
import createClient, { type Middleware } from "openapi-fetch";

import type { paths } from "./schema";
export type * from "./schema";
import type { components } from "./schema";

type SCHEMA = components["schemas"];

const throwOnError: Middleware = {
  async onResponse({ response }) {
    if (response.status >= 400) {
      const body = response.headers.get("content-type")?.includes("json")
        ? await response.clone().json()
        : await response.clone().text();
      throw new Error(body["status_code"]);
    }
    return undefined;
  },
};

const client = createClient<paths>({ baseUrl: "/api" });

client.use(throwOnError);

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
};

const MeRepository = {
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

export { UserRepository, MeRepository };

export default client;
