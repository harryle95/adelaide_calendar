import * as PrimitiveAvatar from "@radix-ui/react-avatar";
import type { SCHEMA } from "../../service";
import "./avatar.css";

const getInitials = (name?: string) => {
  if (name) {
    const nameSplit = name.split(" ");
    if (nameSplit.length === 1) {
      const nameStr = nameSplit[0];
      return nameStr.length === 1 ? nameStr[0] : nameStr[0] + nameStr[1];
    }
    const firstInitial = nameSplit[0][0].toUpperCase();
    const lastInitial = nameSplit[nameSplit.length - 1][0].toUpperCase();
    return firstInitial + lastInitial;
  }
  return "JD";
};

const Avatar = ({ user }: { user: SCHEMA["User"] }) => {
  return (
    <PrimitiveAvatar.Root className="AvatarRoot">
      <PrimitiveAvatar.Image
        className="AvatarImage"
        src={user.avatarUrl!}
        alt={user.name!}
      />
      <PrimitiveAvatar.Fallback className="AvatarFallback" delayMs={600}>
        {getInitials(user.name!)}
      </PrimitiveAvatar.Fallback>
    </PrimitiveAvatar.Root>
  );
};

export { Avatar };
