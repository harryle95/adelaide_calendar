import { RouteObject } from "react-router-dom";
import { Page } from "./page";
import { MeService } from "./service";

const route: RouteObject[] = [
  {
    path: "/me",
    element: <Page />,
    loader: MeService.GetMe,
  },
];

export { route };
