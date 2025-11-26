import Hero from "../components/Hero";
import Features from "../components/Features";
import Footer from "../components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen bg-zinc-50 dark:bg-black text-slate-900 dark:text-slate-100">
      <div className="max-w-7xl mx-auto px-6 py-6 ">
        <Hero />
        <Features />
      </div>
      <Footer />
    </main>
  );
}
