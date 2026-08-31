"use client";

import HeaderLanding from "@/components/features/landing/HeaderLanding";
import FormCadastro from "@/components/features/auth/cadastro/FormCadastro";

export default function Page() {
  return (
    <>
      <HeaderLanding />
      <main
        className="
          flex flex-1 
          items-center 
          justify-center
          flex-col
          bg-gray-100
          h-screen
        "
        style={{
          backgroundColor: "#171717", // Substitua pelo fundo da imagem
        }}
      >
        <FormCadastro />
      </main>
    </>
  );
}