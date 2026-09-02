"use client";

import Button from "@/components/ui/Button";
import InputAuth from "@/components/features/auth/InputAuth";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import FieldError from "@/components/features/auth/FieldError";
import { LoginFormData, loginSchema } from "@/lib/schemas/auth";
import { login } from "@/actions/auth";
import { alert } from "@/lib/alert";


export default function FormLogin() {
  const router = useRouter();
  const {register, handleSubmit, formState: { isSubmitting, errors }} = useForm<LoginFormData>({
    mode: "onBlur",
    reValidateMode: "onBlur",
    defaultValues: {
      email: "",
      senha: ""
    },
    resolver: zodResolver(loginSchema)
  });

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
        })
        router.push('/home');
      } else if (response?.status === 401) {
        alert.fire({
          icon: "question",
          title: "Credenciais inválidas",
          text: "E-mail e/ou senha incorretos"
        })
      }
    } catch(error) {
      console.log(error);
      alert.fire({
        icon: "question",
        title: "Erro",
        text: "Erro interno"
      });
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div 
        className="
          flex flex-col gap-2 w-90
        "
      >
        <h1 className="text-4xl font-medium mb-8 text-center">
          Login
        </h1>

        <div>
          <InputAuth type="email" id="email" labelValue="Email" {...register("email")}/>
          {errors.email && (<FieldError>{errors.email.message}</FieldError>)}
        </div>
        <div>
          <InputAuth type="password" id="senha" labelValue="Senha" {...register("senha")}/>
          {errors.senha && (<FieldError>{errors.senha.message}</FieldError>)}
        </div>

        <Button type="submit" className="mt-4" disabled={isSubmitting}>{isSubmitting ? "Aguarde..." : "Iniciar sessão"}</Button>
      </div>
    </form>
  );
}