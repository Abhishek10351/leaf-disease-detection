"use client";

import { MenuIcon, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
    NavigationMenu,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import {
    Sheet,
    SheetContent,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
} from "@/components/ui/sheet";
import { useAppDispatch, useAppSelector } from "@/lib/redux/hooks";
import { logout } from "@/lib/redux/slices/authSlice";
import { useRouter } from "next/navigation";
import Link from "next/link";

interface NavigationLink {
    title: string;
    href: string;
}

const navigationLinks: NavigationLink[] = [
    { title: "Home", href: "/" },
    { title: "Analysis", href: "/analysis" },
];

const Header: React.FC = () => {
    const dispatch = useAppDispatch();
    const router = useRouter();
    const { isAuthenticated, user } = useAppSelector((state) => state.auth);

    const handleLogout = () => {
        dispatch(logout());
        router.push("/");
    };

    const isInternalRoute = (href: string) => href.startsWith("/");

    return (
        <header className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-sm shadow-sm py-4 z-50 border-b border-gray-100">
            <nav className="container mx-auto px-6 flex justify-between items-center h-12">
                <Link href="/" className="flex items-center gap-2">
                    <span className="text-lg font-semibold tracking-tighter">
                        Leaf Disease Detection
                    </span>
                </Link>
                <NavigationMenu className="hidden lg:block">
                    <NavigationMenuList>
                        {navigationLinks.map((link) => (
                            <NavigationMenuItem key={link.title}>
                                {isInternalRoute(link.href) ? (
                                    <NavigationMenuLink
                                        href={link.href}
                                        className={navigationMenuTriggerStyle()}
                                    >
                                        {link.title}
                                    </NavigationMenuLink>
                                ) : (
                                    <NavigationMenuLink
                                        href={link.href}
                                        className={navigationMenuTriggerStyle()}
                                        target="_blank"
                                        rel="noreferrer"
                                    >
                                        {link.title}
                                    </NavigationMenuLink>
                                )}
                            </NavigationMenuItem>
                        ))}
                    </NavigationMenuList>
                </NavigationMenu>

                <div className="hidden items-center gap-4 lg:flex">
                    {isAuthenticated ? (
                        <div className="flex items-center gap-4">
                            <span className="text-sm text-gray-600">
                                Welcome, {user?.name || user?.email}
                            </span>
                            <Button
                                variant="outline"
                                onClick={handleLogout}
                                className="text-gray-600 hover:text-red-600 transition-colors duration-200 cursor-pointer flex items-center gap-2"
                            >
                                <LogOut className="h-4 w-4" />
                                Sign out
                            </Button>
                        </div>
                    ) : (
                        <>
                            <Button
                                variant="outline"
                                className="text-gray-600 hover:text-indigo-600 transition-colors duration-200 cursor-pointer"
                                asChild
                            >
                                <Link href="/auth/login">Sign in</Link>
                            </Button>
                            <Button
                                className="bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700 transition-colors duration-200 shadow-md cursor-pointer"
                                asChild
                            >
                                <Link href="/auth/signup">Create Account</Link>
                            </Button>
                        </>
                    )}
                </div>
                <Sheet>
                    <SheetTrigger asChild className="lg:hidden">
                        <Button variant="outline" size="icon">
                            <MenuIcon className="h-4 w-4" />
                        </Button>
                    </SheetTrigger>
                    <SheetContent
                        side="top"
                        className="max-h-screen overflow-auto z-[60]"
                    >
                        <SheetHeader>
                            <SheetTitle>
                                <Link href="/" className="flex items-center gap-2">
                                    <span className="text-lg font-semibold tracking-tighter">
                                        Leaf Disease Detection
                                    </span>
                                </Link>
                            </SheetTitle>
                        </SheetHeader>
                        <div className="flex flex-col p-4">
                            <div className="flex flex-col gap-6">
                                {navigationLinks.map((link) => (
                                    isInternalRoute(link.href) ? (
                                        <Link
                                            key={link.title}
                                            href={link.href}
                                            className="font-medium"
                                        >
                                            {link.title}
                                        </Link>
                                    ) : (
                                        <a
                                            key={link.title}
                                            href={link.href}
                                            className="font-medium"
                                            target="_blank"
                                            rel="noreferrer"
                                        >
                                            {link.title}
                                        </a>
                                    )
                                ))}
                            </div>
                            <div className="mt-6 flex flex-col gap-4">
                                {isAuthenticated ? (
                                    <div className="flex flex-col gap-4">
                                        <span className="text-sm text-gray-600">
                                            Welcome, {user?.name || user?.email}
                                        </span>
                                        <Button
                                            variant="outline"
                                            onClick={handleLogout}
                                            className="text-gray-600 hover:text-red-600 transition-colors duration-200 cursor-pointer flex items-center gap-2"
                                        >
                                            <LogOut className="h-4 w-4" />
                                            Sign out
                                        </Button>
                                    </div>
                                ) : (
                                    <>
                                        <Button
                                            variant="outline"
                                            className="text-gray-600 hover:text-indigo-600 transition-colors duration-200 cursor-pointer"
                                            asChild
                                        >
                                            <Link href="/auth/login">Sign in</Link>
                                        </Button>
                                        <Button
                                            className="bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700 transition-colors duration-200 shadow-md cursor-pointer"
                                            asChild
                                        >
                                            <Link href="/auth/signup">
                                                Create Account
                                            </Link>
                                        </Button>
                                    </>
                                )}
                            </div>
                        </div>
                    </SheetContent>
                </Sheet>
            </nav>
        </header>
    );
};

export default Header;
