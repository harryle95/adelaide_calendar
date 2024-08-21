import { NavigationMenu } from "./navigation_menu";
import { Outlet } from "react-router-dom";

function Root() {
  return (
    <main>
      <NavigationMenu />
      <Outlet />
    </main>
  );
}

export default Root;
