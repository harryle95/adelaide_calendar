import { RouteObject } from "react-router-dom";
import Page, {
  ChangePasswordForm,
  ForgotPasswordForm,
  LoginForm,
  Profile,
} from "./page";
import { MeService, UserService } from "./service";
import RegisterForm from "./signup";
import "./style.css";

const route: RouteObject[] = [
  {
    path: "/auth",
    element: <Page />,

    children: [
      { path: "/auth", element: <LoginForm />, action: UserService.LoginUser },
      {
        path: "/auth/signup",
        element: <RegisterForm />,
        action: UserService.RegisterUser,
      },
      { path: "/auth/forgotPassword", element: <ForgotPasswordForm /> },
      { path: "/auth/changePassword", element: <ChangePasswordForm /> },
      { path: "/auth/me", element: <Profile />, loader: MeService.GetMe },
    ],
  },
];

export { route };
