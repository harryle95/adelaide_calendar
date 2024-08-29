/* eslint-disable @typescript-eslint/no-explicit-any */
import React from "react";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  useForm,
  FormProvider,
  useFormContext,
  FieldValues,
} from "react-hook-form";
import { SubmitOptions, useActionData, useSubmit } from "react-router-dom";

interface RootProps<T extends FieldValues> extends SubmitOptions {
  schema: z.ZodType<T>;
  children: React.ReactNode;
}

interface _TextInputProps extends React.ComponentPropsWithoutRef<"input"> {
  error: React.ReactNode;
  label: React.ReactNode;
  labelAsterisk?: boolean;
  description?: React.ReactNode;
  rightSectionInput?: React.ReactNode;
  rightSectionLabel?: React.ReactNode;
  leftSectionInput?: React.ReactNode;
  leftSectionLabel?: React.ReactNode;
}

const _TextInput = React.forwardRef<HTMLInputElement, _TextInputProps>(
  (props, ref) => {
    const {
      description,
      error,
      label,
      labelAsterisk,
      rightSectionInput,
      rightSectionLabel,
      leftSectionInput,
      leftSectionLabel,
      ...rest
    } = props;
    const id = React.useId();
    return (
      <div className="TextInputRoot">
        <div className="TextInputLabelContainer">
          {leftSectionLabel}
          <label htmlFor={id} className="TextInputLabel">
            {label}
            {labelAsterisk ? "*" : ""}
          </label>
          {rightSectionLabel}
        </div>
        <p className="TextInputDescription">{description}</p>
        <div className="TextInputContainer">
          {leftSectionInput}
          <input id={id} {...rest} className="TextInputInput" ref={ref} />
          {rightSectionInput}
        </div>
        <p
          className="TextInputDescription"
          data-valid={error ? "invalid" : "valid"}
        >
          {error}
        </p>
      </div>
    );
  }
);

const Root = <T extends FieldValues>(props: RootProps<T>) => {
  const { schema, children, ...options } = props;
  const submit = useSubmit();
  const error = useActionData() as any;
  const methods = useForm<T>({ resolver: zodResolver(schema) });
  const onSubmit = async (data: T) => {
    submit(data, { ...options, encType: "application/json" });
  };
  return (
    <FormProvider {...methods}>
      <p>{error?.message}</p>
      <form className="formRoot" onSubmit={methods.handleSubmit(onSubmit)}>
        {children}
      </form>
    </FormProvider>
  );
};

interface TextInputProps extends Omit<_TextInputProps, "error"> {
  name: string;
}

function TextInput(props: TextInputProps) {
  const { name, ...rest } = props;
  const { formState, register } = useFormContext();
  const error = formState.errors[name];
  return (
    <_TextInput
      {...register(name)}
      {...rest}
      error={error?.message as string}
    />
  );
}

export { Root, TextInput };
export type { TextInputProps };
