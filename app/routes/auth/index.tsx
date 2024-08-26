import { RouteObject } from "react-router-dom";
import Page, {
  ChangePasswordForm,
  ForgotPasswordForm,
  LoginForm,
  SignUpForm,
} from "./page";
import { UserService } from "./service";

const route: RouteObject[] = [
  {
    path: "/auth",
    element: <Page />,

    children: [
      { path: "/auth", element: <LoginForm />, action: UserService.LoginUser },
      {
        path: "/auth/signup",
        element: <SignUpForm />,
        action: UserService.RegisterUser,
      },
      { path: "/auth/forgotPassword", element: <ForgotPasswordForm /> },
      { path: "/auth/changePassword", element: <ChangePasswordForm /> },
    ],
  },
];

export { route };
