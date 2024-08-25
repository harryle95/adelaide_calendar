import { RouteObject } from "react-router-dom";
import Page, {
  ChangePasswordForm,
  ForgotPasswordForm,
  LoginForm,
  SignUpForm,
} from "./page";

const route: RouteObject[] = [
  {
    path: "/auth",
    element: <Page />,
    children: [
      { path: "/auth", element: <LoginForm /> },
      { path: "/auth/signup", element: <SignUpForm /> },
      { path: "/auth/forgotPassword", element: <ForgotPasswordForm /> },
      { path: "/auth/changePassword", element: <ChangePasswordForm /> },
    ],
  },
];

export { route };
