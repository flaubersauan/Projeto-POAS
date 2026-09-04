"use client";

import Button from "@/components/ui/Button";
import InputAuth from "@/components/features/auth/InputAuth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import FieldError from "@/components/features/auth/FieldError";
import { LoginFormData, loginSchema } from "@/lib/schemas/auth";
import { login } from "@/actions/auth";
import { alert } from "@/lib/alert";
import useStepForm from "@/hooks/useStepForm";


export default function FormLogin() {
  const {register, handleSubmit, trigger, setFocus, formState: { isSubmitting, errors }} = useForm<LoginFormData>({
    mode: "onBlur",
    reValidateMode: "onBlur",
    defaultValues: {
      email: "",
      senha: ""
    },
    resolver: zodResolver(loginSchema)
  });
  const { fields, step, handleNextStep, handleStepKeyDown } = useStepForm(
    loginSchema,
    trigger,
    setFocus,
  );

  const handleButtonClick =
    step < fields.length - 1
      ? handleNextStep
      : handleSubmit(onSubmit);

  async function onSubmit(data: LoginFormData) {
    try {
      const response = await login({
        email: data.email,
        senha: data.senha
      });
      
      if (response?.status === 200) {
        alert.fire({
          icon: "success",
          title: "Login realizado",
          text: "Bem vindo!"
        });
      } else if (response?.status === 401) {
        alert.fire({
          icon: "question",
          title: "Credenciais inválidas",
          text: "E-mail e/ou senha incorretos"
        });
      } else if (!response.success) {
        console.log(response.status, response.error);
        alert.fire({
          icon: "error",
          title: "Erro",
          text: "Erro interno"
        });
      }
    } catch(error) {
      console.log(error);
      alert.fire({
        icon: "error",
        title: "Erro",
        text: "Erro interno"
      });
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div className="flex flex-col gap-2 w-90">
        <h1 className="text-4xl font-medium mb-8 text-center">Login</h1>

        {step >= 0 && (
          <div>
            <InputAuth type="email" id="email" labelValue="Email" {...register("email")} onKeyDown={handleStepKeyDown} />
            {errors.email && (<FieldError>{errors.email.message}</FieldError>)}
          </div>
        )}

        {step >= 1 && (
          <div>
            <InputAuth type="password" id="senha" labelValue="Senha" {...register("senha")} />
            {errors.senha && (<FieldError>{errors.senha.message}</FieldError>)}
          </div>
        )}

        
        <Button
          type="button"
          variant={step < fields.length - 1 ? "outline" : "primary"}
          onClick={handleButtonClick}
          disabled={isSubmitting}
        >
          {step < fields.length - 1
            ? "Próximo"
            : isSubmitting
              ? "Aguarde..."
              : "Iniciar Sessão"}
        </Button>
      </div>
    </form>
  );
}