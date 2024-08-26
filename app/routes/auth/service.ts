import { redirect } from "react-router-dom";
import type { components } from "../../service";
import { UserRepository } from "./repository";

type SCHEMA = components["schemas"];

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
    return redirect("/");
  },
  LoginUser: async ({ request }: { request: Request }) => {
    const data = formDataToObject(
      await request.formData()
    ) as SCHEMA["UserLogin"];
    await UserRepository.LoginUser(data);
    return redirect("/");
  },
  LogoutUser: async () => {
    await UserRepository.LogoutUser();
    return redirect("/");
  },
  GetMe: async () => {
    return await UserRepository.GetMe();
  },
  UpdateMe: async (data: SCHEMA["UserUpdate"]) => {
    await UserRepository.UpdateMe(data);
    return redirect("/");
  },
  UpdateMyPassword: async (data: SCHEMA["UserChangePassword"]) => {
    await UserRepository.UpdateMyPassword(data);
    return redirect("/");
  },
};

export { UserService, formDataToObject };
