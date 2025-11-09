import { HeroSection, FeaturesSection } from "@/app/components/home";

const HomePage = async () => {
    return (
        <div className="bg-gray-50 text-gray-800">
            <HeroSection />
            <FeaturesSection />
        </div>
    );
};

export default HomePage;
