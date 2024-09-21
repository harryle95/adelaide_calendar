import createClient, { type Middleware } from "openapi-fetch";
import type { paths } from "./schema";
export type * from "./schema";
import type { components } from "./schema";
import { createContext } from "@radix-ui/react-context";

type SCHEMA = components["schemas"];
const DEV = import.meta.env.DEV;
const BASE_URL = DEV ? "/api" : import.meta.env.VITE_PROXY;

const throwOnError: Middleware = {
  async onResponse({ response }) {
    if (response.status >= 400) {
      const body = response.headers.get("content-type")?.includes("json")
        ? await response.clone().json()
        : await response.clone().text();
      console.log(body);
      throw new Error(body["detail"]);
    }
    return undefined;
  },
};

const client = createClient<paths>({ baseUrl: BASE_URL });

client.use(throwOnError);

const UserRepository = {
  RegisterUser: async (data: SCHEMA["UserCreate"]) => {
    return await client.POST("/auth/register", {
      mode: "cors",
      credentials: "include",
      body: data,
      headers: {
        "Content-Type": "application/json",
      },
    });
  },
  LoginUser: async (data: SCHEMA["UserLogin"]) => {
    return await client.POST("/auth/login", {
      mode: "cors",
      credentials: "include",
      body: data,
      headers: {
        "Content-Type": "application/json",
      },
    });
  },
  LogoutUser: async () => {
    return await client.POST("/auth/logout", {
      mode: "cors",
      credentials: "include",
    });
  },
};

const MeRepository = {
  GetMe: async () => {
    return await client.GET("/me", { mode: "cors", credentials: "include" });
  },
  UpdateMe: async (data: SCHEMA["UserUpdate"]) => {
    return await client.PATCH("/me", {
      mode: "cors",
      body: data,
      credentials: "include",
    });
  },
  UpdateMyPassword: async (data: SCHEMA["UserChangePassword"]) => {
    return await client.POST("/me/password", {
      mode: "cors",
      body: data,
      credentials: "include",
    });
  },
};

type User = SCHEMA["User"];

type AuthContextType = {
  user: User;
  setUser: React.Dispatch<React.SetStateAction<User>>;
  isLoggedIn: boolean;
};

const [AuthProvider, useAuthContext] =
  createContext<AuthContextType>("AuthProvider");

export { UserRepository, MeRepository, useAuthContext, AuthProvider, BASE_URL };
export type { SCHEMA, User, AuthContextType };
export default client;
