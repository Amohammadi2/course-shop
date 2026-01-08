import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    (<div className="flex flex-col min-h-screen">
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48">
          <div className="container px-4 md:px-6">
            <div
              className="flex flex-col items-center space-y-4 text-center">
              <h1
                className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl/none">
                E-Learning Platform
              </h1>
              <p
                className="mx-auto max-w-[700px] text-gray-500 md:text-xl dark:text-gray-400">
                The best place to learn new things.
              </p>
              <div className="space-x-4">
                <Link href="/login">
                  <Button>Login</Button>
                </Link>
                <Link href="/signup">
                  <Button variant="outline">Sign Up</Button>
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>)
  );
}
