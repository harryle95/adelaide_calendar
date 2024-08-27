import { redirect } from "react-router-dom";
import type { SCHEMA } from "../../service";
import { UserRepository, MeRepository } from "../../service";

function formDataToObject(data: FormData) {
  const result: { [key: string]: FormDataEntryValue } = {};
  data.forEach((value, key) => (result[key] = value));
  return result;
}

const UserService = {
  RegisterUser: async ({ request }: { request: Request }) => {
    const data = formDataToObject(
      await request.formData()
    ) as SCHEMA["UserCreate"];
    await UserRepository.RegisterUser(data);
    return redirect("/me");
  },
  LoginUser: async ({ request }: { request: Request }) => {
    const data = formDataToObject(
      await request.formData()
    ) as SCHEMA["UserLogin"];
    await UserRepository.LoginUser(data);
    return redirect("/me");
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
      return result.data;
    } catch (error) {
      console.log(error);
      return redirect("/auth/");
    }
  },
  UpdateMe: async (data: SCHEMA["UserUpdate"]) => {
    await MeRepository.UpdateMe(data);
    return redirect("/");
  },
  UpdateMyPassword: async (data: SCHEMA["UserChangePassword"]) => {
    await MeRepository.UpdateMyPassword(data);
    return redirect("/");
  },
};

export { UserService, formDataToObject, MeService };
