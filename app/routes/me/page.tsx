import { useLoaderData } from "react-router-dom";

function Page() {
  const profile = useLoaderData();
  console.log(profile);
  return <div>Profile</div>;
}

export { Page };
