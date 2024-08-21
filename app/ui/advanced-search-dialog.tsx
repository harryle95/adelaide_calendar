import React from "react";
import * as Dialog from "@radix-ui/react-dialog";
import { GearIcon } from "@radix-ui/react-icons";
import AdvancedSearchForm from "./advanced-search-form.tsx";

const AdvancedSearchDialog = () => (
  <Dialog.Root>
    <Dialog.Trigger asChild>
      <button className="">
        <GearIcon className="mx-1 size-6 stroke-2" />
      </button>
    </Dialog.Trigger>
    <Dialog.Portal>
      <Dialog.Overlay className="fixed inset-0 bg-black opacity-50" />
      <Dialog.Content className="fixed inset-1/4 rounded-lg bg-white p-6 shadow-lg">
        <AdvancedSearchForm />
        <Dialog.Close asChild>
          <button className="absolute right-2 top-2 text-gray-500 hover:text-gray-700">
            &times;
          </button>
        </Dialog.Close>
      </Dialog.Content>
    </Dialog.Portal>
  </Dialog.Root>
);

export default AdvancedSearchDialog;
