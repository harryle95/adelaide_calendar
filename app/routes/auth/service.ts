import { redirect } from "react-router-dom";
import type { components } from "../../service";
import { UserRepository } from "../../service";

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

export { UserService, formDataToObject };
