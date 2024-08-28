import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

const Schema = z.object({
  name: z
    .string()
    .min(2, { message: "Name must be at least 2 characters long" })
    .max(20, { message: "Name must be at most 20 characters long" }),
  password: z
    .string()
    .min(6, { message: "Password must be at least 6 characters long" })
    .max(50, { message: "Password must be at most 50 characters long" }),
  email: z.string().email(),
});

export default function RegisterForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<z.infer<typeof Schema>>({
    resolver: zodResolver(Schema),
  });

  const onSubmit = (data: z.infer<typeof Schema>) => console.log(data);
  return (
    <form className="formRoot" onSubmit={handleSubmit(onSubmit)}>
      <label className="formLabel">
        <p className="formLabelHeader">Username*</p>
        <div className="formLabelGroup">
          <input
            className="formInput"
            placeholder="Enter username"
            {...register("name")}
            data-valid={errors.name ? "invalid" : "valid"}
          />
          <p className="formValidationError">{errors.name?.message}</p>
        </div>
      </label>

      <label className="formLabel">
        <p className="formLabelHeader">Password*</p>
        <div className="formLabelGroup">
          <input
            className="formInput"
            placeholder="Enter password"
            type="password"
            {...register("password")}
            data-valid={errors.password ? "invalid" : "valid"}
          />
          <p className="formValidationError">{errors.password?.message}</p>
        </div>
      </label>

      <label className="formLabel">
        <p className="formLabelHeader">Email*</p>
        <div className="formLabelGroup">
          <input
            className="formInput"
            placeholder="Enter email address"
            type="email"
            {...register("email")}
            data-valid={errors.email ? "invalid" : "valid"}
          />
          <p className="formValidationError">{errors.email?.message}</p>
        </div>
      </label>

      <button type="submit" className="formSubmitButton">
        Submit
      </button>
    </form>
  );
}
