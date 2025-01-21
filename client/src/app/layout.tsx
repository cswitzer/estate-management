import { ThemeProvider } from "@/components/theme-provider";
import { openSans, robotoSlab } from "@/lib/fonts";
import type { Metadata } from "next";
import React from "react";
import "./globals.css";

export const metadata: Metadata = {
	title: "Create Next App",
	description: "Generated by create next app",
};

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang="en" suppressHydrationWarning>
			<body className={`${openSans.variable} ${robotoSlab.variable}`}>
				<ThemeProvider
					attribute="class"
					defaultTheme="dark"
					enableSystem
					disableTransitionOnChange
				>
					{children}
				</ThemeProvider>
			</body>
		</html>
	);
}
