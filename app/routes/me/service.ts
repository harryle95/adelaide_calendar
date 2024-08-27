import { redirect } from "react-router-dom";
import { MeRepository } from "../../service";
import type { components } from "../../service";

type SCHEMA = components["schemas"];

const MeService = {
  GetMe: async () => {
    try {
      return await MeRepository.GetMe();
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

export { MeService };
