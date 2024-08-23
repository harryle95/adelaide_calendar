import React from "react";
import * as Tooltip from "@radix-ui/react-tooltip";
import { QuestionMarkCircledIcon } from "@radix-ui/react-icons";

const HelpTooltip = () => {
  return (
    <Tooltip.Provider>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>
          <QuestionMarkCircledIcon className="size-5 stroke-2" />
        </Tooltip.Trigger>
        <Tooltip.Portal>
          <Tooltip.Content className="rounded bg-black p-2 text-white">
            What is your question?
            <Tooltip.Arrow />
          </Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>
    </Tooltip.Provider>
  );
};

export default HelpTooltip;
