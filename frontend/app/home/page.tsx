
import FilmesEmAlta from "@/components/features/home/FilmesEmAlta";
import SeriesEmAlta from "@/components/features/home/SeriesEmAlta";
import Header from "@/components/ui/Header";

export default async function HomePage() {

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Header />

      <main className="px-5 py-8 md:px-8">
        <FilmesEmAlta />
        <SeriesEmAlta />
      </main>
    </div>
  );
}

export const dynamic = "force-dynamic";