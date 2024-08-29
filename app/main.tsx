import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { RouterProvider } from "react-router-dom";
import { createBrowserRouter } from "react-router-dom";
import IndexPage from "./routes/root.tsx";
import ErrorPage from "./routes/error.tsx";
import { routes } from "./routes/index.tsx";
import { MeService } from "./routes/auth/service.ts";

const router = createBrowserRouter([
  {
    path: "/",
    element: <IndexPage />,
    errorElement: <ErrorPage />,
    loader: MeService.GetMe,
    children: [
      {
        errorElement: <ErrorPage />,
        children: [...routes],
      },
    ],
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
