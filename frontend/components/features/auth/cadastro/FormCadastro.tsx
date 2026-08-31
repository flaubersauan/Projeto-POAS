"use client";

import { useState } from "react";
import Button from "@/components/ui/Button";

export default function FormCadastro() {
  const [step, setStep] = useState(0); // Estado para controlar o passo atual
  const [formData, setFormData] = useState({
    email: "",
    nome: "",
    senha: "",
    confirmarSenha: "",
  });
  const [showPassword, setShowPassword] = useState(false); // Estado para controlar a visibilidade da senha

  // Função para lidar com mudanças nos campos
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // Função para alternar a visibilidade da senha
  const togglePasswordVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  // Função para avançar para o próximo passo
  const handleNext = () => {
    if (step < 3) {
      setStep((prevStep) => prevStep + 1);
    } else {
      // Aqui você pode adicionar a lógica para cadastrar o usuário
      console.log("Dados do formulário:", formData);
      alert("Cadastro realizado com sucesso!");
    }
  };

  return (
    <form
      className="flex flex-col gap-4 p-4 rounded shadow-md w-96"
      style={{ backgroundColor: "#373739" }}
      onSubmit={(e) => e.preventDefault()}
    >
      {/* Campo de Email */}
      <div>
        <label htmlFor="email" className="text-white">
          Email:
        </label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          className="border p-2 rounded w-full"
        />
      </div>

      {/* Campo de Nome de Usuário */}
      {step >= 1 && (
        <div>
          <label htmlFor="nome" className="text-white">
            Nome de Usuário:
          </label>
          <input
            type="text"
            id="nome"
            name="nome"
            value={formData.nome}
            onChange={handleChange}
            required
            className="border p-2 rounded w-full"
          />
        </div>
      )}

      {/* Campo de Senha */}
      {step >= 2 && (
        <div className="relative">
          <label htmlFor="senha" className="text-white">
            Senha:
          </label>
          <input
            type={showPassword ? "text" : "password"}
            id="senha"
            name="senha"
            value={formData.senha}
            onChange={handleChange}
            required
            className="border p-2 rounded w-full"
          />
          <button
            type="button"
            onClick={togglePasswordVisibility}
            className="absolute right-2 top-9"
          >
            {showPassword ? (
              // Ícone de olho cortado
              <svg
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 16 16"
                width="20"
                height="20"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M1.5 2.5h13v10a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1zM0 1h16v11.5a2.5 2.5 0 0 1-2.5 2.5h-11A2.5 2.5 0 0 1 0 12.5zm3.75 4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5M7 4.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0m1.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5"
                  fill="#666"
                />
              </svg>
            ) : (
              // Ícone de olho normal
              <svg
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 16 16"
                width="20"
                height="20"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M1.5 2.5h13v10a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1zM0 1h16v11.5a2.5 2.5 0 0 1-2.5 2.5h-11A2.5 2.5 0 0 1 0 12.5zm3.75 4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5M7 4.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0m1.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5"
                  fill="#666"
                />
              </svg>
            )}
          </button>
        </div>
      )}

      {/* Campo de Confirmar Senha */}
      {step >= 3 && (
        <div className="relative">
          <label htmlFor="confirmarSenha" className="text-white">
            Confirmar Senha:
          </label>
          <input
            type={showPassword ? "text" : "password"}
            id="confirmarSenha"
            name="confirmarSenha"
            value={formData.confirmarSenha}
            onChange={handleChange}
            required
            className="border p-2 rounded w-full"
          />
          <button
            type="button"
            onClick={togglePasswordVisibility}
            className="absolute right-2 top-9"
          >
            {showPassword ? (
              // Ícone de olho cortado
              <svg
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 16 16"
                width="20"
                height="20"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M1.5 2.5h13v10a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1zM0 1h16v11.5a2.5 2.5 0 0 1-2.5 2.5h-11A2.5 2.5 0 0 1 0 12.5zm3.75 4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5M7 4.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0m1.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5"
                  fill="#666"
                />
              </svg>
            ) : (
              // Ícone de olho normal
              <svg
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 16 16"
                width="20"
                height="20"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M1.5 2.5h13v10a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1zM0 1h16v11.5a2.5 2.5 0 0 1-2.5 2.5h-11A2.5 2.5 0 0 1 0 12.5zm3.75 4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5M7 4.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0m1.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5"
                  fill="#13E00"
                />
              </svg>
            )}
          </button>
        </div>
      )}

      {/* Botão Dinâmico */}
      <Button onClick={handleNext} className="mt-4">
        {step < 3 ? "Próximo" : "Cadastrar-se"}
      </Button>
    </form>
  );
}