import HeaderHome from "@/components/features/home/HeaderHome";
import Image from "next/image";
import filmesImage from "@/public/filmes-landing.jpeg";

export default async function HomePage() {
  const mockCards = new Array(5).fill(0);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <HeaderHome />

      <main className="px-8 py-8">
        
      </main>
    </div>
  );
}
