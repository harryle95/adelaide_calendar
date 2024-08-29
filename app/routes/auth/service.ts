import { redirect } from "react-router-dom";
import type { SCHEMA } from "../../service";
import { UserRepository, MeRepository } from "../../service";
import { defer } from "react-router-dom";

const UserService = {
  RegisterUser: async ({ request }: { request: Request }) => {
    const data = await request.json();
    try {
      await UserRepository.RegisterUser(data);
      return redirect("/auth/me");
    } catch (error) {
      return error;
    }
  },
  LoginUser: async ({ request }: { request: Request }) => {
    const data = await request.json();
    try {
      await UserRepository.LoginUser(data);
      return redirect("/auth/me");
    } catch (error) {
      return error;
    }
  },
  LogoutUser: async () => {
    await UserRepository.LogoutUser();
    return redirect("/");
  },
};

const MeService = {
  GetMe: async () => {
    try {
      const result = await MeRepository.GetMe();
      return defer({ user: result.data });
    } catch (error) {
      console.log(error);
      return { user: { id: null, name: null, email: null } };
    }
  },
  UpdateMe: async (data: SCHEMA["UserUpdate"]) => {
    await MeRepository.UpdateMe(data);
    return redirect("/");
  },
  UpdateMyPassword: async ({ request }: { request: Request }) => {
    const data: SCHEMA["UserChangePassword"] = await request.json();
    await MeRepository.UpdateMyPassword(data);
    return redirect("/");
  },
};

export { UserService, MeService };
