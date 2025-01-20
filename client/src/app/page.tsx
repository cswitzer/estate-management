import { ArrowRightIcon } from "@heroicons/react/20/solid";
import { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import buildings from "public/assets/images/buildings.webp";

export const metadata: Metadata = {
	title: "Home | Chase Apartments",
	description: "Chas Apartments Home Page. Create your account to get started.",
};

export default function Home() {
	return (
		<div className="relative h-screen">
			<div className="absolute inset-0 z-0">
				<Image
					src={buildings}
					alt="Apartments"
					fill
					style={{ objectFit: "cover", objectPosition: "center" }}
					priority
				/>
			</div>
			<main className="flex-center relative z-10 h-full  bg-black/50">
				<div className="text-center">
					<h1 className="font-robotoSlab mb-4 text-4xl font-semibold text-cyan-400 antialiased sm:text-6xl md:text-8xl">
						Welcome to Chase Apartments
					</h1>
					<p className="my-8 text-2xl text-teal-300 sm:text-4xl">
						Are you a tenant? Or an existing tenant?
					</p>
					{/* We do not want to prefetch for our landing page */}
					<Link href="/register" prefetch={false}>
						<button className="bg-asparagus rounded-3xl px-4 py-2 text-lg font-semibold text-white hover:bg-lime-700 sm:px-6 sm:text-2xl">
							<span className="inline-flex items-center">
								Create Your Account
								<ArrowRightIcon className="ml-2 size-6" />
							</span>
						</button>
					</Link>
				</div>
			</main>
		</div>
	);
}
