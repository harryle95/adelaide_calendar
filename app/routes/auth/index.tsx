import { RouteObject } from "react-router-dom";
import {
  RegisterPage,
  LoginPage,
  ProfilePage,
  ChangePasswordPage,
  ForgotPasswordPage,
  Page,
} from "./page";
import "./style.css";
import { MeService, UserService } from "./service";

const route: RouteObject[] = [
  {
    path: "/auth",
    element: <Page />,

    children: [
      { path: "/auth", element: <LoginPage />, action: UserService.LoginUser },
      {
        path: "/auth/signup",
        element: <RegisterPage />,
        action: UserService.RegisterUser,
      },
      { path: "/auth/forgotPassword", element: <ForgotPasswordPage /> },
      {
        path: "/auth/changePassword",
        element: <ChangePasswordPage />,
        action: MeService.UpdateMyPassword,
      },
      {
        path: "/auth/me",
        element: <ProfilePage />,
      },
      { path: "/auth/logout", loader: UserService.LogoutUser },
    ],
  },
];

export { route };
