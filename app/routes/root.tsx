import { NavigationMenu } from "./navigation_menu";
import { Outlet } from "react-router-dom";
import axios from "axios";

function Root() {
  return (
    <main>
      <NavigationMenu />
      <Outlet />
    </main>
  );
}

export default Root;
