"use client";

import { useState } from "react";
import Button from "@/components/ui/Button";

// Ícone de olho
function EyeIcon({ visible }: { visible: boolean }) {
  return visible ? (
    // Olho aberto
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke="#f97316"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  ) : (
    // Olho fechado/riscado
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke="#f97316"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M3 3l18 18" />
      <path d="M10.6 10.6a2 2 0 0 0 2.8 2.8" />
      <path d="M9.9 4.2A10.5 10.5 0 0 1 12 4c6.5 0 10 8 10 8a18.5 18.5 0 0 1-3.1 4.3" />
      <path d="M6.6 6.6C3.8 8.4 2 12 2 12s3.5 8 10 8c1.4 0 2.7-.3 3.8-.8" />
    </svg>
  );
}

export default function FormCadastro() {
  const [step, setStep] = useState(0);

  const [formData, setFormData] = useState({
    email: "",
    nome: "",
    senha: "",
    confirmarSenha: "",
  });

  // Controle independente para cada senha
  const [showSenha, setShowSenha] = useState(false);
  const [showConfirmarSenha, setShowConfirmarSenha] = useState(false);

  // Função para lidar com mudanças nos campos
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Avançar para o próximo passo
  const handleNext = () => {
    if (step < 3) {
      setStep((prevStep) => prevStep + 1);
    } else {
      // Verifica se as senhas são iguais
      if (formData.senha !== formData.confirmarSenha) {
        alert("As senhas não coincidem!");
        return;
      }

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
            type={showSenha ? "text" : "password"}
            id="senha"
            name="senha"
            value={formData.senha}
            onChange={handleChange}
            required
            className="border p-2 rounded w-full pr-10"
          />

          {/* Botão mostrar/ocultar senha */}
          <button
            type="button"
            onClick={() => setShowSenha((prev) => !prev)}
            className="absolute right-2 top-9"
            aria-label={showSenha ? "Ocultar senha" : "Mostrar senha"}
          >
            <EyeIcon visible={showSenha} />
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
            type={showConfirmarSenha ? "text" : "password"}
            id="confirmarSenha"
            name="confirmarSenha"
            value={formData.confirmarSenha}
            onChange={handleChange}
            required
            className="border p-2 rounded w-full pr-10"
          />

          {/* Botão mostrar/ocultar confirmação */}
          <button
            type="button"
            onClick={() =>
              setShowConfirmarSenha((prev) => !prev)
            }
            className="absolute right-2 top-9"
            aria-label={
              showConfirmarSenha
                ? "Ocultar confirmação de senha"
                : "Mostrar confirmação de senha"
            }
          >
            <EyeIcon visible={showConfirmarSenha} />
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